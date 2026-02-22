"""
CIA and Risk Analysis API Endpoints
Dedicated endpoints for CIA analysis and risk prediction
"""

from fastapi import APIRouter, HTTPException
from typing import List, Dict
import logging

from app.models.schemas import CIAAnalysisResponse, RiskPredictionResponse
from app.modules.cia_validator import cia_validator
from app.modules.audit_predictor import audit_predictor

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/cia", response_model=CIAAnalysisResponse)
async def analyze_cia(clauses: List[Dict[str, str]]):
    """
    Perform CIA (Confidentiality, Integrity, Availability) analysis
    
    - Classifies controls into CIA pillars
    - Calculates CIA Balance Index
    - Identifies imbalances and risks
    """
    try:
        if not clauses:
            raise HTTPException(status_code=400, detail="No clauses provided")
        
        logger.info(f"Performing CIA analysis on {len(clauses)} clauses")
        
        cia_analysis = cia_validator.analyze_document_cia(clauses)
        
        return CIAAnalysisResponse(
            total_clauses=cia_analysis['total_clauses'],
            cia_coverage=cia_analysis['cia_coverage'],
            cia_balance_index=cia_analysis['cia_balance_index'],
            balance_rating=cia_analysis['balance_rating'],
            imbalances=cia_analysis['imbalances'],
            recommendations=cia_analysis['recommendations']
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"CIA analysis error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="CIA analysis failed")


@router.post("/risk-prediction", response_model=RiskPredictionResponse)
async def predict_risk(analysis_data: Dict):
    """
    Predict audit risk level using ML model
    
    - Input: Compliance analysis metrics
    - Output: Risk level (Low/Medium/High) with confidence
    """
    try:
        logger.info("Predicting audit risk")
        
        risk_prediction = audit_predictor.predict_risk(analysis_data)
        
        return RiskPredictionResponse(
            risk_level=risk_prediction['risk_level'],
            confidence=risk_prediction['confidence'],
            probability_distribution=risk_prediction['probability_distribution'],
            recommendations=risk_prediction['recommendations']
        )
        
    except Exception as e:
        logger.error(f"Risk prediction error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Risk prediction failed")


@router.get("/cia-definitions")
async def get_cia_definitions():
    """Get CIA pillar definitions and indicators"""
    return {
        "confidentiality": {
            "name": "Confidentiality",
            "description": "Ensuring that information is accessible only to authorized individuals",
            "indicators": cia_validator.cia_keywords['confidentiality'],
            "icon": "🔒"
        },
        "integrity": {
            "name": "Integrity",
            "description": "Maintaining accuracy and completeness of data",
            "indicators": cia_validator.cia_keywords['integrity'],
            "icon": "✓"
        },
        "availability": {
            "name": "Availability",
            "description": "Ensuring timely and reliable access to information and systems",
            "indicators": cia_validator.cia_keywords['availability'],
            "icon": "🔄"
        }
    }
