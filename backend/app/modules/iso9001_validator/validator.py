"""
Module 4: ISO 9001 Quality Management Validator
Validates documented information, risk-based thinking, and continuous improvement
"""

import logging
from typing import Dict, List
import re

logger = logging.getLogger(__name__)


class ISO9001Validator:
    """
    ISO 9001:2015 Quality Management System Validator
    Validates key QMS requirements
    """
    
    def __init__(self):
        # ISO 9001 key requirements
        self.requirements = {
            'documented_information': {
                'keywords': ['document', 'record', 'procedure', 'documented information',
                           'quality manual', 'process', 'work instruction'],
                'weight': 0.25
            },
            'risk_based_thinking': {
                'keywords': ['risk', 'opportunity', 'threat', 'mitigation', 'risk assessment',
                           'risk management', 'contingency', 'preventive'],
                'weight': 0.25
            },
            'continuous_improvement': {
                'keywords': ['improvement', 'corrective action', 'preventive action',
                           'capa', 'nonconformity', 'audit', 'review', 'enhance'],
                'weight': 0.20
            },
            'customer_satisfaction': {
                'keywords': ['customer', 'client', 'satisfaction', 'feedback',
                           'complaint', 'requirement', 'expectation', 'service level'],
                'weight': 0.15
            },
            'leadership': {
                'keywords': ['leadership', 'management', 'commitment', 'responsibility',
                           'authority', 'policy', 'objective', 'management review'],
                'weight': 0.15
            }
        }
    
    def validate_iso9001_compliance(self, clauses: List[Dict[str, str]]) -> Dict[str, any]:
        """
        Validate document against ISO 9001 requirements
        
        Args:
            clauses: List of document clauses
            
        Returns:
            ISO 9001 validation results
        """
        if not clauses:
            return {
                'error': 'No clauses provided',
                'compliance_score': 0
            }
        
        requirement_scores = {}
        requirement_coverage = {}
        
        # Analyze each requirement
        for req_name, req_data in self.requirements.items():
            score, covered_clauses = self._check_requirement(clauses, req_data['keywords'])
            requirement_scores[req_name] = score
            requirement_coverage[req_name] = {
                'score': score,
                'weight': req_data['weight'],
                'covered_clauses_count': len(covered_clauses),
                'status': 'Covered' if score > 50 else 'Insufficient'
            }
        
        # Calculate weighted compliance score
        weighted_score = sum(
            requirement_scores[req] * self.requirements[req]['weight']
            for req in requirement_scores
        )
        
        # Identify gaps
        gaps = self._identify_iso9001_gaps(requirement_coverage)
        
        # Generate recommendations
        recommendations = self._generate_iso9001_recommendations(requirement_coverage, gaps)
        
        return {
            'framework': 'ISO 9001:2015',
            'compliance_score': round(weighted_score, 2),
            'compliance_rating': self._get_compliance_rating(weighted_score),
            'requirement_coverage': requirement_coverage,
            'gaps': gaps,
            'recommendations': recommendations
        }
    
    def _check_requirement(self, clauses: List[Dict[str, str]], keywords: List[str]) -> tuple:
        """Check coverage of specific requirement"""
        matching_clauses = []
        total_matches = 0
        
        for clause in clauses:
            clause_text = clause.get('text', '').lower()
            matches = sum(1 for keyword in keywords if keyword in clause_text)
            
            if matches > 0:
                matching_clauses.append(clause)
                total_matches += matches
        
        # Calculate score based on keyword density
        coverage_percentage = min((total_matches / len(keywords)) * 100, 100)
        
        return coverage_percentage, matching_clauses
    
    def _identify_iso9001_gaps(self, requirement_coverage: Dict) -> List[Dict[str, str]]:
        """Identify missing or weak ISO 9001 requirements"""
        gaps = []
        
        for req_name, coverage in requirement_coverage.items():
            if coverage['score'] < 50:
                gaps.append({
                    'requirement': req_name.replace('_', ' ').title(),
                    'current_score': coverage['score'],
                    'severity': 'High' if coverage['score'] < 25 else 'Medium',
                    'impact': f"Insufficient coverage of {req_name.replace('_', ' ')}"
                })
        
        return gaps
    
    def _generate_iso9001_recommendations(self, requirement_coverage: Dict, 
                                         gaps: List[Dict]) -> List[str]:
        """Generate ISO 9001 improvement recommendations"""
        recommendations = []
        
        for gap in gaps:
            req_name = gap['requirement'].lower().replace(' ', '_')
            
            if 'documented information' in gap['requirement'].lower():
                recommendations.append(
                    "📄 Add documented information controls: Include procedures for document "
                    "creation, approval, revision, and retention."
                )
            elif 'risk' in gap['requirement'].lower():
                recommendations.append(
                    "⚠️ Implement risk-based thinking: Add risk assessment processes, "
                    "risk registers, and mitigation strategies."
                )
            elif 'continuous improvement' in gap['requirement'].lower():
                recommendations.append(
                    "📈 Strengthen continuous improvement: Define corrective action procedures, "
                    "audit processes, and improvement metrics."
                )
            elif 'customer' in gap['requirement'].lower():
                recommendations.append(
                    "👥 Enhance customer focus: Add customer feedback mechanisms, "
                    "satisfaction surveys, and complaint handling procedures."
                )
            elif 'leadership' in gap['requirement'].lower():
                recommendations.append(
                    "🎯 Clarify leadership commitment: Define management responsibilities, "
                    "quality policy, and management review processes."
                )
        
        return recommendations
    
    def _get_compliance_rating(self, score: float) -> str:
        """Convert score to rating"""
        if score >= 85:
            return "Excellent"
        elif score >= 70:
            return "Good"
        elif score >= 50:
            return "Fair"
        else:
            return "Poor"
    
    def detect_quality_indicators(self, clauses: List[Dict[str, str]]) -> Dict[str, any]:
        """Detect quality management indicators in document"""
        indicators = {
            'pdca_cycle': False,  # Plan-Do-Check-Act
            'process_approach': False,
            'quality_objectives': False,
            'management_review': False,
            'internal_audit': False
        }
        
        full_text = ' '.join([c.get('text', '').lower() for c in clauses])
        
        # Check for PDCA cycle
        if all(word in full_text for word in ['plan', 'check', 'act']):
            indicators['pdca_cycle'] = True
        
        # Check for process approach
        if 'process' in full_text and ('input' in full_text or 'output' in full_text):
            indicators['process_approach'] = True
        
        # Check for quality objectives
        if 'quality objective' in full_text or 'measurable objective' in full_text:
            indicators['quality_objectives'] = True
        
        # Check for management review
        if 'management review' in full_text:
            indicators['management_review'] = True
        
        # Check for internal audit
        if 'internal audit' in full_text or 'audit program' in full_text:
            indicators['internal_audit'] = True
        
        present_count = sum(indicators.values())
        
        return {
            'indicators': indicators,
            'present_count': present_count,
            'total_count': len(indicators),
            'maturity_level': self._get_qms_maturity(present_count)
        }
    
    def _get_qms_maturity(self, present_count: int) -> str:
        """Determine QMS maturity level"""
        if present_count >= 4:
            return "Mature"
        elif present_count >= 3:
            return "Developing"
        elif present_count >= 1:
            return "Initial"
        else:
            return "Ad-hoc"


# Singleton instance
iso9001_validator = ISO9001Validator()
