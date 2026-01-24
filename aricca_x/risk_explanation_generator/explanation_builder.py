"""
Explanation Builder - Builds natural language explanations

Implements proprietary explanation generation templates.
Copyright (c) 2026. All rights reserved.
"""

from typing import Dict
from dataclasses import dataclass


@dataclass
class Explanation:
    """Structured explanation"""
    summary: str
    details: str
    severity: str


class ExplanationBuilder:
    """
    Builds human-readable explanations of risk assessments.
    
    Uses proprietary templates and natural language generation.
    """
    
    # Proprietary explanation templates (copyright-protected)
    RISK_TEMPLATES = {
        'low': {
            'summary': "This venue appears LEGITIMATE with minimal risk indicators.",
            'intro': "Based on our comprehensive analysis, this venue demonstrates strong credibility indicators.",
            'conclusion': "This venue meets most quality standards for academic publishing."
        },
        'medium': {
            'summary': "This venue shows MIXED signals - exercise CAUTION.",
            'intro': "Our analysis reveals both positive and concerning indicators for this venue.",
            'conclusion': "Carefully verify key claims before submitting to this venue."
        },
        'high': {
            'summary': "This venue shows SIGNIFICANT predatory indicators - HIGH RISK.",
            'intro': "Our analysis has identified multiple serious concerns with this venue.",
            'conclusion': "We strongly recommend considering alternative publication venues."
        },
        'critical': {
            'summary': "This venue shows SEVERE predatory characteristics - CRITICAL RISK.",
            'intro': "Our analysis has detected critical warning signs indicating this venue is likely predatory.",
            'conclusion': "DO NOT submit to this venue. Seek reputable alternatives."
        }
    }
    
    def __init__(self):
        """Initialize the explanation builder"""
        pass
    
    def build_summary(self, assessment_data: Dict, risk_category: any) -> str:
        """
        Build concise summary of risk assessment.
        
        Proprietary template-based generation.
        """
        risk_level = assessment_data.get('risk_level', 'medium')
        venue_name = assessment_data.get('venue_name', 'Unknown Venue')
        credibility_score = assessment_data.get('overall_credibility_score', 0.5)
        
        template = self.RISK_TEMPLATES.get(risk_level, self.RISK_TEMPLATES['medium'])
        
        summary = f"{venue_name}: {template['summary']}\n"
        summary += f"Credibility Score: {credibility_score:.2%} | Risk Level: {risk_level.upper()}"
        
        return summary
    
    def build_detailed_explanation(
        self,
        assessment_data: Dict,
        risk_category: any,
        target_audience: str = "researcher"
    ) -> str:
        """
        Build detailed explanation tailored to audience.
        
        Proprietary explanation algorithm.
        """
        risk_level = assessment_data.get('risk_level', 'medium')
        template = self.RISK_TEMPLATES.get(risk_level, self.RISK_TEMPLATES['medium'])
        
        explanation_parts = []
        
        # Introduction
        explanation_parts.append(template['intro'])
        explanation_parts.append("")
        
        # Analysis details
        explanation_parts.append("ANALYSIS BREAKDOWN:")
        
        # Component scores
        components = assessment_data.get('score_components', {})
        if hasattr(components, 'cfp_risk_score'):
            risk_desc = self._describe_risk_level(components.cfp_risk_score)
            explanation_parts.append(
                f"• Call for Papers Risk: {risk_desc} ({components.cfp_risk_score:.2f})"
            )
        
        if hasattr(components, 'website_credibility_score'):
            cred_desc = self._describe_credibility_level(components.website_credibility_score)
            explanation_parts.append(
                f"• Website Credibility: {cred_desc} ({components.website_credibility_score:.2f})"
            )
        
        if hasattr(components, 'indexing_credibility_score'):
            cred_desc = self._describe_credibility_level(components.indexing_credibility_score)
            explanation_parts.append(
                f"• Indexing Claims: {cred_desc} ({components.indexing_credibility_score:.2f})"
            )
        
        explanation_parts.append("")
        
        # Heuristic results
        heuristic_results = assessment_data.get('heuristic_results', [])
        failed_heuristics = [h for h in heuristic_results if hasattr(h, 'passed') and not h.passed]
        
        if failed_heuristics:
            explanation_parts.append("FAILED CREDIBILITY CHECKS:")
            for h in failed_heuristics[:5]:  # Top 5
                explanation_parts.append(f"• {h.name}: {h.description}")
        else:
            explanation_parts.append("All credibility checks passed successfully.")
        
        explanation_parts.append("")
        
        # Conclusion
        explanation_parts.append(template['conclusion'])
        
        return '\n'.join(explanation_parts)
    
    def _describe_risk_level(self, score: float) -> str:
        """Describe risk level in natural language"""
        if score < 0.25:
            return "Very Low"
        elif score < 0.50:
            return "Low"
        elif score < 0.75:
            return "Moderate"
        else:
            return "High"
    
    def _describe_credibility_level(self, score: float) -> str:
        """Describe credibility level in natural language"""
        if score < 0.25:
            return "Very Low"
        elif score < 0.50:
            return "Low"
        elif score < 0.75:
            return "Moderate"
        else:
            return "High"
