"""
ARICCA-X: Automated Research Integrity, Credibility & Compliance Analyzer - Extended Edition

A software system designed to analyze research venues and manuscript submissions by generating 
structured venue fingerprints, evaluating submission compliance, analyzing citation behavior, 
and producing deterministic credibility and risk scores using rule-based logic and explainable heuristics.

Copyright (c) 2026. All rights reserved.
"""

__version__ = "1.0.0"
__author__ = "ARICCA-X Development Team"

from .credibility_logic_engine import CredibilityLogicEngine
from .venue_fingerprint_builder import VenueFingerprintBuilder
from .compliance_compiler import ComplianceCompiler
from .citation_graph_analyzer import CitationGraphAnalyzer
from .risk_explanation_generator import RiskExplanationGenerator
from .report_renderer import ReportRenderer

__all__ = [
    'CredibilityLogicEngine',
    'VenueFingerprintBuilder',
    'ComplianceCompiler',
    'CitationGraphAnalyzer',
    'RiskExplanationGenerator',
    'ReportRenderer'
]
