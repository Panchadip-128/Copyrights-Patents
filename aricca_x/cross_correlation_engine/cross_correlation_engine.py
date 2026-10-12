"""
Cross-Correlation Engine & Six-Phase Deterministic Pipeline

Aggregates outputs from the four independent modules:
  - Module A: Venue Intelligence (s_venue)
  - Module B: Researcher Auditing (s_researcher)
  - Module C: Peer-Review Forensics (s_review)
  - Module D: Grant Compliance (s_grant)

Executes a six-phase strictly serializable pipeline:
  Phase 1 (Component Scoring): Evaluates available module signals using Adaptive Decay Weighting (ADW)
  Phase 2 (Heuristic Evaluation): Evaluates domain Boolean heuristics across all modules
  Phase 3 (Credibility & Anomaly Aggregation): Combines scores and applies Cross-Signal Anomaly Detection (CSAD) amplification
  Phase 4 (Risk Classification): Maps risk to 4-tier classification (low, medium, high, critical)
  Phase 5 (Recommendation Generation): Produces deterministic remediation recommendations
  Phase 6 (Flag Generation & Audit Hash Chaining): Assembles complete audit trail with tamper-evident hash chain

Every intermediate state is strictly serializable, canonicalized, and bound to a
SHA-256 hash chain so that decisions can be audited offline.

Copyright (c) 2026. All rights reserved. Patent Pending.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple

from ..deterministic_core import (
    DEFAULT_REGISTRY,
    SUBSTRATE,
    SURFACE,
    ADWResult,
    AuditChain,
    CSADResult,
    RuleRegistry,
    adaptive_decay_weighting,
    clamp01,
    cross_signal_anomaly_detection,
    digest,
)
from ..grant_compliance.grant_compliance import GrantComplianceResult
from ..peer_review_forensics.peer_review_forensics import PeerReviewAuditResult
from ..researcher_auditor.researcher_auditor import ResearcherAuditResult
from ..venue_intelligence.venue_intelligence import VenueIntelligenceResult


@dataclass
class Phase1State:
    signals: Dict[str, Optional[float]]
    adw_result: Dict[str, Any]
    observed_dimensions: Tuple[str, ...]
    unknown_dimensions: Tuple[str, ...]


@dataclass
class Phase2State:
    triggered_rules: List[Dict[str, Any]]
    total_heuristic_penalty: float


@dataclass
class Phase3State:
    base_credibility: float
    base_risk: float
    csad_result: Dict[str, Any]
    amplified_risk: float
    epistemic_interval: Tuple[float, float]
    interval_width: float


@dataclass
class Phase4State:
    risk_score: float
    risk_level: str   # "low" | "medium" | "high" | "critical"
    confidence: float


@dataclass
class Phase5State:
    recommendations: List[str]


@dataclass
class Phase6State:
    flags: List[str]
    audit_chain_digest: str
    final_record_hash: str


@dataclass
class CompositeRiskProfile:
    target_id: str
    target_type: str            # "venue" | "researcher" | "publication" | "composite"
    overall_credibility_score: float
    total_risk_score: float
    risk_level: str             # "low" | "medium" | "high" | "critical"
    confidence: float
    epistemic_interval: Tuple[float, float]
    interval_width: float
    insufficient_evidence: bool
    module_signals: Dict[str, Optional[float]]
    flags: List[str]
    recommendations: List[str]
    csad_amplification_applied: bool
    audit_chain: Dict[str, Any]
    mathematical_justification: List[str] = field(default_factory=list)


class CrossCorrelationEngine:
    """Deterministic multi-signal correlation pipeline."""

    def __init__(self, rules: RuleRegistry = DEFAULT_REGISTRY):
        self.rules = rules

    def run_pipeline(
        self,
        target_id: str,
        target_type: str = "composite",
        venue_result: Optional[VenueIntelligenceResult] = None,
        researcher_result: Optional[ResearcherAuditResult] = None,
        peer_review_result: Optional[PeerReviewAuditResult] = None,
        grant_result: Optional[GrantComplianceResult] = None,
    ) -> CompositeRiskProfile:
        """Run the six-phase deterministic assessment pipeline."""
        input_digest = digest({
            "target_id": target_id,
            "target_type": target_type,
            "venue": venue_result.credibility_signal if venue_result else None,
            "researcher": researcher_result.credibility_signal if researcher_result else None,
            "peer_review": peer_review_result.credibility_signal if peer_review_result else None,
            "grant": grant_result.credibility_signal if grant_result else None,
        })
        audit = AuditChain(pipeline_id=target_id, input_digest=input_digest, ruleset_digest=self.rules.digest())

        # =====================================================================
        # PHASE 1: Component Scoring (ADW)
        # =====================================================================
        signals: Dict[str, Optional[float]] = {
            "venue": venue_result.credibility_signal if venue_result else None,
            "researcher": researcher_result.credibility_signal if researcher_result else None,
            "peer_review": peer_review_result.credibility_signal if peer_review_result else None,
            "grant": grant_result.credibility_signal if grant_result else None,
        }

        base_weights = {
            "venue": self.rules.param("ADW-MODULE-WEIGHTS", "venue"),
            "researcher": self.rules.param("ADW-MODULE-WEIGHTS", "researcher"),
            "peer_review": self.rules.param("ADW-MODULE-WEIGHTS", "peer_review"),
            "grant": self.rules.param("ADW-MODULE-WEIGHTS", "grant"),
        }

        adw = adaptive_decay_weighting(base_weights, signals)
        p1_state = Phase1State(
            signals=signals,
            adw_result={
                "effective_weights": adw.effective_weights,
                "score": adw.score,
                "lower": adw.lower_bound,
                "upper": adw.upper_bound,
                "width": adw.interval_width,
            },
            observed_dimensions=adw.observed,
            unknown_dimensions=adw.unknown,
        )
        audit.append("Phase_1_ComponentScoring", p1_state)

        # =====================================================================
        # PHASE 2: Boolean Heuristic Evaluation
        # =====================================================================
        triggered_heuristics: List[Dict[str, Any]] = []
        heuristic_penalty = 0.0

        p_crit = self.rules.param("HEURISTIC-PENALTIES", "critical")
        p_high = self.rules.param("HEURISTIC-PENALTIES", "high")
        p_med = self.rules.param("HEURISTIC-PENALTIES", "medium")

        if venue_result:
            if venue_result.url_audit.is_spoofed:
                triggered_heuristics.append({"rule": "URL_SPOOF", "severity": "critical", "penalty": p_crit})
                heuristic_penalty += p_crit
            if venue_result.temporal_integrity.predatory_urgency:
                triggered_heuristics.append({"rule": "PREDATORY_URGENCY", "severity": "high", "penalty": p_high})
                heuristic_penalty += p_high
            if venue_result.tfet_drift and venue_result.tfet_drift.hijack_suspected:
                triggered_heuristics.append({"rule": "HIJACK_SUSPECTED", "severity": "critical", "penalty": p_crit})
                heuristic_penalty += p_crit

        if researcher_result:
            if researcher_result.inflation_alert:
                triggered_heuristics.append({"rule": "CIR_INFLATION_ALERT", "severity": "high", "penalty": p_high})
                heuristic_penalty += p_high
            if researcher_result.loops:
                triggered_heuristics.append({"rule": "CITATION_LOOPS_DETECTED", "severity": "high", "penalty": p_high})
                heuristic_penalty += p_high

        if peer_review_result:
            if peer_review_result.sentiment_alignment.is_misaligned:
                triggered_heuristics.append({"rule": "REVIEW_MISALIGNMENT", "severity": "high", "penalty": p_high})
                heuristic_penalty += p_high
            if peer_review_result.fingerprint.is_unnaturally_uniform:
                triggered_heuristics.append({"rule": "SYNTHETIC_REVIEW_UNIFORMITY", "severity": "medium", "penalty": p_med})
                heuristic_penalty += p_med

        if grant_result and not grant_result.overall_compliant:
            triggered_heuristics.append({"rule": "GRANT_MANDATE_VIOLATION", "severity": "high", "penalty": p_high})
            heuristic_penalty += p_high

        p2_state = Phase2State(
            triggered_rules=triggered_heuristics,
            total_heuristic_penalty=heuristic_penalty,
        )
        audit.append("Phase_2_HeuristicEvaluation", p2_state)

        # =====================================================================
        # PHASE 3: Credibility & Anomaly Aggregation (ADW + CSAD)
        # =====================================================================
        base_cred = adw.score if adw.score is not None else 0.5
        raw_risk = clamp01(1.0 - base_cred + heuristic_penalty)

        # Layer assignment: venue/peer_review are SURFACE, researcher/grant are SUBSTRATE
        layers = {
            "venue": SURFACE,
            "peer_review": SURFACE,
            "researcher": SUBSTRATE,
            "grant": SUBSTRATE,
        }

        tau = self.rules.param("CSAD-CROSS-MODULE", "tau")
        a_facade = self.rules.param("CSAD-CROSS-MODULE", "alpha_facade")
        a_neutral = self.rules.param("CSAD-CROSS-MODULE", "alpha_neutral")

        csad = cross_signal_anomaly_detection(
            signals=signals,
            layers=layers,
            risk=raw_risk,
            tau=tau,
            alpha_facade=a_facade,
            alpha_neutral=a_neutral,
        )

        final_risk = csad.risk_out
        final_cred = clamp01(1.0 - final_risk)

        p3_state = Phase3State(
            base_credibility=base_cred,
            base_risk=raw_risk,
            csad_result={
                "triggered": csad.triggered,
                "amplification_factor": csad.amplification_factor,
                "max_divergence": csad.max_divergence,
                "pair": f"{csad.selected_pair.signal_a} vs {csad.selected_pair.signal_b}" if csad.selected_pair else None,
            },
            amplified_risk=final_risk,
            epistemic_interval=(adw.lower_bound, adw.upper_bound),
            interval_width=adw.interval_width,
        )
        audit.append("Phase_3_CredibilityAnomalyAggregation", p3_state)

        # =====================================================================
        # PHASE 4: Risk Classification
        # =====================================================================
        t_med = self.rules.param("RISK-TIERS", "t_medium")
        t_hi = self.rules.param("RISK-TIERS", "t_high")
        t_crit = self.rules.param("RISK-TIERS", "t_critical")

        if final_risk >= t_crit:
            risk_tier = "critical"
        elif final_risk >= t_hi:
            risk_tier = "high"
        elif final_risk >= t_med:
            risk_tier = "medium"
        else:
            risk_tier = "low"

        # Confidence is derived from observed evidence completeness
        confidence = clamp01(1.0 - adw.interval_width)

        p4_state = Phase4State(
            risk_score=final_risk,
            risk_level=risk_tier,
            confidence=confidence,
        )
        audit.append("Phase_4_RiskClassification", p4_state)

        # =====================================================================
        # PHASE 5: Rule-Based Recommendation Generation
        # =====================================================================
        recommendations: List[str] = []
        if venue_result and venue_result.url_audit.is_spoofed:
            recommendations.append(
                f"INTERDICT VENUE: Domain '{venue_result.url_audit.candidate_domain}' is a fraudulent lookalike of {venue_result.url_audit.organization}."
            )
        if venue_result and venue_result.temporal_integrity.predatory_urgency:
            recommendations.append(
                "VERIFY TIMELINE: CFP interval < 30 days is characteristic of predatory deadline cycling."
            )
        if researcher_result and researcher_result.inflation_alert:
            recommendations.append(
                f"AUDIT CITATION INDEPENDENCE: Citation Independence Ratio ({researcher_result.citation_independence_ratio:.2f}) is below 0.30."
            )
        if researcher_result and researcher_result.loops:
            recommendations.append(
                f"DISCLOSE RECIPROCAL COLLABORATIONS: {len(researcher_result.loops)} citation loop(s) detected with {len(researcher_result.loop_members)} authors."
            )
        if peer_review_result and peer_review_result.sentiment_alignment.is_misaligned:
            recommendations.append(
                "FLAG PEER REVIEW: Reviewer sentiment polarity conflicts with nominal recommendation."
            )
        if grant_result and not grant_result.overall_compliant:
            for funder, f_res in grant_result.funder_results.items():
                if not f_res.is_fully_compliant:
                    recommendations.extend(f_res.remediations)

        if not recommendations:
            recommendations.append("ASSESSMENT CLEAR: No high-risk integrity anomalies detected.")

        p5_state = Phase5State(recommendations=recommendations)
        audit.append("Phase_5_RecommendationGeneration", p5_state)

        # =====================================================================
        # PHASE 6: Flag Generation & Tamper-Evident Hash Chaining
        # =====================================================================
        all_flags: List[str] = []
        if venue_result:
            all_flags.extend(venue_result.flags)
        if researcher_result:
            all_flags.extend(researcher_result.flags)
        if peer_review_result:
            all_flags.extend(peer_review_result.flags)
        if grant_result:
            all_flags.extend(grant_result.flags)
        if csad.triggered:
            all_flags.append("CSAD_CROSS_SIGNAL_DIVERGENCE_AMPLIFIED")

        width_threshold = self.rules.param("ADW-MODULE-WEIGHTS", "insufficient_evidence_width")
        insufficient_evidence = adw.interval_width > width_threshold
        if insufficient_evidence:
            all_flags.append("ADW_INSUFFICIENT_EVIDENCE_INTERVAL_WIDE")

        all_flags = sorted(set(all_flags))

        p6_state = Phase6State(
            flags=all_flags,
            audit_chain_digest=audit.genesis_hash,
            final_record_hash=audit.head,
        )
        audit.append("Phase_6_FlagGenerationAndAuditSealing", p6_state)

        # Build comprehensive mathematical justification
        math_justification = [
            f"ARICCA-X 6-Phase Deterministic Pipeline Assessment for '{target_id}' ({target_type})",
            f"Phase 1: ADW observed={list(adw.observed)}, unknown={list(adw.unknown)}. Base credibility C = {base_cred:.4f}",
            f"         Epistemic evidence interval = [{adw.lower_bound:.4f}, {adw.upper_bound:.4f}] (width {adw.interval_width:.4f})",
            f"Phase 2: Triggered heuristics={len(triggered_heuristics)} (penalty = {heuristic_penalty:.4f})",
            f"Phase 3: Base risk = {raw_risk:.4f}",
            *csad.justification,
            f"Phase 4: Final composite risk = {final_risk:.4f} -> TIER: {risk_tier.upper()} (Confidence = {confidence:.4f})",
            f"Phase 5: Generated {len(recommendations)} actionable recommendation(s)",
            f"Phase 6: Assembled {len(all_flags)} verified flags. Tamper-evident final hash: {audit.head[:16]}...",
        ]

        return CompositeRiskProfile(
            target_id=target_id,
            target_type=target_type,
            overall_credibility_score=final_cred,
            total_risk_score=final_risk,
            risk_level=risk_tier,
            confidence=confidence,
            epistemic_interval=(adw.lower_bound, adw.upper_bound),
            interval_width=adw.interval_width,
            insufficient_evidence=insufficient_evidence,
            module_signals=signals,
            flags=all_flags,
            recommendations=recommendations,
            csad_amplification_applied=csad.triggered,
            audit_chain=audit.to_dict(),
            mathematical_justification=math_justification,
        )
