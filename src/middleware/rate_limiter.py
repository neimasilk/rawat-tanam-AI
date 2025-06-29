from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import time
import asyncio
from typing import Dict, Tuple
from config import settings
import logging

logger = logging.getLogger(__name__)

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        # In-memory storage for rate limiting (use Redis in production)
        self.requests: Dict[str, Dict[str, any]] = {}
        self.rate_limits = {
            "free": {"requests": 100, "window": 3600},  # 100/hour
            "professional": {"requests": 1000, "window": 3600},  # 1000/hour
            "enterprise": {"requests": 10000, "window": 3600},  # 10000/hour
            "partner": {"requests": float('inf'), "window": 3600}  # unlimited
        }
    
    def get_client_identifier(self, request: Request) -> str:
        """Get unique identifier for client (IP + API key if available)"""
        client_ip = request.client.host
        api_key = request.headers.get("X-API-Key", "")
        return f"{client_ip}:{api_key}"
    
    def get_client_tier(self, request: Request) -> str:
        """Determine client tier based on API key or default to free"""
        api_key = request.headers.get("X-API-Key")
        
        if not api_key:
            return "free"
        
        # Mock tier detection - in production, query database
        if api_key.startswith("partner_"):
            return "partner"
        elif api_key.startswith("enterprise_"):
            return "enterprise"
        elif api_key.startswith("professional_"):
            return "professional"
        else:
            return "free"
    
    def is_rate_limited(self, client_id: str, tier: str) -> Tuple[bool, Dict[str, any]]:
        """Check if client has exceeded rate limit"""
        current_time = time.time()
        rate_limit = self.rate_limits[tier]
        
        if client_id not in self.requests:
            self.requests[client_id] = {
                "count": 0,
                "window_start": current_time,
                "tier": tier
            }
        
        client_data = self.requests[client_id]
        
        # Reset window if expired
        if current_time - client_data["window_start"] >= rate_limit["window"]:
            client_data["count"] = 0
            client_data["window_start"] = current_time
        
        # Check if limit exceeded
        if client_data["count"] >= rate_limit["requests"]:
            remaining_time = rate_limit["window"] - (current_time - client_data["window_start"])
            return True, {
                "retry_after": int(remaining_time),
                "limit": rate_limit["requests"],
                "remaining": 0,
                "reset_time": int(client_data["window_start"] + rate_limit["window"])
            }
        
        # Increment counter
        client_data["count"] += 1
        remaining = rate_limit["requests"] - client_data["count"]
        
        return False, {
            "limit": rate_limit["requests"],
            "remaining": remaining if remaining != float('inf') else -1,
            "reset_time": int(client_data["window_start"] + rate_limit["window"])
        }
    
    async def dispatch(self, request: Request, call_next) -> Response:
        # Skip rate limiting for health check and docs
        if request.url.path in ["/health", "/api/v1/docs", "/api/v1/redoc", "/api/v1/openapi.json"]:
            return await call_next(request)
        
        client_id = self.get_client_identifier(request)
        tier = self.get_client_tier(request)
        
        is_limited, rate_info = self.is_rate_limited(client_id, tier)
        
        if is_limited:
            logger.warning(f"Rate limit exceeded for client {client_id} (tier: {tier})")
            raise HTTPException(
                status_code=429,
                detail={
                    "message": "Rate limit exceeded",
                    "retry_after": rate_info["retry_after"],
                    "limit": rate_info["limit"],
                    "remaining": rate_info["remaining"]
                },
                headers={
                    "Retry-After": str(rate_info["retry_after"]),
                    "X-RateLimit-Limit": str(rate_info["limit"]),
                    "X-RateLimit-Remaining": str(rate_info["remaining"]),
                    "X-RateLimit-Reset": str(rate_info["reset_time"])
                }
            )
        
        # Add rate limit headers to response
        response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(rate_info["limit"])
        response.headers["X-RateLimit-Remaining"] = str(rate_info["remaining"])
        response.headers["X-RateLimit-Reset"] = str(rate_info["reset_time"])
        response.headers["X-RateLimit-Tier"] = tier
        
        return response