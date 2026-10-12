"""
Inference API
Module: x_mpfd_e_plus.inference_api.api

Production inference API wrapping the deterministic multimodal detection pipeline.
Patent Claims 1, 10, and 14.

Copyright © 2026 Panchadip B & Somyajeet A. All Rights Reserved.
"""

from typing import Dict, Any, List, Optional
from ..decision_risk_core.detector import PhishingDetector
from ..report_generator import ReportGenerator


class InferenceAPI:
    """
    High-level, deterministic inference API.
    """
    def __init__(self, default_policy: str = "gated"):
        self.detector = PhishingDetector(fusion_policy=default_policy)
        self.report_gen = ReportGenerator()

    def predict(
        self,
        url: str,
        html: Optional[str] = None,
        screenshot: Optional[bytes] = None,
        tls_valid: bool = True,
        is_self_signed: bool = False,
    ) -> Dict[str, Any]:
        """Runs deterministic analysis and returns structured dictionary."""
        result = self.detector.analyze_url(
            url=url,
            html=html,
            screenshot=screenshot,
            tls_valid=tls_valid,
            is_self_signed=is_self_signed,
        )
        return {
            "url": url,
            "decision": result.decision,
            "risk_score": result.risk_score,
            "confidence": result.confidence,
            "policy": result.policy_name,
            "hardware_bypassed": result.hardware_compute_bypassed,
            "explanation": result.explanation,
            "sha256_audit_hash": result.sha256_audit_hash,
        }

    def batch_predict(self, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Batch evaluates multiple inputs deterministically."""
        return [
            self.predict(
                url=item["url"],
                html=item.get("html"),
                screenshot=item.get("screenshot"),
                tls_valid=item.get("tls_valid", True),
                is_self_signed=item.get("is_self_signed", False),
            )
            for item in items
        ]
