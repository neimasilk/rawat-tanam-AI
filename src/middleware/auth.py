from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from starlette.requests import Request
from fastapi import HTTPException
from jose import JWTError, jwt
from typing import Optional, Dict, Any
from config import settings
import logging
import time

logger = logging.getLogger(__name__)

class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        # Mock API keys storage (use database in production)
        self.valid_api_keys = {
            "free_demo_key_123": {"tier": "free", "user_id": "demo_user", "active": True},
            "professional_key_456": {"tier": "professional", "user_id": "pro_user", "active": True},
            "enterprise_key_789": {"tier": "enterprise", "user_id": "enterprise_user", "active": True},
            "partner_key_abc": {"tier": "partner", "user_id": "partner_user", "active": True}
        }
    
    def validate_api_key(self, api_key: str) -> Optional[Dict[str, Any]]:
        """Validate API key and return user info"""
        if api_key in self.valid_api_keys:
            key_info = self.valid_api_keys[api_key]
            if key_info["active"]:
                return key_info
        return None
    
    def validate_jwt_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Validate JWT token and return payload"""
        try:
            payload = jwt.decode(
                token, 
                settings.SECRET_KEY, 
                algorithms=[settings.ALGORITHM]
            )
            
            # Check token expiration
            exp = payload.get("exp")
            if exp and exp < time.time():
                return None
            
            return payload
        except JWTError as e:
            logger.warning(f"JWT validation failed: {e}")
            return None
    
    def is_public_endpoint(self, path: str) -> bool:
        """Check if endpoint is public (doesn't require authentication)"""
        public_paths = [
            "/health",
            "/api/v1/docs",
            "/api/v1/redoc",
            "/api/v1/openapi.json",
            "/api/v1/auth/login",
            "/api/v1/auth/register",
            "/api/v1/auth/tiers",
            "/api/v1/info"
        ]
        return path in public_paths
    
    async def dispatch(self, request: Request, call_next) -> Response:
        # Skip authentication for public endpoints
        if self.is_public_endpoint(request.url.path):
            return await call_next(request)
        
        # Check for API key in headers
        api_key = request.headers.get("X-API-Key")
        jwt_token = None
        
        # Check for JWT token in Authorization header
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            jwt_token = auth_header[7:]  # Remove "Bearer " prefix
        
        user_info = None
        auth_method = None
        
        # Try API key authentication first
        if api_key:
            user_info = self.validate_api_key(api_key)
            if user_info:
                auth_method = "api_key"
        
        # Try JWT authentication if API key failed
        if not user_info and jwt_token:
            jwt_payload = self.validate_jwt_token(jwt_token)
            if jwt_payload:
                user_info = {
                    "user_id": jwt_payload.get("sub"),
                    "tier": jwt_payload.get("tier", "free"),
                    "active": True
                }
                auth_method = "jwt"
        
        # Reject request if no valid authentication
        if not user_info:
            logger.warning(f"Authentication failed for {request.url.path}")
            import json
            error_response = {
                "error": {
                    "code": 401,
                    "message": "Authentication required",
                    "error_code": "INVALID_CREDENTIALS",
                    "supported_methods": ["API Key (X-API-Key header)", "JWT Token (Authorization: Bearer)"]
                }
            }
            return Response(
                content=json.dumps(error_response),
                status_code=401,
                headers={
                    "Content-Type": "application/json",
                    "WWW-Authenticate": "Bearer"
                }
            )
        
        # Add user info to request state
        request.state.user = user_info
        request.state.auth_method = auth_method
        
        # Log successful authentication
        logger.info(f"Authenticated user {user_info['user_id']} via {auth_method} for {request.url.path}")
        
        response = await call_next(request)
        
        # Add authentication info to response headers
        response.headers["X-Auth-Method"] = auth_method
        response.headers["X-User-Tier"] = user_info["tier"]
        
        return response