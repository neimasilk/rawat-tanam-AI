from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from typing import Optional
from jose import jwt
from passlib.context import CryptContext
import time
from config import settings
import logging

logger = logging.getLogger(__name__)

router = APIRouter()
security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Request/Response models
class UserRegister(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    organization: Optional[str] = None
    intended_use: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    user_info: dict

class APIKeyRequest(BaseModel):
    name: str
    tier: str = "free"
    description: Optional[str] = None

class APIKeyResponse(BaseModel):
    api_key: str
    tier: str
    name: str
    created_at: float
    expires_at: Optional[float] = None

# Mock user database
class MockUserDatabase:
    def __init__(self):
        self.users = {
            "demo@rawat-tanam-ai.com": {
                "user_id": "demo_user",
                "email": "demo@rawat-tanam-ai.com",
                "full_name": "Demo User",
                "hashed_password": pwd_context.hash("demo123"),
                "tier": "free",
                "organization": "Demo Organization",
                "created_at": time.time(),
                "active": True
            }
        }
        
        self.api_keys = {
            "free_demo_key_123": {
                "user_id": "demo_user",
                "tier": "free",
                "name": "Demo API Key",
                "created_at": time.time(),
                "active": True
            }
        }
    
    def get_user_by_email(self, email: str) -> Optional[dict]:
        return self.users.get(email)
    
    def create_user(self, user_data: dict) -> dict:
        user_id = f"user_{int(time.time())}"
        user_data["user_id"] = user_id
        user_data["created_at"] = time.time()
        user_data["active"] = True
        self.users[user_data["email"]] = user_data
        return user_data
    
    def create_api_key(self, user_id: str, key_data: dict) -> str:
        import secrets
        api_key = f"{key_data['tier']}_{secrets.token_urlsafe(16)}"
        self.api_keys[api_key] = {
            "user_id": user_id,
            "tier": key_data["tier"],
            "name": key_data["name"],
            "description": key_data.get("description"),
            "created_at": time.time(),
            "active": True
        }
        return api_key

# Initialize mock database
user_db = MockUserDatabase()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash password"""
    return pwd_context.hash(password)

def create_access_token(data: dict) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    expire = time.time() + (settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.SECRET_KEY, 
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current user from JWT token"""
    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return payload
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.post("/register", response_model=TokenResponse)
async def register_user(user_data: UserRegister):
    """Register new user"""
    # Check if user already exists
    if user_db.get_user_by_email(user_data.email):
        raise HTTPException(
            status_code=400,
            detail="User with this email already exists"
        )
    
    # Determine tier based on intended use
    tier = "free"
    if "research" in user_data.intended_use.lower() or "academic" in user_data.intended_use.lower():
        tier = "professional"
    elif "commercial" in user_data.intended_use.lower() or "enterprise" in user_data.intended_use.lower():
        tier = "enterprise"
    
    # Create user
    hashed_password = get_password_hash(user_data.password)
    new_user = user_db.create_user({
        "email": user_data.email,
        "full_name": user_data.full_name,
        "hashed_password": hashed_password,
        "organization": user_data.organization,
        "intended_use": user_data.intended_use,
        "tier": tier
    })
    
    # Create access token
    access_token = create_access_token({
        "sub": new_user["user_id"],
        "email": new_user["email"],
        "tier": new_user["tier"]
    })
    
    logger.info(f"New user registered: {user_data.email}")
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user_info={
            "user_id": new_user["user_id"],
            "email": new_user["email"],
            "full_name": new_user["full_name"],
            "tier": new_user["tier"],
            "organization": new_user["organization"]
        }
    )

@router.post("/login", response_model=TokenResponse)
async def login_user(user_credentials: UserLogin):
    """Login user and return access token"""
    user = user_db.get_user_by_email(user_credentials.email)
    
    if not user or not verify_password(user_credentials.password, user["hashed_password"]):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password"
        )
    
    if not user["active"]:
        raise HTTPException(
            status_code=401,
            detail="User account is disabled"
        )
    
    # Create access token
    access_token = create_access_token({
        "sub": user["user_id"],
        "email": user["email"],
        "tier": user["tier"]
    })
    
    logger.info(f"User logged in: {user_credentials.email}")
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user_info={
            "user_id": user["user_id"],
            "email": user["email"],
            "full_name": user["full_name"],
            "tier": user["tier"],
            "organization": user.get("organization")
        }
    )

@router.post("/api-key", response_model=APIKeyResponse)
async def create_api_key(
    key_request: APIKeyRequest,
    current_user: dict = Depends(get_current_user)
):
    """Create new API key for authenticated user"""
    # Validate tier request
    user_tier = current_user.get("tier", "free")
    requested_tier = key_request.tier
    
    # Users can only create API keys for their tier or lower
    tier_hierarchy = {"free": 0, "professional": 1, "enterprise": 2, "partner": 3}
    if tier_hierarchy.get(requested_tier, 0) > tier_hierarchy.get(user_tier, 0):
        raise HTTPException(
            status_code=403,
            detail=f"Cannot create {requested_tier} API key with {user_tier} account"
        )
    
    # Create API key
    api_key = user_db.create_api_key(current_user["sub"], {
        "tier": requested_tier,
        "name": key_request.name,
        "description": key_request.description
    })
    
    logger.info(f"API key created for user {current_user['sub']}: {key_request.name}")
    
    return APIKeyResponse(
        api_key=api_key,
        tier=requested_tier,
        name=key_request.name,
        created_at=time.time()
    )

@router.get("/me")
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """Get current user information"""
    user_email = current_user.get("email")
    user_data = user_db.get_user_by_email(user_email)
    
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "user_id": user_data["user_id"],
        "email": user_data["email"],
        "full_name": user_data["full_name"],
        "tier": user_data["tier"],
        "organization": user_data.get("organization"),
        "created_at": user_data["created_at"],
        "active": user_data["active"]
    }

@router.get("/tiers")
async def get_available_tiers():
    """Get information about available API tiers"""
    return {
        "tiers": {
            "free": {
                "name": "Free",
                "rate_limit": "100 requests/hour",
                "features": ["Basic plant identification", "Species database access"],
                "price": "Free"
            },
            "professional": {
                "name": "Professional",
                "rate_limit": "1,000 requests/hour",
                "features": ["Advanced identification", "Batch processing", "Priority support"],
                "price": "$29/month"
            },
            "enterprise": {
                "name": "Enterprise",
                "rate_limit": "10,000 requests/hour",
                "features": ["Custom models", "White-label API", "SLA guarantee"],
                "price": "Contact sales"
            },
            "partner": {
                "name": "Partner",
                "rate_limit": "Unlimited",
                "features": ["Full API access", "Custom integration", "Revenue sharing"],
                "price": "Partnership agreement"
            }
        }
    }