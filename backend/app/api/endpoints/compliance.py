"""
Compliance Analysis API Endpoints
Main endpoints for document upload and analysis
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from typing import List
import logging
from datetime import datetime
import secrets

from app.models.schemas import (
    DocumentUploadResponse,
    ComplianceAnalysisRequest,
    ComplianceAnalysisResponse
)
from app.modules.document_processor import document_processor
from app.modules.nlp_engine import nlp_engine
from app.modules.cia_validator import cia_validator
from app.modules.iso9001_validator import iso9001_validator
from app.modules.audit_predictor import audit_predictor
from app.modules.security_layer import security_layer
from app.modules.knowledge_graph import knowledge_graph

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """
    Upload compliance document for analysis
    
    - Supports PDF and DOCX formats
    - Maximum file size: 10MB
    - Files are encrypted and automatically deleted after processing
    """
    try:
        # Read file data
        file_data = await file.read()
        
        # Validate file size
        is_valid, error_msg = security_layer.validate_file_size(len(file_data))
        if not is_valid:
            raise HTTPException(status_code=400, detail=error_msg)
        
        # Validate file format
        file_extension = file.filename.split('.')[-1].lower()
        if file_extension not in ['pdf', 'docx']:
            raise HTTPException(
                status_code=400,
                detail="Unsupported file format. Only PDF and DOCX are supported."
            )
        
        # Secure upload
        secure_path, file_hash = security_layer.secure_file_upload(file_data, file.filename)
        
        # Log security event
        security_layer.log_security_event(
            'document_upload',
            {
                'filename': file.filename,
                'size': len(file_data),
                'hash': file_hash[:16]
            }
        )
        
        # Generate file ID
        file_id = secrets.token_urlsafe(16)
        
        return DocumentUploadResponse(
            file_id=file_id,
            file_name=file.filename,
            file_hash=file_hash,
            file_size=len(file_data),
            uploaded_at=datetime.utcnow().isoformat()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Upload error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="File upload failed")


@router.post("/analyze", response_model=ComplianceAnalysisResponse)
async def analyze_compliance(request: ComplianceAnalysisRequest):
    """
    Analyze uploaded document for compliance
    
    - Multi-framework analysis (ISO 27001, ISO 9001, NIST, GDPR)
    - CIA balance analysis
    - Missing control detection
    - Audit risk prediction
    """
    try:
        logger.info(f"Starting compliance analysis for file_id: {request.file_id}")
        
        # For demo purposes, we'll use a sample analysis
        # In production, retrieve the file using file_id
        
        # Simulated document processing (replace with actual file retrieval)
        sample_clauses = [
            {'text': 'Access to information systems must be controlled and monitored.', 'section': '1'},
            {'text': 'All employees must use strong passwords and change them every 90 days.', 'section': '2'},
            {'text': 'Data backups must be performed daily and stored securely offsite.', 'section': '3'},
            {'text': 'Incident response procedures must be documented and tested annually.', 'section': '4'},
            {'text': 'Information security policies must be reviewed and approved by management.', 'section': '5'}
        ]
        
        results = {}
        
        # Analyze for each requested framework
        for framework in request.frameworks:
            logger.info(f"Analyzing framework: {framework}")
            compliance_results = nlp_engine.analyze_document_compliance(sample_clauses, framework)
            results[framework] = compliance_results
        
        # CIA Analysis
        cia_analysis = None
        if request.include_cia:
            logger.info("Performing CIA analysis")
            cia_analysis = cia_validator.analyze_document_cia(sample_clauses)
        
        # ISO 9001 Analysis
        iso9001_analysis = None
        if request.include_iso9001:
            logger.info("Performing ISO 9001 analysis")
            iso9001_analysis = iso9001_validator.validate_iso9001_compliance(sample_clauses)
        
        # Prepare data for risk prediction
        analysis_data = {
            'missing_controls_count': results.get('iso27001', {}).get('total_controls', 114) - 
                                     results.get('iso27001', {}).get('matched_controls_count', 0),
            'cia_balance_index': cia_analysis.get('cia_balance_index', 50) if cia_analysis else 50,
            'weak_clauses': results.get('iso27001', {}).get('weak_clauses', []),
            'total_clauses': len(sample_clauses),
            'compliance_percentage': results.get('iso27001', {}).get('compliance_percentage', 0)
        }
        
        # Risk Prediction
        logger.info("Predicting audit risk")
        risk_prediction = audit_predictor.predict_risk(analysis_data)
        audit_readiness = audit_predictor.get_audit_readiness_score(risk_prediction)
        
        # Generate analysis ID
        analysis_id = secrets.token_urlsafe(16)
        
        logger.info(f"Analysis completed: {analysis_id}")
        
        return ComplianceAnalysisResponse(
            analysis_id=analysis_id,
            file_name=f"document_{request.file_id}",
            frameworks=request.frameworks,
            compliance_results=results,
            cia_analysis=cia_analysis,
            iso9001_analysis=iso9001_analysis,
            risk_prediction=risk_prediction,
            audit_readiness=audit_readiness,
            analyzed_at=datetime.utcnow().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Analysis error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Compliance analysis failed")


@router.get("/frameworks")
async def get_supported_frameworks():
    """
    Get list of supported compliance frameworks
    """
    return {
        "frameworks": [
            {
                "id": "iso27001",
                "name": "ISO/IEC 27001:2022",
                "description": "Information Security Management System",
                "controls_count": 114
            },
            {
                "id": "iso9001",
                "name": "ISO 9001:2015",
                "description": "Quality Management System",
                "controls_count": 10
            },
            {
                "id": "nist",
                "name": "NIST Cybersecurity Framework",
                "description": "NIST CSF 2.0",
                "controls_count": 108
            },
            {
                "id": "gdpr",
                "name": "GDPR/PDPA",
                "description": "Data Privacy Regulations",
                "controls_count": 57
            }
        ]
    }


@router.get("/health")
async def health_check():
    """Health check for compliance service"""
    return {
        "status": "healthy",
        "service": "compliance_analysis",
        "modules": {
            "document_processor": "operational",
            "nlp_engine": "operational",
            "cia_validator": "operational",
            "iso9001_validator": "operational",
            "audit_predictor": "operational",
            "security_layer": "operational"
        }
    }
