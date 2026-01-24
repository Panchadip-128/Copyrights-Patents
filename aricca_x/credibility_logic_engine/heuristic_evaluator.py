"""
Heuristic Evaluator - Evaluates rule-based heuristics

Implements proprietary heuristic evaluation rules.
Copyright (c) 2026. All rights reserved.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class HeuristicResult:
    """Result from a single heuristic evaluation"""
    name: str
    description: str
    passed: bool
    importance: str  # "critical", "high", "medium", "low"
    evidence: List[str]
    score_impact: float


class HeuristicEvaluator:
    """
    Evaluates credibility using rule-based heuristics.
    
    Implements proprietary heuristic rules for predatory venue detection.
    """
    
    def __init__(self):
        """Initialize the heuristic evaluator"""
        pass
    
    def evaluate_all(
        self,
        venue_data: Dict,
        cfp_data: Optional[Dict] = None,
        website_data: Optional[Dict] = None,
        fingerprint_data: Optional[Dict] = None
    ) -> List[HeuristicResult]:
        """
        Evaluate all heuristics.
        
        Returns list of heuristic results.
        """
        results = []
        
        # Heuristic 1: Unrealistic acceptance rates
        results.append(self._eval_acceptance_rate(cfp_data))
        
        # Heuristic 2: Excessive urgency in CFP
        results.append(self._eval_urgency_indicators(cfp_data))
        
        # Heuristic 3: Website quality
        results.append(self._eval_website_quality(website_data))
        
        # Heuristic 4: Indexing claim validity
        results.append(self._eval_indexing_claims(fingerprint_data))
        
        # Heuristic 5: Contact information
        results.append(self._eval_contact_info(cfp_data, website_data))
        
        # Heuristic 6: Fees mentioned prominently
        results.append(self._eval_fee_prominence(cfp_data))
        
        # Heuristic 7: Publication speed claims
        results.append(self._eval_publication_speed(cfp_data))
        
        return results
    
    def _eval_acceptance_rate(self, cfp_data: Optional[Dict]) -> HeuristicResult:
        """Evaluate claimed acceptance rates"""
        if not cfp_data:
            return HeuristicResult(
                name="Acceptance Rate Check",
                description="Checks for unrealistic acceptance guarantees",
                passed=True,
                importance="high",
                evidence=["No CFP data available"],
                score_impact=0.0
            )
        
        suspicious = cfp_data.get('suspicious_patterns', [])
        acceptance_suspicious = any(
            'acceptance' in s.lower() or 'guarantee' in s.lower()
            for s in suspicious
        )
        
        return HeuristicResult(
            name="Acceptance Rate Check",
            description="Checks for unrealistic acceptance guarantees",
            passed=not acceptance_suspicious,
            importance="critical",
            evidence=suspicious if acceptance_suspicious else ["No suspicious acceptance claims"],
            score_impact=0.3 if acceptance_suspicious else 0.0
        )
    
    def _eval_urgency_indicators(self, cfp_data: Optional[Dict]) -> HeuristicResult:
        """Evaluate urgency indicators in CFP"""
        if not cfp_data:
            return HeuristicResult(
                name="Urgency Check",
                description="Checks for excessive deadline pressure",
                passed=True,
                importance="medium",
                evidence=["No CFP data available"],
                score_impact=0.0
            )
        
        urgency_indicators = cfp_data.get('urgency_indicators', [])
        excessive_urgency = len(urgency_indicators) > 3
        
        return HeuristicResult(
            name="Urgency Check",
            description="Checks for excessive deadline pressure",
            passed=not excessive_urgency,
            importance="medium",
            evidence=urgency_indicators if excessive_urgency else ["Normal urgency levels"],
            score_impact=0.15 if excessive_urgency else 0.0
        )
    
    def _eval_website_quality(self, website_data: Optional[Dict]) -> HeuristicResult:
        """Evaluate website quality"""
        if not website_data:
            return HeuristicResult(
                name="Website Quality Check",
                description="Evaluates website professionalism and completeness",
                passed=False,
                importance="high",
                evidence=["No website data available"],
                score_impact=0.2
            )
        
        has_ssl = website_data.get('has_ssl', False)
        has_contact = website_data.get('has_contact_page', False)
        page_count = website_data.get('page_count', 0)
        
        passed = has_ssl and has_contact and page_count >= 5
        
        evidence = []
        if not has_ssl:
            evidence.append("No SSL/HTTPS")
        if not has_contact:
            evidence.append("No contact page")
        if page_count < 5:
            evidence.append(f"Limited pages ({page_count})")
        
        return HeuristicResult(
            name="Website Quality Check",
            description="Evaluates website professionalism and completeness",
            passed=passed,
            importance="high",
            evidence=evidence if not passed else ["Website meets quality standards"],
            score_impact=0.2 if not passed else 0.0
        )
    
    def _eval_indexing_claims(self, fingerprint_data: Optional[Dict]) -> HeuristicResult:
        """Evaluate indexing claims"""
        if not fingerprint_data:
            return HeuristicResult(
                name="Indexing Claims Check",
                description="Validates database indexing claims",
                passed=True,
                importance="high",
                evidence=["No indexing claims to verify"],
                score_impact=0.0
            )
        
        indexing_status = fingerprint_data.get('indexing_verification_status', {})
        claimed_indexers = fingerprint_data.get('claimed_indexers', [])
        
        if not claimed_indexers:
            return HeuristicResult(
                name="Indexing Claims Check",
                description="Validates database indexing claims",
                passed=True,
                importance="high",
                evidence=["No indexing claims made"],
                score_impact=0.0
            )
        
        suspicious_claims = sum(
            1 for status in indexing_status.values()
            if status in ['unverified', 'suspicious', 'false']
        )
        
        passed = suspicious_claims == 0
        
        return HeuristicResult(
            name="Indexing Claims Check",
            description="Validates database indexing claims",
            passed=passed,
            importance="high",
            evidence=[
                f"{suspicious_claims} unverified/suspicious indexing claims"
            ] if not passed else ["Indexing claims appear legitimate"],
            score_impact=0.25 if not passed else 0.0
        )
    
    def _eval_contact_info(
        self,
        cfp_data: Optional[Dict],
        website_data: Optional[Dict]
    ) -> HeuristicResult:
        """Evaluate contact information legitimacy"""
        evidence = []
        score = 0.0
        
        if cfp_data:
            emails = cfp_data.get('email_contacts', [])
            academic_emails = sum(1 for e in emails if '.edu' in e or '.ac.' in e)
            
            if emails and academic_emails == 0:
                evidence.append("No academic email addresses")
                score += 0.15
        
        if website_data:
            if not website_data.get('has_contact_page', False):
                evidence.append("No contact page on website")
                score += 0.1
        
        passed = len(evidence) == 0
        
        return HeuristicResult(
            name="Contact Information Check",
            description="Validates legitimacy of contact information",
            passed=passed,
            importance="medium",
            evidence=evidence if not passed else ["Contact information appears legitimate"],
            score_impact=score
        )
    
    def _eval_fee_prominence(self, cfp_data: Optional[Dict]) -> HeuristicResult:
        """Evaluate prominence of fee mentions"""
        if not cfp_data:
            return HeuristicResult(
                name="Fee Prominence Check",
                description="Checks for excessive emphasis on fees",
                passed=True,
                importance="medium",
                evidence=["No CFP data available"],
                score_impact=0.0
            )
        
        # Check for fee-related suspicious patterns
        suspicious = cfp_data.get('suspicious_patterns', [])
        fee_suspicious = any('fee' in s.lower() or 'payment' in s.lower() for s in suspicious)
        
        return HeuristicResult(
            name="Fee Prominence Check",
            description="Checks for excessive emphasis on fees",
            passed=not fee_suspicious,
            importance="medium",
            evidence=["Excessive fee emphasis detected"] if fee_suspicious else ["Normal fee mentions"],
            score_impact=0.1 if fee_suspicious else 0.0
        )
    
    def _eval_publication_speed(self, cfp_data: Optional[Dict]) -> HeuristicResult:
        """Evaluate publication speed claims"""
        if not cfp_data:
            return HeuristicResult(
                name="Publication Speed Check",
                description="Checks for unrealistic publication speed claims",
                passed=True,
                importance="low",
                evidence=["No CFP data available"],
                score_impact=0.0
            )
        
        cfp_text = cfp_data.get('cfp_text', '').lower()
        speed_claims = [
            'fast publication', 'quick publication', 'rapid publication',
            'immediate publication', 'fast track'
        ]
        
        has_speed_claims = any(claim in cfp_text for claim in speed_claims)
        
        return HeuristicResult(
            name="Publication Speed Check",
            description="Checks for unrealistic publication speed claims",
            passed=not has_speed_claims,
            importance="low",
            evidence=["Suspicious publication speed claims"] if has_speed_claims else ["No speed claims"],
            score_impact=0.1 if has_speed_claims else 0.0
        )
