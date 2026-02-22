"""
Pydantic models for API requests and responses
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime


class DocumentUploadResponse(BaseModel):
    """Response for document upload"""
    file_id: str
    file_name: str
    file_hash: str
    file_size: int
    uploaded_at: str


class ComplianceAnalysisRequest(BaseModel):
    """Request for compliance analysis"""
    file_id: str
    frameworks: List[str] = Field(default=["iso27001"], description="List of frameworks to analyze")
    include_cia: bool = Field(default=True, description="Include CIA analysis")
    include_iso9001: bool = Field(default=False, description="Include ISO 9001 validation")


class ComplianceAnalysisResponse(BaseModel):
    """Response for compliance analysis"""
    analysis_id: str
    file_name: str
    frameworks: List[str]
    compliance_results: Dict
    cia_analysis: Optional[Dict] = None
    iso9001_analysis: Optional[Dict] = None
    risk_prediction: Optional[Dict] = None
    audit_readiness: Optional[Dict] = None
    analyzed_at: str


class CIAAnalysisResponse(BaseModel):
    """Response for CIA analysis"""
    total_clauses: int
    cia_coverage: Dict[str, float]
    cia_balance_index: float
    balance_rating: str
    imbalances: List[Dict]
    recommendations: List[str]


class RiskPredictionResponse(BaseModel):
    """Response for audit risk prediction"""
    risk_level: str
    confidence: float
    probability_distribution: Dict[str, float]
    recommendations: List[str]


class UserLogin(BaseModel):
    """User login request"""
    email: str
    password: str


class UserRegister(BaseModel):
    """User registration request"""
    email: str
    password: str
    full_name: str
    organization: Optional[str] = None


class TokenResponse(BaseModel):
    """JWT token response"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class ErrorResponse(BaseModel):
    """Error response"""
    error: str
    message: str
    details: Optional[Dict] = None
