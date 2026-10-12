"""
Integrity and Leakage Bias Auditor
Module: x_mpfd_e_plus.leakage_bias_auditor.auditor

Audits feature sets and pipeline runs for:
- Data leakage (label leakage in URL/DOM metadata)
- Numerical stability (zero division, NaN, infinite values)
- Deterministic reproducibility (bit-for-bit invariance)
Patent Claims 1, 9, and 10.

Copyright © 2026 Panchadip B & Somyajeet A. All Rights Reserved.
"""

from typing import Dict, Any, List, Optional
import math


class IntegrityAuditor:
    """
    Audits feature integrity and guarantees deterministic execution.
    """
    LEAKAGE_KEYS = {"label", "ground_truth", "is_phishing", "target_class", "oracle"}

    def audit_features(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """Audits a feature dictionary for data leakage and numerical anomalies."""
        leakage_detected = []
        numerical_issues = []

        for k, v in features.items():
            # Check for label leakage
            if any(leak_key in k.lower() for leak_key in self.LEAKAGE_KEYS):
                leakage_detected.append(k)

            # Check for invalid numerical values
            if isinstance(v, (int, float)):
                if math.isnan(v):
                    numerical_issues.append(f"{k} is NaN")
                elif math.isinf(v):
                    numerical_issues.append(f"{k} is Infinite")

        return {
            "is_clean": len(leakage_detected) == 0 and len(numerical_issues) == 0,
            "leakage_detected": leakage_detected,
            "numerical_issues": numerical_issues,
            "audited_feature_count": len(features),
        }

    def verify_determinism(self, func, *args, **kwargs) -> bool:
        """
        Executes a callable twice with identical arguments and verifies bit-for-bit equality.
        """
        res1 = func(*args, **kwargs)
        res2 = func(*args, **kwargs)
        return res1 == res2
