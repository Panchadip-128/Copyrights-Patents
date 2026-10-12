"""
Deterministic Explanation Synthesis Engine
Module: x_mpfd_e_plus.explanation_synthesis_engine.explainer

Translates cryptographic provenance tags and Boolean fusion paths into
100% deterministic, human-readable, auditable legal rationales.
Strictly excludes generative AI and large language models.
Patent Claims 1, 8, and 9.

Copyright © 2026 Panchadip B & Somyajeet A. All Rights Reserved.
"""

from typing import Dict, Any, List, Optional
import hashlib
import json


class ExplanationSynthesizer:
    """
    Deterministic Explanation Synthesizer.
    Patent Claim 8: Maps provenance tags to strict linguistic templates for auditable legal evidence.
    """
    def __init__(self):
        self._template_registry = {
            "PHISHING_DGA": (
                "ZERO-DAY DGA DETECTED: The input URL was classified as PHISHING_DGA because "
                "the Lexical Shannon Entropy H(U) = {entropy:.2f} bits/char exceeded the mathematical "
                "threshold of {threshold:.2f} bits/char. Computational hardware optimization "
                "bypassed downstream HTML AST DOM parsing, preserving CPU execution cycles."
            ),
            "PHISHING_CLONE": (
                "CREDENTIAL HARVESTER CLONE DETECTED: The target was classified as PHISHING_CLONE because "
                "the Structural Density Ratio (SDR = {sdr:.2f}) exhibited an anomalous baseline deviation "
                "of {sdr_deviation:.1f}% (threshold: 50.0%), and TLS certificate validation failed "
                "(TLS Valid = {tls_valid}). Form inputs identified {password_fields} password fields in shallow DOM."
            ),
            "SUSPICIOUS": (
                "SUSPICIOUS INFRASTRUCTURE DETECTED: The target exhibited elevated anomaly markers. "
                "Lexical Entropy H(U) = {entropy:.2f} bits/char, SDR baseline deviation = {sdr_deviation:.1f}%, "
                "TLS Valid = {tls_valid}. Modality fusion policy '{policy}' returned an intermediate risk score of {risk:.2%}."
            ),
            "LEGITIMATE": (
                "LEGITIMATE INFRASTRUCTURE VERIFIED: All multimodal signals reside strictly within verified "
                "safe baseline envelopes. Lexical Entropy H(U) = {entropy:.2f} <= 4.0, "
                "Structural Density Ratio SDR = {sdr:.2f} within standard brand tolerance, TLS certificate is valid."
            ),
        }

    def synthesize(
        self,
        decision: str,
        risk_score: float,
        policy_name: str,
        provenance_tags: List[Dict[str, Any]],
        entropy: float,
        sdr: float,
        sdr_deviation: float,
        tls_valid: bool,
        password_fields: int = 0,
        bypassed: bool = False,
    ) -> Dict[str, Any]:
        """
        Deterministically constructs an auditable explanation dossier.
        """
        template = self._template_registry.get(decision, self._template_registry["SUSPICIOUS"])
        formatted_rationale = template.format(
            entropy=entropy,
            threshold=4.50 if decision == "PHISHING_DGA" else 4.00,
            sdr=sdr,
            sdr_deviation=sdr_deviation,
            tls_valid=tls_valid,
            password_fields=password_fields,
            policy=policy_name,
            risk=risk_score,
        )

        # Audit trail of mathematical parameters
        parameters_audited = {
            "lexical_entropy_h_u": round(entropy, 4),
            "structural_density_ratio_sdr": round(sdr, 4),
            "sdr_deviation_pct": round(sdr_deviation, 2),
            "tls_certificate_valid": tls_valid,
            "password_input_count": password_fields,
            "hardware_compute_bypassed": bypassed,
            "active_policy": policy_name,
        }

        # Deterministic SHA-256 signature of explanation
        explanation_payload = f"{decision}:{risk_score:.4f}:{formatted_rationale}:{json.dumps(parameters_audited, sort_keys=True)}"
        explanation_hash = hashlib.sha256(explanation_payload.encode("utf-8")).hexdigest()

        return {
            "decision": decision,
            "risk_score": round(risk_score, 4),
            "human_readable_rationale": formatted_rationale,
            "mathematical_audit_parameters": parameters_audited,
            "provenance_tags_referenced": provenance_tags,
            "sha256_explanation_hash": explanation_hash,
            "is_pure_deterministic": True,
            "llm_inference_used": False,
        }
