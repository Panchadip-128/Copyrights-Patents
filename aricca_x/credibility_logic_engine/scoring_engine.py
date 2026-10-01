"""
Scoring Engine - Calculates individual score components

Implements patent-pending Adaptive Decay Weighting and Cross-Signal
Anomaly Detection algorithms for credibility factor scoring.
Copyright (c) 2026. All rights reserved. Patent Pending.
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field


@dataclass
class CrossSignalAnomaly:
    """
    Represents a detected contradiction between two independent data signals.

    Patent-pending data structure for cross-signal anomaly detection.
    When independent signals about the same venue contradict each other
    (e.g., professional CFP but amateur website), that contradiction itself
    is a strong indicator of deceptive behavior.
    """
    signal_a_name: str
    signal_a_value: float
    signal_b_name: str
    signal_b_value: float
    divergence_magnitude: float   # abs(signal_a - signal_b)
    anomaly_type: str             # "quality_mismatch", "claim_contradiction", "temporal_inconsistency"
    risk_amplification_factor: float  # multiplied against base risk


@dataclass
class ScoreComponents:
    """Individual score components for credibility assessment"""
    cfp_risk_score: float = 0.5
    website_credibility_score: float = 0.5
    indexing_credibility_score: float = 0.5
    contact_legitimacy_score: float = 0.5
    organizational_structure_score: float = 0.5
    publication_history_score: float = 0.5
    total_risk_score: float = 0.5
    # Patent-pending: adaptive weight distribution and anomaly detection
    effective_weights: Dict[str, float] = field(default_factory=dict)
    data_completeness_ratio: float = 0.0
    cross_signal_anomalies: List[CrossSignalAnomaly] = field(default_factory=list)
    anomaly_risk_amplification: float = 0.0


class ScoringEngine:
    """
    Calculates individual score components using patent-pending algorithms.

    PATENT-PENDING INNOVATIONS:

    1. Adaptive Decay Weighting (ADW):
       Instead of fixed static weights, the engine dynamically redistributes
       weight among available data sources based on a completeness-decay function.
       When a data source is absent, its weight does NOT default to neutral —
       instead it is redistributed proportionally to remaining sources, and a
       "data-absence penalty" is applied to the confidence. This prevents the
       common prior-art failure mode where missing data causes false-neutral
       assessments.

    2. Cross-Signal Anomaly Detection (CSAD):
       After computing independent scores for each signal, the engine performs
       pairwise divergence analysis between signals that should correlate
       (e.g., CFP professionalism and website quality). Large divergences are
       flagged as "cross-signal anomalies" and produce a risk amplification
       factor that is applied to the final score. This detects sophisticated
       predatory venues that invest in one visible signal while neglecting
       correlated ones — a pattern invisible to single-signal analysis.

    All scoring formulas are explicitly defined and deterministic.
    """

    # Base weight allocation — these are starting points, NOT final weights.
    # Final weights are computed by the Adaptive Decay Weighting algorithm.
    BASE_WEIGHTS = {
        'cfp_risk': 0.25,
        'website_credibility': 0.20,
        'indexing_credibility': 0.20,
        'contact_legitimacy': 0.15,
        'organizational_structure': 0.10,
        'publication_history': 0.10
    }

    # Patent-pending: signal correlation matrix.
    # Pairs of signals that should move together. Large divergence = anomaly.
    CORRELATED_SIGNAL_PAIRS = [
        ('cfp_risk', 'website_credibility', 'quality_mismatch'),
        ('cfp_risk', 'contact_legitimacy', 'quality_mismatch'),
        ('website_credibility', 'indexing_credibility', 'claim_contradiction'),
        ('indexing_credibility', 'organizational_structure', 'claim_contradiction'),
        ('contact_legitimacy', 'organizational_structure', 'quality_mismatch'),
    ]

    # Divergence threshold above which a cross-signal anomaly is flagged
    ANOMALY_DIVERGENCE_THRESHOLD = 0.40

    # Data-absence penalty factor per missing source
    DATA_ABSENCE_PENALTY = 0.08

    def __init__(self):
        """Initialize the scoring engine"""
        pass

    def calculate_components(
        self,
        cfp_data: Optional[Dict] = None,
        website_data: Optional[Dict] = None,
        fingerprint_data: Optional[Dict] = None
    ) -> ScoreComponents:
        """
        Calculate all score components using Adaptive Decay Weighting.

        Patent-pending scoring algorithm with three phases:
          Phase 1: Score individual components
          Phase 2: Compute adaptive weights via data-completeness decay
          Phase 3: Detect cross-signal anomalies and amplify risk
        """
        # Phase 1: Calculate individual component scores
        cfp_risk = self._score_cfp_risk(cfp_data)
        website_cred = self._score_website_credibility(website_data)
        indexing_cred = self._score_indexing_credibility(fingerprint_data)
        contact_legit = self._score_contact_legitimacy(cfp_data, website_data)
        org_structure = self._score_organizational_structure(website_data, fingerprint_data)
        pub_history = self._score_publication_history(fingerprint_data)

        # Phase 2: Adaptive Decay Weighting (Patent-Pending)
        raw_scores = {
            'cfp_risk': cfp_risk,
            'website_credibility': website_cred,
            'indexing_credibility': indexing_cred,
            'contact_legitimacy': contact_legit,
            'organizational_structure': org_structure,
            'publication_history': pub_history
        }

        data_availability = {
            'cfp_risk': cfp_data is not None,
            'website_credibility': website_data is not None,
            'indexing_credibility': fingerprint_data is not None,
            'contact_legitimacy': cfp_data is not None or website_data is not None,
            'organizational_structure': website_data is not None or fingerprint_data is not None,
            'publication_history': fingerprint_data is not None
        }

        effective_weights = self._compute_adaptive_weights(data_availability)
        data_completeness = sum(1 for v in data_availability.values() if v) / len(data_availability)

        # Phase 3: Cross-Signal Anomaly Detection (Patent-Pending)
        # Convert to credibility-space for comparison (invert risk scores)
        credibility_scores = {
            'cfp_risk': 1.0 - cfp_risk,  # invert: low risk = high credibility
            'website_credibility': website_cred,
            'indexing_credibility': indexing_cred,
            'contact_legitimacy': contact_legit,
            'organizational_structure': org_structure,
            'publication_history': pub_history
        }
        anomalies = self._detect_cross_signal_anomalies(credibility_scores, data_availability)
        anomaly_amplification = sum(a.risk_amplification_factor for a in anomalies)

        # Calculate weighted total risk using adaptive weights
        total_risk = (
            cfp_risk * effective_weights.get('cfp_risk', 0) +
            (1.0 - website_cred) * effective_weights.get('website_credibility', 0) +
            (1.0 - indexing_cred) * effective_weights.get('indexing_credibility', 0) +
            (1.0 - contact_legit) * effective_weights.get('contact_legitimacy', 0) +
            (1.0 - org_structure) * effective_weights.get('organizational_structure', 0) +
            (1.0 - pub_history) * effective_weights.get('publication_history', 0)
        )

        # Apply data-absence penalty (missing data increases risk)
        absent_count = sum(1 for v in data_availability.values() if not v)
        absence_penalty = absent_count * self.DATA_ABSENCE_PENALTY
        total_risk += absence_penalty

        # Apply cross-signal anomaly amplification
        total_risk += anomaly_amplification

        return ScoreComponents(
            cfp_risk_score=cfp_risk,
            website_credibility_score=website_cred,
            indexing_credibility_score=indexing_cred,
            contact_legitimacy_score=contact_legit,
            organizational_structure_score=org_structure,
            publication_history_score=pub_history,
            total_risk_score=min(total_risk, 1.0),
            effective_weights=effective_weights,
            data_completeness_ratio=data_completeness,
            cross_signal_anomalies=anomalies,
            anomaly_risk_amplification=anomaly_amplification
        )

    def _compute_adaptive_weights(
        self,
        data_availability: Dict[str, bool]
    ) -> Dict[str, float]:
        """
        Patent-pending Adaptive Decay Weighting algorithm.

        When a data source is absent, its base weight is NOT lost — it is
        redistributed proportionally among the remaining available sources.
        This ensures the scoring surface utilizes 100% of the weight budget
        regardless of how many sources are available, while penalizing
        confidence separately.

        The redistribution follows the formula:
            effective_weight[i] = base_weight[i] + (base_weight[i] / sum_available) * sum_absent

        Where sum_absent is the total base weight of absent sources and
        sum_available is the total base weight of available sources.
        """
        available_weight = 0.0
        absent_weight = 0.0

        for component, is_available in data_availability.items():
            base_w = self.BASE_WEIGHTS.get(component, 0.0)
            if is_available:
                available_weight += base_w
            else:
                absent_weight += base_w

        effective_weights = {}
        for component, is_available in data_availability.items():
            base_w = self.BASE_WEIGHTS.get(component, 0.0)
            if is_available and available_weight > 0:
                # Proportionally absorb weight from absent sources
                effective_weights[component] = base_w + (base_w / available_weight) * absent_weight
            else:
                effective_weights[component] = 0.0  # Absent sources contribute zero

        return effective_weights

    def _detect_cross_signal_anomalies(
        self,
        credibility_scores: Dict[str, float],
        data_availability: Dict[str, bool]
    ) -> List[CrossSignalAnomaly]:
        """
        Patent-pending Cross-Signal Anomaly Detection algorithm.

        Performs pairwise divergence analysis between correlated signals.
        When two signals that should move together (e.g., CFP quality and
        website quality) show large divergence, this flags a cross-signal
        anomaly — a strong indicator of deceptive venue behavior.

        The risk amplification is proportional to the divergence magnitude:
            amplification = (divergence - threshold) * 0.3

        This ensures that only significant contradictions (above threshold)
        contribute to risk, and the contribution scales linearly.
        """
        anomalies = []

        for signal_a, signal_b, anomaly_type in self.CORRELATED_SIGNAL_PAIRS:
            # Only compare when both signals have real data
            if not data_availability.get(signal_a, False):
                continue
            if not data_availability.get(signal_b, False):
                continue

            score_a = credibility_scores.get(signal_a, 0.5)
            score_b = credibility_scores.get(signal_b, 0.5)
            divergence = abs(score_a - score_b)

            if divergence > self.ANOMALY_DIVERGENCE_THRESHOLD:
                amplification = (divergence - self.ANOMALY_DIVERGENCE_THRESHOLD) * 0.3
                anomalies.append(CrossSignalAnomaly(
                    signal_a_name=signal_a,
                    signal_a_value=score_a,
                    signal_b_name=signal_b,
                    signal_b_value=score_b,
                    divergence_magnitude=divergence,
                    anomaly_type=anomaly_type,
                    risk_amplification_factor=amplification
                ))

        return anomalies

    def _score_cfp_risk(self, cfp_data: Optional[Dict]) -> float:
        """Score CFP risk (0.0 = low risk, 1.0 = high risk)"""
        if not cfp_data:
            return 0.5  # Neutral when no data

        return cfp_data.get('overall_cfp_risk', 0.5)

    def _score_website_credibility(self, website_data: Optional[Dict]) -> float:
        """Score website credibility (0.0 = low, 1.0 = high)"""
        if not website_data:
            return 0.5  # Neutral when no data

        return website_data.get('credibility_score', 0.5)

    def _score_indexing_credibility(self, fingerprint_data: Optional[Dict]) -> float:
        """Score indexing claim credibility (0.0 = low, 1.0 = high)"""
        if not fingerprint_data:
            return 0.5

        indexing_data = fingerprint_data.get('indexing_analysis', {})
        return indexing_data.get('overall_credibility', 0.5)

    def _score_contact_legitimacy(
        self,
        cfp_data: Optional[Dict],
        website_data: Optional[Dict]
    ) -> float:
        """Score contact information legitimacy (0.0 = low, 1.0 = high)"""
        score = 0.5

        if cfp_data:
            score = max(score, cfp_data.get('contact_legitimacy_score', 0.5))

        if website_data:
            contact_score = website_data.get('contact_legitimacy', 0.5)
            score = (score + contact_score) / 2

        return score

    def _score_organizational_structure(
        self,
        website_data: Optional[Dict],
        fingerprint_data: Optional[Dict]
    ) -> float:
        """Score organizational structure (0.0 = weak, 1.0 = strong)"""
        score = 0.5

        if website_data:
            # Check for organizational indicators
            has_committee = website_data.get('has_committee_page', False)
            has_about = website_data.get('has_about_page', False)

            if has_committee:
                score += 0.2
            if has_about:
                score += 0.1

        if fingerprint_data:
            # Check for institutional affiliations
            affiliations = fingerprint_data.get('institutional_affiliations', [])
            if affiliations:
                score += min(len(affiliations) * 0.05, 0.2)

        return min(score, 1.0)

    def _score_publication_history(self, fingerprint_data: Optional[Dict]) -> float:
        """Score publication history (0.0 = no history, 1.0 = established)"""
        if not fingerprint_data:
            return 0.5

        # In a real implementation, this would check historical data
        # For now, return neutral
        return 0.5
