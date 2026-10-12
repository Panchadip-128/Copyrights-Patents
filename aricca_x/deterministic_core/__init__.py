"""
Deterministic Core - shared, ML-free primitives for the ARICCA-X pipeline

  canonical          bit-stable serialization + SHA-256 digests
  audit_chain        hash-chained, strictly serializable phase records
  rules              sealed ProductionRule registry (bifurcated architecture)
  determinism_guard  refuses to run if probabilistic ML libraries are loaded
  adw                Adaptive Decay Weighting + epistemic evidence interval
  csad               layer-asymmetric Cross-Signal Anomaly Detection

Copyright (c) 2026. All rights reserved. Patent Pending.
"""

from .canonical import canonical_json, digest, sha256_hex, to_canonical
from .audit_chain import AuditChain, PhaseRecord, verify_exported_chain
from .rules import DEFAULT_REGISTRY, DEFAULT_RULES, ProductionRule, RuleRegistry, make_rule
from .determinism_guard import (
    DeterminismReport,
    DeterminismViolation,
    enforce_deterministic_runtime,
    inspect_runtime,
)
from .adw import ADWResult, adaptive_decay_weighting, clamp01
from .csad import (
    SUBSTRATE,
    SURFACE,
    CSADResult,
    DivergencePair,
    cross_signal_anomaly_detection,
    g_function,
)

__all__ = [
    'canonical_json', 'digest', 'sha256_hex', 'to_canonical',
    'AuditChain', 'PhaseRecord', 'verify_exported_chain',
    'DEFAULT_REGISTRY', 'DEFAULT_RULES', 'ProductionRule', 'RuleRegistry', 'make_rule',
    'DeterminismReport', 'DeterminismViolation', 'enforce_deterministic_runtime', 'inspect_runtime',
    'ADWResult', 'adaptive_decay_weighting', 'clamp01',
    'SUBSTRATE', 'SURFACE', 'CSADResult', 'DivergencePair',
    'cross_signal_anomaly_detection', 'g_function',
]
