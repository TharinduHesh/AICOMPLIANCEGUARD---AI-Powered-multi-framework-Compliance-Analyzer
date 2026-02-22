"""
Module 5: Knowledge Graph Mapping Engine
Cross-maps controls between ISO 27001, ISO 9001, NIST, and GDPR
"""

import logging
from typing import Dict, List, Set
import json
from pathlib import Path

from app.config.settings import settings

logger = logging.getLogger(__name__)


class KnowledgeGraphMapper:
    """
    Knowledge Graph for multi-framework compliance mapping
    Maps controls across different frameworks to identify overlaps
    """
    
    def __init__(self):
        self.mappings = {
            'iso27001_to_iso9001': {
                # ISO 27001 Annex A controls to ISO 9001 clauses
                'A.5.1': ['7.5', '4.4'],  # Documented information
                'A.8.1': ['6.1', '8.1'],  # Risk assessment
                'A.12.1': ['8.5', '8.6'],  # Operational planning
                'A.18.1': ['9.3', '10.2'],  # Compliance & improvement
            },
            'iso27001_to_nist': {
                # ISO 27001 to NIST CSF
                'A.5': ['ID.GV', 'ID.RA'],  # Governance & Risk
                'A.9': ['PR.AC'],  # Access Control
                'A.12': ['DE.CM', 'RS.AN'],  # Operations & Detection
                'A.16': ['RS.RP', 'RC.RP'],  # Incident Response
            },
            'iso27001_to_gdpr': {
                # ISO 27001 to GDPR Articles
                'A.9': ['Art.32'],  # Access Control -> Security
                'A.18': ['Art.5', 'Art.24'],  # Compliance -> Lawfulness
                'A.16': ['Art.33', 'Art.34'],  # Incident -> Breach Notification
            }
        }
        
        self.framework_relationships = self._build_relationships()
    
    def _build_relationships(self) -> Dict[str, List[Dict]]:
        """Build bidirectional relationships between frameworks"""
        relationships = {
            'iso27001': [],
            'iso9001': [],
            'nist': [],
            'gdpr': []
        }
        
        # ISO 27001 ↔ ISO 9001
        relationships['iso27001'].append({
            'target_framework': 'iso9001',
            'relationship': 'complements',
            'description': 'Information security complements quality management'
        })
        
        relationships['iso9001'].append({
            'target_framework': 'iso27001',
            'relationship': 'aligns_with',
            'description': 'Quality processes align with security controls'
        })
        
        # ISO 27001 ↔ NIST
        relationships['iso27001'].append({
            'target_framework': 'nist',
            'relationship': 'maps_to',
            'description': 'Security controls map to NIST functions'
        })
        
        # ISO 27001 ↔ GDPR
        relationships['iso27001'].append({
            'target_framework': 'gdpr',
            'relationship': 'supports',
            'description': 'Security controls support GDPR compliance'
        })
        
        return relationships
    
    def map_control(self, control_id: str, source_framework: str, 
                   target_framework: str) -> List[str]:
        """
        Map a control from source framework to target framework
        
        Args:
            control_id: Control identifier (e.g., 'A.9.1')
            source_framework: Source framework name
            target_framework: Target framework name
            
        Returns:
            List of mapped control IDs in target framework
        """
        mapping_key = f"{source_framework}_to_{target_framework}"
        
        if mapping_key not in self.mappings:
            logger.warning(f"No mapping found for {mapping_key}")
            return []
        
        # Find matching control
        for source_control, target_controls in self.mappings[mapping_key].items():
            if control_id.startswith(source_control):
                return target_controls
        
        return []
    
    def generate_unified_view(self, matched_controls: Dict[str, List[str]]) -> Dict[str, any]:
        """
        Generate unified compliance view across multiple frameworks
        
        Args:
            matched_controls: Dictionary of framework -> list of matched control IDs
            
        Returns:
            Unified compliance view with cross-framework insights
        """
        unified_controls = {}
        coverage_overlap = {}
        
        # Analyze overlaps
        for framework, controls in matched_controls.items():
            for control_id in controls:
                # Find mappings to other frameworks
                for other_framework in matched_controls.keys():
                    if other_framework != framework:
                        mapped = self.map_control(control_id, framework, other_framework)
                        
                        if mapped:
                            overlap_key = f"{framework}_{other_framework}"
                            if overlap_key not in coverage_overlap:
                                coverage_overlap[overlap_key] = []
                            
                            coverage_overlap[overlap_key].append({
                                'source_control': control_id,
                                'target_controls': mapped,
                                'benefit': 'Single control satisfies multiple frameworks'
                            })
        
        # Calculate efficiency gains
        total_controls = sum(len(controls) for controls in matched_controls.values())
        overlapping_controls = sum(len(overlaps) for overlaps in coverage_overlap.values())
        
        efficiency_gain = 0
        if total_controls > 0:
            efficiency_gain = (overlapping_controls / total_controls) * 100
        
        return {
            'frameworks': list(matched_controls.keys()),
            'total_controls': total_controls,
            'overlapping_controls': overlapping_controls,
            'efficiency_gain_percentage': round(efficiency_gain, 2),
            'coverage_overlap': coverage_overlap,
            'recommendations': self._generate_mapping_recommendations(coverage_overlap)
        }
    
    def _generate_mapping_recommendations(self, coverage_overlap: Dict) -> List[str]:
        """Generate recommendations based on framework mappings"""
        recommendations = []
        
        if not coverage_overlap:
            recommendations.append(
                "ℹ️ Consider implementing controls that satisfy multiple frameworks "
                "to reduce compliance effort."
            )
        else:
            recommendations.append(
                f"✅ {len(coverage_overlap)} control mappings identified across frameworks. "
                "Leverage these overlaps to reduce duplicate work."
            )
            
            recommendations.append(
                "💡 Document cross-framework mappings to demonstrate comprehensive compliance "
                "during audits."
            )
        
        return recommendations
    
    def get_framework_relationships(self, framework: str) -> List[Dict]:
        """Get relationships between frameworks"""
        return self.framework_relationships.get(framework, [])
    
    def calculate_multi_framework_score(self, framework_scores: Dict[str, float]) -> Dict[str, any]:
        """
        Calculate overall multi-framework compliance score
        
        Args:
            framework_scores: Dictionary of framework -> compliance percentage
            
        Returns:
            Multi-framework analysis
        """
        if not framework_scores:
            return {
                'overall_score': 0,
                'framework_count': 0
            }
        
        # Calculate weighted average (can be customized)
        weights = {
            'iso27001': 0.35,
            'iso9001': 0.25,
            'nist': 0.25,
            'gdpr': 0.15
        }
        
        weighted_score = 0
        weight_sum = 0
        
        for framework, score in framework_scores.items():
            weight = weights.get(framework, 0.25)  # Default weight
            weighted_score += score * weight
            weight_sum += weight
        
        overall_score = weighted_score / weight_sum if weight_sum > 0 else 0
        
        # Identify strongest and weakest frameworks
        sorted_frameworks = sorted(framework_scores.items(), key=lambda x: x[1], reverse=True)
        
        return {
            'overall_score': round(overall_score, 2),
            'framework_count': len(framework_scores),
            'framework_scores': framework_scores,
            'strongest_framework': sorted_frameworks[0][0] if sorted_frameworks else None,
            'weakest_framework': sorted_frameworks[-1][0] if sorted_frameworks else None,
            'rating': self._get_multi_framework_rating(overall_score)
        }
    
    def _get_multi_framework_rating(self, score: float) -> str:
        """Convert multi-framework score to rating"""
        if score >= 85:
            return "Excellent - Comprehensive multi-framework compliance"
        elif score >= 70:
            return "Good - Strong compliance across frameworks"
        elif score >= 50:
            return "Fair - Moderate compliance, improvement needed"
        else:
            return "Poor - Significant gaps in compliance"


# Singleton instance
knowledge_graph = KnowledgeGraphMapper()
