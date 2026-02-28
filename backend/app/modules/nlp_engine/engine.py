"""
Module 2: NLP Compliance Intelligence Engine
DistilBERT-based clause classification and semantic similarity matching
"""

import logging
from typing import Dict, List, Tuple, Optional
import numpy as np
import json
from pathlib import Path

from app.config.settings import settings

logger = logging.getLogger(__name__)


class NLPComplianceEngine:
    """
    NLP-powered compliance intelligence using transformer models
    Performs clause classification, semantic matching, and gap analysis
    """
    
    def __init__(self):
        self.model_name = "sentence-transformers/all-MiniLM-L6-v2"
        self.model = None
        self.frameworks_data = {}
        try:
            import torch
            self.device = "cuda" if settings.USE_GPU and torch.cuda.is_available() else "cpu"
        except ImportError:
            self.device = "cpu"
        
        # Load model lazily
        self._load_model()
        self._load_frameworks()
    
    def _load_model(self):
        """Load sentence transformer model for semantic similarity"""
        try:
            from sentence_transformers import SentenceTransformer
            logger.info(f"Loading NLP model: {self.model_name} on {self.device}")
            self.model = SentenceTransformer(self.model_name, device=self.device)
            logger.info("NLP model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load NLP model: {str(e)}")
            self.model = None
    
    def _load_frameworks(self):
        """Load compliance framework data"""
        try:
            frameworks_dir = Path(settings.FRAMEWORKS_DATA_DIR)
            
            # Load each framework
            framework_files = {
                'iso27001': 'iso27001_controls.json',
                'iso9001': 'iso9001_requirements.json',
                'nist': 'nist_csf.json',
                'gdpr': 'pdpa_gdpr.json'
            }
            
            for framework, filename in framework_files.items():
                filepath = frameworks_dir / filename
                if filepath.exists():
                    with open(filepath, 'r', encoding='utf-8') as f:
                        self.frameworks_data[framework] = json.load(f)
                    logger.info(f"Loaded framework: {framework}")
                else:
                    logger.warning(f"Framework file not found: {filepath}")
                    
        except Exception as e:
            logger.error(f"Failed to load frameworks: {str(e)}")
    
    def encode_text(self, text: str) -> np.ndarray:
        """
        Encode text to embeddings
        
        Args:
            text: Input text
            
        Returns:
            Embedding vector
        """
        if self.model is None:
            self._load_model()
        
        return self.model.encode(text, convert_to_numpy=True)
    
    def encode_batch(self, texts: List[str]) -> np.ndarray:
        """
        Encode multiple texts to embeddings
        
        Args:
            texts: List of input texts
            
        Returns:
            Matrix of embedding vectors
        """
        if self.model is None:
            self._load_model()
        
        return self.model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
    
    def calculate_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate semantic similarity between two texts
        
        Args:
            text1: First text
            text2: Second text
            
        Returns:
            Similarity score (0-1)
        """
        embedding1 = self.encode_text(text1)
        embedding2 = self.encode_text(text2)
        
        from sklearn.metrics.pairwise import cosine_similarity
        similarity = cosine_similarity(
            embedding1.reshape(1, -1),
            embedding2.reshape(1, -1)
        )[0][0]
        
        return float(similarity)
    
    def classify_clause(self, clause_text: str, framework: str = 'iso27001') -> Dict[str, any]:
        """
        Classify a clause against framework controls
        
        Args:
            clause_text: The clause text to classify
            framework: Target framework (iso27001, iso9001, nist, gdpr)
            
        Returns:
            Classification results with matched controls
        """
        if framework not in self.frameworks_data:
            logger.warning(f"Framework {framework} not loaded. Using default classification.")
            return self._default_classification(clause_text)
        
        framework_controls = self.frameworks_data[framework].get('controls', [])
        
        # Encode clause
        clause_embedding = self.encode_text(clause_text)
        
        # Encode all control descriptions
        control_texts = [ctrl.get('description', ctrl.get('title', '')) for ctrl in framework_controls]
        control_embeddings = self.encode_batch(control_texts)
        
        # Calculate similarities
        from sklearn.metrics.pairwise import cosine_similarity
        similarities = cosine_similarity(
            clause_embedding.reshape(1, -1),
            control_embeddings
        )[0]
        
        # Get top matches
        top_indices = np.argsort(similarities)[::-1][:3]
        
        matches = []
        for idx in top_indices:
            if similarities[idx] > 0.3:  # Threshold for relevance
                control = framework_controls[idx]
                matches.append({
                    'control_id': control.get('id', 'Unknown'),
                    'control_title': control.get('title', 'Unknown'),
                    'similarity_score': float(similarities[idx]),
                    'category': control.get('category', 'General')
                })
        
        return {
            'clause': clause_text[:100] + '...' if len(clause_text) > 100 else clause_text,
            'framework': framework,
            'matches': matches,
            'best_match': matches[0] if matches else None,
            'is_matched': len(matches) > 0
        }
    
    def _default_classification(self, clause_text: str) -> Dict[str, any]:
        """Default classification when framework data not available"""
        # Simple keyword-based classification
        keywords_map = {
            'access_control': ['access', 'authentication', 'authorization', 'login', 'password'],
            'data_protection': ['data', 'privacy', 'confidential', 'encryption', 'protection'],
            'incident_management': ['incident', 'breach', 'response', 'emergency'],
            'risk_management': ['risk', 'assessment', 'threat', 'vulnerability'],
            'compliance': ['compliance', 'audit', 'regulation', 'policy']
        }
        
        clause_lower = clause_text.lower()
        detected_categories = []
        
        for category, keywords in keywords_map.items():
            if any(keyword in clause_lower for keyword in keywords):
                detected_categories.append(category)
        
        return {
            'clause': clause_text[:100] + '...' if len(clause_text) > 100 else clause_text,
            'framework': 'default',
            'detected_categories': detected_categories,
            'is_matched': len(detected_categories) > 0
        }
    
    def analyze_document_compliance(self, clauses: List[Dict[str, str]], framework: str = 'iso27001') -> Dict[str, any]:
        """
        Analyze entire document for compliance
        
        Args:
            clauses: List of document clauses
            framework: Target framework
            
        Returns:
            Comprehensive compliance analysis
        """
        if not clauses:
            return {
                'error': 'No clauses provided',
                'compliance_percentage': 0
            }
        
        classified_clauses = []
        matched_controls = set()
        weak_clauses = []
        
        for clause in clauses:
            clause_text = clause.get('text', '')
            
            # Classify clause
            classification = self.classify_clause(clause_text, framework)
            classified_clauses.append(classification)
            
            # Track matched controls
            if classification.get('best_match'):
                matched_controls.add(classification['best_match']['control_id'])
            
            # Detect weak clauses (low similarity)
            if classification.get('best_match') and classification['best_match']['similarity_score'] < 0.5:
                weak_clauses.append({
                    'clause': clause_text[:100],
                    'reason': 'Low similarity to framework controls',
                    'score': classification['best_match']['similarity_score']
                })
        
        # Calculate compliance metrics
        total_controls = len(self.frameworks_data.get(framework, {}).get('controls', []))
        if total_controls == 0:
            total_controls = 100  # Default assumption
        
        matched_count = len(matched_controls)
        compliance_percentage = (matched_count / total_controls) * 100
        
        # Identify missing controls
        missing_controls = self._identify_missing_controls(matched_controls, framework)
        
        return {
            'framework': framework,
            'total_clauses': len(clauses),
            'matched_clauses': len([c for c in classified_clauses if c.get('is_matched')]),
            'compliance_percentage': round(compliance_percentage, 2),
            'matched_controls': list(matched_controls),
            'matched_controls_count': matched_count,
            'total_controls': total_controls,
            'missing_controls': missing_controls[:10],  # Top 10
            'weak_clauses': weak_clauses[:5],  # Top 5
            'classified_clauses': classified_clauses[:10]  # Sample
        }
    
    def _identify_missing_controls(self, matched_controls: set, framework: str) -> List[Dict[str, str]]:
        """Identify controls not covered in document"""
        if framework not in self.frameworks_data:
            return []
        
        all_controls = self.frameworks_data[framework].get('controls', [])
        missing = []
        
        for control in all_controls:
            control_id = control.get('id', '')
            if control_id not in matched_controls:
                missing.append({
                    'control_id': control_id,
                    'title': control.get('title', 'Unknown'),
                    'category': control.get('category', 'General'),
                    'priority': control.get('priority', 'Medium')
                })
        
        # Sort by priority
        priority_order = {'Critical': 0, 'High': 1, 'Medium': 2, 'Low': 3}
        missing.sort(key=lambda x: priority_order.get(x.get('priority', 'Medium'), 2))
        
        return missing
    
    def detect_weak_policies(self, clauses: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        Detect weak or vague policy statements
        
        Args:
            clauses: Document clauses
            
        Returns:
            List of weak clauses with reasons
        """
        weak_indicators = [
            'may', 'might', 'could', 'should consider', 'as appropriate',
            'where possible', 'if feasible', 'efforts will be made'
        ]
        
        weak_clauses = []
        
        for clause in clauses:
            clause_text = clause.get('text', '').lower()
            
            # Check for weak language
            found_indicators = [ind for ind in weak_indicators if ind in clause_text]
            
            if found_indicators:
                weak_clauses.append({
                    'clause': clause.get('text', '')[:100],
                    'section': clause.get('section', 'Unknown'),
                    'weak_indicators': found_indicators,
                    'suggestion': 'Use stronger, mandatory language (shall, must, will)'
                })
            
            # Check for vague statements (very short)
            if len(clause_text.split()) < 10:
                weak_clauses.append({
                    'clause': clause.get('text', '')[:100],
                    'section': clause.get('section', 'Unknown'),
                    'weak_indicators': ['too_short'],
                    'suggestion': 'Provide more specific details and requirements'
                })
        
        return weak_clauses[:10]  # Top 10


# Lazy singleton instance
_nlp_engine_instance = None

def _get_nlp_engine():
    global _nlp_engine_instance
    if _nlp_engine_instance is None:
        _nlp_engine_instance = NLPComplianceEngine()
    return _nlp_engine_instance

class _LazyNLPEngine:
    """Proxy that defers NLPComplianceEngine construction until first use."""
    def __getattr__(self, name):
        return getattr(_get_nlp_engine(), name)

nlp_engine = _LazyNLPEngine()
