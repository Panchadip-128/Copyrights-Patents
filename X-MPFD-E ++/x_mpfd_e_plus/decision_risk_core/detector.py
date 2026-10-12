"""
Decision Risk Core - Phishing Detector
Module: x_mpfd_e_plus.decision_risk_core.detector

Coordinates signal ingestion, feature registry recording, fusion policy evaluation,
and deterministic explanation synthesis.
Patent Claims 1 through 15.

Fulfills CRI Guidelines 2025 (Paras 4.5.1, 4.5.3, 4.5.4):
Physically suppresses parser worker thread allocation when H(U) > 4.50.

Copyright © 2026 Panchadip B & Somyajeet A. All Rights Reserved.
"""

from typing import Optional, Dict, Any, List
from ..multimodal_orchestrator.orchestrator import MultimodalOrchestrator, MultimodalSignalTensor
from ..fusion_policy_engine.fusion_engine import FusionPolicyEngine, FusionStrategy, AnalysisResult
from ..explanation_synthesis_engine.explainer import ExplanationSynthesizer
from ..feature_registry.registry import FeatureRegistry, FeatureCategory, FeatureLineage


class PhishingDetector:
    """
    Deterministic Multimodal Phishing Detector.
    Patent Claim 1.
    """
    def __init__(
        self,
        fusion_policy: str = "gated",
        explain: bool = True,
        entropy_scope: str = "url",
        entropy_threshold: Optional[float] = None,
    ):
        self.orchestrator = MultimodalOrchestrator()
        self.fusion_engine = FusionPolicyEngine()
        self.fusion_engine.set_policy(self.fusion_engine.get_policy(fusion_policy))
        self.explainer = ExplanationSynthesizer()
        self.feature_registry = FeatureRegistry()
        self.explain = explain
        self.entropy_scope = entropy_scope
        default_thresh = 3.80 if entropy_scope == "hostname" else (4.15 if entropy_scope == "host_path" else 4.50)
        self.entropy_threshold = entropy_threshold or default_thresh

    def analyze_url(
        self,
        url: str,
        html: Optional[str] = None,
        screenshot: Optional[bytes] = None,
        tls_valid: bool = True,
        is_self_signed: bool = False,
        entropy_scope: Optional[str] = None,
        entropy_threshold: Optional[float] = None,
    ) -> AnalysisResult:
        """
        Analyzes a URL and optional multimodal artifacts deterministically.
        Physically implements the Conditional Gated Fusion compute bypass (Claims 6 & 15).
        Supports configurable Shannon entropy evaluation over:
        1. Full URL string (baseline gateway mode, threshold 4.50)
        2. Host plus path excluding query string (middle scope, threshold 4.15)
        3. Hostname component (pure domain mode, threshold 3.80)
        """
        active_scope = entropy_scope or self.entropy_scope
        default_active_thresh = 3.80 if active_scope == "hostname" else (4.15 if active_scope == "host_path" else 4.50)
        active_thresh = entropy_threshold or self.entropy_threshold or default_active_thresh

        # Step 1: Upstream Lexical Extraction (Shannon Entropy)
        # Evaluated in lightweight O(L) buffer before thread allocation
        v_l = self.orchestrator.lexical_analyzer.analyze_url(url)
        if active_scope == "hostname":
            entropy = v_l["hostname_entropy"]
        elif active_scope == "host_path":
            entropy = v_l["host_path_entropy"]
        else:
            entropy = v_l["shannon_entropy"]

        # Step 2: Conditional Gating Check (Claims 6 & 15, Section 3(m) Appliance Control)
        # If Gated Policy is active and H(U) > active_thresh, WITHHOLD downstream HTML AST parsing
        is_gated = (self.fusion_engine.current_policy.strategy == FusionStrategy.GATED)
        bypass_downstream = is_gated and (entropy > active_thresh)

        if bypass_downstream:
            # Physically WITHHOLD HTML AST parsing and visual rendering
            # Do NOT pass html into DeterministicDOMAnalyzer
            v_s = {
                "has_html": False,
                "total_nodes": 0,
                "max_depth": 0,
                "sdr": 0.0,
                "sdr_deviation_pct": 0.0,
                "form_count": 0,
                "password_fields": 0,
                "bypassed": True,
            }
            v_m = {
                "tls_valid": tls_valid,
                "is_self_signed": is_self_signed,
                "bypassed": True,
                "visual_risk_score": 0.05,
            }
            mst = MultimodalSignalTensor(
                lexical_vector=v_l,
                structural_vector=v_s,
                visual_vector=v_m,
                provenance_tags=[
                    {
                        "modality": "lexical",
                        "algorithm": "shannon_entropy_base_2",
                        "value": entropy,
                        "bypassed_downstream": True,
                    }
                ]
            )
        else:
            # Allocate worker threads and execute full HTML AST parsing & visual metadata analysis
            mst = self.orchestrator.orchestrate(
                url=url,
                html=html,
                screenshot=screenshot,
                tls_valid=tls_valid,
                is_self_signed=is_self_signed,
            )
            v_s = mst.structural_vector
            v_m = mst.visual_vector

        sdr = v_s.get("sdr", 0.0)
        sdr_deviation = v_s.get("sdr_deviation_pct", 0.0)
        password_fields = v_s.get("password_fields", 0)
        max_depth = v_s.get("max_depth", 0)

        # Step 3: Feature Registry with Cryptographic Provenance (Claims 1, 7)
        feat_entropy = self.feature_registry.register_feature(
            name="Shannon Entropy",
            category=FeatureCategory.LEXICAL,
            value=entropy,
            source_modality="lexical",
            extraction_method="shannon_entropy_base_2",
            confidence=1.0,
            parameters={"threshold": active_thresh, "scope": active_scope},
        )

        feat_sdr = self.feature_registry.register_feature(
            name="Structural Density Ratio",
            category=FeatureCategory.STRUCTURAL,
            value=sdr,
            source_modality="structural",
            extraction_method="ast_node_depth_sdr",
            confidence=0.95 if not bypass_downstream else 0.0,
            parameters={
                "baseline_sdr": 16.0,
                "deviation_pct": sdr_deviation,
                "has_html": v_s.get("has_html", False),
                "password_fields": password_fields,
                "max_depth": max_depth,
                "bypassed": bypass_downstream,
            },
        )

        feat_tls = self.feature_registry.register_feature(
            name="TLS Certificate Validity",
            category=FeatureCategory.VISUAL,
            value=tls_valid,
            source_modality="visual",
            extraction_method="tls_certificate_evaluator",
            confidence=1.0 if not bypass_downstream else 0.5,
            parameters={"is_self_signed": is_self_signed, "bypassed": bypass_downstream},
        )

        features = [feat_entropy, feat_sdr, feat_tls]

        # Step 4: Execute Deterministic Fusion Policy (Claims 5, 6, 12, 15)
        result: AnalysisResult = self.fusion_engine.execute(
            entropy=entropy,
            sdr_deviation=sdr_deviation,
            tls_valid=tls_valid,
            url=url,
            features=features,
            lexical_risk=v_l.get("lexical_risk_score"),
            structural_risk=v_s.get("structural_risk_score"),
            visual_risk=v_m.get("visual_risk_score"),
            has_html=v_s.get("has_html", False),
            password_fields=password_fields,
            max_depth=max_depth,
            entropy_threshold=active_thresh,
        )

        # Step 5: Explanation Synthesis (Claim 8)
        if self.explain:
            synth_dossier = self.explainer.synthesize(
                decision=result.decision,
                risk_score=result.risk_score,
                policy_name=result.policy_name,
                provenance_tags=mst.provenance_tags,
                entropy=entropy,
                sdr=sdr,
                sdr_deviation=sdr_deviation,
                tls_valid=tls_valid,
                password_fields=password_fields,
                bypassed=result.hardware_compute_bypassed,
            )
            result.explanation = synth_dossier["human_readable_rationale"]

        return result
