"""
Credibility Logic Engine - Non-ML core with explicit scoring formulas

Implements proprietary deterministic credibility scoring algorithms.
Copyright (c) 2026. All rights reserved.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime
from .scoring_engine import ScoringEngine, ScoreComponents
from .heuristic_evaluator import HeuristicEvaluator, HeuristicResult
from .credibility_calculator import CredibilityCalculator, CredibilityScore


@dataclass
class CredibilityAssessment:
    """Complete credibility assessment result"""
    venue_id: str
    venue_name: str
    overall_credibility_score: float
    risk_level: str  # "low", "medium", "high", "critical"
    score_components: ScoreComponents
    heuristic_results: List[HeuristicResult]
    confidence: float
    assessment_timestamp: datetime
    recommendations: List[str]
    flags: List[str]


class CredibilityLogicEngine:
    """
    Non-ML credibility assessment engine using explicit rule-based logic.
    
    This proprietary engine implements deterministic scoring algorithms
    without relying on machine learning or external datasets. All logic
    is explicitly defined and reproducible.
    """
    
    # Proprietary risk level thresholds (copyright-protected)
    RISK_THRESHOLDS = {
        'low': (0.0, 0.25),
        'medium': (0.25, 0.50),
        'high': (0.50, 0.75),
        'critical': (0.75, 1.0)
    }
    
    def __init__(self):
        """Initialize the credibility logic engine"""
        self.scoring_engine = ScoringEngine()
        self.heuristic_evaluator = HeuristicEvaluator()
        self.calculator = CredibilityCalculator()
    
    def assess_credibility(
        self,
        venue_data: Dict,
        cfp_data: Optional[Dict] = None,
        website_data: Optional[Dict] = None,
        fingerprint_data: Optional[Dict] = None
    ) -> CredibilityAssessment:
        """
        Perform complete credibility assessment of a venue.
        
        This is the main entry point that orchestrates all credibility
        evaluation components using deterministic logic.
        
        Args:
            venue_data: Basic venue information
            cfp_data: Call for Papers analysis data
            website_data: Website analysis data
            fingerprint_data: Venue fingerprint data
            
        Returns:
            CredibilityAssessment object
        """
        venue_id = venue_data.get('venue_id', 'unknown')
        venue_name = venue_data.get('venue_name', 'Unknown Venue')
        
        # Phase 1: Calculate score components
        score_components = self.scoring_engine.calculate_components(
            cfp_data=cfp_data,
            website_data=website_data,
            fingerprint_data=fingerprint_data
        )
        
        # Phase 2: Evaluate heuristics
        heuristic_results = self.heuristic_evaluator.evaluate_all(
            venue_data=venue_data,
            cfp_data=cfp_data,
            website_data=website_data,
            fingerprint_data=fingerprint_data
        )
        
        # Phase 3: Calculate final credibility score
        credibility_score = self.calculator.calculate_credibility(
            score_components=score_components,
            heuristic_results=heuristic_results
        )
        
        # Phase 4: Determine risk level
        risk_level = self._determine_risk_level(credibility_score.total_risk_score)
        
        # Phase 5: Generate recommendations and flags
        recommendations = self._generate_recommendations(
            score_components,
            heuristic_results,
            credibility_score
        )
        flags = self._generate_flags(score_components, heuristic_results)
        
        # Phase 6: Calculate assessment confidence
        confidence = self._calculate_confidence(
            cfp_data, website_data, fingerprint_data
        )
        
        return CredibilityAssessment(
            venue_id=venue_id,
            venue_name=venue_name,
            overall_credibility_score=credibility_score.credibility_score,
            risk_level=risk_level,
            score_components=score_components,
            heuristic_results=heuristic_results,
            confidence=confidence,
            assessment_timestamp=datetime.now(),
            recommendations=recommendations,
            flags=flags
        )
    
    def _determine_risk_level(self, risk_score: float) -> str:
        """
        Determine risk level from risk score.
        
        Proprietary risk classification logic.
        """
        for level, (min_score, max_score) in self.RISK_THRESHOLDS.items():
            if min_score <= risk_score < max_score:
                return level
        
        return 'critical'
    
    def _generate_recommendations(
        self,
        components: ScoreComponents,
        heuristics: List[HeuristicResult],
        credibility: CredibilityScore
    ) -> List[str]:
        """
        Generate actionable recommendations.
        
        Proprietary recommendation generation algorithm.
        """
        recommendations = []
        
        # CFP-related recommendations
        if components.cfp_risk_score > 0.6:
            recommendations.append(
                "CFP shows high-risk indicators. Carefully review submission requirements "
                "and verify indexing claims before submitting."
            )
        
        # Website-related recommendations
        if components.website_credibility_score < 0.4:
            recommendations.append(
                "Website shows low credibility. Check for SSL certification, contact "
                "information, and organizational structure."
            )
        
        # Indexing-related recommendations
        if components.indexing_credibility_score < 0.5:
            recommendations.append(
                "Indexing claims are questionable. Independently verify indexing status "
                "with claimed databases before submission."
            )
        
        # Overall risk recommendations
        if credibility.total_risk_score > 0.7:
            recommendations.append(
                "HIGH RISK: This venue shows multiple predatory indicators. "
                "Consider alternative publication venues."
            )
        elif credibility.total_risk_score > 0.5:
            recommendations.append(
                "MODERATE RISK: Exercise caution. Verify venue credentials through "
                "independent sources before proceeding."
            )
        
        # Heuristic-based recommendations
        failed_heuristics = [h for h in heuristics if not h.passed]
        if len(failed_heuristics) > 3:
            recommendations.append(
                f"Failed {len(failed_heuristics)} credibility checks. "
                "Review venue carefully against established predatory indicators."
            )
        
        return recommendations
    
    def _generate_flags(
        self,
        components: ScoreComponents,
        heuristics: List[HeuristicResult]
    ) -> List[str]:
        """
        Generate warning flags.
        
        Proprietary flag generation algorithm.
        """
        flags = []
        
        # Critical flags
        if components.cfp_risk_score > 0.8:
            flags.append("🚨 CRITICAL: CFP shows severe predatory indicators")
        
        if components.indexing_credibility_score < 0.3:
            flags.append("⚠️ WARNING: Indexing claims highly suspicious")
        
        # Important flags
        if components.contact_legitimacy_score < 0.4:
            flags.append("⚠️ WARNING: Contact information appears illegitimate")
        
        if components.website_credibility_score < 0.3:
            flags.append("⚠️ WARNING: Website quality below acceptable standards")
        
        # Heuristic flags
        critical_failures = [
            h for h in heuristics
            if not h.passed and h.importance == 'critical'
        ]
        if critical_failures:
            for failure in critical_failures:
                flags.append(f"🚨 CRITICAL: {failure.name}")
        
        return flags
    
    def _calculate_confidence(
        self,
        cfp_data: Optional[Dict],
        website_data: Optional[Dict],
        fingerprint_data: Optional[Dict]
    ) -> float:
        """
        Calculate confidence in the assessment.
        
        Proprietary confidence calculation algorithm.
        """
        confidence = 0.0
        
        # Data availability
        if cfp_data:
            confidence += 0.35
        if website_data:
            confidence += 0.35
        if fingerprint_data:
            confidence += 0.30
        
        return min(confidence, 1.0)
    
    def batch_assess(
        self,
        venues: List[Dict]
    ) -> List[CredibilityAssessment]:
        """
        Assess multiple venues in batch.
        
        Args:
            venues: List of venue data dictionaries
            
        Returns:
            List of CredibilityAssessment objects
        """
        assessments = []
        
        for venue in venues:
            try:
                assessment = self.assess_credibility(
                    venue_data=venue,
                    cfp_data=venue.get('cfp_data'),
                    website_data=venue.get('website_data'),
                    fingerprint_data=venue.get('fingerprint_data')
                )
                assessments.append(assessment)
            except Exception as e:
                # Create error assessment
                assessments.append(CredibilityAssessment(
                    venue_id=venue.get('venue_id', 'error'),
                    venue_name=venue.get('venue_name', 'Error'),
                    overall_credibility_score=0.0,
                    risk_level='critical',
                    score_components=ScoreComponents(),
                    heuristic_results=[],
                    confidence=0.0,
                    assessment_timestamp=datetime.now(),
                    recommendations=[f"Assessment failed: {str(e)}"],
                    flags=["🚨 CRITICAL: Assessment error"]
                ))
        
        return assessments
    
    def compare_venues(
        self,
        assessments: List[CredibilityAssessment]
    ) -> Dict[str, any]:
        """
        Compare multiple venue assessments.
        
        Proprietary comparison algorithm.
        """
        if not assessments:
            return {}
        
        # Calculate statistics
        scores = [a.overall_credibility_score for a in assessments]
        risk_scores = [a.score_components.total_risk_score for a in assessments]
        
        # Rank venues
        ranked = sorted(
            assessments,
            key=lambda a: a.overall_credibility_score,
            reverse=True
        )
        
        return {
            'total_venues': len(assessments),
            'average_credibility': sum(scores) / len(scores),
            'average_risk': sum(risk_scores) / len(risk_scores),
            'risk_distribution': {
                level: sum(1 for a in assessments if a.risk_level == level)
                for level in ['low', 'medium', 'high', 'critical']
            },
            'best_venue': {
                'name': ranked[0].venue_name,
                'score': ranked[0].overall_credibility_score
            },
            'worst_venue': {
                'name': ranked[-1].venue_name,
                'score': ranked[-1].overall_credibility_score
            },
            'recommended_venues': [
                {'name': a.venue_name, 'score': a.overall_credibility_score}
                for a in ranked if a.risk_level in ['low', 'medium']
            ][:5]
        }
