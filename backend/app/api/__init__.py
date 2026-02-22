"""
AIComplianceGuard - API Router
Main API routing configuration
"""

from fastapi import APIRouter
from app.api.endpoints import compliance, analysis, auth, admin

router = APIRouter()

# Include endpoint routers
router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
router.include_router(compliance.router, prefix="/compliance", tags=["Compliance Analysis"])
router.include_router(analysis.router, prefix="/analysis", tags=["CIA & Risk Analysis"])
router.include_router(admin.router, prefix="/admin", tags=["Admin"])
