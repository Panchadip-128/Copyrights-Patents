"""
Risk Explanation Generator - Generates human-readable risk explanations

Implements proprietary explanation generation algorithms.
Copyright (c) 2026. All rights reserved.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from .explanation_builder import ExplanationBuilder, Explanation
from .risk_categorizer import RiskCategorizer, RiskCategory


@dataclass
class RiskExplanation:
    """Complete risk explanation"""
    summary: str
    detailed_explanation: str
    risk_factors: List[str]
    mitigation_strategies: List[str]
    evidence: List[str]
    risk_level: str
    confidence: float


class RiskExplanationGenerator:
    """
    Generates human-readable explanations of risk assessments.
    
    Implements proprietary natural language generation for risk communication.
    """
    
    def __init__(self):
        """Initialize the risk explanation generator"""
        self.builder = ExplanationBuilder()
        self.categorizer = RiskCategorizer()
    
    def generate_explanation(
        self,
        assessment_data: Dict,
        target_audience: str = "researcher"
    ) -> RiskExplanation:
        """
        Generate comprehensive risk explanation.
        
        Args:
            assessment_data: Credibility assessment data
            target_audience: "researcher", "administrator", or "general"
            
        Returns:
            RiskExplanation object
        """
        # Categorize risk
        risk_category = self.categorizer.categorize_risk(assessment_data)
        
        # Build summary
        summary = self.builder.build_summary(assessment_data, risk_category)
        
        # Build detailed explanation
        detailed = self.builder.build_detailed_explanation(
            assessment_data,
            risk_category,
            target_audience
        )
        
        # Extract risk factors
        risk_factors = self._extract_risk_factors(assessment_data)
        
        # Generate mitigation strategies
        mitigation = self._generate_mitigation_strategies(
            assessment_data,
            risk_category
        )
        
        # Collect evidence
        evidence = self._collect_evidence(assessment_data)
        
        # Get risk level and confidence
        risk_level = assessment_data.get('risk_level', 'unknown')
        confidence = assessment_data.get('confidence', 0.5)
        
        return RiskExplanation(
            summary=summary,
            detailed_explanation=detailed,
            risk_factors=risk_factors,
            mitigation_strategies=mitigation,
            evidence=evidence,
            risk_level=risk_level,
            confidence=confidence
        )
    
    def _extract_risk_factors(self, assessment_data: Dict) -> List[str]:
        """Extract key risk factors from assessment"""
        factors = []
        
        components = assessment_data.get('score_components', {})
        
        # Check CFP risk
        if hasattr(components, 'cfp_risk_score'):
            if components.cfp_risk_score > 0.6:
                factors.append(
                    f"High-risk CFP indicators (score: {components.cfp_risk_score:.2f})"
                )
        
        # Check website credibility
        if hasattr(components, 'website_credibility_score'):
            if components.website_credibility_score < 0.4:
                factors.append(
                    f"Low website credibility (score: {components.website_credibility_score:.2f})"
                )
        
        # Check indexing credibility
        if hasattr(components, 'indexing_credibility_score'):
            if components.indexing_credibility_score < 0.5:
                factors.append(
                    f"Questionable indexing claims (score: {components.indexing_credibility_score:.2f})"
                )
        
        # Check flags
        flags = assessment_data.get('flags', [])
        factors.extend(flags)
        
        return factors
    
    def _generate_mitigation_strategies(
        self,
        assessment_data: Dict,
        risk_category: RiskCategory
    ) -> List[str]:
        """Generate mitigation strategies based on risk"""
        strategies = []
        
        risk_level = assessment_data.get('risk_level', 'medium')
        
        if risk_level in ['high', 'critical']:
            strategies.append(
                "Consider alternative venues: Look for venues with verified "
                "indexing and established reputation."
            )
            strategies.append(
                "Consult colleagues: Discuss this venue with experienced researchers "
                "in your field."
            )
        
        if risk_level in ['medium', 'high', 'critical']:
            strategies.append(
                "Independent verification: Verify all claims (indexing, impact factor, "
                "etc.) through official databases."
            )
            strategies.append(
                "Review publication history: Check previous publications and their "
                "quality/visibility."
            )
        
        # Add recommendations from assessment
        recommendations = assessment_data.get('recommendations', [])
        strategies.extend(recommendations)
        
        return strategies
    
    def _collect_evidence(self, assessment_data: Dict) -> List[str]:
        """Collect evidence supporting the assessment"""
        evidence = []
        
        # Collect heuristic evidence
        heuristic_results = assessment_data.get('heuristic_results', [])
        for result in heuristic_results:
            if hasattr(result, 'evidence') and not result.passed:
                evidence.extend(result.evidence)
        
        # Collect component evidence
        components = assessment_data.get('score_components', {})
        if hasattr(components, 'cfp_risk_score') and components.cfp_risk_score > 0.7:
            evidence.append("CFP contains multiple predatory indicators")
        
        return evidence[:10]  # Limit to top 10
