"""
Authentication API Endpoints
User authentication and authorization
"""

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from datetime import datetime, timedelta
import logging

from app.models.schemas import UserLogin, TokenResponse
from app.config.settings import settings

logger = logging.getLogger(__name__)
router = APIRouter()
security = HTTPBearer()


def create_access_token(data: dict) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=settings.JWT_EXPIRATION_HOURS)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """Verify JWT token"""
    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")


@router.post("/login", response_model=TokenResponse)
async def login(user_data: UserLogin):
    """
    User login endpoint
    
    Returns JWT token for authenticated requests
    """
    try:
        # In production, validate against Firebase/database
        # For demo, accept any credentials
        logger.info(f"Login attempt: {user_data.email}")
        
        # Create token
        access_token = create_access_token(
            data={"sub": user_data.email, "type": "user"}
        )
        
        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=settings.JWT_EXPIRATION_HOURS * 3600
        )
        
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(status_code=500, detail="Login failed")


@router.get("/me")
async def get_current_user(token_data: dict = Depends(verify_token)):
    """Get current user information"""
    return {
        "email": token_data.get("sub"),
        "user_type": token_data.get("type", "user")
    }


@router.post("/logout")
async def logout():
    """User logout endpoint"""
    return {"message": "Logged out successfully"}
