"""
Scoring Engine - Calculates individual score components

Implements proprietary scoring algorithms for credibility factors.
Copyright (c) 2026. All rights reserved.
"""

from typing import Dict, Optional
from dataclasses import dataclass


@dataclass
class ScoreComponents:
    """Individual score components for credibility assessment"""
    cfp_risk_score: float = 0.5
    website_credibility_score: float = 0.5
    indexing_credibility_score: float = 0.5
    contact_legitimacy_score: float = 0.5
    organizational_structure_score: float = 0.5
    publication_history_score: float = 0.5
    total_risk_score: float = 0.5


class ScoringEngine:
    """
    Calculates individual score components using proprietary algorithms.
    
    All scoring formulas are explicitly defined and deterministic.
    """
    
    # Proprietary weighting scheme (copyright-protected)
    COMPONENT_WEIGHTS = {
        'cfp_risk': 0.25,
        'website_credibility': 0.20,
        'indexing_credibility': 0.20,
        'contact_legitimacy': 0.15,
        'organizational_structure': 0.10,
        'publication_history': 0.10
    }
    
    def __init__(self):
        """Initialize the scoring engine"""
        pass
    
    def calculate_components(
        self,
        cfp_data: Optional[Dict] = None,
        website_data: Optional[Dict] = None,
        fingerprint_data: Optional[Dict] = None
    ) -> ScoreComponents:
        """
        Calculate all score components.
        
        Proprietary scoring algorithm.
        """
        # Calculate individual components
        cfp_risk = self._score_cfp_risk(cfp_data)
        website_cred = self._score_website_credibility(website_data)
        indexing_cred = self._score_indexing_credibility(fingerprint_data)
        contact_legit = self._score_contact_legitimacy(cfp_data, website_data)
        org_structure = self._score_organizational_structure(website_data, fingerprint_data)
        pub_history = self._score_publication_history(fingerprint_data)
        
        # Calculate weighted total risk (proprietary formula)
        total_risk = (
            cfp_risk * self.COMPONENT_WEIGHTS['cfp_risk'] +
            (1.0 - website_cred) * self.COMPONENT_WEIGHTS['website_credibility'] +
            (1.0 - indexing_cred) * self.COMPONENT_WEIGHTS['indexing_credibility'] +
            (1.0 - contact_legit) * self.COMPONENT_WEIGHTS['contact_legitimacy'] +
            (1.0 - org_structure) * self.COMPONENT_WEIGHTS['organizational_structure'] +
            (1.0 - pub_history) * self.COMPONENT_WEIGHTS['publication_history']
        )
        
        return ScoreComponents(
            cfp_risk_score=cfp_risk,
            website_credibility_score=website_cred,
            indexing_credibility_score=indexing_cred,
            contact_legitimacy_score=contact_legit,
            organizational_structure_score=org_structure,
            publication_history_score=pub_history,
            total_risk_score=min(total_risk, 1.0)
        )
    
    def _score_cfp_risk(self, cfp_data: Optional[Dict]) -> float:
        """Score CFP risk (0.0 = low risk, 1.0 = high risk)"""
        if not cfp_data:
            return 0.5  # Neutral when no data
        
        return cfp_data.get('overall_cfp_risk', 0.5)
    
    def _score_website_credibility(self, website_data: Optional[Dict]) -> float:
        """Score website credibility (0.0 = low, 1.0 = high)"""
        if not website_data:
            return 0.5  # Neutral when no data
        
        return website_data.get('credibility_score', 0.5)
    
    def _score_indexing_credibility(self, fingerprint_data: Optional[Dict]) -> float:
        """Score indexing claim credibility (0.0 = low, 1.0 = high)"""
        if not fingerprint_data:
            return 0.5
        
        indexing_data = fingerprint_data.get('indexing_analysis', {})
        return indexing_data.get('overall_credibility', 0.5)
    
    def _score_contact_legitimacy(
        self,
        cfp_data: Optional[Dict],
        website_data: Optional[Dict]
    ) -> float:
        """Score contact information legitimacy (0.0 = low, 1.0 = high)"""
        score = 0.5
        
        if cfp_data:
            score = max(score, cfp_data.get('contact_legitimacy_score', 0.5))
        
        if website_data:
            contact_score = website_data.get('contact_legitimacy', 0.5)
            score = (score + contact_score) / 2
        
        return score
    
    def _score_organizational_structure(
        self,
        website_data: Optional[Dict],
        fingerprint_data: Optional[Dict]
    ) -> float:
        """Score organizational structure (0.0 = weak, 1.0 = strong)"""
        score = 0.5
        
        if website_data:
            # Check for organizational indicators
            has_committee = website_data.get('has_committee_page', False)
            has_about = website_data.get('has_about_page', False)
            
            if has_committee:
                score += 0.2
            if has_about:
                score += 0.1
        
        if fingerprint_data:
            # Check for institutional affiliations
            affiliations = fingerprint_data.get('institutional_affiliations', [])
            if affiliations:
                score += min(len(affiliations) * 0.05, 0.2)
        
        return min(score, 1.0)
    
    def _score_publication_history(self, fingerprint_data: Optional[Dict]) -> float:
        """Score publication history (0.0 = no history, 1.0 = established)"""
        if not fingerprint_data:
            return 0.5
        
        # In a real implementation, this would check historical data
        # For now, return neutral
        return 0.5
