"""
Risk Categorizer - Categorizes risks into meaningful categories

Implements proprietary risk categorization algorithms.
Copyright (c) 2026. All rights reserved.
"""

from typing import Dict, List
from dataclasses import dataclass
from enum import Enum


class RiskType(Enum):
    """Types of risks"""
    FINANCIAL = "financial"
    REPUTATIONAL = "reputational"
    TIME = "time"
    CAREER = "career"
    ETHICAL = "ethical"


@dataclass
class RiskCategory:
    """Categorized risk information"""
    primary_risk_type: RiskType
    risk_level: str
    risk_description: str
    affected_areas: List[str]


class RiskCategorizer:
    """
    Categorizes identified risks into meaningful categories.
    
    Uses proprietary risk classification algorithms.
    """
    
    def __init__(self):
        """Initialize the risk categorizer"""
        pass
    
    def categorize_risk(self, assessment_data: Dict) -> RiskCategory:
        """
        Categorize risk based on assessment data.
        
        Proprietary categorization algorithm.
        """
        risk_level = assessment_data.get('risk_level', 'medium')
        risk_score = assessment_data.get('overall_credibility_score', 0.5)
        
        # Determine primary risk type
        primary_risk = self._determine_primary_risk(assessment_data)
        
        # Generate risk description
        description = self._generate_risk_description(primary_risk, risk_level)
        
        # Identify affected areas
        affected = self._identify_affected_areas(assessment_data, primary_risk)
        
        return RiskCategory(
            primary_risk_type=primary_risk,
            risk_level=risk_level,
            risk_description=description,
            affected_areas=affected
        )
    
    def _determine_primary_risk(self, assessment_data: Dict) -> RiskType:
        """
        Determine the primary risk type.
        
        Proprietary risk classification algorithm.
        """
        components = assessment_data.get('score_components', {})
        
        # Check for financial risk indicators
        flags = assessment_data.get('flags', [])
        financial_flags = sum(1 for f in flags if 'fee' in f.lower() or 'payment' in f.lower())
        
        if financial_flags > 0:
            return RiskType.FINANCIAL
        
        # Check for reputational risk
        if hasattr(components, 'indexing_credibility_score'):
            if components.indexing_credibility_score < 0.4:
                return RiskType.REPUTATIONAL
        
        # Check for time waste risk
        if hasattr(components, 'cfp_risk_score'):
            if components.cfp_risk_score > 0.7:
                return RiskType.TIME
        
        # Default to reputational risk
        return RiskType.REPUTATIONAL
    
    def _generate_risk_description(self, risk_type: RiskType, risk_level: str) -> str:
        """Generate description of the risk"""
        descriptions = {
            RiskType.FINANCIAL: {
                'low': "Minimal financial risk - fees appear standard",
                'medium': "Moderate financial risk - verify fee structure",
                'high': "High financial risk - questionable fee practices",
                'critical': "Critical financial risk - likely predatory fees"
            },
            RiskType.REPUTATIONAL: {
                'low': "Minimal reputational risk - venue appears credible",
                'medium': "Moderate reputational risk - mixed credibility signals",
                'high': "High reputational risk - venue shows predatory indicators",
                'critical': "Critical reputational risk - publishing here may harm your career"
            },
            RiskType.TIME: {
                'low': "Minimal time risk - standard publishing process expected",
                'medium': "Moderate time risk - review process may be problematic",
                'high': "High time risk - significant delays or issues likely",
                'critical': "Critical time risk - likely to waste substantial time"
            },
            RiskType.CAREER: {
                'low': "Minimal career risk - venue meets academic standards",
                'medium': "Moderate career risk - venue acceptance may vary",
                'high': "High career risk - venue may not be recognized",
                'critical': "Critical career risk - publication may be dismissed or penalized"
            },
            RiskType.ETHICAL: {
                'low': "Minimal ethical concerns - venue follows academic standards",
                'medium': "Moderate ethical concerns - some questionable practices",
                'high': "High ethical concerns - predatory characteristics present",
                'critical': "Critical ethical concerns - venue clearly violates academic ethics"
            }
        }
        
        return descriptions.get(risk_type, {}).get(risk_level, "Unknown risk level")
    
    def _identify_affected_areas(self, assessment_data: Dict, risk_type: RiskType) -> List[str]:
        """Identify areas affected by the risk"""
        affected = []
        
        if risk_type == RiskType.FINANCIAL:
            affected.extend(["Publication fees", "Registration costs", "Hidden charges"])
        elif risk_type == RiskType.REPUTATIONAL:
            affected.extend(["Academic reputation", "CV quality", "Future citations"])
        elif risk_type == RiskType.TIME:
            affected.extend(["Research time", "Publication timeline", "Career progression"])
        elif risk_type == RiskType.CAREER:
            affected.extend(["Tenure evaluation", "Grant applications", "Academic recognition"])
        elif risk_type == RiskType.ETHICAL:
            affected.extend(["Academic integrity", "Institutional reputation", "Research ethics"])
        
        return affected
