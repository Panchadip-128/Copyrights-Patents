"""
X-MPFD-E++: Explainable Multimodal Phishing & Fraud Detection and Reasoning Engine

Copyright © 2026. All Rights Reserved.

Main package initialization for X-MPFD-E++ framework.
"""

__version__ = "1.0.0"
__author__ = "X-MPFD-E++ Development Team"
__copyright__ = "Copyright © 2026. All Rights Reserved."

from .multimodal_orchestrator.orchestrator import MultimodalOrchestrator
from .fusion_policy_engine.fusion_engine import FusionPolicyEngine, FusionPolicy
from .decision_risk_core.detector import PhishingDetector
from .explanation_synthesis_engine.explainer import ExplanationSynthesizer
from .leakage_bias_auditor.auditor import IntegrityAuditor
from .inference_api.api import InferenceAPI

__all__ = [
    'PhishingDetector',
    'MultimodalOrchestrator',
    'FusionPolicyEngine',
    'FusionPolicy',
    'ExplanationSynthesizer',
    'IntegrityAuditor',
    'InferenceAPI'
]
