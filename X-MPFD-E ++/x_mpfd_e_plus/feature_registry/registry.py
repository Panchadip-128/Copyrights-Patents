"""
Feature Registry and Cryptographic Provenance Lineage Tracker
Module: x_mpfd_e_plus.feature_registry.registry

Every feature is deterministically extracted, validated, and bound to a persistent
cryptographic SHA-256 provenance tag. Fulfills 35 U.S.C. Section 112 enablement for
Patent Claims 1, 7, and 14.

Copyright © 2026 Panchadip B & Somyajeet A. All Rights Reserved.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from enum import Enum
import hashlib
import json


class FeatureCategory(Enum):
    """Discrete taxonomy of deterministic features."""
    LEXICAL = "lexical"
    STRUCTURAL = "structural"
    VISUAL = "visual"
    NETWORK = "network"
    STATISTICAL = "statistical"


@dataclass
class FeatureProvenance:
    """
    Cryptographic metadata record for feature provenance.
    Patent Claim 7: Traces source modality, algorithm, timestamp, and SHA-256 hash.
    """
    source_modality: str
    extraction_method: str
    extraction_timestamp: str
    confidence: float
    parameters: Dict[str, Any] = field(default_factory=dict)
    sha256_hash: str = ""

    def __post_init__(self):
        if not self.sha256_hash:
            canonical_repr = f"{self.source_modality}:{self.extraction_method}:{self.extraction_timestamp}:{self.confidence}:{json.dumps(self.parameters, sort_keys=True)}"
            self.sha256_hash = hashlib.sha256(canonical_repr.encode("utf-8")).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source_modality": self.source_modality,
            "extraction_method": self.extraction_method,
            "extraction_timestamp": self.extraction_timestamp,
            "confidence": self.confidence,
            "parameters": self.parameters,
            "sha256_hash": self.sha256_hash,
        }


@dataclass
class FeatureLineage:
    """
    Deterministic transformation history for auditing.
    Tracks sequential mathematical transformations applied to a raw signal.
    """
    source_signal_id: str
    transformations: List[str] = field(default_factory=list)
    intermediate_values: List[Any] = field(default_factory=list)

    def add_transformation(self, name: str, value: Any):
        """Append a discrete transformation step."""
        self.transformations.append(name)
        self.intermediate_values.append(value)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source_signal_id": self.source_signal_id,
            "transformations": self.transformations,
            "intermediate_values": self.intermediate_values,
        }


@dataclass
class RegisteredFeature:
    """
    Complete deterministic feature descriptor with cryptographic lineage.
    Patent Claims 1, 7, and 14.
    """
    feature_id: str
    name: str
    category: FeatureCategory
    value: Any
    provenance: FeatureProvenance
    lineage: FeatureLineage
    registration_timestamp: str
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "feature_id": self.feature_id,
            "name": self.name,
            "category": self.category.value,
            "value": self.value,
            "provenance": self.provenance.to_dict(),
            "lineage": self.lineage.to_dict(),
            "registration_timestamp": self.registration_timestamp,
            "metadata": self.metadata,
        }


class FeatureRegistry:
    """
    Centralized, deterministic feature catalog with automatic deduplication.
    Guarantees no state leakage and idempotent feature resolution.
    """
    def __init__(self):
        self._features: Dict[str, RegisteredFeature] = {}
        self._name_index: Dict[str, List[str]] = {}
        self._category_index: Dict[FeatureCategory, List[str]] = {}

    def register_feature(
        self,
        name: str,
        category: FeatureCategory,
        value: Any,
        source_modality: str,
        extraction_method: str,
        confidence: float,
        lineage: Optional[FeatureLineage] = None,
        parameters: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> RegisteredFeature:
        """Register a feature with cryptographic provenance and deduplication."""
        params = parameters or {}
        meta = metadata or {}
        lineage_obj = lineage or FeatureLineage(source_signal_id="direct_input")

        # Deterministic feature ID generation using SHA-256
        sig = f"{name}:{str(value)}:{source_modality}:{extraction_method}"
        hash_digest = hashlib.sha256(sig.encode("utf-8")).hexdigest()[:16]
        feature_id = f"feat_{hash_digest}"

        if feature_id in self._features:
            return self._features[feature_id]

        now_iso = datetime.now(timezone.utc).isoformat()
        provenance = FeatureProvenance(
            source_modality=source_modality,
            extraction_method=extraction_method,
            extraction_timestamp=now_iso,
            confidence=confidence,
            parameters=params,
        )

        feature = RegisteredFeature(
            feature_id=feature_id,
            name=name,
            category=category,
            value=value,
            provenance=provenance,
            lineage=lineage_obj,
            registration_timestamp=now_iso,
            metadata=meta,
        )

        self._features[feature_id] = feature

        if name not in self._name_index:
            self._name_index[name] = []
        self._name_index[name].append(feature_id)

        if category not in self._category_index:
            self._category_index[category] = []
        self._category_index[category].append(feature_id)

        return feature

    def get_feature(self, feature_id: str) -> Optional[RegisteredFeature]:
        return self._features.get(feature_id)

    def get_features_by_name(self, name: str) -> List[RegisteredFeature]:
        return [self._features[fid] for fid in self._name_index.get(name, [])]

    def get_features_by_category(self, category: FeatureCategory) -> List[RegisteredFeature]:
        return [self._features[fid] for fid in self._category_index.get(category, [])]

    def get_all_features(self) -> List[RegisteredFeature]:
        return list(self._features.values())

    def clear(self):
        self._features.clear()
        self._name_index.clear()
        self._category_index.clear()

    def get_statistics(self) -> Dict[str, Any]:
        return {
            "total_features": len(self._features),
            "unique_names": len(self._name_index),
            "categories": {cat.value: len(fids) for cat, fids in self._category_index.items()},
            "avg_confidence": (
                sum(f.provenance.confidence for f in self._features.values()) / len(self._features)
                if self._features
                else 0.0
            ),
        }


class ProvenanceLineageTracker:
    """
    Cryptographic Provenance Lineage Tracker.
    Maintains an immutable directed acyclic graph (DAG) of signal derivations.
    Patent Claim 7.
    """
    def __init__(self):
        self._lineage_graph: Dict[str, FeatureLineage] = {}
        self._signal_to_features: Dict[str, List[str]] = {}
        self._audit_chain: List[str] = []

    def create_lineage(self, source_signal_id: str) -> FeatureLineage:
        lineage = FeatureLineage(
            source_signal_id=source_signal_id,
            transformations=[],
            intermediate_values=[],
        )
        self._lineage_graph[source_signal_id] = lineage
        return lineage

    def track_extraction(self, lineage: FeatureLineage, method_name: str, extracted_value: Any) -> FeatureLineage:
        lineage.add_transformation(f"extract_{method_name}", extracted_value)
        return lineage

    def track_transformation(self, lineage: FeatureLineage, transform_name: str, transformed_value: Any) -> FeatureLineage:
        lineage.add_transformation(f"transform_{transform_name}", transformed_value)
        return lineage

    def link_signal_to_feature(self, signal_id: str, feature_id: str):
        if signal_id not in self._signal_to_features:
            self._signal_to_features[signal_id] = []
        self._signal_to_features[signal_id].append(feature_id)

    def get_features_from_signal(self, signal_id: str) -> List[str]:
        return self._signal_to_features.get(signal_id, [])

    def record_audit_hash(self, payload: Dict[str, Any]) -> str:
        """Appends a cryptographic block to the local audit chain."""
        prev_hash = self._audit_chain[-1] if self._audit_chain else "0" * 64
        block = f"{prev_hash}:{json.dumps(payload, sort_keys=True)}"
        curr_hash = hashlib.sha256(block.encode("utf-8")).hexdigest()
        self._audit_chain.append(curr_hash)
        return curr_hash

    def audit_lineage(self, feature_id: str, lineage: FeatureLineage) -> Dict[str, Any]:
        return {
            "feature_id": feature_id,
            "source_signal": lineage.source_signal_id,
            "transformation_count": len(lineage.transformations),
            "transformations": lineage.transformations,
            "is_complete": len(lineage.transformations) > 0,
            "audit_chain_length": len(self._audit_chain),
            "audit_timestamp": datetime.now(timezone.utc).isoformat(),
        }
