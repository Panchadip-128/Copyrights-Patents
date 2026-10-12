"""
Cross-Signal Anomaly Detection (CSAD) - layer-asymmetric divergence amplification

Each independent signal s_i is expressed in a common credibility space [0, 1]
and tagged with an evidence LAYER:

  SURFACE   - inexpensive for a bad actor to polish (CFP prose, indexing
              claims, peer-review wording)
  SUBSTRATE - expensive to fabricate (citation-network structure, compliance
              records, registry/domain facts)

For every admissible pair (i, j):

    D_ij  = |s_i - s_j|
    g     = max(0, (D_ij - tau) / (1 - tau))
    alpha = alpha_facade   if layers differ and the SURFACE score exceeds the
                           SUBSTRATE score (the "facade" pattern)
            alpha_neutral  otherwise

The pair maximising alpha_ij * g(D_ij) is selected (deterministic tie-break on
divergence then on pair name) and the risk is amplified proportionally:

    Risk' = min(1, Risk * (1 + alpha* * g(D*, tau)))

No machine-learning classifier is used; every quantity is an explicit formula.

Copyright (c) 2026. All rights reserved. Patent Pending.
"""

from dataclasses import dataclass, field
from itertools import combinations
from typing import List, Mapping, Optional, Sequence, Tuple

SURFACE = "surface"
SUBSTRATE = "substrate"


@dataclass(frozen=True)
class DivergencePair:
    signal_a: str
    signal_b: str
    score_a: float
    score_b: float
    divergence: float
    layer_a: str
    layer_b: str
    pattern: str      # "facade" | "reverse_facade" | "intra_layer"
    g_value: float
    alpha: float

    @property
    def amplification(self) -> float:
        return self.alpha * self.g_value


@dataclass
class CSADResult:
    pairs: List[DivergencePair]
    selected_pair: Optional[DivergencePair]
    max_divergence: float
    g_value: float
    alpha: float
    amplification_factor: float   # 1 + alpha * g
    risk_in: float
    risk_out: float
    triggered: bool
    justification: List[str] = field(default_factory=list)


def g_function(divergence: float, tau: float) -> float:
    """Normalised excess divergence above the threshold, in [0, 1]."""
    if not 0.0 <= tau < 1.0:
        raise ValueError("tau must lie in [0, 1)")
    if divergence <= tau:
        return 0.0
    return min(1.0, (divergence - tau) / (1.0 - tau))


def _classify_pattern(score_a: float, score_b: float, layer_a: str, layer_b: str) -> str:
    if layer_a == layer_b:
        return "intra_layer"
    surface_score, substrate_score = (score_a, score_b) if layer_a == SURFACE else (score_b, score_a)
    return "facade" if surface_score > substrate_score else "reverse_facade"


def cross_signal_anomaly_detection(
    signals: Mapping[str, Optional[float]],
    layers: Mapping[str, str],
    risk: float,
    tau: float,
    alpha_facade: float,
    alpha_neutral: float,
    correlated_pairs: Optional[Sequence[Tuple[str, str]]] = None,
) -> CSADResult:
    """Run CSAD over the observed signals and amplify `risk`."""
    available = sorted(k for k, v in signals.items() if v is not None)
    if correlated_pairs is None:
        candidate_pairs = list(combinations(available, 2))
    else:
        candidate_pairs = [
            tuple(sorted(p)) for p in correlated_pairs
            if p[0] in available and p[1] in available
        ]

    pairs: List[DivergencePair] = []
    for a, b in sorted(set(candidate_pairs)):
        s_a, s_b = float(signals[a]), float(signals[b])
        layer_a = layers.get(a, SURFACE)
        layer_b = layers.get(b, SURFACE)
        divergence = abs(s_a - s_b)
        pattern = _classify_pattern(s_a, s_b, layer_a, layer_b)
        alpha = alpha_facade if pattern == "facade" else alpha_neutral
        pairs.append(DivergencePair(
            signal_a=a, signal_b=b, score_a=s_a, score_b=s_b,
            divergence=divergence, layer_a=layer_a, layer_b=layer_b,
            pattern=pattern, g_value=g_function(divergence, tau), alpha=alpha,
        ))

    justification: List[str] = []
    max_divergence = max((p.divergence for p in pairs), default=0.0)
    selected = None
    if pairs:
        selected = sorted(
            pairs,
            key=lambda p: (-p.amplification, -p.divergence, p.signal_a, p.signal_b),
        )[0]

    if selected is None or selected.g_value == 0.0:
        justification.append(
            f"CSAD: max divergence D = {max_divergence:.4f} <= tau = {tau:.2f}; no amplification"
        )
        return CSADResult(
            pairs=pairs, selected_pair=selected, max_divergence=max_divergence,
            g_value=0.0, alpha=0.0, amplification_factor=1.0,
            risk_in=risk, risk_out=risk, triggered=False, justification=justification,
        )

    factor = 1.0 + selected.alpha * selected.g_value
    risk_out = min(1.0, risk * factor)
    justification.extend([
        f"CSAD pair ({selected.signal_a}, {selected.signal_b}): "
        f"D = |{selected.score_a:.4f} - {selected.score_b:.4f}| = {selected.divergence:.4f} "
        f"[{selected.pattern}]",
        f"g(D, tau) = ({selected.divergence:.4f} - {tau:.2f}) / (1 - {tau:.2f}) = {selected.g_value:.4f}",
        f"Risk' = min(1, {risk:.4f} * (1 + {selected.alpha:.2f} * {selected.g_value:.4f})) = {risk_out:.4f}",
    ])
    return CSADResult(
        pairs=pairs, selected_pair=selected, max_divergence=max_divergence,
        g_value=selected.g_value, alpha=selected.alpha, amplification_factor=factor,
        risk_in=risk, risk_out=risk_out, triggered=True, justification=justification,
    )
