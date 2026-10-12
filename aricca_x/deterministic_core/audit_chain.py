"""
Hash-Chained Phase Audit Trail

Implements the strictly-serializable, tamper-evident evidence chain for the
six-phase deterministic pipeline.  After each phase the complete phase state
is canonically serialized and linked to the previous phase by a SHA-256 hash:

    genesis  = SHA256( "0"*64 | pipeline_id | input_digest | ruleset_digest )
    h_i      = SHA256( h_{i-1} | i | phase_name_i | SHA256(canonical(state_i)) )

Consequences:
  * any later modification of an input, a rule parameter or an intermediate
    phase state changes every subsequent hash (tamper evidence);
  * an exported chain can be re-verified offline by an auditor without
    re-running the pipeline;
  * identical inputs + identical rule set => identical final hash
    (reproducibility proof).

Copyright (c) 2026. All rights reserved. Patent Pending.
"""

from dataclasses import dataclass
from typing import Any, Dict, List

from .canonical import canonical_json, sha256_hex, to_canonical

GENESIS_SEED = "0" * 64


@dataclass(frozen=True)
class PhaseRecord:
    """One serialized, hash-linked phase state."""
    index: int
    phase: str
    state: Any
    state_digest: str
    previous_hash: str
    record_hash: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "index": self.index,
            "phase": self.phase,
            "state": self.state,
            "state_digest": self.state_digest,
            "previous_hash": self.previous_hash,
            "record_hash": self.record_hash,
        }


def _link(previous_hash: str, index: int, phase: str, state_digest: str) -> str:
    return sha256_hex(f"{previous_hash}|{index}|{phase}|{state_digest}")


class AuditChain:
    """Append-only, hash-linked sequence of phase states."""

    def __init__(self, pipeline_id: str, input_digest: str, ruleset_digest: str):
        self.pipeline_id = pipeline_id
        self.input_digest = input_digest
        self.ruleset_digest = ruleset_digest
        self.genesis_hash = sha256_hex(
            f"{GENESIS_SEED}|{pipeline_id}|{input_digest}|{ruleset_digest}"
        )
        self.records: List[PhaseRecord] = []

    @property
    def head(self) -> str:
        return self.records[-1].record_hash if self.records else self.genesis_hash

    def append(self, phase: str, state: Any) -> PhaseRecord:
        """Serialize a phase state and link it to the chain."""
        canonical_state = to_canonical(state)
        state_digest = sha256_hex(canonical_json(canonical_state))
        index = len(self.records) + 1
        record = PhaseRecord(
            index=index,
            phase=phase,
            state=canonical_state,
            state_digest=state_digest,
            previous_hash=self.head,
            record_hash=_link(self.head, index, phase, state_digest),
        )
        self.records.append(record)
        return record

    def verify(self) -> bool:
        """Recompute every digest and link; False if anything was altered."""
        return verify_exported_chain(self.to_dict())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "pipeline_id": self.pipeline_id,
            "input_digest": self.input_digest,
            "ruleset_digest": self.ruleset_digest,
            "genesis_hash": self.genesis_hash,
            "records": [r.to_dict() for r in self.records],
            "final_hash": self.head,
        }


def verify_exported_chain(chain: Dict[str, Any]) -> bool:
    """Independently verify an exported (e.g. JSON-loaded) audit chain."""
    expected_genesis = sha256_hex(
        f"{GENESIS_SEED}|{chain['pipeline_id']}|{chain['input_digest']}|{chain['ruleset_digest']}"
    )
    if chain.get("genesis_hash") != expected_genesis:
        return False
    previous = expected_genesis
    for position, record in enumerate(chain.get("records", []), start=1):
        if record["index"] != position or record["previous_hash"] != previous:
            return False
        if sha256_hex(canonical_json(record["state"])) != record["state_digest"]:
            return False
        if _link(previous, position, record["phase"], record["state_digest"]) != record["record_hash"]:
            return False
        previous = record["record_hash"]
    return chain.get("final_hash") == previous
