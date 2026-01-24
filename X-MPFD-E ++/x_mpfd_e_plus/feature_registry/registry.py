"""
Feature Registry and Provenance Lineage Tracker

Every feature is tracked with complete lineage - core copyright innovation.
Copyright © 2026. All Rights Reserved.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum
import hashlib


class FeatureCategory(Enum):
    """Feature categories"""
    LEXICAL = "lexical"
    STRUCTURAL = "structural"
    VISUAL = "visual"
    BEHAVIORAL = "behavioral"
    STATISTICAL = "statistical"


@dataclass
class FeatureProvenance:
    """
    Feature provenance metadata.
    Copyright-protected structure.
    """
    source_modality: str
    extraction_method: str
    extraction_timestamp: datetime
    confidence: float
    parameters: Dict[str, Any]


@dataclass
class FeatureLineage:
    """
    Complete transformation history.
    Copyright-protected lineage tracking.
    """
    transformations: List[str]
    source_signal_id: str
    intermediate_values: List[Any]
    
    def add_transformation(self, name: str, value: Any):
        """Add transformation step"""
        self.transformations.append(name)
        self.intermediate_values.append(value)


@dataclass
class RegisteredFeature:
    """
    Complete feature descriptor with provenance and lineage.
    Copyright-protected feature representation - major innovation.
    """
    feature_id: str
    name: str
    category: FeatureCategory
    value: Any
    provenance: FeatureProvenance
    lineage: FeatureLineage
    registration_timestamp: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Export to dictionary"""
        return {
            'feature_id': self.feature_id,
            'name': self.name,
            'category': self.category.value,
            'value': self.value,
            'provenance': {
                'source_modality': self.provenance.source_modality,
                'extraction_method': self.provenance.extraction_method,
                'timestamp': self.provenance.extraction_timestamp.isoformat(),
                'confidence': self.provenance.confidence,
                'parameters': self.provenance.parameters
            },
            'lineage': {
                'transformations': self.lineage.transformations,
                'source_signal_id': self.lineage.source_signal_id,
            },
            'registration_timestamp': self.registration_timestamp.isoformat(),
            'metadata': self.metadata
        }


class FeatureRegistry:
    """
    Centralized feature catalog with deduplication.
    Prevents feature leakage and duplication.
    Copyright-protected registry logic.
    """
    
    def __init__(self):
        self._features: Dict[str, RegisteredFeature] = {}
        self._name_index: Dict[str, List[str]] = {}  # name -> feature_ids
        self._category_index: Dict[FeatureCategory, List[str]] = {}
    
    def register_feature(self, 
                        name: str,
                        category: FeatureCategory,
                        value: Any,
                        source_modality: str,
                        extraction_method: str,
                        confidence: float,
                        lineage: FeatureLineage,
                        parameters: Optional[Dict] = None,
                        metadata: Optional[Dict] = None) -> RegisteredFeature:
        """
        Register a new feature with full provenance.
        
        Proprietary registration with automatic deduplication.
        """
        # Generate feature ID
        feature_id = self._generate_feature_id(name, value, source_modality)
        
        # Check if already registered
        if feature_id in self._features:
            return self._features[feature_id]
        
        # Create provenance
        provenance = FeatureProvenance(
            source_modality=source_modality,
            extraction_method=extraction_method,
            extraction_timestamp=datetime.now(),
            confidence=confidence,
            parameters=parameters or {}
        )
        
        # Create feature
        feature = RegisteredFeature(
            feature_id=feature_id,
            name=name,
            category=category,
            value=value,
            provenance=provenance,
            lineage=lineage,
            registration_timestamp=datetime.now(),
            metadata=metadata or {}
        )
        
        # Store in registry
        self._features[feature_id] = feature
        
        # Update indices
        if name not in self._name_index:
            self._name_index[name] = []
        self._name_index[name].append(feature_id)
        
        if category not in self._category_index:
            self._category_index[category] = []
        self._category_index[category].append(feature_id)
        
        return feature
    
    def _generate_feature_id(self, name: str, value: Any, source: str) -> str:
        """
        Generate unique feature ID.
        Proprietary ID generation algorithm.
        """
        signature = f"{name}|{str(value)}|{source}"
        hash_val = hashlib.md5(signature.encode()).hexdigest()[:12]
        return f"feat_{hash_val}"
    
    def get_feature(self, feature_id: str) -> Optional[RegisteredFeature]:
        """Retrieve feature by ID"""
        return self._features.get(feature_id)
    
    def get_features_by_name(self, name: str) -> List[RegisteredFeature]:
        """Get all features with given name"""
        feature_ids = self._name_index.get(name, [])
        return [self._features[fid] for fid in feature_ids]
    
    def get_features_by_category(self, category: FeatureCategory) -> List[RegisteredFeature]:
        """Get all features in category"""
        feature_ids = self._category_index.get(category, [])
        return [self._features[fid] for fid in feature_ids]
    
    def get_all_features(self) -> List[RegisteredFeature]:
        """Get all registered features"""
        return list(self._features.values())
    
    def clear(self):
        """Clear all registered features"""
        self._features.clear()
        self._name_index.clear()
        self._category_index.clear()
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get registry statistics"""
        return {
            'total_features': len(self._features),
            'unique_names': len(self._name_index),
            'categories': {
                cat.value: len(fids) 
                for cat, fids in self._category_index.items()
            },
            'avg_confidence': sum(f.provenance.confidence for f in self._features.values()) / len(self._features) if self._features else 0.0
        }


class ProvenanceLineageTracker:
    """
    Tracks feature provenance and lineage throughout processing.
    Copyright-protected tracking system.
    """
    
    def __init__(self):
        self._lineage_graph: Dict[str, FeatureLineage] = {}
        self._signal_to_features: Dict[str, List[str]] = {}
    
    def create_lineage(self, source_signal_id: str) -> FeatureLineage:
        """Create new lineage starting from signal"""
        lineage = FeatureLineage(
            transformations=[],
            source_signal_id=source_signal_id,
            intermediate_values=[]
        )
        return lineage
    
    def track_extraction(self, lineage: FeatureLineage, 
                        method_name: str, 
                        extracted_value: Any) -> FeatureLineage:
        """Track feature extraction step"""
        lineage.add_transformation(f"extract_{method_name}", extracted_value)
        return lineage
    
    def track_transformation(self, lineage: FeatureLineage,
                            transform_name: str,
                            transformed_value: Any) -> FeatureLineage:
        """Track feature transformation step"""
        lineage.add_transformation(f"transform_{transform_name}", transformed_value)
        return lineage
    
    def link_signal_to_feature(self, signal_id: str, feature_id: str):
        """Link signal to extracted feature"""
        if signal_id not in self._signal_to_features:
            self._signal_to_features[signal_id] = []
        self._signal_to_features[signal_id].append(feature_id)
    
    def get_features_from_signal(self, signal_id: str) -> List[str]:
        """Get all feature IDs extracted from signal"""
        return self._signal_to_features.get(signal_id, [])
    
    def audit_lineage(self, feature_id: str, lineage: FeatureLineage) -> Dict[str, Any]:
        """
        Audit feature lineage for integrity.
        Returns audit report.
        """
        return {
            'feature_id': feature_id,
            'source_signal': lineage.source_signal_id,
            'transformation_count': len(lineage.transformations),
            'transformations': lineage.transformations,
            'is_complete': len(lineage.transformations) > 0,
            'audit_timestamp': datetime.now().isoformat()
        }
