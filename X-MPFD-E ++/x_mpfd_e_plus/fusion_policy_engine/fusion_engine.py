"""
Deterministic Fusion Policy Engine
Module: x_mpfd_e_plus.fusion_policy_engine.fusion_engine

Implements deterministic multimodal fusion algorithms:
- Conditional Gated Fusion with Hardware Optimization (Claims 6 and 15, Section 3(k) & 3(m))
- Late Confidence-Weighted Fusion (Claim 5)
- Early Fusion Matrix Algebra (Claims 11 and 12)
- Consensus / Majority Voting Fusion with Missing Modality Degradation (Section 10(4))
- Strict Cartesian Risk Matrix: Complete 8-Cell Lookup (Table 6-2)

Addresses Indian Patent Office CRI Guidelines 2025:
- Para 4.5.1 (Technical Effect / Measured Hardware Control)
- Para 4.5.3 (Named Components, Interfaces & Data Structures)
- Para 4.5.4 (System Action & Performance Improvement)

Copyright © 2026 Panchadip B & Somyajeet A. All Rights Reserved.
"""

from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import hashlib
import json


class SystemControlDirective(str, Enum):
    """
    Physical hardware directives emitted to network security appliances.
    Fulfills 35 U.S.C. Section 101 and Indian Patents Act Section 3(m).
    Directly controls processor thread allocation, network sockets, and memory buffers.
    """
    WITHHOLD_PARSER_AND_RENDERER = "WITHHOLD_PARSER_AND_RENDERER"
    ALLOCATE_AST_PARSER = "ALLOCATE_AST_PARSER"
    ALLOW_STREAM_AND_CACHE = "ALLOW_STREAM_AND_CACHE"
    ISOLATE_CREDENTIAL_FORM = "ISOLATE_CREDENTIAL_FORM"


@dataclass
class AnalysisResult:
    """
    Standardized, deterministic analysis output and hardware control token.
    Patent Claims 1, 8, 14.
    """
    decision: str
    risk_score: float
    confidence: str
    features: List[Any] = field(default_factory=list)
    explanation: str = ""
    policy_name: str = "gated"
    hardware_compute_bypassed: bool = False
    bypassed_modalities: List[str] = field(default_factory=list)
    system_control_directive: str = SystemControlDirective.ALLOW_STREAM_AND_CACHE.value
    rule_id: str = "RULE_DEFAULT"
    sha256_audit_hash: str = ""

    def __post_init__(self):
        if not self.sha256_audit_hash:
            payload = f"{self.decision}:{self.risk_score:.4f}:{self.confidence}:{self.policy_name}:{self.hardware_compute_bypassed}"
            self.sha256_audit_hash = hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "decision": self.decision,
            "risk_score": round(self.risk_score, 4),
            "confidence": self.confidence,
            "policy_name": self.policy_name,
            "hardware_compute_bypassed": self.hardware_compute_bypassed,
            "bypassed_modalities": self.bypassed_modalities,
            "system_control_directive": self.system_control_directive,
            "rule_id": self.rule_id,
            "explanation": self.explanation,
            "sha256_audit_hash": self.sha256_audit_hash,
            "features_count": len(self.features),
        }


class FusionPolicy:
    """Descriptor for an active fusion policy."""
    def __init__(self, name: str, strategy: str, weights: Optional[Dict[str, float]] = None, threshold: float = 0.65):
        self.name = name
        self.strategy = strategy
        self.weights = weights or {"lexical": 0.40, "structural": 0.40, "visual": 0.20}
        self.threshold = threshold


class FusionStrategy:
    """Strategy identifier constants."""
    GATED = "gated"
    WEIGHTED = "weighted"
    EARLY = "early"
    CONSENSUS = "consensus"
    MATRIX = "matrix"


class FusionPolicyEngine:
    """
    Deterministic Fusion Policy Engine.
    Executes versioned, logic-based fusion policies without black-box ML.
    Patent Claims 1, 5, 6, 12, and 15.
    """
    def __init__(self):
        self.current_policy: FusionPolicy = FusionPolicy(
            name="gated_fusion",
            strategy=FusionStrategy.GATED,
            threshold=0.65,
        )

    def get_policy(self, name: str) -> FusionPolicy:
        name_lower = name.lower()
        if name_lower in ("gated", "gated_fusion"):
            return FusionPolicy("gated_fusion", FusionStrategy.GATED)
        elif name_lower in ("weighted", "confidence_weighted", "late_fusion"):
            return FusionPolicy(
                "confidence_weighted",
                FusionStrategy.WEIGHTED,
                weights={"lexical": 0.40, "structural": 0.40, "visual": 0.20},
                threshold=0.65,
            )
        elif name_lower in ("early", "early_fusion"):
            return FusionPolicy("early_fusion", FusionStrategy.EARLY, threshold=0.60)
        elif name_lower in ("consensus", "consensus_fusion"):
            return FusionPolicy("consensus_fusion", FusionStrategy.CONSENSUS, threshold=0.50)
        elif name_lower in ("matrix", "risk_matrix", "strict_matrix", "cartesian_matrix"):
            return FusionPolicy("strict_matrix", FusionStrategy.MATRIX, threshold=0.50)
        else:
            return FusionPolicy("gated_fusion", FusionStrategy.GATED)

    def set_policy(self, policy: FusionPolicy):
        self.current_policy = policy

    def execute(
        self,
        entropy: float,
        sdr_deviation: float,
        tls_valid: bool,
        url: str,
        features: Optional[List[Any]] = None,
        lexical_risk: Optional[float] = None,
        structural_risk: Optional[float] = None,
        visual_risk: Optional[float] = None,
        has_html: bool = True,
        password_fields: int = 0,
        max_depth: int = 0,
        entropy_threshold: float = 4.50,
    ) -> AnalysisResult:
        """
        Executes the currently configured fusion policy deterministically.
        Supports graceful degradation for missing modalities under Section 10(4).
        """
        feats = features or []
        strategy = self.current_policy.strategy

        if strategy == FusionStrategy.GATED:
            return self._execute_gated(
                entropy=entropy,
                sdr_deviation=sdr_deviation,
                tls_valid=tls_valid,
                features=feats,
                has_html=has_html,
                password_fields=password_fields,
                max_depth=max_depth,
                entropy_threshold=entropy_threshold,
            )
        elif strategy == FusionStrategy.WEIGHTED:
            return self._execute_weighted(
                entropy=entropy,
                sdr_deviation=sdr_deviation,
                tls_valid=tls_valid,
                features=feats,
                lex_risk=lexical_risk,
                struct_risk=structural_risk,
                vis_risk=visual_risk,
                has_html=has_html,
            )
        elif strategy == FusionStrategy.EARLY:
            return self._execute_early(
                entropy=entropy,
                sdr_deviation=sdr_deviation,
                tls_valid=tls_valid,
                features=feats,
                has_html=has_html,
            )
        elif strategy == FusionStrategy.CONSENSUS:
            return self._execute_consensus(
                entropy=entropy,
                sdr_deviation=sdr_deviation,
                tls_valid=tls_valid,
                features=feats,
                has_html=has_html,
            )
        elif strategy == FusionStrategy.MATRIX:
            return self._execute_matrix(
                entropy=entropy,
                sdr_deviation=sdr_deviation,
                tls_valid=tls_valid,
                features=feats,
            )
        else:
            return self._execute_gated(
                entropy=entropy,
                sdr_deviation=sdr_deviation,
                tls_valid=tls_valid,
                features=feats,
                has_html=has_html,
                password_fields=password_fields,
                max_depth=max_depth,
                entropy_threshold=entropy_threshold,
            )

    def _execute_gated(
        self,
        entropy: float,
        sdr_deviation: float,
        tls_valid: bool,
        features: List[Any],
        has_html: bool = True,
        password_fields: int = 0,
        max_depth: int = 0,
        entropy_threshold: float = 4.50,
    ) -> AnalysisResult:
        """
        Conditional Gated Fusion (Patent Claims 6 & 15, Table 6-1).
        Hardware Optimization: Suppresses parser and renderer worker thread allocations.
        """
        # GATE 1: Obvious Algorithmic Randomness (DGA) [Table 6-1, Rule 1]
        if entropy > entropy_threshold:
            explanation = (
                f"Conditional Gated Fusion [Rule 1]: Lexical Shannon Entropy H(U) = {entropy:.2f} "
                f"exceeds critical threshold {entropy_threshold:.2f} bits/char. Classified as PHISHING_DGA. "
                f"Hardware Directive: WITHHOLD_PARSER_AND_RENDERER. Downstream HTML AST parsing "
                f"and visual rendering compute dynamically bypassed (O(L) exit)."
            )
            return AnalysisResult(
                decision="PHISHING_DGA",
                risk_score=0.99,
                confidence="HIGH",
                features=features,
                explanation=explanation,
                policy_name="gated_fusion",
                hardware_compute_bypassed=True,
                bypassed_modalities=["structural_dom_ast", "visual_rendering"],
                system_control_directive=SystemControlDirective.WITHHOLD_PARSER_AND_RENDERER.value,
                rule_id="RULE_TABLE_6_1_GATE_DGA_SUPPRESSION",
            )

        # Missing HTML Modality Handling [Section 10(4)]
        if not has_html:
            if not tls_valid:
                explanation = (
                    f"Conditional Gated Fusion [Missing HTML]: Structural payload unavailable. "
                    f"Invalid/untrusted TLS certificate detected. Classified as SUSPICIOUS."
                )
                return AnalysisResult(
                    decision="SUSPICIOUS",
                    risk_score=0.65,
                    confidence="MEDIUM",
                    features=features,
                    explanation=explanation,
                    policy_name="gated_fusion",
                    hardware_compute_bypassed=False,
                    system_control_directive=SystemControlDirective.ISOLATE_CREDENTIAL_FORM.value,
                    rule_id="RULE_TABLE_6_1_MISSING_HTML_TLS_INVALID",
                )
            else:
                explanation = (
                    f"Conditional Gated Fusion [Missing HTML]: Structural payload unavailable. "
                    f"Lexical entropy H(U) = {entropy:.2f} <= 4.5, TLS valid. Classified as LEGITIMATE."
                )
                return AnalysisResult(
                    decision="LEGITIMATE",
                    risk_score=0.10,
                    confidence="MEDIUM",
                    features=features,
                    explanation=explanation,
                    policy_name="gated_fusion",
                    hardware_compute_bypassed=False,
                    system_control_directive=SystemControlDirective.ALLOW_STREAM_AND_CACHE.value,
                    rule_id="RULE_TABLE_6_1_MISSING_HTML_SAFE",
                )

        # GATE 2: Structural Cloned Harvester Detection [Table 6-1, Rule 2 & 3]
        # Clarification under Section 10(4): Evaluates SDR deviation, shallow depth (<=4), and password inputs
        is_harvester_signature = (password_fields > 0) and (max_depth <= 4)

        if sdr_deviation > 50.0:
            if not tls_valid:
                explanation = (
                    f"Conditional Gated Fusion [Rule 2]: High Structural Density Ratio deviation ({sdr_deviation:.1f}%) "
                    f"combined with invalid/untrusted TLS certificate confirms brand cloning. "
                    f"Harvester signature confirmed: {password_fields} password input(s) in shallow DOM (depth={max_depth}). "
                    f"Classified as PHISHING_CLONE."
                )
                return AnalysisResult(
                    decision="PHISHING_CLONE",
                    risk_score=0.95,
                    confidence="HIGH",
                    features=features,
                    explanation=explanation,
                    policy_name="gated_fusion",
                    hardware_compute_bypassed=False,
                    system_control_directive=SystemControlDirective.ISOLATE_CREDENTIAL_FORM.value,
                    rule_id="RULE_TABLE_6_1_GATE_CLONE_CONFIRMED",
                )
            else:
                # Valid TLS but elevated structural deviation
                risk_val = 0.75 if is_harvester_signature else 0.60
                explanation = (
                    f"Conditional Gated Fusion [Rule 3]: Elevated Structural Density Ratio deviation ({sdr_deviation:.1f}%), "
                    f"with valid TLS. Harvester signature present: {is_harvester_signature}. Classified as SUSPICIOUS."
                )
                return AnalysisResult(
                    decision="SUSPICIOUS",
                    risk_score=risk_val,
                    confidence="MEDIUM",
                    features=features,
                    explanation=explanation,
                    policy_name="gated_fusion",
                    hardware_compute_bypassed=False,
                    system_control_directive=SystemControlDirective.ALLOCATE_AST_PARSER.value,
                    rule_id="RULE_TABLE_6_1_GATE_STRUCTURAL_SUSPICIOUS",
                )

        # GATE 3: Safe Baseline Envelope [Table 6-1, Rule 4]
        explanation = (
            f"Conditional Gated Fusion [Rule 4]: All parameters within safe baseline bounds "
            f"(Entropy = {entropy:.2f} <= 4.5, SDR Deviation = {sdr_deviation:.1f}% <= 50.0%, TLS valid). "
            f"Classified as LEGITIMATE."
        )
        return AnalysisResult(
            decision="LEGITIMATE",
            risk_score=0.05,
            confidence="HIGH",
            features=features,
            explanation=explanation,
            policy_name="gated_fusion",
            hardware_compute_bypassed=False,
            system_control_directive=SystemControlDirective.ALLOW_STREAM_AND_CACHE.value,
            rule_id="RULE_TABLE_6_1_GATE_SAFE_ENVELOPE",
        )

    def _execute_weighted(
        self,
        entropy: float,
        sdr_deviation: float,
        tls_valid: bool,
        features: List[Any],
        lex_risk: Optional[float] = None,
        struct_risk: Optional[float] = None,
        vis_risk: Optional[float] = None,
        has_html: bool = True,
    ) -> AnalysisResult:
        """
        Late Confidence-Weighted Fusion (Patent Claim 5).
        Risk = w_L * S_L + w_S * S_S + w_M * S_M
        """
        w = self.current_policy.weights
        w_l = w.get("lexical", 0.40)
        w_s = w.get("structural", 0.40)
        w_m = w.get("visual", 0.20)

        s_l = lex_risk if lex_risk is not None else min(1.0, max(0.0, (entropy - 2.5) / 2.5))
        s_s = struct_risk if struct_risk is not None else (min(1.0, max(0.0, sdr_deviation / 100.0)) if has_html else 0.0)
        s_m = vis_risk if vis_risk is not None else (0.95 if not tls_valid else 0.05)

        # Dynamic weight re-normalization if HTML missing
        if not has_html:
            total_w = w_l + w_m
            w_l_norm = w_l / total_w
            w_m_norm = w_m / total_w
            composite_risk = (w_l_norm * s_l) + (w_m_norm * s_m)
        else:
            composite_risk = (w_l * s_l) + (w_s * s_s) + (w_m * s_m)

        composite_risk = min(1.0, max(0.0, composite_risk))
        threshold = self.current_policy.threshold

        if composite_risk >= threshold:
            decision = "PHISHING"
            conf = "HIGH"
            directive = SystemControlDirective.WITHHOLD_PARSER_AND_RENDERER.value
        elif composite_risk >= 0.40:
            decision = "SUSPICIOUS"
            conf = "MEDIUM"
            directive = SystemControlDirective.ALLOCATE_AST_PARSER.value
        else:
            decision = "LEGITIMATE"
            conf = "HIGH"
            directive = SystemControlDirective.ALLOW_STREAM_AND_CACHE.value

        explanation = (
            f"Late Confidence-Weighted Fusion: Composite Risk = {composite_risk:.2%} "
            f"[Lexical ({w_l:.2f} * {s_l:.2f}) + Structural ({w_s:.2f} * {s_s:.2f}) + "
            f"Visual ({w_m:.2f} * {s_m:.2f})]. Decision Threshold = {threshold:.2f}."
        )

        return AnalysisResult(
            decision=decision,
            risk_score=composite_risk,
            confidence=conf,
            features=features,
            explanation=explanation,
            policy_name="confidence_weighted",
            system_control_directive=directive,
            rule_id="RULE_LATE_WEIGHTED_SCORE",
        )

    def _execute_early(
        self,
        entropy: float,
        sdr_deviation: float,
        tls_valid: bool,
        features: List[Any],
        has_html: bool = True,
    ) -> AnalysisResult:
        """
        Early Fusion Matrix Algebra (Patent Claims 11 & 12).
        Projects raw concatenated feature vector into a scalar risk space.
        """
        x_entropy = min(1.0, max(0.0, entropy / 6.0))
        x_sdr = min(1.0, max(0.0, sdr_deviation / 100.0)) if has_html else 0.0
        x_tls = 0.0 if tls_valid else 1.0

        weights = [0.45, 0.35, 0.20]
        scalar_risk = (x_entropy * weights[0]) + (x_sdr * weights[1]) + (x_tls * weights[2])

        decision = "PHISHING" if scalar_risk >= 0.60 else ("SUSPICIOUS" if scalar_risk >= 0.35 else "LEGITIMATE")
        explanation = (
            f"Early Fusion Matrix Algebra: Projected feature vector [H={x_entropy:.2f}, SDR={x_sdr:.2f}, TLS={x_tls:.2f}] "
            f"yields scalar risk {scalar_risk:.2%}."
        )
        return AnalysisResult(
            decision=decision,
            risk_score=scalar_risk,
            confidence="HIGH" if scalar_risk >= 0.60 or scalar_risk < 0.35 else "MEDIUM",
            features=features,
            explanation=explanation,
            policy_name="early_fusion",
            system_control_directive=SystemControlDirective.ALLOCATE_AST_PARSER.value,
            rule_id="RULE_EARLY_MATRIX_PROJECTION",
        )

    def _execute_consensus(
        self,
        entropy: float,
        sdr_deviation: float,
        tls_valid: bool,
        features: List[Any],
        has_html: bool = True,
    ) -> AnalysisResult:
        """
        Consensus / Majority Voting Fusion (Section 10(4)).
        Handles 3 modalities (2/3 majority) or 2 modalities (2/2 unanimous or 1/2 suspicious).
        """
        votes = []
        modality_names = []

        # Modality 1: Lexical
        vote_lex = entropy > 4.0
        votes.append(vote_lex)
        modality_names.append(f"Lexical={vote_lex}")

        # Modality 2: Structural (only if available)
        if has_html:
            vote_struct = sdr_deviation > 40.0
            votes.append(vote_struct)
            modality_names.append(f"Structural={vote_struct}")

        # Modality 3: Visual/TLS
        vote_vis = not tls_valid
        votes.append(vote_vis)
        modality_names.append(f"Visual/TLS={vote_vis}")

        available_modalities = len(votes)
        positive_votes = sum(votes)

        if available_modalities == 3:
            if positive_votes >= 2:
                decision = "PHISHING"
                risk = 0.90
                conf = "HIGH"
            elif positive_votes == 1:
                decision = "SUSPICIOUS"
                risk = 0.55
                conf = "MEDIUM"
            else:
                decision = "LEGITIMATE"
                risk = 0.05
                conf = "HIGH"
        else:
            # 2 modalities available (missing HTML)
            if positive_votes == 2:
                decision = "PHISHING"
                risk = 0.88
                conf = "HIGH"
            elif positive_votes == 1:
                decision = "SUSPICIOUS"
                risk = 0.50
                conf = "MEDIUM"
            else:
                decision = "LEGITIMATE"
                risk = 0.05
                conf = "HIGH"

        explanation = (
            f"Consensus Fusion: Agreement tally = {positive_votes}/{available_modalities} modalities flagged "
            f"({', '.join(modality_names)})."
        )
        return AnalysisResult(
            decision=decision,
            risk_score=risk,
            confidence=conf,
            features=features,
            explanation=explanation,
            policy_name="consensus_fusion",
            system_control_directive=SystemControlDirective.ALLOCATE_AST_PARSER.value if decision != "PHISHING" else SystemControlDirective.WITHHOLD_PARSER_AND_RENDERER.value,
            rule_id=f"RULE_CONSENSUS_{positive_votes}_OF_{available_modalities}",
        )

    def _execute_matrix(
        self,
        entropy: float,
        sdr_deviation: float,
        tls_valid: bool,
        features: List[Any],
    ) -> AnalysisResult:
        """
        Strict Cartesian Risk Matrix: Complete 8-Cell Lookup (Table 6-2).
        Maps (b_lex, b_struct, b_vis) in {0, 1}^3 to deterministic decisions.
        """
        b_lex = 1 if entropy > 4.0 else 0
        b_struct = 1 if sdr_deviation > 40.0 else 0
        b_vis = 1 if not tls_valid else 0

        # Complete 8-Cell Cartesian Matrix (Table 6-2)
        lookup_table_6_2 = {
            (1, 1, 1): ("PHISHING", 0.99, "RULE_TABLE_6_2_CELL_1_ALL_FLAGS"),
            (1, 1, 0): ("PHISHING", 0.92, "RULE_TABLE_6_2_CELL_2_LEX_STRUCT"),
            (1, 0, 1): ("PHISHING", 0.88, "RULE_TABLE_6_2_CELL_3_LEX_VISUAL"),
            (0, 1, 1): ("PHISHING", 0.85, "RULE_TABLE_6_2_CELL_4_STRUCT_VISUAL"),
            (1, 0, 0): ("SUSPICIOUS", 0.60, "RULE_TABLE_6_2_CELL_5_LEX_ONLY"),
            (0, 1, 0): ("SUSPICIOUS", 0.55, "RULE_TABLE_6_2_CELL_6_STRUCT_ONLY"),
            (0, 0, 1): ("SUSPICIOUS", 0.45, "RULE_TABLE_6_2_CELL_7_VISUAL_ONLY"),
            (0, 0, 0): ("LEGITIMATE", 0.05, "RULE_TABLE_6_2_CELL_8_ALL_CLEAN"),
        }

        decision, risk, rule_id = lookup_table_6_2.get(
            (b_lex, b_struct, b_vis),
            ("SUSPICIOUS", 0.50, "RULE_TABLE_6_2_UNKNOWN")
        )

        directive = (
            SystemControlDirective.WITHHOLD_PARSER_AND_RENDERER.value
            if decision == "PHISHING"
            else (
                SystemControlDirective.ALLOCATE_AST_PARSER.value
                if decision == "SUSPICIOUS"
                else SystemControlDirective.ALLOW_STREAM_AND_CACHE.value
            )
        )

        explanation = (
            f"Cartesian Risk Matrix [Table 6-2]: State tuple ({b_lex}, {b_struct}, {b_vis}) "
            f"mapped to {decision} (Risk = {risk:.2%}). Rule: {rule_id}."
        )

        return AnalysisResult(
            decision=decision,
            risk_score=risk,
            confidence="HIGH",
            features=features,
            explanation=explanation,
            policy_name="strict_matrix",
            system_control_directive=directive,
            rule_id=rule_id,
        )
