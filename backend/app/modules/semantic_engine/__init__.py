"""
Layer 2: Sentence-BERT Semantic Similarity Engine
Cosine-similarity matching between uploaded document and framework clauses.
"""

from .engine import SemanticSimilarityEngine, semantic_engine

__all__ = ['SemanticSimilarityEngine', 'semantic_engine']
