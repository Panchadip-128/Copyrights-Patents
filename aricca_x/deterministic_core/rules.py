"""
Frozen Production Rule Registry - the bifurcated-architecture boundary

ARICCA-X separates research from production:

  OFFLINE (research / validation)            PRODUCTION (delivered pipeline)
  --------------------------------           ------------------------------
  ML models, notebooks, corpora   --human-->  ProductionRule records only
  (e.g. ml_verification.py)        approval   (explicit formula + constants)

Every threshold and weight used by the production pipeline is a field of an
immutable ProductionRule.  The registry is sealed before use and its SHA-256
digest is written into the genesis block of every audit chain, so each
decision is bound to the exact rule set that produced it.  New rules can only
enter production through `RuleRegistry.promote()`, which records who approved
the rule and which offline evidence it was derived from.

Copyright (c) 2026. All rights reserved. Patent Pending.
"""

from dataclasses import dataclass
from typing import Dict, Iterable, List, Mapping, Tuple

from .canonical import digest

REFERENCE_PROVENANCE = "ARICCA-X reference parameterisation v2026.1"


@dataclass(frozen=True)
class ProductionRule:
    """An immutable, human-readable deterministic rule."""
    rule_id: str
    module: str
    expression: str
    parameters: Tuple[Tuple[str, float], ...]
    provenance: str = REFERENCE_PROVENANCE

    def param(self, name: str) -> float:
        for key, value in self.parameters:
            if key == name:
                return value
        raise KeyError(f"Rule '{self.rule_id}' has no parameter '{name}'")

    def as_dict(self) -> Dict[str, float]:
        return dict(self.parameters)

    @property
    def digest(self) -> str:
        return digest(self)


def make_rule(rule_id: str, module: str, expression: str,
              provenance: str = REFERENCE_PROVENANCE, **params: float) -> ProductionRule:
    """Build a rule with parameters stored in sorted, hashable form."""
    return ProductionRule(
        rule_id=rule_id,
        module=module,
        expression=expression,
        parameters=tuple(sorted((k, float(v)) for k, v in params.items())),
        provenance=provenance,
    )


class RuleRegistry:
    """Sealed collection of ProductionRules with a content digest."""

    def __init__(self, rules: Iterable[ProductionRule] = ()):
        self._rules: Dict[str, ProductionRule] = {}
        self._sealed = False
        for rule in rules:
            self.register(rule)

    def register(self, rule: ProductionRule) -> None:
        if self._sealed:
            raise RuntimeError("RuleRegistry is sealed; use promote() to derive a new registry")
        if rule.rule_id in self._rules:
            raise ValueError(f"Duplicate rule id '{rule.rule_id}'")
        self._rules[rule.rule_id] = rule

    def seal(self) -> "RuleRegistry":
        self._sealed = True
        return self

    @property
    def sealed(self) -> bool:
        return self._sealed

    def get(self, rule_id: str) -> ProductionRule:
        return self._rules[rule_id]

    def param(self, rule_id: str, name: str) -> float:
        return self._rules[rule_id].param(name)

    def rules(self) -> List[ProductionRule]:
        return [self._rules[k] for k in sorted(self._rules)]

    def digest(self) -> str:
        return digest(self.rules())

    def promote(self, rule_id: str, module: str, expression: str,
                parameters: Mapping[str, float], approved_by: str,
                evidence_ref: str) -> "RuleRegistry":
        """
        Promote a finding from the offline research environment into a NEW
        sealed registry.  The existing registry is never mutated.
        """
        if not approved_by or not evidence_ref:
            raise ValueError("Rule promotion requires a named approver and an evidence reference")
        promoted = make_rule(
            rule_id, module, expression,
            provenance=f"promoted-from-offline:{evidence_ref};approved-by:{approved_by}",
            **parameters,
        )
        rules = [r for r in self.rules() if r.rule_id != rule_id] + [promoted]
        return RuleRegistry(rules).seal()


DEFAULT_RULES: Tuple[ProductionRule, ...] = (
    # ---------------- Module A: Venue Intelligence ----------------
    make_rule(
        "VI-URGENCY", "venue_intelligence",
        "interval_days = submission_deadline - cfp_announcement; "
        "PREDATORY_URGENCY iff 0 <= interval_days < min_interval_days",
        min_interval_days=30,
    ),
    make_rule(
        "VI-SPOOF", "venue_intelligence",
        "d = Levenshtein(normalise(candidate), normalise(registry_entry)); "
        "TYPOSQUAT iff 1 <= d <= max(absolute_floor, floor(relative_ratio * len(normalise(registry_entry))))",
        relative_ratio=0.20, absolute_floor=1,
    ),
    make_rule(
        "VI-URL-SCORES", "venue_intelligence",
        "s_url = score[verdict]",
        verified_registry=1.0, unrelated=0.70, lookalike_domain=0.0,
        typosquat=0.0, brand_embedding=0.10,
    ),
    make_rule(
        "VI-SUBSIGNAL-WEIGHTS", "venue_intelligence",
        "s_venue = ADW over {url, temporal, claims, cfp_integrity}",
        url=0.30, temporal=0.20, claims=0.30, cfp_integrity=0.20,
    ),
    # ---------------- Grammatical Tense Analysis ----------------
    make_rule(
        "GTA-WEIGHTS", "grammatical_tense_analysis",
        "suspicion += w[tense]; suspicion += website_location_penalty if tense in {future, conditional} "
        "and source == website; credibility -= contradiction_penalty per same-indexer tense contradiction; "
        "credibility -= impossible_anchor_penalty per anachronistic 'since YYYY' anchor",
        past=-0.05, present=0.0, future=0.25, conditional=0.30, unknown=0.05,
        website_location_penalty=0.10, contradiction_penalty=0.20, impossible_anchor_penalty=0.30,
    ),
    # ---------------- Module B: Researcher Auditing ----------------
    make_rule(
        "RA-DFS", "researcher_auditing",
        "enumerate simple directed author cycles with 2 <= length <= max_depth by bounded DFS; "
        "each cycle enumerated once from its minimum node",
        max_depth=5, max_cycles=10000,
    ),
    make_rule(
        "RA-CIR", "researcher_auditing",
        "CIR = (independent + loop) / total; LACIR = independent / total; "
        "INFLATION_ALERT iff CIR < alert_threshold; LOOP_INFLATION_ALERT iff LACIR < alert_threshold",
        alert_threshold=0.30, healthy_reference=0.60,
    ),
    # ---------------- Module C: Peer-Review Forensics ----------------
    make_rule(
        "PR-UNIFORMITY", "peer_review_forensics",
        "CV = stdev(sentence_lengths) / mean(sentence_lengths); UNIFORM iff CV < cv_threshold "
        "(evaluated only when n_sentences >= min_sentences)",
        cv_threshold=0.20, min_sentences=3,
    ),
    make_rule(
        "PR-HEDGING", "peer_review_forensics",
        "hedging_density = 100 * hedge_phrase_matches / words; HEDGE_DENSE iff density > density_threshold",
        density_threshold=4.0,
    ),
    make_rule(
        "PR-SPECIFICITY", "peer_review_forensics",
        "specificity = manuscript_element_references / sentences; LOW_SPECIFICITY iff specificity < min_specificity",
        min_specificity=0.15,
    ),
    make_rule(
        "PR-MISALIGNMENT", "peer_review_forensics",
        "P = (pos - neg) / (pos + neg); MISALIGNED iff (P >= polarity_threshold and rec == reject) "
        "or (P <= -polarity_threshold and rec == accept)",
        polarity_threshold=0.50,
    ),
    make_rule(
        "PR-INDICATOR-WEIGHTS", "peer_review_forensics",
        "s_review = 1 - min(1, sum_k w_k * indicator_k)",
        uniform=0.25, hedge_dense=0.20, low_specificity=0.20, misaligned=0.25, phantom_reference=0.35,
    ),
    # ---------------- Cross-correlation engine ----------------
    make_rule(
        "ADW-MODULE-WEIGHTS", "correlation_engine",
        "w'_i = w_i / sum_{k in A} w_k ; C = sum_{i in A} w'_i * s_i ; "
        "interval = [sum_A w_i s_i, sum_A w_i s_i + sum_{k not in A} w_k]",
        venue=0.30, researcher=0.25, peer_review=0.25, grant=0.20, insufficient_evidence_width=0.50,
    ),
    make_rule(
        "HEURISTIC-PENALTIES", "correlation_engine",
        "Risk_1 = min(1, Risk_0 + sum penalty[severity] over triggered Boolean rules)",
        critical=0.15, high=0.08, medium=0.04, low=0.02,
    ),
    make_rule(
        "CSAD-CROSS-MODULE", "correlation_engine",
        "D_ij = |s_i - s_j|; g(D, tau) = max(0, (D - tau) / (1 - tau)); "
        "alpha_ij = alpha_facade if surface-layer score > substrate-layer score else alpha_neutral; "
        "Risk_2 = min(1, Risk_1 * (1 + alpha* * g(D*, tau))) for the pair maximising alpha_ij * g(D_ij, tau)",
        tau=0.35, alpha_facade=0.60, alpha_neutral=0.20,
    ),
    make_rule(
        "CSAD-VENUE", "credibility_logic_engine",
        "intra-venue correlated pairs; Risk' = min(1, Risk * (1 + alpha * g(D*, tau)))",
        tau=0.40, alpha=0.50,
    ),
    make_rule(
        "TFET", "temporal_fingerprint",
        "dF = F(T2) - F(T1); ||dF||_W = sqrt(sum_k w_k dF_k^2 / sum_k w_k); "
        "STABILITY_ALERT iff ||dF||_W > stability_threshold; "
        "velocity = ||dF||_W * 30 / max(1, days(T2 - T1))",
        stability_threshold=0.25,
        w_cfp_risk=0.15, w_website_depth=0.10, w_structural_completeness=0.10,
        w_indexing_claims=0.25, w_cfp_signature=0.10, w_organizer_continuity=0.15, w_ownership=0.15,
        adjustment_gain=0.50, adjustment_cap=0.25, hijack_bonus=0.10, trend_epsilon=0.02,
    ),
    make_rule(
        "RISK-TIERS", "correlation_engine",
        "low < t_medium <= medium < t_high <= high < t_critical <= critical",
        t_medium=0.25, t_high=0.50, t_critical=0.75,
    ),
)

DEFAULT_REGISTRY: RuleRegistry = RuleRegistry(DEFAULT_RULES).seal()
