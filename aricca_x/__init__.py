"""
ARICCA-X: Automated Research Integrity, Credibility & Compliance Analyzer - Extended Edition

A software system designed to analyze research venues and manuscript submissions by generating 
structured venue fingerprints, evaluating submission compliance, analyzing citation behavior, 
and producing deterministic credibility and risk scores using rule-based logic and explainable heuristics.

Copyright (c) 2026. All rights reserved. Patent Pending.
"""

__version__ = "1.0.0"
__author__ = "ARICCA-X Development Team"

# Core deterministic primitives and rule registries
from .deterministic_core import (
    DEFAULT_REGISTRY,
    RuleRegistry,
    AuditChain,
    PhaseRecord,
    adaptive_decay_weighting,
    cross_signal_anomaly_detection,
    enforce_deterministic_runtime,
)

# Four dedicated deterministic modules
from .venue_intelligence import (
    VenueIntelligenceAnalyzer,
    VenueIntelligenceResult,
    UrlAuditResult,
    TemporalIntegrityResult,
    TFETDriftReport,
    FingerprintSnapshot,
)
from .researcher_auditor import (
    ResearcherAuditor,
    ResearcherAuditResult,
    AuthorCitationGraph,
    CitationLoop,
    h_index,
)
from .peer_review_forensics import (
    PeerReviewForensicsAnalyzer,
    PeerReviewAuditResult,
    LinguisticFingerprint,
    SentimentAlignmentResult,
)
from .grant_compliance import (
    GrantComplianceEvaluator,
    GrantComplianceResult,
    PublicationMetadata,
    RuleEvaluationRecord,
)

# Cross-correlation engine & six-phase pipeline
from .cross_correlation_engine import (
    CrossCorrelationEngine,
    CompositeRiskProfile,
)

# Submission gateway & hardware interdiction controller
from .submission_gateway import (
    SubmissionGatewayInterdictionController,
    ManuscriptSubmissionPayload,
    GatewayActionCode,
    ActuationRecord,
)

# Architectural and legacy components
from .credibility_logic_engine import CredibilityLogicEngine
from .venue_fingerprint_builder import VenueFingerprintBuilder
from .compliance_compiler import ComplianceCompiler
from .citation_graph_analyzer import CitationGraphAnalyzer
from .risk_explanation_generator import RiskExplanationGenerator
from .report_renderer import ReportRenderer

__all__ = [
    # Core deterministic components
    'DEFAULT_REGISTRY',
    'RuleRegistry',
    'AuditChain',
    'PhaseRecord',
    'adaptive_decay_weighting',
    'cross_signal_anomaly_detection',
    'enforce_deterministic_runtime',
    # Modules A, B, C, D
    'VenueIntelligenceAnalyzer',
    'VenueIntelligenceResult',
    'UrlAuditResult',
    'TemporalIntegrityResult',
    'TFETDriftReport',
    'FingerprintSnapshot',
    'ResearcherAuditor',
    'ResearcherAuditResult',
    'AuthorCitationGraph',
    'CitationLoop',
    'h_index',
    'PeerReviewForensicsAnalyzer',
    'PeerReviewAuditResult',
    'LinguisticFingerprint',
    'SentimentAlignmentResult',
    'GrantComplianceEvaluator',
    'GrantComplianceResult',
    'PublicationMetadata',
    'RuleEvaluationRecord',
    # Cross-correlation pipeline
    'CrossCorrelationEngine',
    'CompositeRiskProfile',
    # Submission gateway & physical interdiction
    'SubmissionGatewayInterdictionController',
    'ManuscriptSubmissionPayload',
    'GatewayActionCode',
    'ActuationRecord',
    # Structural legacy components
    'CredibilityLogicEngine',
    'VenueFingerprintBuilder',
    'ComplianceCompiler',
    'CitationGraphAnalyzer',
    'RiskExplanationGenerator',
    'ReportRenderer',
]

