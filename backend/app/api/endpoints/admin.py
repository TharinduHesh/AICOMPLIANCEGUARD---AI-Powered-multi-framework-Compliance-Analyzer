"""
Admin API Endpoints
User management (add/list/delete) + system administration
Only the admin account can access these endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import logging

from app.api.endpoints.auth import (
    verify_admin, verify_token,
    _users, get_user,
    _fb_set_user, _fb_delete_user, _fb_list_users,
    _activity_log, record_activity,
)
from app.modules.security_layer import security_layer
from app.modules.firebase_storage import firebase_storage

logger = logging.getLogger(__name__)
router = APIRouter()


# ── Schemas ──────────────────────────────────────────────────
class CreateUserRequest(BaseModel):
    company_id: str = Field(..., min_length=3, max_length=50)
    company_name: str = Field(..., min_length=2, max_length=100)
    password: str = Field(..., min_length=6)
    role: str = Field(default="user", pattern="^(user|admin)$")


class UserOut(BaseModel):
    company_id: str
    company_name: str
    role: str = "user"
    created_at: Optional[str] = None
    last_login: Optional[str] = None


# ── User Management (Admin only) ────────────────────────────
@router.get("/users", response_model=List[UserOut])
async def list_users(token_data: dict = Depends(verify_admin)):
    """List all registered users (admin only)"""
    users = []
    for cid, u in _users.items():
        users.append(UserOut(
            company_id=cid,
            company_name=u.get("company_name", ""),
            role=u.get("role", "user"),
            created_at=u.get("created_at"),
            last_login=u.get("last_login"),
        ))
    return users


@router.post("/users", response_model=UserOut, status_code=201)
async def create_user(body: CreateUserRequest, token_data: dict = Depends(verify_admin)):
    """Create a new user account (admin only). Saved to Firebase + memory."""
    cid = body.company_id.strip()

    if cid.lower() in (k.lower() for k in _users):
        raise HTTPException(status_code=409, detail="Company ID already exists")

    user_data = {
        "company_name": body.company_name.strip(),
        "password": body.password,
        "role": body.role,
        "created_at": datetime.utcnow().isoformat(),
    }

    # Save to memory
    _users[cid] = user_data
    # Persist to Firebase
    _fb_set_user(cid, user_data)

    logger.info(f"Admin created user: {cid} (role={body.role})")
    record_activity(token_data.get("sub", "admin"), "create_user", f"Created user '{cid}' (role={body.role})")
    return UserOut(
        company_id=cid,
        company_name=user_data["company_name"],
        role=user_data["role"],
        created_at=user_data["created_at"],
    )


@router.delete("/users/{company_id}")
async def delete_user(company_id: str, token_data: dict = Depends(verify_admin)):
    """Delete a user account (admin only). Cannot delete the admin itself."""
    from app.api.endpoints.auth import ADMIN_EMAIL
    if company_id == ADMIN_EMAIL:
        raise HTTPException(status_code=400, detail="Cannot delete the admin account")

    if company_id not in _users:
        raise HTTPException(status_code=404, detail="User not found")

    del _users[company_id]
    _fb_delete_user(company_id)

    logger.info(f"Admin deleted user: {company_id}")
    record_activity(token_data.get("sub", "admin"), "delete_user", f"Deleted user '{company_id}'")
    return {"message": f"User '{company_id}' deleted successfully"}


@router.get("/activities")
async def list_activities(
    user: Optional[str] = None,
    limit: int = 100,
    token_data: dict = Depends(verify_admin),
):
    """List recent user activities. Optionally filter by user company_id."""
    logs = _activity_log
    if user:
        logs = [a for a in logs if a.get("user") == user]
    return logs[:limit]


@router.get("/history")
async def admin_history(
    category: Optional[str] = None,
    user: Optional[str] = None,
    limit: int = 200,
    token_data: dict = Depends(verify_admin),
):
    """
    Return upload-document and chat history for all users.
    category: 'upload' | 'chat' | None (both)
    """
    allowed = set()
    if category == "upload":
        allowed = {"upload", "analysis"}
    elif category == "chat":
        allowed = {"chat"}
    else:
        allowed = {"upload", "analysis", "chat"}

    logs = _activity_log
    if user:
        logs = [a for a in logs if a.get("user") == user]
    results = [a for a in logs if a.get("action") in allowed]

    # Enrich with company_name from _users
    enriched = []
    for entry in results[:limit]:
        uid = entry.get("user", "")
        udata = _users.get(uid, {})
        enriched.append({
            **entry,
            "company_name": udata.get("company_name", uid),
            "role": udata.get("role", "user"),
        })
    return enriched


# ── System endpoints (unchanged) ────────────────────────────
@router.get("/stats")
async def get_system_stats(token_data: dict = Depends(verify_token)):
    """Get system statistics"""
    return {
        "total_analyses": 0,
        "active_users": len(_users),
        "frameworks_supported": 4,
        "models_loaded": 7,
    }


@router.post("/cleanup")
async def cleanup_temp_files(token_data: dict = Depends(verify_token)):
    """Cleanup temporary files"""
    try:
        cleaned_count = security_layer.cleanup_temp_files()
        return {"message": f"Cleaned up {cleaned_count} temporary files", "count": cleaned_count}
    except Exception as e:
        logger.error(f"Cleanup error: {str(e)}")
        raise HTTPException(status_code=500, detail="Cleanup failed")


@router.get("/system-health")
async def get_system_health():
    """Get detailed system health status"""
    firebase_stats = firebase_storage.get_storage_stats()
    return {
        "status": "healthy",
        "modules": {
            "document_processor": "operational",
            "nlp_engine": "operational",
            "cia_validator": "operational",
            "iso9001_validator": "operational",
            "knowledge_graph": "operational",
            "audit_predictor": "operational",
            "security_layer": "operational",
            "firebase_storage": "operational" if firebase_stats.get("enabled") else "disabled",
        },
        "firebase": firebase_stats,
        "disk_usage": "low",
        "memory_usage": "normal",
    }


@router.get("/firebase-stats")
async def get_firebase_stats(token_data: dict = Depends(verify_token)):
    """Get Firebase storage statistics"""
    try:
        stats = firebase_storage.get_storage_stats()
        return stats
    except Exception as e:
        logger.error(f"Failed to get Firebase stats: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve Firebase stats")


@router.post("/firebase-cleanup")
async def cleanup_firebase_metadata(token_data: dict = Depends(verify_token)):
    """Clean up expired metadata from Firebase"""
    try:
        deleted_count = firebase_storage.cleanup_expired_metadata()
        return {"message": f"Cleaned up {deleted_count} expired metadata entries", "count": deleted_count}
    except Exception as e:
        logger.error(f"Firebase cleanup error: {str(e)}")
        raise HTTPException(status_code=500, detail="Firebase cleanup failed")
