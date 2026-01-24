"""
Multimodal Signal Orchestrator

The heart of X-MPFD-E++ originality.
Handles signal normalization, temporal alignment, and MST generation.
Copyright © 2026. All Rights Reserved.
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from datetime import datetime
import hashlib

from ..input_signal_manager import SignalDescriptor, SignalType


@dataclass
class MultimodalSignalTensor:
    """
    Unified representation of multimodal signals.
    Copyright-protected data structure - core innovation.
    """
    tensor_id: str
    signals: Dict[SignalType, SignalDescriptor]
    alignment_score: float
    completeness_score: float
    timestamp: datetime
    metadata: Dict[str, Any]
    
    def has_modality(self, modality: SignalType) -> bool:
        """Check if MST contains specific modality"""
        return modality in self.signals and self.signals[modality].is_valid()
    
    def get_signal(self, modality: SignalType) -> Optional[SignalDescriptor]:
        """Get signal for specific modality"""
        return self.signals.get(modality)


class TemporalAligner:
    """
    Aligns signals across modalities temporally.
    Proprietary temporal alignment logic.
    """
    
    # Alignment thresholds (proprietary)
    MAX_TIME_DELTA_SECONDS = 300  # 5 minutes
    ALIGNMENT_WEIGHT_URL = 1.0
    ALIGNMENT_WEIGHT_HTML = 0.9
    ALIGNMENT_WEIGHT_VISUAL = 0.8
    
    def align_signals(self, signals: List[SignalDescriptor]) -> float:
        """
        Calculate temporal alignment score.
        
        Proprietary algorithm: weighted time-distance calculation
        with modality-specific importance factors.
        
        Returns:
            Alignment score [0.0, 1.0]
        """
        if len(signals) <= 1:
            return 1.0
        
        # Get timestamps
        timestamps = [(s.timestamp, s.signal_type) for s in signals]
        timestamps.sort()
        
        # Calculate pairwise time deltas
        deltas = []
        weights = []
        
        for i in range(len(timestamps) - 1):
            t1, type1 = timestamps[i]
            t2, type2 = timestamps[i + 1]
            
            delta = abs((t2 - t1).total_seconds())
            deltas.append(delta)
            
            # Apply modality-specific weights
            weight = self._get_alignment_weight(type1, type2)
            weights.append(weight)
        
        # Calculate weighted alignment score
        if not deltas:
            return 1.0
        
        max_delta = max(deltas)
        if max_delta == 0:
            return 1.0
        
        # Proprietary scoring formula
        normalized_deltas = [d / max_delta for d in deltas]
        weighted_penalty = sum(nd * w for nd, w in zip(normalized_deltas, weights)) / sum(weights)
        
        # Apply time threshold penalty
        if max_delta > self.MAX_TIME_DELTA_SECONDS:
            weighted_penalty *= 1.5
        
        alignment_score = max(0.0, 1.0 - weighted_penalty)
        
        return alignment_score
    
    def _get_alignment_weight(self, type1: SignalType, type2: SignalType) -> float:
        """Get importance weight for signal pair"""
        weight_map = {
            SignalType.URL: self.ALIGNMENT_WEIGHT_URL,
            SignalType.HTML: self.ALIGNMENT_WEIGHT_HTML,
            SignalType.VISUAL: self.ALIGNMENT_WEIGHT_VISUAL
        }
        
        w1 = weight_map.get(type1, 0.5)
        w2 = weight_map.get(type2, 0.5)
        
        return (w1 + w2) / 2


class NoiseFilter:
    """
    Filters noise and redundant signals.
    Proprietary noise reduction algorithms.
    """
    
    # Noise detection thresholds
    MIN_SIGNAL_QUALITY = 0.3
    REDUNDANCY_SIMILARITY_THRESHOLD = 0.95
    
    def filter_signals(self, signals: List[SignalDescriptor]) -> List[SignalDescriptor]:
        """
        Filter out low-quality and redundant signals.
        
        Proprietary filtering logic.
        """
        # Remove low-quality signals
        high_quality = [s for s in signals if s.validity_score >= self.MIN_SIGNAL_QUALITY]
        
        # Remove redundant signals of same type
        deduplicated = self._remove_redundancy(high_quality)
        
        return deduplicated
    
    def _remove_redundancy(self, signals: List[SignalDescriptor]) -> List[SignalDescriptor]:
        """Remove redundant signals of same type"""
        # Group by signal type
        by_type: Dict[SignalType, List[SignalDescriptor]] = {}
        for signal in signals:
            if signal.signal_type not in by_type:
                by_type[signal.signal_type] = []
            by_type[signal.signal_type].append(signal)
        
        # Keep highest quality signal of each type
        filtered = []
        for signal_type, signal_list in by_type.items():
            if len(signal_list) == 1:
                filtered.append(signal_list[0])
            else:
                # Keep signal with highest validity score
                best = max(signal_list, key=lambda s: s.validity_score)
                filtered.append(best)
        
        return filtered


class CompletenessEvaluator:
    """
    Evaluates signal completeness across modalities.
    Proprietary completeness scoring.
    """
    
    # Completeness weights (proprietary)
    MODALITY_IMPORTANCE = {
        SignalType.URL: 0.40,
        SignalType.HTML: 0.35,
        SignalType.VISUAL: 0.20,
        SignalType.NETWORK: 0.05
    }
    
    def evaluate_completeness(self, signals: Dict[SignalType, SignalDescriptor]) -> float:
        """
        Calculate completeness score.
        
        Proprietary formula: weighted presence + quality scoring
        
        Returns:
            Completeness score [0.0, 1.0]
        """
        if not signals:
            return 0.0
        
        score = 0.0
        total_weight = 0.0
        
        for modality, weight in self.MODALITY_IMPORTANCE.items():
            total_weight += weight
            
            if modality in signals:
                signal = signals[modality]
                if signal.is_valid():
                    # Presence bonus + quality bonus
                    presence_score = weight
                    quality_bonus = weight * signal.validity_score * 0.2
                    score += presence_score + quality_bonus
        
        # Normalize
        completeness = score / total_weight if total_weight > 0 else 0.0
        
        return min(1.0, completeness)


class MultimodalOrchestrator:
    """
    Main orchestration interface.
    Coordinates signal processing, alignment, and MST generation.
    
    Copyright-protected orchestration logic - core system innovation.
    """
    
    def __init__(self):
        self.aligner = TemporalAligner()
        self.filter = NoiseFilter()
        self.completeness_evaluator = CompletenessEvaluator()
        self._mst_cache: Dict[str, MultimodalSignalTensor] = {}
    
    def orchestrate(self, signals: List[SignalDescriptor], 
                   metadata: Optional[Dict] = None) -> MultimodalSignalTensor:
        """
        Main orchestration method.
        
        Proprietary 4-phase process:
        1. Noise filtering
        2. Temporal alignment
        3. Completeness evaluation
        4. MST generation
        
        Args:
            signals: List of signal descriptors
            metadata: Optional metadata
        
        Returns:
            Multimodal Signal Tensor (MST)
        """
        # Phase 1: Filter noise and redundancy
        filtered_signals = self.filter.filter_signals(signals)
        
        if not filtered_signals:
            raise ValueError("No valid signals after filtering")
        
        # Phase 2: Calculate temporal alignment
        alignment_score = self.aligner.align_signals(filtered_signals)
        
        # Phase 3: Organize by modality
        signals_by_modality: Dict[SignalType, SignalDescriptor] = {}
        for signal in filtered_signals:
            signals_by_modality[signal.signal_type] = signal
        
        # Phase 4: Evaluate completeness
        completeness_score = self.completeness_evaluator.evaluate_completeness(
            signals_by_modality
        )
        
        # Generate MST
        mst = self._generate_mst(
            signals_by_modality,
            alignment_score,
            completeness_score,
            metadata or {}
        )
        
        # Cache MST
        self._mst_cache[mst.tensor_id] = mst
        
        return mst
    
    def _generate_mst(self, 
                     signals: Dict[SignalType, SignalDescriptor],
                     alignment_score: float,
                     completeness_score: float,
                     metadata: Dict) -> MultimodalSignalTensor:
        """
        Generate Multimodal Signal Tensor.
        Proprietary MST generation with unique ID.
        """
        # Generate unique tensor ID (proprietary)
        tensor_signature = self._compute_tensor_signature(signals)
        
        mst = MultimodalSignalTensor(
            tensor_id=tensor_signature,
            signals=signals,
            alignment_score=alignment_score,
            completeness_score=completeness_score,
            timestamp=datetime.now(),
            metadata=metadata
        )
        
        return mst
    
    def _compute_tensor_signature(self, signals: Dict[SignalType, SignalDescriptor]) -> str:
        """
        Compute unique MST signature.
        Proprietary signature algorithm.
        """
        # Combine signal IDs in deterministic order
        signal_ids = [signals[st].signal_id for st in sorted(signals.keys(), key=lambda x: x.value)]
        combined = '|'.join(signal_ids)
        
        # Hash for unique ID
        signature = hashlib.sha256(combined.encode()).hexdigest()[:16]
        
        return f"mst_{signature}"
    
    def get_mst(self, tensor_id: str) -> Optional[MultimodalSignalTensor]:
        """Retrieve cached MST by ID"""
        return self._mst_cache.get(tensor_id)
    
    def clear_cache(self):
        """Clear MST cache"""
        self._mst_cache.clear()
