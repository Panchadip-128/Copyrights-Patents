"""
Input Signal Manager

Handles heterogeneous input sources and converts them to canonical signal descriptors.
Copyright © 2026. All Rights Reserved.
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional, List
from enum import Enum
from datetime import datetime
import re


class SignalType(Enum):
    """Types of input signals"""
    URL = "url"
    HTML = "html"
    VISUAL = "visual"
    NETWORK = "network"
    METADATA = "metadata"


class SignalStatus(Enum):
    """Signal processing status"""
    RAW = "raw"
    VALIDATED = "validated"
    NORMALIZED = "normalized"
    PROCESSED = "processed"
    ERROR = "error"


@dataclass
class SignalDescriptor:
    """
    Canonical representation of any input signal.
    Copyright-protected data structure.
    """
    signal_id: str
    signal_type: SignalType
    raw_content: Any
    normalized_content: Optional[Any]
    metadata: Dict[str, Any]
    status: SignalStatus
    timestamp: datetime
    validity_score: float
    errors: List[str]
    
    def is_valid(self) -> bool:
        """Check if signal is valid for processing"""
        return self.status != SignalStatus.ERROR and self.validity_score >= 0.5


class SignalValidator:
    """
    Validates input signals for quality and completeness.
    Proprietary validation logic.
    """
    
    # Validation thresholds (proprietary)
    MIN_URL_LENGTH = 10
    MAX_URL_LENGTH = 2048
    MIN_HTML_LENGTH = 50
    MAX_HTML_SIZE = 10 * 1024 * 1024  # 10MB
    
    # Suspicious patterns
    URL_SUSPICIOUS_PATTERNS = [
        r'\.tk$', r'\.ml$', r'\.ga$', r'\.cf$',  # Free TLDs
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',   # IP addresses
        r'[^\x00-\x7F]+',                          # Non-ASCII
        r'@',                                      # @ in URL
    ]
    
    def validate_url(self, url: str) -> tuple[bool, float, List[str]]:
        """
        Validate URL signal.
        Returns: (is_valid, validity_score, errors)
        """
        errors = []
        score = 1.0
        
        # Length check
        if len(url) < self.MIN_URL_LENGTH:
            errors.append(f"URL too short (min: {self.MIN_URL_LENGTH})")
            score -= 0.3
        
        if len(url) > self.MAX_URL_LENGTH:
            errors.append(f"URL too long (max: {self.MAX_URL_LENGTH})")
            score -= 0.2
        
        # Protocol check
        if not url.startswith(('http://', 'https://', 'ftp://')):
            errors.append("Missing or invalid protocol")
            score -= 0.3
        
        # Suspicious pattern check
        suspicious_count = 0
        for pattern in self.URL_SUSPICIOUS_PATTERNS:
            if re.search(pattern, url):
                suspicious_count += 1
                score -= 0.1
        
        if suspicious_count > 0:
            errors.append(f"Contains {suspicious_count} suspicious pattern(s)")
        
        is_valid = len(errors) == 0 or score >= 0.5
        return is_valid, max(0.0, score), errors
    
    def validate_html(self, html: str) -> tuple[bool, float, List[str]]:
        """
        Validate HTML signal.
        Returns: (is_valid, validity_score, errors)
        """
        errors = []
        score = 1.0
        
        # Length check
        if len(html) < self.MIN_HTML_LENGTH:
            errors.append(f"HTML too short (min: {self.MIN_HTML_LENGTH})")
            return False, 0.0, errors
        
        if len(html) > self.MAX_HTML_SIZE:
            errors.append(f"HTML too large (max: {self.MAX_HTML_SIZE} bytes)")
            return False, 0.0, errors
        
        # Basic structure check
        if '<html' not in html.lower():
            errors.append("Missing <html> tag")
            score -= 0.2
        
        if '<body' not in html.lower():
            errors.append("Missing <body> tag")
            score -= 0.1
        
        # Suspicious patterns
        if '<script>' in html and 'document.write' in html:
            errors.append("Suspicious JavaScript detected")
            score -= 0.2
        
        if 'eval(' in html:
            errors.append("Dangerous eval() detected")
            score -= 0.3
        
        is_valid = score >= 0.5
        return is_valid, max(0.0, score), errors
    
    def validate_visual(self, image_data: bytes) -> tuple[bool, float, List[str]]:
        """Validate visual (screenshot) signal"""
        errors = []
        score = 1.0
        
        if not image_data:
            errors.append("Empty image data")
            return False, 0.0, errors
        
        # Check size
        size_mb = len(image_data) / (1024 * 1024)
        if size_mb > 10:
            errors.append(f"Image too large: {size_mb:.1f}MB")
            score -= 0.3
        
        # Check magic bytes for PNG/JPEG
        is_png = image_data[:8] == b'\x89PNG\r\n\x1a\n'
        is_jpeg = image_data[:3] == b'\xff\xd8\xff'
        
        if not (is_png or is_jpeg):
            errors.append("Invalid image format (expected PNG or JPEG)")
            score -= 0.5
        
        is_valid = score >= 0.5
        return is_valid, max(0.0, score), errors


class SignalNormalizer:
    """
    Normalizes signals into standard formats.
    Proprietary normalization algorithms.
    """
    
    def normalize_url(self, url: str) -> str:
        """
        Normalize URL to canonical form.
        Proprietary URL normalization logic.
        """
        # Remove whitespace
        url = url.strip()
        
        # Convert to lowercase (except path)
        parts = url.split('/', 3)
        if len(parts) >= 3:
            parts[0] = parts[0].lower()  # protocol
            parts[2] = parts[2].lower()  # domain
            url = '/'.join(parts)
        else:
            url = url.lower()
        
        # Remove trailing slash
        if url.endswith('/'):
            url = url[:-1]
        
        # Remove default ports
        url = url.replace(':80/', '/').replace(':443/', '/')
        
        # Remove www. prefix
        url = re.sub(r'://(www\.)', '://', url)
        
        # Remove fragment
        url = url.split('#')[0]
        
        return url
    
    def normalize_html(self, html: str) -> str:
        """Normalize HTML structure"""
        # Remove excessive whitespace
        html = re.sub(r'\s+', ' ', html)
        
        # Remove comments
        html = re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL)
        
        # Normalize case for tags
        html = re.sub(r'<([A-Z]+)', lambda m: '<' + m.group(1).lower(), html)
        
        return html


class InputSignalManager:
    """
    Main input signal management interface.
    Handles acquisition, validation, and normalization of all input types.
    Copyright-protected orchestration logic.
    """
    
    def __init__(self):
        self.validator = SignalValidator()
        self.normalizer = SignalNormalizer()
        self._signal_cache: Dict[str, SignalDescriptor] = {}
    
    def acquire_url_signal(self, url: str, metadata: Optional[Dict] = None) -> SignalDescriptor:
        """
        Acquire and process URL signal.
        
        Args:
            url: Raw URL string
            metadata: Optional metadata dict
        
        Returns:
            SignalDescriptor with processing results
        """
        signal_id = f"url_{hash(url)}"
        
        # Check cache
        if signal_id in self._signal_cache:
            return self._signal_cache[signal_id]
        
        # Validate
        is_valid, validity_score, errors = self.validator.validate_url(url)
        
        # Normalize if valid
        normalized = None
        status = SignalStatus.ERROR
        
        if is_valid:
            try:
                normalized = self.normalizer.normalize_url(url)
                status = SignalStatus.NORMALIZED
            except Exception as e:
                errors.append(f"Normalization error: {str(e)}")
                status = SignalStatus.ERROR
        
        # Create descriptor
        descriptor = SignalDescriptor(
            signal_id=signal_id,
            signal_type=SignalType.URL,
            raw_content=url,
            normalized_content=normalized,
            metadata=metadata or {},
            status=status,
            timestamp=datetime.now(),
            validity_score=validity_score,
            errors=errors
        )
        
        # Cache
        self._signal_cache[signal_id] = descriptor
        
        return descriptor
    
    def acquire_html_signal(self, html: str, metadata: Optional[Dict] = None) -> SignalDescriptor:
        """Acquire and process HTML signal"""
        signal_id = f"html_{hash(html[:1000])}"  # Hash first 1KB
        
        if signal_id in self._signal_cache:
            return self._signal_cache[signal_id]
        
        is_valid, validity_score, errors = self.validator.validate_html(html)
        
        normalized = None
        status = SignalStatus.ERROR
        
        if is_valid:
            try:
                normalized = self.normalizer.normalize_html(html)
                status = SignalStatus.NORMALIZED
            except Exception as e:
                errors.append(f"Normalization error: {str(e)}")
                status = SignalStatus.ERROR
        
        descriptor = SignalDescriptor(
            signal_id=signal_id,
            signal_type=SignalType.HTML,
            raw_content=html,
            normalized_content=normalized,
            metadata=metadata or {},
            status=status,
            timestamp=datetime.now(),
            validity_score=validity_score,
            errors=errors
        )
        
        self._signal_cache[signal_id] = descriptor
        return descriptor
    
    def acquire_visual_signal(self, image_data: bytes, metadata: Optional[Dict] = None) -> SignalDescriptor:
        """Acquire and process visual (screenshot) signal"""
        signal_id = f"visual_{hash(image_data[:1024])}"
        
        if signal_id in self._signal_cache:
            return self._signal_cache[signal_id]
        
        is_valid, validity_score, errors = self.validator.validate_visual(image_data)
        
        status = SignalStatus.NORMALIZED if is_valid else SignalStatus.ERROR
        
        descriptor = SignalDescriptor(
            signal_id=signal_id,
            signal_type=SignalType.VISUAL,
            raw_content=image_data,
            normalized_content=image_data if is_valid else None,
            metadata=metadata or {},
            status=status,
            timestamp=datetime.now(),
            validity_score=validity_score,
            errors=errors
        )
        
        self._signal_cache[signal_id] = descriptor
        return descriptor
    
    def get_valid_signals(self) -> List[SignalDescriptor]:
        """Get all valid signals from cache"""
        return [s for s in self._signal_cache.values() if s.is_valid()]
    
    def clear_cache(self):
        """Clear signal cache"""
        self._signal_cache.clear()
