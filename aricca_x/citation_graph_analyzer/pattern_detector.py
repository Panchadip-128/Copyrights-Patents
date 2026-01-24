"""
Pattern Detector - Detects suspicious citation patterns

Implements proprietary pattern detection algorithms.
Copyright (c) 2026. All rights reserved.
"""

from typing import List, Dict, Set
from dataclasses import dataclass
from .graph_builder import CitationGraph


@dataclass
class CitationPattern:
    """Represents a detected citation pattern"""
    pattern_type: str
    description: str
    suspicion_score: float
    evidence: List[str]
    affected_references: List[str]


class PatternDetector:
    """
    Detects suspicious patterns in citation behavior.
    
    Implements proprietary pattern detection algorithms for
    identifying potential citation manipulation.
    """
    
    # Thresholds for detection (proprietary)
    SELF_CITATION_THRESHOLD = 0.3
    CLUSTER_DENSITY_THRESHOLD = 0.7
    RECIPROCAL_CITATION_THRESHOLD = 3
    
    def __init__(self):
        """Initialize the pattern detector"""
        pass
    
    def detect_patterns(
        self,
        graph: CitationGraph,
        citations: List[any]
    ) -> List[CitationPattern]:
        """
        Detect suspicious citation patterns.
        
        Args:
            graph: CitationGraph object
            citations: List of citations
            
        Returns:
            List of detected patterns
        """
        patterns = []
        
        # Detect citation clustering
        clustering_pattern = self._detect_clustering(graph)
        if clustering_pattern:
            patterns.append(clustering_pattern)
        
        # Detect citation cartels (reciprocal citation rings)
        cartel_patterns = self._detect_citation_cartels(graph)
        patterns.extend(cartel_patterns)
        
        # Detect abnormal citation concentration
        concentration_pattern = self._detect_concentration(graph, citations)
        if concentration_pattern:
            patterns.append(concentration_pattern)
        
        # Detect temporal anomalies
        temporal_pattern = self._detect_temporal_anomalies(graph)
        if temporal_pattern:
            patterns.append(temporal_pattern)
        
        return patterns
    
    def _detect_clustering(self, graph: CitationGraph) -> CitationPattern:
        """
        Detect excessive citation clustering.
        
        Proprietary clustering detection algorithm.
        """
        if len(graph.nodes) < 3:
            return None
        
        # Calculate clustering coefficient
        total_clustering = 0
        nodes_with_neighbors = 0
        
        for node in graph.nodes:
            neighbors = graph.get_neighbors(node)
            if len(neighbors) < 2:
                continue
            
            nodes_with_neighbors += 1
            
            # Count edges between neighbors
            neighbor_edges = 0
            for i, n1 in enumerate(neighbors):
                for n2 in neighbors[i+1:]:
                    if (n1, n2) in graph.edges or (n2, n1) in graph.edges:
                        neighbor_edges += 1
            
            # Calculate clustering for this node
            max_possible_edges = len(neighbors) * (len(neighbors) - 1) / 2
            if max_possible_edges > 0:
                total_clustering += neighbor_edges / max_possible_edges
        
        if nodes_with_neighbors == 0:
            return None
        
        avg_clustering = total_clustering / nodes_with_neighbors
        
        if avg_clustering > self.CLUSTER_DENSITY_THRESHOLD:
            return CitationPattern(
                pattern_type="excessive_clustering",
                description="Citations show excessive clustering, possibly indicating citation ring",
                suspicion_score=min(avg_clustering, 1.0),
                evidence=[
                    f"Average clustering coefficient: {avg_clustering:.2f}",
                    f"Threshold exceeded: {self.CLUSTER_DENSITY_THRESHOLD}"
                ],
                affected_references=list(graph.nodes)
            )
        
        return None
    
    def _detect_citation_cartels(self, graph: CitationGraph) -> List[CitationPattern]:
        """
        Detect citation cartels (reciprocal citation rings).
        
        Proprietary cartel detection algorithm.
        """
        patterns = []
        
        # Find strongly connected components (simple cycle detection)
        for node in graph.nodes:
            neighbors = graph.get_neighbors(node)
            
            for neighbor in neighbors:
                # Check for reciprocal edges
                if node in graph.get_neighbors(neighbor):
                    # Found reciprocal citation
                    # Check if it's part of a larger ring
                    ring_size = self._find_ring_size(graph, node, neighbor)
                    
                    if ring_size >= self.RECIPROCAL_CITATION_THRESHOLD:
                        patterns.append(CitationPattern(
                            pattern_type="citation_cartel",
                            description=f"Detected potential citation cartel of size {ring_size}",
                            suspicion_score=min(ring_size / 10.0, 1.0),
                            evidence=[
                                f"Ring size: {ring_size}",
                                f"Reciprocal citations detected between {node} and {neighbor}"
                            ],
                            affected_references=[node, neighbor]
                        ))
        
        return patterns
    
    def _find_ring_size(
        self,
        graph: CitationGraph,
        start_node: str,
        current_node: str,
        visited: Set[str] = None
    ) -> int:
        """Find size of citation ring starting from a node"""
        if visited is None:
            visited = {start_node}
        
        if current_node in visited:
            return len(visited)
        
        visited.add(current_node)
        neighbors = graph.get_neighbors(current_node)
        
        max_ring = len(visited)
        for neighbor in neighbors:
            if neighbor == start_node:
                return len(visited) + 1
            elif neighbor not in visited:
                ring_size = self._find_ring_size(graph, start_node, neighbor, visited.copy())
                max_ring = max(max_ring, ring_size)
        
        return max_ring
    
    def _detect_concentration(
        self,
        graph: CitationGraph,
        citations: List[any]
    ) -> CitationPattern:
        """
        Detect abnormal concentration of citations.
        
        Proprietary concentration detection algorithm.
        """
        if not citations:
            return None
        
        # Count citations per reference
        citation_counts = {}
        for citation in citations:
            ref_id = citation.reference_id
            citation_counts[ref_id] = citation_counts.get(ref_id, 0) + 1
        
        if not citation_counts:
            return None
        
        # Find most cited references
        max_citations = max(citation_counts.values())
        total_citations = sum(citation_counts.values())
        
        # Check if top reference has disproportionate citations
        concentration_ratio = max_citations / total_citations
        
        if concentration_ratio > 0.3:  # One ref has >30% of citations
            top_refs = [
                ref_id for ref_id, count in citation_counts.items()
                if count == max_citations
            ]
            
            return CitationPattern(
                pattern_type="citation_concentration",
                description="Abnormal concentration of citations on few references",
                suspicion_score=min(concentration_ratio * 1.5, 1.0),
                evidence=[
                    f"Top reference(s) have {concentration_ratio:.1%} of all citations",
                    f"Max citations to single ref: {max_citations}/{total_citations}"
                ],
                affected_references=top_refs
            )
        
        return None
    
    def _detect_temporal_anomalies(self, graph: CitationGraph) -> CitationPattern:
        """
        Detect temporal anomalies in citations.
        
        Proprietary temporal analysis algorithm.
        """
        # Extract years from node attributes
        years = []
        for node in graph.nodes:
            attrs = graph.node_attributes.get(node, {})
            year = attrs.get('year')
            if year:
                years.append(year)
        
        if len(years) < 5:
            return None
        
        # Check for old citations only (no recent work)
        from datetime import datetime
        current_year = datetime.now().year
        recent_citations = sum(1 for y in years if y >= current_year - 3)
        
        if recent_citations == 0:
            return CitationPattern(
                pattern_type="temporal_anomaly",
                description="No citations to recent work (last 3 years)",
                suspicion_score=0.6,
                evidence=[
                    f"Most recent citation year: {max(years)}",
                    "Consider including more recent references"
                ],
                affected_references=[]
            )
        
        return None
