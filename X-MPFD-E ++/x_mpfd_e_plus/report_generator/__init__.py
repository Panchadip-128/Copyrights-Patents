"""
Report Generator Module
Module: x_mpfd_e_plus.report_generator

Generates text, canonical JSON (Patent Claim 14), and HTML audit reports.
Copyright © 2026 Panchadip B & Somyajeet A. All Rights Reserved.
"""

from typing import Any, Dict
import json
from ..fusion_policy_engine.fusion_engine import AnalysisResult


class ReportGenerator:
    """
    Deterministic Report Generator.
    Patent Claim 14: Encapsulates entirety of deterministic evidence chain in canonical schema.
    """
    def generate_text_report(self, result: AnalysisResult) -> str:
        lines = [
            "=" * 70,
            "X-MPFD-E++ DETERMINISTIC MULTIMODAL AUDIT REPORT",
            "=" * 70,
            f"DECISION:                   {result.decision}",
            f"COMPOSITE RISK SCORE:       {result.risk_score:.2%}",
            f"CONFIDENCE LEVEL:           {result.confidence}",
            f"ACTIVE FUSION POLICY:       {result.policy_name}",
            f"HARDWARE COMPUTE BYPASSED:  {result.hardware_compute_bypassed}",
            f"SHA-256 AUDIT HASH:         {result.sha256_audit_hash}",
            "-" * 70,
            "MATHEMATICAL DECISION RATIONALE:",
            result.explanation,
            "-" * 70,
            "CRYPTOGRAPHIC FEATURE PROVENANCE LINEAGE:",
        ]
        for f in result.features:
            fname = getattr(f, "name", "Feature")
            fval = getattr(f, "value", "N/A")
            fprov = getattr(f, "provenance", None)
            if fprov:
                lines.append(
                    f"  • {fname}: {fval} [Modality: {fprov.source_modality}, "
                    f"Method: {fprov.extraction_method}, SHA-256: {fprov.sha256_hash[:16]}...]"
                )
            else:
                lines.append(f"  • {fname}: {fval}")
        lines.append("=" * 70)
        return "\n".join(lines)

    def generate_json_report(self, result: AnalysisResult) -> str:
        """Generates canonical JSON schema adhering to Patent Claim 14."""
        schema_dict = {
            "schema_version": "1.0.0-patent-claim-14",
            "decision": result.decision,
            "risk_score": round(result.risk_score, 4),
            "confidence": result.confidence,
            "active_policy": result.policy_name,
            "hardware_optimization": {
                "compute_bypassed": result.hardware_compute_bypassed,
                "bypassed_modalities": result.bypassed_modalities,
                "system_control_directive": getattr(result, "system_control_directive", "ALLOW_STREAM_AND_CACHE"),
                "rule_id": getattr(result, "rule_id", "RULE_DEFAULT"),
            },
            "explanation": result.explanation,
            "sha256_audit_hash": result.sha256_audit_hash,
            "feature_provenance_registry": [
                f.to_dict() if hasattr(f, "to_dict") else {"name": getattr(f, "name", str(f))}
                for f in result.features
            ],
            "determinism_guarantee": {
                "llm_inference_used": False,
                "probabilistic_ml_used": False,
                "deterministic_closed_form": True,
            },
        }
        return json.dumps(schema_dict, indent=2, sort_keys=True)

    def generate_html_report(self, result: AnalysisResult) -> str:
        color = "#10b981" if result.decision == "LEGITIMATE" else ("#ef4444" if "PHISHING" in result.decision else "#f59e0b")
        return f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>X-MPFD-E++ Audit Report</title>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #0f172a; color: #f8fafc; padding: 30px; }}
    .card {{ background: #1e293b; border-radius: 12px; padding: 24px; max-width: 800px; margin: 0 auto; border: 1px solid #334155; }}
    .badge {{ display: inline-block; padding: 6px 12px; border-radius: 6px; font-weight: bold; background: {color}; color: #ffffff; }}
    h1 {{ margin-top: 0; font-size: 22px; }}
    .hash {{ font-family: monospace; font-size: 12px; color: #94a3b8; background: #090d16; padding: 8px; border-radius: 6px; word-break: break-all; }}
  </style>
</head>
<body>
  <div class="card">
    <h1>X-MPFD-E++ Deterministic Multimodal Audit Report</h1>
    <p><span class="badge">{result.decision}</span> <strong>Risk Score: {result.risk_score:.2%}</strong> (Confidence: {result.confidence})</p>
    <p><strong>Hardware Compute Bypassed:</strong> {result.hardware_compute_bypassed}</p>
    <p><strong>Rationale:</strong> {result.explanation}</p>
    <div class="hash">SHA-256 Audit Hash: {result.sha256_audit_hash}</div>
  </div>
</body>
</html>"""
