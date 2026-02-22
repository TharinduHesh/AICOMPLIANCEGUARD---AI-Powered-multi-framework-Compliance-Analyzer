"""
Module 3: CIA Validation Engine
Classifies controls into Confidentiality, Integrity, Availability
Calculates CIA coverage, balance, and generates heatmaps
"""

import logging
from typing import Dict, List, Tuple
import numpy as np
from collections import defaultdict

logger = logging.getLogger(__name__)


class CIAValidator:
    """
    CIA (Confidentiality, Integrity, Availability) Validation Engine
    Novel contribution: CIA Balance Index for compliance assessment
    """
    
    def __init__(self):
        # CIA classification keywords
        self.cia_keywords = {
            'confidentiality': [
                'confidential', 'privacy', 'secret', 'classified', 'access control',
                'authentication', 'authorization', 'encryption', 'data protection',
                'information disclosure', 'need-to-know', 'clearance', 'sensitive',
                'personal data', 'pii', 'gdpr', 'data privacy'
            ],
            'integrity': [
                'integrity', 'accuracy', 'validity', 'completeness', 'consistency',
                'verification', 'validation', 'audit trail', 'change control',
                'version control', 'tampering', 'modification', 'alteration',
                'digital signature', 'hash', 'checksum', 'quality', 'correctness'
            ],
            'availability': [
                'availability', 'uptime', 'accessible', 'redundancy', 'backup',
                'disaster recovery', 'business continuity', 'failover', 'resilience',
                'recovery time', 'rto', 'rpo', 'downtime', 'service level',
                'performance', 'reliability', 'fault tolerance', 'high availability'
            ]
        }
        
        # CIA categories definitions
        self.cia_definitions = {
            'confidentiality': {
                'name': 'Confidentiality',
                'description': 'Ensuring that information is accessible only to authorized individuals',
                'icon': '🔒'
            },
            'integrity': {
                'name': 'Integrity',
                'description': 'Maintaining accuracy and completeness of data',
                'icon': '✓'
            },
            'availability': {
                'name': 'Availability',
                'description': 'Ensuring timely and reliable access to information and systems',
                'icon': '🔄'
            }
        }
    
    def classify_clause_cia(self, clause_text: str) -> Dict[str, any]:
        """
        Classify a clause into CIA categories
        
        Args:
            clause_text: The clause text to classify
            
        Returns:
            CIA classification with scores
        """
        clause_lower = clause_text.lower()
        cia_scores = {
            'confidentiality': 0,
            'integrity': 0,
            'availability': 0
        }
        
        # Count keyword matches for each CIA category
        for category, keywords in self.cia_keywords.items():
            for keyword in keywords:
                if keyword in clause_lower:
                    cia_scores[category] += 1
        
        # Normalize scores
        total_matches = sum(cia_scores.values())
        
        if total_matches > 0:
            cia_percentages = {
                cat: (score / total_matches) * 100
                for cat, score in cia_scores.items()
            }
        else:
            # If no keywords found, classify as general (equal distribution)
            cia_percentages = {
                'confidentiality': 33.33,
                'integrity': 33.33,
                'availability': 33.34
            }
        
        # Determine primary category
        primary_category = max(cia_scores.items(), key=lambda x: x[1])[0]
        
        # Determine if clause is multi-category
        non_zero_categories = [cat for cat, score in cia_scores.items() if score > 0]
        is_multi_category = len(non_zero_categories) > 1
        
        return {
            'clause': clause_text[:100] + '...' if len(clause_text) > 100 else clause_text,
            'primary_category': primary_category,
            'cia_scores': cia_scores,
            'cia_percentages': cia_percentages,
            'is_multi_category': is_multi_category,
            'categories': non_zero_categories
        }
    
    def analyze_document_cia(self, clauses: List[Dict[str, str]]) -> Dict[str, any]:
        """
        Analyze entire document for CIA coverage
        
        Args:
            clauses: List of document clauses
            
        Returns:
            Comprehensive CIA analysis
        """
        if not clauses:
            return {
                'error': 'No clauses provided',
                'cia_coverage': {'confidentiality': 0, 'integrity': 0, 'availability': 0}
            }
        
        cia_distribution = {
            'confidentiality': 0,
            'integrity': 0,
            'availability': 0
        }
        
        classified_clauses = []
        
        # Classify each clause
        for clause in clauses:
            clause_text = clause.get('text', '')
            classification = self.classify_clause_cia(clause_text)
            classified_clauses.append(classification)
            
            # Count primary category
            primary = classification['primary_category']
            cia_distribution[primary] += 1
        
        total_clauses = len(clauses)
        
        # Calculate coverage percentages
        cia_coverage = {
            cat: round((count / total_clauses) * 100, 2)
            for cat, count in cia_distribution.items()
        }
        
        # Calculate CIA Balance Index (Novel Metric)
        balance_index = self.calculate_cia_balance_index(cia_coverage)
        
        # Identify imbalances
        imbalances = self._identify_cia_imbalances(cia_coverage)
        
        # Generate CIA heatmap data
        heatmap = self._generate_cia_heatmap(classified_clauses)
        
        return {
            'total_clauses': total_clauses,
            'cia_coverage': cia_coverage,
            'cia_distribution': cia_distribution,
            'cia_balance_index': balance_index,
            'balance_rating': self._get_balance_rating(balance_index),
            'imbalances': imbalances,
            'heatmap': heatmap,
            'recommendations': self._generate_cia_recommendations(cia_coverage, imbalances)
        }
    
    def calculate_cia_balance_index(self, cia_coverage: Dict[str, float]) -> float:
        """
        Calculate CIA Balance Index (Novel Research Contribution)
        
        Measures how balanced the CIA coverage is across the three pillars
        Perfect balance = 100, High imbalance = 0
        
        Formula: CBI = 100 - (StdDev of CIA percentages * scaling factor)
        
        Args:
            cia_coverage: Dictionary with CIA percentages
            
        Returns:
            Balance index (0-100)
        """
        values = list(cia_coverage.values())
        mean_value = np.mean(values)
        std_dev = np.std(values)
        
        # Ideal balance would be 33.33% each (std_dev ≈ 0)
        # Maximum imbalance would be 100-0-0 (std_dev ≈ 47.14)
        
        # Normalize: Maximum possible std_dev for percentages is ~47.14
        normalized_std_dev = (std_dev / 47.14) * 100
        
        # Balance Index: Higher is better
        balance_index = 100 - normalized_std_dev
        
        return round(balance_index, 2)
    
    def _get_balance_rating(self, balance_index: float) -> str:
        """Convert balance index to rating"""
        if balance_index >= 85:
            return "Excellent"
        elif balance_index >= 70:
            return "Good"
        elif balance_index >= 50:
            return "Fair"
        else:
            return "Poor"
    
    def _identify_cia_imbalances(self, cia_coverage: Dict[str, float]) -> List[Dict[str, any]]:
        """Identify CIA imbalances and risks"""
        imbalances = []
        
        # Define ideal range (25-40% for each)
        ideal_min, ideal_max = 25, 40
        
        for category, percentage in cia_coverage.items():
            if percentage < ideal_min:
                imbalances.append({
                    'category': category,
                    'type': 'under_covered',
                    'percentage': percentage,
                    'gap': ideal_min - percentage,
                    'severity': 'High' if percentage < 15 else 'Medium',
                    'risk': f'{category.capitalize()} controls are significantly under-represented'
                })
            elif percentage > ideal_max:
                imbalances.append({
                    'category': category,
                    'type': 'over_covered',
                    'percentage': percentage,
                    'excess': percentage - ideal_max,
                    'severity': 'Low',
                    'note': f'Over-emphasis on {category.capitalize()} may indicate neglect of other areas'
                })
        
        return imbalances
    
    def _generate_cia_heatmap(self, classified_clauses: List[Dict[str, any]]) -> Dict[str, any]:
        """Generate heatmap data for visualization"""
        section_cia = defaultdict(lambda: {'C': 0, 'I': 0, 'A': 0, 'total': 0})
        
        for clause in classified_clauses:
            section = clause.get('clause', 'Unknown')[:20]  # First 20 chars as section ID
            primary = clause['primary_category'][0].upper()  # C, I, or A
            
            section_cia[section][primary] += 1
            section_cia[section]['total'] += 1
        
        # Convert to heatmap format
        heatmap_data = []
        for section, counts in section_cia.items():
            total = counts['total']
            heatmap_data.append({
                'section': section,
                'confidentiality': round((counts['C'] / total) * 100, 1),
                'integrity': round((counts['I'] / total) * 100, 1),
                'availability': round((counts['A'] / total) * 100, 1)
            })
        
        return {
            'data': heatmap_data[:10],  # Top 10 sections
            'chart_type': 'heatmap',
            'labels': ['Confidentiality', 'Integrity', 'Availability']
        }
    
    def _generate_cia_recommendations(self, cia_coverage: Dict[str, float], 
                                     imbalances: List[Dict[str, any]]) -> List[str]:
        """Generate actionable recommendations based on CIA analysis"""
        recommendations = []
        
        for imbalance in imbalances:
            category = imbalance['category']
            
            if imbalance['type'] == 'under_covered':
                recommendations.append(
                    f"⚠️ Strengthen {category.upper()} controls: "
                    f"Currently at {imbalance['percentage']}%, should be 25-40%. "
                    f"Add controls related to {self.cia_definitions[category]['description'].lower()}."
                )
        
        # Check for balanced coverage
        if not imbalances:
            recommendations.append(
                "✅ CIA coverage is well-balanced across all three pillars."
            )
        
        return recommendations


# Singleton instance
cia_validator = CIAValidator()
