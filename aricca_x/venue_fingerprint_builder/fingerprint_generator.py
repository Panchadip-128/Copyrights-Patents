"""
Fingerprint Generator - Creates structured venue fingerprints

Implements proprietary fingerprinting algorithms for academic venues.
Copyright (c) 2026. All rights reserved.
"""

import hashlib
from typing import Dict, List, Optional, Set
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class VenueFingerprint:
    """
    Structured fingerprint of an academic venue.
    
    This proprietary data structure captures unique characteristics
    of conferences and journals for credibility assessment.
    """
    venue_id: str
    venue_name: str
    venue_type: str  # "conference" or "journal"
    
    # CFP characteristics
    cfp_syntax_signature: str
    cfp_risk_score: float
    urgency_indicators: List[str]
    
    # Website characteristics
    website_depth_score: float
    domain_age_indicator: Optional[str]
    structural_completeness: float
    
    # Indexing claims
    claimed_indexers: List[str]
    indexing_verification_status: Dict[str, str]
    
    # Organizer patterns
    organizer_names: List[str]
    organizer_recurrence_score: float
    institutional_affiliations: List[str]
    
    # Publication patterns
    publication_frequency: Optional[str]
    historical_venues: List[str]
    
    # Fingerprint metadata
    fingerprint_hash: str
    generation_timestamp: datetime
    confidence_score: float
    
    # Additional signals
    contact_legitimacy_indicators: Dict[str, float] = field(default_factory=dict)
    suspicious_patterns: List[str] = field(default_factory=list)
    positive_signals: List[str] = field(default_factory=list)


class FingerprintGenerator:
    """
    Generates unique fingerprints for academic venues using proprietary algorithms.
    
    This class implements copyright-protected logic for analyzing and
    characterizing research venues based on multiple data sources.
    """
    
    def __init__(self):
        """Initialize the fingerprint generator"""
        self.known_indexers = {
            'scopus', 'web of science', 'ieee xplore', 'acm digital library',
            'pubmed', 'google scholar', 'dblp', 'arxiv', 'springer', 'elsevier'
        }
    
    def generate_fingerprint(
        self,
        venue_name: str,
        venue_type: str,
        cfp_data: Optional[Dict] = None,
        website_data: Optional[Dict] = None,
        organizer_data: Optional[Dict] = None
    ) -> VenueFingerprint:
        """
        Generate a comprehensive venue fingerprint.
        
        Args:
            venue_name: Name of the venue
            venue_type: Type of venue ("conference" or "journal")
            cfp_data: Optional CFP analysis data
            website_data: Optional website analysis data
            organizer_data: Optional organizer information
            
        Returns:
            VenueFingerprint object
        """
        # Generate unique venue ID
        venue_id = self._generate_venue_id(venue_name, venue_type)
        
        # Process CFP data
        cfp_signature = self._generate_cfp_signature(cfp_data or {})
        cfp_risk = cfp_data.get('overall_cfp_risk', 0.5) if cfp_data else 0.5
        urgency = cfp_data.get('urgency_indicators', []) if cfp_data else []
        
        # Process website data
        website_depth = self._calculate_website_depth(website_data or {})
        domain_age = website_data.get('domain_age') if website_data else None
        structural_score = self._calculate_structural_completeness(website_data or {})
        
        # Process indexing claims
        claimed_indexers = self._extract_indexing_claims(cfp_data or {}, website_data or {})
        verification_status = self._verify_indexing_claims(claimed_indexers)
        
        # Process organizer data
        organizers = organizer_data.get('names', []) if organizer_data else []
        recurrence = self._calculate_organizer_recurrence(organizers)
        affiliations = organizer_data.get('affiliations', []) if organizer_data else []
        
        # Extract patterns
        suspicious = self._identify_suspicious_patterns(cfp_data, website_data, organizer_data)
        positive = self._identify_positive_signals(cfp_data, website_data, organizer_data)
        
        # Calculate contact legitimacy
        contact_indicators = self._analyze_contact_legitimacy(cfp_data or {}, website_data or {})
        
        # Generate fingerprint hash
        fingerprint_hash = self._generate_fingerprint_hash(
            venue_id, cfp_signature, website_depth, claimed_indexers, organizers
        )
        
        # Calculate overall confidence
        confidence = self._calculate_fingerprint_confidence(
            cfp_data, website_data, organizer_data
        )
        
        return VenueFingerprint(
            venue_id=venue_id,
            venue_name=venue_name,
            venue_type=venue_type,
            cfp_syntax_signature=cfp_signature,
            cfp_risk_score=cfp_risk,
            urgency_indicators=urgency,
            website_depth_score=website_depth,
            domain_age_indicator=domain_age,
            structural_completeness=structural_score,
            claimed_indexers=claimed_indexers,
            indexing_verification_status=verification_status,
            organizer_names=organizers,
            organizer_recurrence_score=recurrence,
            institutional_affiliations=affiliations,
            publication_frequency=None,
            historical_venues=[],
            fingerprint_hash=fingerprint_hash,
            generation_timestamp=datetime.now(),
            confidence_score=confidence,
            contact_legitimacy_indicators=contact_indicators,
            suspicious_patterns=suspicious,
            positive_signals=positive
        )
    
    def _generate_venue_id(self, venue_name: str, venue_type: str) -> str:
        """Generate unique venue identifier"""
        normalized = f"{venue_type}:{venue_name.lower().strip()}"
        return hashlib.sha256(normalized.encode()).hexdigest()[:16]
    
    def _generate_cfp_signature(self, cfp_data: Dict) -> str:
        """
        Generate a unique CFP syntax signature.
        
        This proprietary algorithm creates a hash-based signature
        of CFP linguistic characteristics.
        """
        components = []
        
        # Include key characteristics
        if 'syntax_score' in cfp_data:
            components.append(f"syn:{cfp_data['syntax_score']:.2f}")
        if 'professionalism_score' in cfp_data:
            components.append(f"pro:{cfp_data['professionalism_score']:.2f}")
        if 'urgency_indicators' in cfp_data:
            components.append(f"urg:{len(cfp_data['urgency_indicators'])}")
        if 'suspicious_patterns' in cfp_data:
            components.append(f"sus:{len(cfp_data['suspicious_patterns'])}")
        
        signature_string = "|".join(components)
        return hashlib.md5(signature_string.encode()).hexdigest()[:12]
    
    def _calculate_website_depth(self, website_data: Dict) -> float:
        """
        Calculate website structural depth score.
        
        Proprietary scoring algorithm based on website architecture.
        """
        if not website_data:
            return 0.0
        
        score = 0.0
        
        # Check for key pages
        key_pages = website_data.get('pages', [])
        expected_pages = {'about', 'committee', 'submission', 'program', 'contact'}
        
        for page in expected_pages:
            if any(page in p.lower() for p in key_pages):
                score += 0.15
        
        # Check navigation depth
        max_depth = website_data.get('max_navigation_depth', 0)
        depth_score = min(max_depth / 5.0, 0.25)
        score += depth_score
        
        return min(score, 1.0)
    
    def _calculate_structural_completeness(self, website_data: Dict) -> float:
        """
        Calculate structural completeness of venue website.
        
        Proprietary algorithm for assessing website quality.
        """
        if not website_data:
            return 0.0
        
        completeness = 0.0
        
        # Check for required sections
        sections = website_data.get('sections', [])
        required = ['about', 'dates', 'submission', 'contact']
        
        for req in required:
            if any(req in s.lower() for s in sections):
                completeness += 0.2
        
        # Check for SSL/HTTPS
        if website_data.get('has_ssl', False):
            completeness += 0.1
        
        # Check for responsive design indicators
        if website_data.get('is_responsive', False):
            completeness += 0.1
        
        return min(completeness, 1.0)
    
    def _extract_indexing_claims(self, cfp_data: Dict, website_data: Dict) -> List[str]:
        """Extract indexing claims from CFP and website data"""
        claims = set()
        
        # From CFP text
        cfp_text = cfp_data.get('cfp_text', '').lower()
        for indexer in self.known_indexers:
            if indexer in cfp_text:
                claims.add(indexer.title())
        
        # From website
        website_text = website_data.get('full_text', '').lower()
        for indexer in self.known_indexers:
            if indexer in website_text:
                claims.add(indexer.title())
        
        return sorted(list(claims))
    
    def _verify_indexing_claims(self, claimed_indexers: List[str]) -> Dict[str, str]:
        """
        Verify indexing claims.
        
        Note: Actual verification would require external API calls.
        This returns verification status indicators.
        """
        verification = {}
        
        for indexer in claimed_indexers:
            # In a real implementation, this would perform actual verification
            # For now, return status indicating verification is needed
            verification[indexer] = "verification_required"
        
        return verification
    
    def _calculate_organizer_recurrence(self, organizers: List[str]) -> float:
        """
        Calculate organizer recurrence score.
        
        Higher scores indicate organizers are involved in multiple venues.
        """
        if not organizers:
            return 0.0
        
        # In a real implementation, this would check against a database
        # For now, return a neutral score
        return 0.5
    
    def _identify_suspicious_patterns(
        self,
        cfp_data: Optional[Dict],
        website_data: Optional[Dict],
        organizer_data: Optional[Dict]
    ) -> List[str]:
        """Identify suspicious patterns across all data sources"""
        patterns = []
        
        if cfp_data:
            if cfp_data.get('overall_cfp_risk', 0) > 0.7:
                patterns.append("High CFP risk score")
            
            suspicious = cfp_data.get('suspicious_patterns', [])
            patterns.extend(suspicious[:5])  # Limit to top 5
        
        if website_data:
            if website_data.get('domain_age_days', 365) < 180:
                patterns.append("Recently registered domain")
        
        return patterns
    
    def _identify_positive_signals(
        self,
        cfp_data: Optional[Dict],
        website_data: Optional[Dict],
        organizer_data: Optional[Dict]
    ) -> List[str]:
        """Identify positive credibility signals"""
        signals = []
        
        if cfp_data:
            if cfp_data.get('professionalism_score', 0) > 0.7:
                signals.append("High professionalism score")
            
            if cfp_data.get('contact_legitimacy_score', 0) > 0.7:
                signals.append("Legitimate contact information")
        
        if website_data:
            if website_data.get('has_ssl', False):
                signals.append("Secure HTTPS website")
            
            if len(website_data.get('pages', [])) > 5:
                signals.append("Comprehensive website structure")
        
        if organizer_data:
            if organizer_data.get('has_institutional_affiliations', False):
                signals.append("Institutional affiliations present")
        
        return signals
    
    def _analyze_contact_legitimacy(self, cfp_data: Dict, website_data: Dict) -> Dict[str, float]:
        """Analyze legitimacy of contact information"""
        indicators = {}
        
        # Email domain analysis
        emails = cfp_data.get('email_contacts', [])
        if emails:
            academic_count = sum(1 for e in emails if '.edu' in e or '.ac.' in e)
            indicators['academic_email_ratio'] = academic_count / len(emails)
        else:
            indicators['academic_email_ratio'] = 0.0
        
        # Contact page presence
        has_contact_page = any('contact' in p.lower() for p in website_data.get('pages', []))
        indicators['has_contact_page'] = 1.0 if has_contact_page else 0.0
        
        return indicators
    
    def _generate_fingerprint_hash(
        self,
        venue_id: str,
        cfp_signature: str,
        website_depth: float,
        indexers: List[str],
        organizers: List[str]
    ) -> str:
        """Generate unique fingerprint hash"""
        components = [
            venue_id,
            cfp_signature,
            f"{website_depth:.2f}",
            "-".join(sorted(indexers)),
            "-".join(sorted(organizers))
        ]
        
        fingerprint_string = "|".join(components)
        return hashlib.sha256(fingerprint_string.encode()).hexdigest()
    
    def _calculate_fingerprint_confidence(
        self,
        cfp_data: Optional[Dict],
        website_data: Optional[Dict],
        organizer_data: Optional[Dict]
    ) -> float:
        """Calculate overall fingerprint confidence score"""
        confidence = 0.0
        
        if cfp_data:
            confidence += 0.4
        if website_data:
            confidence += 0.4
        if organizer_data:
            confidence += 0.2
        
        return confidence
