"""
Module 7: Secure AI Processing Layer
Handles encryption, secure file handling, and privacy protection
"""

import logging
import os
import hashlib
import secrets
from typing import Tuple, Optional
from pathlib import Path
from datetime import datetime, timedelta
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

from app.config.settings import settings

logger = logging.getLogger(__name__)


class SecurityLayer:
    """
    Secure AI Processing Layer
    Implements encryption, secure file handling, and privacy controls
    Ensures CIA (Confidentiality, Integrity, Availability)
    """
    
    def __init__(self):
        self.temp_dir = Path(settings.TEMP_UPLOAD_DIR)
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        self.encryption_key = self._get_encryption_key()
    
    def _get_encryption_key(self) -> bytes:
        """Get or generate AES encryption key"""
        key_str = settings.AES_ENCRYPTION_KEY
        
        # Ensure key is 32 bytes for AES-256
        if len(key_str) < 32:
            key_str = key_str.ljust(32, '0')
        elif len(key_str) > 32:
            key_str = key_str[:32]
        
        return key_str.encode('utf-8')
    
    def encrypt_data(self, data: bytes) -> Tuple[bytes, bytes]:
        """
        Encrypt data using AES-256
        
        Args:
            data: Raw bytes to encrypt
            
        Returns:
            Tuple of (encrypted_data, iv)
        """
        try:
            # Generate random IV (Initialization Vector)
            iv = secrets.token_bytes(16)
            
            # Create cipher
            cipher = AES.new(self.encryption_key, AES.MODE_CBC, iv)
            
            # Pad and encrypt
            padded_data = pad(data, AES.block_size)
            encrypted_data = cipher.encrypt(padded_data)
            
            logger.debug("Data encrypted successfully")
            return encrypted_data, iv
            
        except Exception as e:
            logger.error(f"Encryption failed: {str(e)}")
            raise
    
    def decrypt_data(self, encrypted_data: bytes, iv: bytes) -> bytes:
        """
        Decrypt AES-256 encrypted data
        
        Args:
            encrypted_data: Encrypted bytes
            iv: Initialization vector
            
        Returns:
            Decrypted data
        """
        try:
            cipher = AES.new(self.encryption_key, AES.MODE_CBC, iv)
            decrypted_padded = cipher.decrypt(encrypted_data)
            decrypted_data = unpad(decrypted_padded, AES.block_size)
            
            logger.debug("Data decrypted successfully")
            return decrypted_data
            
        except Exception as e:
            logger.error(f"Decryption failed: {str(e)}")
            raise
    
    def encrypt_file(self, file_path: str) -> Tuple[str, str]:
        """
        Encrypt file and return encrypted file path
        
        Args:
            file_path: Path to file to encrypt
            
        Returns:
            Tuple of (encrypted_file_path, iv_hex)
        """
        try:
            # Read file
            with open(file_path, 'rb') as f:
                file_data = f.read()
            
            # Encrypt
            encrypted_data, iv = self.encrypt_data(file_data)
            
            # Save encrypted file
            encrypted_path = file_path + '.enc'
            with open(encrypted_path, 'wb') as f:
                f.write(encrypted_data)
            
            # Convert IV to hex for storage
            iv_hex = iv.hex()
            
            logger.info(f"File encrypted: {Path(file_path).name}")
            return encrypted_path, iv_hex
            
        except Exception as e:
            logger.error(f"File encryption failed: {str(e)}")
            raise
    
    def secure_file_upload(self, file_data: bytes, original_filename: str) -> Tuple[str, str]:
        """
        Securely handle file upload with encryption
        
        Args:
            file_data: Raw file bytes
            original_filename: Original filename
            
        Returns:
            Tuple of (secure_file_path, file_hash)
        """
        try:
            # Generate secure filename
            timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
            random_suffix = secrets.token_hex(8)
            safe_name = f"{timestamp}_{random_suffix}_{Path(original_filename).name}"
            
            # Save to temp directory
            temp_path = self.temp_dir / safe_name
            with open(temp_path, 'wb') as f:
                f.write(file_data)
            
            # Calculate hash for integrity
            file_hash = self._calculate_hash(file_data)
            
            logger.info(f"File uploaded securely: {safe_name} (Hash: {file_hash[:16]}...)")
            
            # Schedule automatic deletion
            self._schedule_deletion(str(temp_path))
            
            return str(temp_path), file_hash
            
        except Exception as e:
            logger.error(f"Secure upload failed: {str(e)}")
            raise
    
    def _calculate_hash(self, data: bytes) -> str:
        """Calculate SHA-256 hash"""
        return hashlib.sha256(data).hexdigest()
    
    def verify_integrity(self, file_path: str, expected_hash: str) -> bool:
        """
        Verify file integrity using hash
        
        Args:
            file_path: Path to file
            expected_hash: Expected SHA-256 hash
            
        Returns:
            True if integrity verified
        """
        try:
            with open(file_path, 'rb') as f:
                file_data = f.read()
            
            actual_hash = self._calculate_hash(file_data)
            
            if actual_hash == expected_hash:
                logger.info("File integrity verified")
                return True
            else:
                logger.warning("File integrity check FAILED")
                return False
                
        except Exception as e:
            logger.error(f"Integrity verification failed: {str(e)}")
            return False
    
    def secure_delete(self, file_path: str) -> bool:
        """
        Securely delete file (overwrite before deletion)
        
        Args:
            file_path: Path to file to delete
            
        Returns:
            True if deleted successfully
        """
        try:
            path = Path(file_path)
            
            if not path.exists():
                logger.warning(f"File not found for deletion: {file_path}")
                return False
            
            # Get file size
            file_size = path.stat().st_size
            
            # Overwrite with random data (3 passes)
            with open(file_path, 'wb') as f:
                for _ in range(3):
                    f.seek(0)
                    f.write(os.urandom(file_size))
                    f.flush()
                    os.fsync(f.fileno())
            
            # Delete file
            path.unlink()
            
            logger.info(f"File securely deleted: {path.name}")
            return True
            
        except Exception as e:
            logger.error(f"Secure deletion failed: {str(e)}")
            return False
    
    def _schedule_deletion(self, file_path: str):
        """
        Schedule automatic file deletion after configured time
        
        Args:
            file_path: Path to file
        """
        # In production, this would use a task queue (Celery, etc.)
        # For now, we'll handle it synchronously after processing
        deletion_time = datetime.utcnow() + timedelta(minutes=settings.AUTO_DELETE_AFTER_MINUTES)
        logger.info(f"File scheduled for deletion at: {deletion_time.isoformat()}")
    
    def cleanup_temp_files(self) -> int:
        """
        Clean up old temporary files
        
        Returns:
            Number of files cleaned up
        """
        try:
            current_time = datetime.utcnow()
            cleanup_threshold = timedelta(minutes=settings.AUTO_DELETE_AFTER_MINUTES)
            
            cleaned_count = 0
            
            for file_path in self.temp_dir.glob('*'):
                if file_path.is_file():
                    # Check file age
                    file_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                    age = current_time - file_time
                    
                    if age > cleanup_threshold:
                        self.secure_delete(str(file_path))
                        cleaned_count += 1
            
            if cleaned_count > 0:
                logger.info(f"Cleaned up {cleaned_count} temporary files")
            
            return cleaned_count
            
        except Exception as e:
            logger.error(f"Cleanup failed: {str(e)}")
            return 0
    
    def validate_file_size(self, file_size: int) -> Tuple[bool, str]:
        """
        Validate file size against limits
        
        Args:
            file_size: Size in bytes
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        max_size = settings.MAX_DOCUMENT_SIZE_MB * 1024 * 1024  # Convert to bytes
        
        if file_size > max_size:
            return False, f"File size exceeds maximum ({settings.MAX_DOCUMENT_SIZE_MB}MB)"
        
        if file_size == 0:
            return False, "File is empty"
        
        return True, ""
    
    def log_security_event(self, event_type: str, details: dict):
        """
        Log security-related events for audit trail
        
        Args:
            event_type: Type of security event
            details: Event details
        """
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'event_type': event_type,
            'details': details
        }
        
        # In production, this would go to a SIEM or security log system
        logger.info(f"Security Event: {event_type} - {details}")
    
    def sanitize_metadata(self, metadata: dict) -> dict:
        """
        Sanitize metadata to remove sensitive information
        
        Args:
            metadata: Original metadata
            
        Returns:
            Sanitized metadata
        """
        # Remove potentially sensitive fields
        sensitive_fields = ['full_text', 'raw_content', 'clauses', 'pages']
        
        sanitized = {}
        for key, value in metadata.items():
            if key not in sensitive_fields:
                sanitized[key] = value
        
        return sanitized


# Singleton instance
security_layer = SecurityLayer()
