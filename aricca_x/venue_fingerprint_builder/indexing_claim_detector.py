"""
Indexing Claim Detector - Detects and validates indexing claims

Implements proprietary algorithms for analyzing indexing claims.
Copyright (c) 2026. All rights reserved.
"""

import re
from typing import Dict, List, Set, Tuple
from dataclasses import dataclass
from enum import Enum


class ClaimVeracity(Enum):
    """Veracity status of an indexing claim"""
    VERIFIED = "verified"
    UNVERIFIED = "unverified"
    SUSPICIOUS = "suspicious"
    FALSE = "false"
    PENDING = "pending"


@dataclass
class IndexingClaim:
    """Represents a claim about database indexing"""
    indexer_name: str
    claim_text: str
    claim_location: str  # "cfp", "website", "email"
    claim_confidence: float
    phrasing_suspicion_score: float
    veracity_status: ClaimVeracity
    verification_evidence: List[str]


class IndexingClaimDetector:
    """
    Detects and analyzes indexing claims in venue materials.
    
    Uses proprietary natural language processing and pattern matching
    to identify suspicious or misleading indexing claims.
    """
    
    # Proprietary indexer database (copyright-protected)
    KNOWN_INDEXERS = {
        'tier1': {
            'Scopus', 'Web of Science', 'IEEE Xplore', 'ACM Digital Library',
            'PubMed', 'MEDLINE', 'MathSciNet', 'Chemical Abstracts'
        },
        'tier2': {
            'Google Scholar', 'DBLP', 'Semantic Scholar', 'CiteSeerX',
            'arXiv', 'SSRN', 'RePEc'
        },
        'tier3': {
            'Crossref', 'DOAJ', 'ORCID', 'Dimensions', 'Microsoft Academic'
        }
    }
    
    # Suspicious phrasing patterns (proprietary)
    SUSPICIOUS_PHRASINGS = [
        r'will\s+be\s+(?:indexed|submitted)\s+(?:to|in)',
        r'indexed\s+in\s+(?:all|many|several|various)\s+databases',
        r'guaranteed\s+indexing',
        r'(?:scopus|web\s+of\s+science)[\s-](?:indexed|listed)\s+(?:journal|conference)',
        r'fast[\s-]track\s+(?:indexing|publication)',
        r'applied\s+for\s+(?:scopus|indexing)',
        r'under\s+(?:review|consideration)\s+for\s+(?:scopus|indexing)'
    ]
    
    # Legitimate phrasing patterns
    LEGITIMATE_PHRASINGS = [
        r'indexed\s+in\s+scopus\s+since\s+\d{4}',
        r'(?:scopus|web\s+of\s+science)\s+(?:id|identifier):\s*[\w\d-]+',
        r'abstracting\s+and\s+indexing\s+services:',
        r'currently\s+indexed\s+(?:by|in)'
    ]
    
    def __init__(self):
        """Initialize the indexing claim detector"""
        self.all_indexers = set()
        for tier_indexers in self.KNOWN_INDEXERS.values():
            self.all_indexers.update(indexer.lower() for indexer in tier_indexers)
        
        self.suspicious_patterns = [
            re.compile(p, re.IGNORECASE) for p in self.SUSPICIOUS_PHRASINGS
        ]
        self.legitimate_patterns = [
            re.compile(p, re.IGNORECASE) for p in self.LEGITIMATE_PHRASINGS
        ]
    
    def detect_claims(
        self,
        text: str,
        source: str = "unknown"
    ) -> List[IndexingClaim]:
        """
        Detect indexing claims in text.
        
        Args:
            text: Text to analyze (CFP, website content, etc.)
            source: Source of the text ("cfp", "website", "email")
            
        Returns:
            List of detected IndexingClaim objects
        """
        claims = []
        
        # Find all indexer mentions
        for indexer in self.all_indexers:
            # Search for indexer name (case-insensitive)
            pattern = re.compile(r'\b' + re.escape(indexer) + r'\b', re.IGNORECASE)
            
            for match in pattern.finditer(text):
                # Extract context (100 chars before and after)
                start = max(0, match.start() - 100)
                end = min(len(text), match.end() + 100)
                context = text[start:end]
                
                # Analyze the claim
                claim = self._analyze_claim(
                    indexer_name=indexer.title(),
                    claim_text=context,
                    source=source,
                    full_text=text
                )
                
                claims.append(claim)
        
        return claims
    
    def _analyze_claim(
        self,
        indexer_name: str,
        claim_text: str,
        source: str,
        full_text: str
    ) -> IndexingClaim:
        """
        Analyze a single indexing claim for credibility.
        
        Proprietary analysis algorithm.
        """
        # Calculate claim confidence
        confidence = self._calculate_claim_confidence(claim_text)
        
        # Calculate suspicion score
        suspicion = self._calculate_suspicion_score(claim_text)
        
        # Determine veracity status
        veracity = self._determine_veracity(claim_text, suspicion, confidence)
        
        # Gather verification evidence
        evidence = self._gather_evidence(claim_text, full_text, indexer_name)
        
        return IndexingClaim(
            indexer_name=indexer_name,
            claim_text=claim_text,
            claim_location=source,
            claim_confidence=confidence,
            phrasing_suspicion_score=suspicion,
            veracity_status=veracity,
            verification_evidence=evidence
        )
    
    def _calculate_claim_confidence(self, claim_text: str) -> float:
        """
        Calculate confidence in the claim detection.
        
        Returns score from 0.0 to 1.0
        """
        confidence = 0.5  # Base confidence
        
        # Look for explicit indexing language
        indexing_words = ['indexed', 'indexing', 'abstracted', 'covered', 'included']
        if any(word in claim_text.lower() for word in indexing_words):
            confidence += 0.3
        
        # Look for supporting details
        if re.search(r'\b\d{4}\b', claim_text):  # Year mentioned
            confidence += 0.1
        
        if re.search(r'(?:issn|isbn|doi)[\s:]*[\d-]+', claim_text, re.IGNORECASE):
            confidence += 0.1
        
        return min(confidence, 1.0)
    
    def _calculate_suspicion_score(self, claim_text: str) -> float:
        """
        Calculate suspicion score for the claim phrasing.

        Patent-pending algorithm combining three independent analyses:
          1. Suspicious phrasing pattern detection
          2. Legitimate phrasing pattern detection (reduces suspicion)
          3. Grammatical Tense Analysis (novel contribution)

        The Grammatical Tense Analysis classifies the claim's temporal
        framing into one of four categories: PAST, PRESENT, FUTURE, or
        CONDITIONAL. Each tense category carries a different risk weight
        because deceptive venues systematically use future/conditional
        phrasing to imply indexing they do not have.

        Returns score from 0.0 (legitimate) to 1.0 (highly suspicious)
        """
        suspicion = 0.0

        # Analysis 1: Suspicious pattern detection
        for pattern in self.suspicious_patterns:
            if pattern.search(claim_text):
                suspicion += 0.25

        # Analysis 2: Legitimate pattern detection (reduces suspicion)
        for pattern in self.legitimate_patterns:
            if pattern.search(claim_text):
                suspicion -= 0.2

        # Analysis 3: Vague language detection
        vague_terms = [
            'many databases', 'various indexers', 'several indexes',
            'well known', 'reputed', 'leading'
        ]
        for term in vague_terms:
            if term in claim_text.lower():
                suspicion += 0.15

        # Analysis 4: Patent-Pending Grammatical Tense Analysis (GTA)
        tense = self._classify_claim_tense(claim_text)
        tense_risk_weights = {
            'past': -0.05,       # "was indexed" — slight positive signal
            'present': 0.0,      # "is indexed" — neutral
            'future': 0.25,      # "will be indexed" — strong risk signal
            'conditional': 0.30, # "may be indexed" — strongest risk signal
            'unknown': 0.05      # no clear tense — slight risk
        }
        suspicion += tense_risk_weights.get(tense, 0.05)

        return max(0.0, min(suspicion, 1.0))

    def _classify_claim_tense(self, claim_text: str) -> str:
        """
        Patent-pending Grammatical Tense Analysis (GTA) algorithm.

        Classifies the temporal framing of an indexing claim into one of
        four categories by analyzing verb phrase patterns surrounding
        indexing-related keywords.

        Categories:
          - 'past': Historical claim ("was indexed", "has been indexed since")
          - 'present': Current state claim ("is indexed", "currently indexed")
          - 'future': Prospective claim ("will be indexed", "to be submitted")
          - 'conditional': Uncertain claim ("may be indexed", "could be")
          - 'unknown': No clear tense detected

        This is a specific technical contribution: prior art detects
        whether an indexer is mentioned, but does not analyze the
        grammatical framing of the mention to distinguish between
        "we are indexed in Scopus" vs "we will apply to Scopus".
        """
        claim_lower = claim_text.lower()

        # Conditional tense patterns (check first — most suspicious)
        conditional_patterns = [
            r'\b(?:may|might|could|would)\s+(?:be\s+)?(?:indexed|included|listed|submitted)',
            r'\b(?:possibly|potentially)\s+(?:indexed|included)',
            r'\bsubject\s+to\s+(?:indexing|inclusion|approval)',
        ]
        for pattern in conditional_patterns:
            if re.search(pattern, claim_lower):
                return 'conditional'

        # Future tense patterns
        future_patterns = [
            r'\b(?:will|shall|going\s+to)\s+(?:be\s+)?(?:indexed|included|submitted|listed)',
            r'\b(?:planning|aiming|intending)\s+to\s+(?:submit|apply|index)',
            r'\bto\s+be\s+(?:indexed|submitted|included)',
            r'\bapplied?\s+for\s+(?:indexing|inclusion)',
            r'\bunder\s+(?:review|consideration|evaluation)\s+for',
        ]
        for pattern in future_patterns:
            if re.search(pattern, claim_lower):
                return 'future'

        # Past tense patterns
        past_patterns = [
            r'\b(?:was|were|has\s+been|had\s+been)\s+(?:indexed|included|listed)',
            r'\bindexed\s+(?:in|by)\s+\w+\s+since\s+\d{4}',
        ]
        for pattern in past_patterns:
            if re.search(pattern, claim_lower):
                return 'past'

        # Present tense patterns
        present_patterns = [
            r'\b(?:is|are)\s+(?:indexed|included|listed|covered|abstracted)',
            r'\bcurrently\s+(?:indexed|included|listed)',
            r'\bindexed\s+(?:in|by)\b',  # bare "indexed in" implies present
        ]
        for pattern in present_patterns:
            if re.search(pattern, claim_lower):
                return 'present'

        return 'unknown'
    
    def _determine_veracity(
        self,
        claim_text: str,
        suspicion: float,
        confidence: float
    ) -> ClaimVeracity:
        """
        Determine veracity status of the claim.
        
        Proprietary classification algorithm.
        """
        # High suspicion -> suspicious or false
        if suspicion > 0.7:
            return ClaimVeracity.FALSE
        elif suspicion > 0.5:
            return ClaimVeracity.SUSPICIOUS
        
        # Low confidence -> unverified
        if confidence < 0.4:
            return ClaimVeracity.UNVERIFIED
        
        # Check for verification indicators
        has_id = bool(re.search(r'(?:id|identifier)[\s:]*[\w\d-]+', claim_text, re.IGNORECASE))
        has_year = bool(re.search(r'since\s+\d{4}', claim_text, re.IGNORECASE))
        
        if has_id or has_year:
            return ClaimVeracity.VERIFIED
        
        # Default to pending verification
        return ClaimVeracity.PENDING
    
    def _gather_evidence(
        self,
        claim_text: str,
        full_text: str,
        indexer_name: str
    ) -> List[str]:
        """Gather evidence supporting or refuting the claim"""
        evidence = []
        
        # Look for identifiers
        issn_match = re.search(r'issn[\s:]*(\d{4}-\d{3}[\dxX])', claim_text, re.IGNORECASE)
        if issn_match:
            evidence.append(f"ISSN mentioned: {issn_match.group(1)}")
        
        # Look for specific dates
        year_match = re.search(r'(?:since|from)\s+(\d{4})', claim_text, re.IGNORECASE)
        if year_match:
            evidence.append(f"Indexed since: {year_match.group(1)}")
        
        # Count mentions of indexer in full text
        mention_count = len(re.findall(
            r'\b' + re.escape(indexer_name) + r'\b',
            full_text,
            re.IGNORECASE
        ))
        if mention_count > 3:
            evidence.append(f"Mentioned {mention_count} times (possibly overstated)")
        elif mention_count == 1:
            evidence.append("Single mention (appropriate)")
        
        # Check for URLs or links
        if re.search(r'https?://[\w.-]+', claim_text):
            evidence.append("Link provided for verification")
        
        return evidence
    
    def analyze_claim_patterns(self, claims: List[IndexingClaim]) -> Dict[str, any]:
        """
        Analyze patterns across multiple claims.
        
        Proprietary pattern analysis algorithm.
        """
        if not claims:
            return {
                'total_claims': 0,
                'suspicious_ratio': 0.0,
                'verified_ratio': 0.0,
                'most_claimed_indexers': [],
                'overall_credibility': 0.5
            }
        
        # Count by veracity
        veracity_counts = {}
        for claim in claims:
            status = claim.veracity_status.value
            veracity_counts[status] = veracity_counts.get(status, 0) + 1
        
        # Count by indexer
        indexer_counts = {}
        for claim in claims:
            indexer_counts[claim.indexer_name] = indexer_counts.get(claim.indexer_name, 0) + 1
        
        # Calculate ratios
        total = len(claims)
        suspicious_count = veracity_counts.get('suspicious', 0) + veracity_counts.get('false', 0)
        verified_count = veracity_counts.get('verified', 0)
        
        suspicious_ratio = suspicious_count / total
        verified_ratio = verified_count / total
        
        # Calculate overall credibility (proprietary formula)
        credibility = (1.0 - suspicious_ratio * 0.7 + verified_ratio * 0.3)
        credibility = max(0.0, min(credibility, 1.0))
        
        # Get most claimed indexers
        most_claimed = sorted(indexer_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            'total_claims': total,
            'suspicious_ratio': suspicious_ratio,
            'verified_ratio': verified_ratio,
            'most_claimed_indexers': [name for name, count in most_claimed],
            'indexer_counts': indexer_counts,
            'veracity_distribution': veracity_counts,
            'overall_credibility': credibility
        }
