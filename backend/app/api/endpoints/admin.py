"""
Admin API Endpoints
Administrative functions and system management
"""

from fastapi import APIRouter, Depends, HTTPException
from typing import List
import logging

from app.api.endpoints.auth import verify_token
from app.modules.security_layer import security_layer
from app.modules.firebase_storage import firebase_storage

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/stats")
async def get_system_stats(token_data: dict = Depends(verify_token)):
    """
    Get system statistics
    
    - Requires authentication
    """
    return {
        "total_analyses": 0,  # Would come from database
        "active_users": 0,
        "frameworks_supported": 4,
        "models_loaded": 7
    }


@router.post("/cleanup")
async def cleanup_temp_files(token_data: dict = Depends(verify_token)):
    """
    Cleanup temporary files
    
    - Requires authentication
    """
    try:
        cleaned_count = security_layer.cleanup_temp_files()
        
        return {
            "message": f"Cleaned up {cleaned_count} temporary files",
            "count": cleaned_count
        }
        
    except Exception as e:
        logger.error(f"Cleanup error: {str(e)}")
        raise HTTPException(status_code=500, detail="Cleanup failed")


@router.get("/system-health")
async def get_system_health():
    """
    Get detailed system health status
    """
    # Get Firebase storage stats
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
            "firebase_storage": "operational" if firebase_stats.get('enabled') else "disabled"
        },
        "firebase": firebase_stats,
        "disk_usage": "low",
        "memory_usage": "normal"
    }


@router.get("/firebase-stats")
async def get_firebase_stats(token_data: dict = Depends(verify_token)):
    """
    Get Firebase storage statistics
    
    - Requires authentication
    """
    try:
        stats = firebase_storage.get_storage_stats()
        return stats
    except Exception as e:
        logger.error(f"Failed to get Firebase stats: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve Firebase stats")


@router.post("/firebase-cleanup")
async def cleanup_firebase_metadata(token_data: dict = Depends(verify_token)):
    """
    Clean up expired metadata from Firebase
    
    - Requires authentication
    """
    try:
        deleted_count = firebase_storage.cleanup_expired_metadata()
        
        return {
            "message": f"Cleaned up {deleted_count} expired metadata entries",
            "count": deleted_count
        }
        
    except Exception as e:
        logger.error(f"Firebase cleanup error: {str(e)}")
        raise HTTPException(status_code=500, detail="Firebase cleanup failed")
