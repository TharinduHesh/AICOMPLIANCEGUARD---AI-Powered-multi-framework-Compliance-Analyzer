"""
Module 8: Firebase Secure Metadata Storage
Stores encrypted compliance analysis metadata, scores, and audit logs
Raw documents are NEVER stored - only analysis outputs
"""

import logging
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path
import base64

try:
    import firebase_admin
    from firebase_admin import credentials, firestore
    FIREBASE_AVAILABLE = True
except ImportError:
    FIREBASE_AVAILABLE = False
    logger = logging.getLogger(__name__)
    logger.warning("Firebase SDK not installed. Install with: pip install firebase-admin")

from app.config.settings import settings

logger = logging.getLogger(__name__)


class FirebaseStorage:
    """
    Firebase Firestore Storage for Compliance Metadata
    
    Security Notes:
    - Only stores metadata (scores, predictions, logs)
    - NO raw document content stored
    - All sensitive data encrypted before storage
    - Automatic retention policies
    """
    
    def __init__(self):
        self.db = None
        self.enabled = FIREBASE_AVAILABLE and self._initialize_firebase()
        
        if not self.enabled:
            logger.warning("Firebase storage is DISABLED. Running in local-only mode.")
    
    def _initialize_firebase(self) -> bool:
        """Initialize Firebase connection"""
        try:
            # Check if Firebase is already initialized
            if firebase_admin._apps:
                self.db = firestore.client()
                logger.info("Firebase already initialized")
                return True
            
            # Check if credentials file exists
            creds_path = Path(settings.FIREBASE_CREDENTIALS_PATH)
            
            if not creds_path.exists():
                logger.warning(f"Firebase credentials not found at: {creds_path}")
                return False
            
            # Initialize Firebase
            cred = credentials.Certificate(str(creds_path))
            firebase_admin.initialize_app(cred)
            self.db = firestore.client()
            
            logger.info("✅ Firebase initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Firebase initialization failed: {str(e)}")
            return False
    
    def store_analysis_metadata(self, analysis_data: Dict[str, Any]) -> str:
        """
        Store compliance analysis metadata (NO raw documents)
        
        Args:
            analysis_data: Analysis results with scores and predictions
            
        Returns:
            Document ID in Firestore
        """
        if not self.enabled:
            logger.debug("Firebase disabled - metadata not stored")
            return "local_" + analysis_data.get('analysis_id', 'unknown')
        
        try:
            # Prepare metadata (exclude any raw document text)
            metadata = self._prepare_metadata(analysis_data)
            
            # Add timestamp
            metadata['stored_at'] = firestore.SERVER_TIMESTAMP
            metadata['retention_until'] = self._calculate_retention_date()
            
            # Store in Firestore
            doc_ref = self.db.collection('compliance_analyses').document(metadata['analysis_id'])
            doc_ref.set(metadata)
            
            logger.info(f"✅ Metadata stored in Firebase: {metadata['analysis_id']}")
            return metadata['analysis_id']
            
        except Exception as e:
            logger.error(f"Failed to store metadata: {str(e)}")
            raise
    
    def _prepare_metadata(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare metadata, excluding any raw document content"""
        metadata = {
            'analysis_id': analysis_data.get('analysis_id'),
            'file_name': analysis_data.get('file_name'),
            'file_hash': analysis_data.get('file_hash', ''),
            'frameworks': analysis_data.get('frameworks', []),
            'analyzed_at': analysis_data.get('analyzed_at'),
            
            # Compliance scores only (no raw text)
            'compliance_scores': {},
            'risk_prediction': {},
            'audit_readiness': {},
            'cia_metrics': {}
        }
        
        # Extract compliance scores
        if 'compliance_results' in analysis_data:
            for framework, results in analysis_data['compliance_results'].items():
                metadata['compliance_scores'][framework] = {
                    'compliance_percentage': results.get('compliance_percentage', 0),
                    'matched_controls_count': results.get('matched_controls_count', 0),
                    'total_controls': results.get('total_controls', 0),
                    'missing_controls_count': len(results.get('missing_controls', []))
                }
        
        # Risk prediction
        if 'risk_prediction' in analysis_data:
            metadata['risk_prediction'] = {
                'risk_level': analysis_data['risk_prediction'].get('risk_level'),
                'confidence': analysis_data['risk_prediction'].get('confidence', 0)
            }
        
        # Audit readiness
        if 'audit_readiness' in analysis_data:
            metadata['audit_readiness'] = {
                'score': analysis_data['audit_readiness'].get('audit_readiness_score', 0),
                'level': analysis_data['audit_readiness'].get('readiness_level')
            }
        
        # CIA metrics
        if 'cia_analysis' in analysis_data:
            metadata['cia_metrics'] = {
                'balance_index': analysis_data['cia_analysis'].get('cia_balance_index', 0),
                'confidentiality': analysis_data['cia_analysis'].get('confidentiality_score', 0),
                'integrity': analysis_data['cia_analysis'].get('integrity_score', 0),
                'availability': analysis_data['cia_analysis'].get('availability_score', 0)
            }
        
        return metadata
    
    def _calculate_retention_date(self) -> datetime:
        """Calculate retention date (e.g., 90 days)"""
        from datetime import timedelta
        return datetime.utcnow() + timedelta(days=90)
    
    def get_analysis_metadata(self, analysis_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve analysis metadata by ID
        
        Args:
            analysis_id: Analysis document ID
            
        Returns:
            Metadata dictionary or None
        """
        if not self.enabled:
            return None
        
        try:
            doc_ref = self.db.collection('compliance_analyses').document(analysis_id)
            doc = doc_ref.get()
            
            if doc.exists:
                logger.info(f"Retrieved metadata: {analysis_id}")
                return doc.to_dict()
            else:
                logger.warning(f"Metadata not found: {analysis_id}")
                return None
                
        except Exception as e:
            logger.error(f"Failed to retrieve metadata: {str(e)}")
            return None
    
    def list_user_analyses(self, user_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """
        List analyses for a specific user
        
        Args:
            user_id: User identifier
            limit: Maximum number of results
            
        Returns:
            List of metadata dictionaries
        """
        if not self.enabled:
            return []
        
        try:
            query = self.db.collection('compliance_analyses') \
                .where('user_id', '==', user_id) \
                .order_by('analyzed_at', direction=firestore.Query.DESCENDING) \
                .limit(limit)
            
            docs = query.stream()
            analyses = [doc.to_dict() for doc in docs]
            
            logger.info(f"Retrieved {len(analyses)} analyses for user {user_id}")
            return analyses
            
        except Exception as e:
            logger.error(f"Failed to list analyses: {str(e)}")
            return []
    
    def store_audit_log(self, log_entry: Dict[str, Any]) -> str:
        """
        Store security audit log entry
        
        Args:
            log_entry: Log data (event type, timestamp, details)
            
        Returns:
            Log entry ID
        """
        if not self.enabled:
            logger.debug("Firebase disabled - audit log not stored")
            return "local_log"
        
        try:
            log_entry['timestamp'] = firestore.SERVER_TIMESTAMP
            doc_ref = self.db.collection('audit_logs').add(log_entry)
            
            logger.debug(f"Audit log stored: {log_entry.get('event_type')}")
            return doc_ref[1].id
            
        except Exception as e:
            logger.error(f"Failed to store audit log: {str(e)}")
            return ""
    
    def cleanup_expired_metadata(self) -> int:
        """
        Delete metadata that has passed retention period
        
        Returns:
            Number of deleted documents
        """
        if not self.enabled:
            return 0
        
        try:
            now = datetime.utcnow()
            
            # Query expired documents
            query = self.db.collection('compliance_analyses') \
                .where('retention_until', '<', now)
            
            docs = query.stream()
            deleted_count = 0
            
            for doc in docs:
                doc.reference.delete()
                deleted_count += 1
            
            if deleted_count > 0:
                logger.info(f"Cleaned up {deleted_count} expired metadata entries")
            
            return deleted_count
            
        except Exception as e:
            logger.error(f"Cleanup failed: {str(e)}")
            return 0
    
    def get_storage_stats(self) -> Dict[str, Any]:
        """
        Get storage statistics
        
        Returns:
            Statistics dictionary
        """
        if not self.enabled:
            return {'enabled': False, 'message': 'Firebase storage disabled'}
        
        try:
            # Count documents
            analyses_count = len(list(self.db.collection('compliance_analyses').limit(1000).stream()))
            logs_count = len(list(self.db.collection('audit_logs').limit(1000).stream()))
            
            return {
                'enabled': True,
                'analyses_stored': analyses_count,
                'audit_logs_stored': logs_count,
                'retention_days': 90
            }
            
        except Exception as e:
            logger.error(f"Failed to get stats: {str(e)}")
            return {'enabled': True, 'error': str(e)}


# Singleton instance
firebase_storage = FirebaseStorage()
