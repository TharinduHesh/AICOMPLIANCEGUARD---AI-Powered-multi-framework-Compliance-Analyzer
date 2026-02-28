"""
Authentication API Endpoints
User login with Company ID + Password
Admin-only user creation — no self-registration
"""

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from datetime import datetime, timedelta
import hashlib, secrets
import logging
from typing import Dict, Optional

from app.models.schemas import UserLogin, UserRegister, UserResponse, TokenResponse
from app.config.settings import settings

logger = logging.getLogger(__name__)
router = APIRouter()
security = HTTPBearer()

# ── Activity log (in-memory + Firebase) ──────────────────────
_activity_log: list = []  # [{user, action, detail, timestamp}, ...]
_MAX_ACTIVITY_LOG = 500

def record_activity(user_id: str, action: str, detail: str = ""):
    """Record a user activity event"""
    entry = {
        "user": user_id,
        "action": action,
        "detail": detail,
        "timestamp": datetime.utcnow().isoformat(),
    }
    _activity_log.insert(0, entry)  # newest first
    if len(_activity_log) > _MAX_ACTIVITY_LOG:
        _activity_log.pop()  # trim oldest
    # Persist to Firebase asynchronously (best effort)
    _fb_store_activity(entry)

def _fb_store_activity(entry: dict):
    db = _get_firestore()
    if db is None:
        return
    try:
        db.collection("user_activities").add(entry)
    except Exception as e:
        logger.error(f"Firebase activity log error: {e}")

def _fb_load_activities(limit: int = 200) -> list:
    db = _get_firestore()
    if db is None:
        return []
    try:
        docs = db.collection("user_activities").order_by("timestamp", direction="DESCENDING").limit(limit).stream()
        return [d.to_dict() for d in docs]
    except Exception:
        return []

# ── Firebase helpers ─────────────────────────────────────────
_fb_available = False
_fb_db = None

def _get_firestore():
    """Lazy-init Firestore client"""
    global _fb_available, _fb_db
    if _fb_db is not None:
        return _fb_db
    try:
        import firebase_admin
        from firebase_admin import firestore
        if firebase_admin._apps:
            _fb_db = firestore.client()
            _fb_available = True
            return _fb_db
    except Exception:
        pass
    _fb_available = False
    return None

def _fb_get_user(company_id: str) -> Optional[dict]:
    db = _get_firestore()
    if db is None:
        return None
    try:
        doc = db.collection("users").document(company_id).get()
        return doc.to_dict() if doc.exists else None
    except Exception as e:
        logger.error(f"Firebase read error: {e}")
        return None

def _fb_set_user(company_id: str, data: dict):
    db = _get_firestore()
    if db is None:
        return
    try:
        db.collection("users").document(company_id).set(data)
    except Exception as e:
        logger.error(f"Firebase write error: {e}")

def _fb_delete_user(company_id: str):
    db = _get_firestore()
    if db is None:
        return
    try:
        db.collection("users").document(company_id).delete()
    except Exception as e:
        logger.error(f"Firebase delete error: {e}")

def _fb_list_users() -> list:
    db = _get_firestore()
    if db is None:
        return []
    try:
        docs = db.collection("users").stream()
        return [{"company_id": d.id, **d.to_dict()} for d in docs]
    except Exception as e:
        logger.error(f"Firebase list error: {e}")
        return []


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


# ── In-memory user store (mirror of Firebase) ───────────────
# { company_id: { company_name, pw_hash, pw_salt, role, created_at } }
_users: Dict[str, dict] = {}

# Admin credentials
ADMIN_EMAIL = "Admin@ACG.lk"
ADMIN_PASSWORD = "@Admin123"


def _seed_admin():
    """Ensure admin account exists in memory + Firebase"""
    if ADMIN_EMAIL not in _users:
        pw_hash, pw_salt = _hash_password(ADMIN_PASSWORD)
        admin_data = {
            "company_name": "ACG Admin",
            "pw_hash": pw_hash,
            "pw_salt": pw_salt,
            "role": "admin",
            "created_at": datetime.utcnow().isoformat(),
        }
        _users[ADMIN_EMAIL] = admin_data
        _fb_set_user(ADMIN_EMAIL, admin_data)
        logger.info("Admin account seeded")

def _load_users_from_firebase():
    """Load all users from Firebase into memory on startup"""
    fb_users = _fb_list_users()
    for u in fb_users:
        cid = u.pop("company_id", None)
        if cid and cid not in _users:
            _users[cid] = u
    if fb_users:
        logger.info(f"Loaded {len(fb_users)} users from Firebase")

# Run on module import
_load_users_from_firebase()
_seed_admin()

# Pre-load recent activities from Firebase
try:
    _fb_activities = _fb_load_activities(200)
    if _fb_activities:
        _activity_log.extend(_fb_activities)
        logger.info(f"Loaded {len(_fb_activities)} activities from Firebase")
except Exception:
    pass


def get_user(company_id: str) -> Optional[dict]:
    """Get user from memory (primary) or Firebase (fallback)"""
    if company_id in _users:
        return _users[company_id]
    fb = _fb_get_user(company_id)
    if fb:
        _users[company_id] = fb
        return fb
    return None


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


def verify_admin(token_data: dict = Depends(verify_token)) -> dict:
    """Verify the caller is an admin"""
    if token_data.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return token_data


# ── Login ────────────────────────────────────────────────────
@router.post("/login", response_model=TokenResponse)
async def login(data: UserLogin):
    """
    Login with Company ID and password.
    Returns a JWT token on success.
    """
    cid = data.company_id.strip()
    user = get_user(cid)

    if not user or not _verify_password(data.password, user["pw_hash"], user["pw_salt"]):
        raise HTTPException(status_code=401, detail="Invalid Company ID or password")

    role = user.get("role", "user")
    logger.info(f"Login success: {cid} (role={role})")

    # Track login activity & update last_login
    record_activity(cid, "login", f"Logged in (role={role})")
    _users[cid]["last_login"] = datetime.utcnow().isoformat()
    _fb_set_user(cid, _users[cid])

    token = create_access_token(
        data={"sub": cid, "name": user["company_name"], "type": "user", "role": role}
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
    user = get_user(cid)
    return {
        "company_id": cid,
        "company_name": user["company_name"] if user else token_data.get("name", cid),
        "role": token_data.get("role", "user"),
        "created_at": user.get("created_at") if user else None,
    }


# ── Logout (client-side token removal) ──────────────────────
@router.post("/logout")
async def logout():
    """Logout - client should discard the token"""
    return {"message": "Logged out successfully"}

