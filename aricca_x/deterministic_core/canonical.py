"""
Canonical Serialization - bit-stable representation of pipeline state

Every intermediate state produced by ARICCA-X is reduced to a canonical JSON
form before hashing, so that identical inputs always yield byte-identical
serializations (and therefore identical SHA-256 digests) regardless of
dictionary insertion order, set iteration order, platform or Python hash seed.

Copyright (c) 2026. All rights reserved. Patent Pending.
"""

import dataclasses
import enum
import hashlib
import json
import math
from datetime import date, datetime
from typing import Any

# Floats are rounded to a fixed number of decimal places before serialization
# so that the canonical form is independent of floating-point print artefacts.
FLOAT_PRECISION = 6


def to_canonical(obj: Any) -> Any:
    """Recursively convert an object into a JSON-compatible canonical structure."""
    if obj is None or isinstance(obj, (bool, str)):
        return obj
    if isinstance(obj, int):
        return obj
    if isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            return str(obj)
        rounded = round(obj, FLOAT_PRECISION)
        return 0.0 if rounded == 0 else rounded  # normalise -0.0
    if isinstance(obj, enum.Enum):
        return to_canonical(obj.value)
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    if dataclasses.is_dataclass(obj) and not isinstance(obj, type):
        return {f.name: to_canonical(getattr(obj, f.name)) for f in dataclasses.fields(obj)}
    if isinstance(obj, dict):
        return {
            str(k): to_canonical(v)
            for k, v in sorted(obj.items(), key=lambda kv: str(kv[0]))
        }
    if isinstance(obj, (set, frozenset)):
        items = [to_canonical(v) for v in obj]
        return sorted(items, key=lambda x: json.dumps(x, sort_keys=True))
    if isinstance(obj, (list, tuple)):
        return [to_canonical(v) for v in obj]
    if hasattr(obj, "__dict__"):
        return to_canonical(vars(obj))
    return str(obj)


def canonical_json(obj: Any) -> str:
    """Serialize an object to its canonical JSON string."""
    return json.dumps(
        to_canonical(obj),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    )


def sha256_hex(text: str) -> str:
    """SHA-256 hex digest of a UTF-8 string."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def digest(obj: Any) -> str:
    """SHA-256 digest of the canonical serialization of an object."""
    return sha256_hex(canonical_json(obj))
