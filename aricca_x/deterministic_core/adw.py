"""
Adaptive Decay Weighting (ADW) with Epistemic Evidence Interval

Formula (preferred embodiment):

    A        = set of dimensions whose evidence is OBSERVED
    w'_i     = w_i / sum_{k in A} w_k                    for i in A
    w'_j     = 0                                         for j not in A (UNKNOWN)
    C        = sum_{i in A} w'_i * s_i

Distinguishing features over prior art (e.g. AU2012231158B2, which averages
whatever measures are available, and the Journal Checker Tool, which emits a
categorical "Unknown"):

  1. An absent dimension is carried as UNKNOWN (None); no neutral or default
     score is ever fabricated for it.
  2. Its weight is redistributed strictly in proportion to the predetermined
     weights of the observed dimensions.
  3. A closed-form EPISTEMIC INTERVAL is computed alongside the point score:

        lower = sum_{i in A} w_i * s_i                  (all unknowns = 0)
        upper = lower + sum_{j not in A} w_j            (all unknowns = 1)
        width = sum_{j not in A} w_j

     The width quantifies exactly how much of the decision is unsupported by
     evidence and drives an INSUFFICIENT_EVIDENCE flag.

Copyright (c) 2026. All rights reserved. Patent Pending.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Mapping, Optional, Tuple


def clamp01(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


@dataclass
class ADWResult:
    base_weights: Dict[str, float]
    effective_weights: Dict[str, float]
    observed: Tuple[str, ...]
    unknown: Tuple[str, ...]
    score: Optional[float]
    lower_bound: float
    upper_bound: float
    interval_width: float
    justification: List[str] = field(default_factory=list)


def adaptive_decay_weighting(base_weights: Mapping[str, float],
                             scores: Mapping[str, Optional[float]]) -> ADWResult:
    """Apply ADW to a set of dimension scores; None means UNKNOWN."""
    if not base_weights:
        raise ValueError("ADW requires at least one dimension")
    total = sum(float(w) for w in base_weights.values())
    if total <= 0:
        raise ValueError("ADW base weights must sum to a positive value")

    keys = sorted(base_weights)
    weights = {k: float(base_weights[k]) / total for k in keys}  # normalise to sum 1
    observed = tuple(k for k in keys if scores.get(k) is not None)
    unknown = tuple(k for k in keys if scores.get(k) is None)
    denominator = sum(weights[k] for k in observed)

    justification: List[str] = []
    effective = {k: 0.0 for k in keys}
    if denominator > 0:
        for k in observed:
            effective[k] = weights[k] / denominator
            justification.append(
                f"w'_{k} = {weights[k]:.4f} / {denominator:.4f} = {effective[k]:.4f}"
            )
        score = sum(effective[k] * clamp01(scores[k]) for k in observed)
        terms = " + ".join(f"{effective[k]:.4f}*{clamp01(scores[k]):.4f}" for k in observed)
        justification.append(f"C = {terms} = {score:.4f}")
    else:
        score = None
        justification.append("C = UNKNOWN (no observed dimensions)")

    for k in unknown:
        justification.append(
            f"{k}: UNKNOWN - weight {weights[k]:.4f} redistributed, no score fabricated"
        )

    lower = sum(weights[k] * clamp01(scores[k]) for k in observed)
    width = sum(weights[k] for k in unknown)
    upper = lower + width
    justification.append(
        f"Epistemic interval = [{lower:.4f}, {upper:.4f}] (width {width:.4f})"
    )

    return ADWResult(
        base_weights=weights,
        effective_weights=effective,
        observed=observed,
        unknown=unknown,
        score=score,
        lower_bound=lower,
        upper_bound=upper,
        interval_width=width,
        justification=justification,
    )
