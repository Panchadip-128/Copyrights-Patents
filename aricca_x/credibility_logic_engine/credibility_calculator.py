"""
Credibility Calculator - Calculates final credibility scores

Implements proprietary credibility calculation algorithms.
Copyright (c) 2026. All rights reserved.
"""

from typing import List
from dataclasses import dataclass
from .scoring_engine import ScoreComponents
from .heuristic_evaluator import HeuristicResult


@dataclass
class CredibilityScore:
    """Final credibility score with breakdown"""
    credibility_score: float
    total_risk_score: float
    component_contribution: dict
    heuristic_contribution: dict
    calculation_method: str = "proprietary_weighted_formula"


class CredibilityCalculator:
    """
    Calculates final credibility scores using proprietary algorithms.
    
    All formulas are explicitly defined and deterministic.
    """
    
    # Proprietary calculation parameters (copyright-protected)
    COMPONENT_TO_CREDIBILITY_WEIGHT = 0.60
    HEURISTIC_TO_CREDIBILITY_WEIGHT = 0.40
    
    def __init__(self):
        """Initialize the credibility calculator"""
        pass
    
    def calculate_credibility(
        self,
        score_components: ScoreComponents,
        heuristic_results: List[HeuristicResult]
    ) -> CredibilityScore:
        """
        Calculate final credibility score.
        
        Proprietary calculation formula combining component scores
        and heuristic evaluations.
        
        Returns credibility score from 0.0 (low credibility) to 1.0 (high credibility).
        """
        # Calculate component-based credibility
        component_credibility = self._calculate_component_credibility(score_components)
        
        # Calculate heuristic-based credibility
        heuristic_credibility = self._calculate_heuristic_credibility(heuristic_results)
        
        # Combine using proprietary weighting (copyright-protected formula)
        final_credibility = (
            component_credibility * self.COMPONENT_TO_CREDIBILITY_WEIGHT +
            heuristic_credibility * self.HEURISTIC_TO_CREDIBILITY_WEIGHT
        )
        
        # Calculate component contributions
        component_contribution = {
            'cfp_risk': self._component_impact(score_components.cfp_risk_score, invert=True),
            'website_credibility': self._component_impact(score_components.website_credibility_score),
            'indexing_credibility': self._component_impact(score_components.indexing_credibility_score),
            'contact_legitimacy': self._component_impact(score_components.contact_legitimacy_score),
            'organizational_structure': self._component_impact(score_components.organizational_structure_score),
            'publication_history': self._component_impact(score_components.publication_history_score)
        }
        
        # Calculate heuristic contributions
        heuristic_contribution = self._calculate_heuristic_contributions(heuristic_results)
        
        return CredibilityScore(
            credibility_score=final_credibility,
            total_risk_score=score_components.total_risk_score,
            component_contribution=component_contribution,
            heuristic_contribution=heuristic_contribution
        )
    
    def _calculate_component_credibility(self, components: ScoreComponents) -> float:
        """
        Calculate credibility from score components.
        
        Proprietary formula.
        """
        # Invert risk scores to get credibility scores
        cfp_credibility = 1.0 - components.cfp_risk_score
        
        # Weighted average of all credibility indicators
        credibility = (
            cfp_credibility * 0.25 +
            components.website_credibility_score * 0.20 +
            components.indexing_credibility_score * 0.20 +
            components.contact_legitimacy_score * 0.15 +
            components.organizational_structure_score * 0.10 +
            components.publication_history_score * 0.10
        )
        
        return min(max(credibility, 0.0), 1.0)
    
    def _calculate_heuristic_credibility(self, results: List[HeuristicResult]) -> float:
        """
        Calculate credibility from heuristic results.
        
        Proprietary formula.
        """
        if not results:
            return 0.5  # Neutral when no heuristics
        
        # Start with perfect score
        credibility = 1.0
        
        # Deduct for failed heuristics based on importance
        importance_weights = {
            'critical': 0.25,
            'high': 0.15,
            'medium': 0.10,
            'low': 0.05
        }
        
        for result in results:
            if not result.passed:
                weight = importance_weights.get(result.importance, 0.10)
                credibility -= weight
        
        return min(max(credibility, 0.0), 1.0)
    
    def _component_impact(self, score: float, invert: bool = False) -> float:
        """Calculate component's impact on final score"""
        if invert:
            score = 1.0 - score
        return score
    
    def _calculate_heuristic_contributions(
        self,
        results: List[HeuristicResult]
    ) -> dict:
        """Calculate individual heuristic contributions"""
        contributions = {}
        
        for result in results:
            contributions[result.name] = {
                'passed': result.passed,
                'importance': result.importance,
                'impact': result.score_impact
            }
        
        return contributions
