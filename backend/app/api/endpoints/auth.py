"""
Authentication API Endpoints
User registration and login with Company ID + Password
"""

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from datetime import datetime, timedelta
import hashlib, secrets
import logging
from typing import Dict

from app.models.schemas import UserLogin, UserRegister, UserResponse, TokenResponse
from app.config.settings import settings

logger = logging.getLogger(__name__)
router = APIRouter()
security = HTTPBearer()

# ── Password hashing (PBKDF2-SHA256, no extra deps) ─────────
def _hash_password(password: str, salt: str = None) -> tuple:
    """Returns (hash_hex, salt_hex)"""
    if salt is None:
        salt = secrets.token_hex(16)
    h = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 260_000)
    return h.hex(), salt

def _verify_password(password: str, stored_hash: str, salt: str) -> bool:
    h = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 260_000)
    return secrets.compare_digest(h.hex(), stored_hash)

# ── In-memory user store ─────────────────────────────────────
# { company_id: { company_name, hashed_password, created_at } }
_users: Dict[str, dict] = {}


def create_access_token(data: dict) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=settings.JWT_EXPIRATION_HOURS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """Verify JWT token and return payload"""
    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
        )
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


# ── Register ─────────────────────────────────────────────────
@router.post("/register", response_model=TokenResponse)
async def register(data: UserRegister):
    """
    Create a new account with Company ID and password.
    Returns a JWT token on success.
    """
    cid = data.company_id.strip()
    if cid.lower() in (k.lower() for k in _users):
        raise HTTPException(status_code=409, detail="Company ID already exists")

    pw_hash, pw_salt = _hash_password(data.password)
    _users[cid] = {
        "company_name": data.company_name.strip(),
        "pw_hash": pw_hash,
        "pw_salt": pw_salt,
        "created_at": datetime.utcnow().isoformat(),
    }

    logger.info(f"New account registered: {cid}")

    token = create_access_token(
        data={"sub": cid, "name": data.company_name.strip(), "type": "user"}
    )
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        expires_in=settings.JWT_EXPIRATION_HOURS * 3600,
    )


# ── Login ────────────────────────────────────────────────────
@router.post("/login", response_model=TokenResponse)
async def login(data: UserLogin):
    """
    Login with Company ID and password.
    Returns a JWT token on success.
    """
    cid = data.company_id.strip()
    user = _users.get(cid)

    if not user or not _verify_password(data.password, user["pw_hash"], user["pw_salt"]):
        raise HTTPException(status_code=401, detail="Invalid Company ID or password")

    logger.info(f"Login success: {cid}")

    token = create_access_token(
        data={"sub": cid, "name": user["company_name"], "type": "user"}
    )
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        expires_in=settings.JWT_EXPIRATION_HOURS * 3600,
    )


# ── Current user info ────────────────────────────────────────
@router.get("/me")
async def get_current_user(token_data: dict = Depends(verify_token)):
    """Get current authenticated user info"""
    cid = token_data.get("sub")
    user = _users.get(cid)
    if not user:
        return {
            "company_id": cid,
            "company_name": token_data.get("name", cid),
        }
    return {
        "company_id": cid,
        "company_name": user["company_name"],
        "created_at": user["created_at"],
    }


# ── Logout (client-side token removal) ──────────────────────
@router.post("/logout")
async def logout():
    """Logout — client should discard the token"""
    return {"message": "Logged out successfully"}

