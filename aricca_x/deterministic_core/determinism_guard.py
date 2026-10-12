"""
Determinism Guard - enforces the "no probabilistic classifier in production" property

The production pipeline refuses to run if a machine-learning / probabilistic
inference library has been loaded into the interpreter.  ML is permitted only
in the isolated offline research environment (see ml_verification.py and
RuleRegistry.promote()).

Copyright (c) 2026. All rights reserved. Patent Pending.
"""

import sys
from dataclasses import dataclass
from typing import Iterable, List, Optional, Tuple

FORBIDDEN_MODULE_PREFIXES: Tuple[str, ...] = (
    "sklearn",
    "torch",
    "tensorflow",
    "keras",
    "transformers",
    "sentence_transformers",
    "xgboost",
    "lightgbm",
    "catboost",
    "jax",
    "onnxruntime",
)


class DeterminismViolation(RuntimeError):
    """Raised when a probabilistic inference library is present in production."""


@dataclass(frozen=True)
class DeterminismReport:
    compliant: bool
    forbidden_modules_loaded: Tuple[str, ...]
    checked_prefixes: Tuple[str, ...]


def inspect_runtime(loaded_modules: Optional[Iterable[str]] = None,
                    prefixes: Tuple[str, ...] = FORBIDDEN_MODULE_PREFIXES) -> DeterminismReport:
    """Return which forbidden top-level packages are loaded."""
    names = list(loaded_modules) if loaded_modules is not None else list(sys.modules)
    hits: List[str] = sorted({
        name.split(".")[0] for name in names
        if name.split(".")[0] in prefixes
    })
    return DeterminismReport(
        compliant=not hits,
        forbidden_modules_loaded=tuple(hits),
        checked_prefixes=prefixes,
    )


def enforce_deterministic_runtime(strict: bool = True,
                                  loaded_modules: Optional[Iterable[str]] = None) -> DeterminismReport:
    """Raise DeterminismViolation (strict) or return the report (non-strict)."""
    report = inspect_runtime(loaded_modules)
    if strict and not report.compliant:
        raise DeterminismViolation(
            "Production pipeline must be free of probabilistic classifiers; loaded: "
            + ", ".join(report.forbidden_modules_loaded)
        )
    return report
