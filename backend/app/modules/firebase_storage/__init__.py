"""
Firebase Secure Metadata Storage Module
"""

from .storage import FirebaseStorage

firebase_storage = FirebaseStorage()

__all__ = ['firebase_storage', 'FirebaseStorage']
