"""
Citation Graph Analyzer - Analyzes citation patterns using graph algorithms

Implements proprietary graph-based citation analysis.
Copyright (c) 2026. All rights reserved.
"""

from typing import Dict, List, Set, Tuple, Optional
from dataclasses import dataclass, field
from datetime import datetime
from .citation_extractor import CitationExtractor, ExtractedCitation
from .graph_builder import GraphBuilder, CitationGraph
from .pattern_detector import PatternDetector, CitationPattern


@dataclass
class CitationAnalysisResult:
    """Complete citation analysis results"""
    manuscript_id: str
    total_citations: int
    unique_citations: int
    self_citations: int
    self_citation_rate: float
    citation_clusters: List[Set[str]]
    suspicious_patterns: List[CitationPattern]
    citation_network_density: float
    temporal_distribution: Dict[int, int]
    author_citation_diversity: float
    analysis_timestamp: datetime
    risk_score: float
    recommendations: List[str] = field(default_factory=list)


class CitationGraphAnalyzer:
    """
    Analyzes citation behavior using graph-based algorithms.
    
    Implements proprietary citation pattern detection and manipulation
    detection algorithms.
    """
    
    def __init__(self):
        """Initialize the citation graph analyzer"""
        self.extractor = CitationExtractor()
        self.graph_builder = GraphBuilder()
        self.pattern_detector = PatternDetector()
    
    def analyze(
        self,
        manuscript_text: str,
        references: List[Dict],
        author_names: Optional[List[str]] = None
    ) -> CitationAnalysisResult:
        """
        Perform complete citation analysis.
        
        Args:
            manuscript_text: Full text of the manuscript
            references: List of reference dictionaries
            author_names: Optional list of manuscript author names
            
        Returns:
            CitationAnalysisResult object
        """
        # Phase 1: Extract citations
        citations = self.extractor.extract_citations(manuscript_text, references)
        
        # Phase 2: Build citation graph
        graph = self.graph_builder.build_graph(citations, references)
        
        # Phase 3: Detect patterns
        patterns = self.pattern_detector.detect_patterns(graph, citations)
        
        # Calculate metrics
        total_citations = len(citations)
        unique_citations = len(set(c.reference_id for c in citations))
        
        # Detect self-citations
        self_citations = self._count_self_citations(
            citations, references, author_names or []
        )
        self_citation_rate = self_citations / max(total_citations, 1)
        
        # Find citation clusters
        clusters = self._find_clusters(graph)
        
        # Calculate network density
        density = self._calculate_network_density(graph)
        
        # Analyze temporal distribution
        temporal_dist = self._analyze_temporal_distribution(references)
        
        # Calculate citation diversity
        diversity = self._calculate_citation_diversity(citations, references)
        
        # Calculate risk score
        risk_score = self._calculate_citation_risk_score(
            self_citation_rate,
            patterns,
            density,
            diversity
        )
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            self_citation_rate,
            patterns,
            diversity,
            temporal_dist
        )
        
        return CitationAnalysisResult(
            manuscript_id="manuscript",
            total_citations=total_citations,
            unique_citations=unique_citations,
            self_citations=self_citations,
            self_citation_rate=self_citation_rate,
            citation_clusters=clusters,
            suspicious_patterns=[p for p in patterns if p.suspicion_score > 0.5],
            citation_network_density=density,
            temporal_distribution=temporal_dist,
            author_citation_diversity=diversity,
            analysis_timestamp=datetime.now(),
            risk_score=risk_score,
            recommendations=recommendations
        )
    
    def _count_self_citations(
        self,
        citations: List[ExtractedCitation],
        references: List[Dict],
        author_names: List[str]
    ) -> int:
        """
        Count self-citations in the manuscript.
        
        Proprietary self-citation detection algorithm.
        """
        if not author_names:
            return 0
        
        # Normalize author names
        normalized_authors = set(name.lower().split()[-1] for name in author_names)
        
        self_count = 0
        for ref in references:
            ref_authors = ref.get('authors', [])
            for ref_author in ref_authors:
                # Check last name match
                ref_lastname = ref_author.lower().split()[-1]
                if ref_lastname in normalized_authors:
                    self_count += 1
                    break
        
        return self_count
    
    def _find_clusters(self, graph: CitationGraph) -> List[Set[str]]:
        """
        Find citation clusters in the graph.
        
        Proprietary clustering algorithm.
        """
        # Simplified clustering: find connected components
        visited = set()
        clusters = []
        
        for node in graph.nodes:
            if node not in visited:
                cluster = self._explore_cluster(graph, node, visited)
                if len(cluster) > 1:
                    clusters.append(cluster)
        
        return clusters
    
    def _explore_cluster(
        self,
        graph: CitationGraph,
        start_node: str,
        visited: Set[str]
    ) -> Set[str]:
        """Explore a citation cluster using DFS"""
        cluster = set()
        stack = [start_node]
        
        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                cluster.add(node)
                
                # Add connected nodes
                neighbors = graph.get_neighbors(node)
                stack.extend(n for n in neighbors if n not in visited)
        
        return cluster
    
    def _calculate_network_density(self, graph: CitationGraph) -> float:
        """
        Calculate citation network density.
        
        Proprietary density metric.
        """
        num_nodes = len(graph.nodes)
        if num_nodes < 2:
            return 0.0
        
        num_edges = len(graph.edges)
        max_edges = num_nodes * (num_nodes - 1)  # For directed graph
        
        return num_edges / max_edges if max_edges > 0 else 0.0
    
    def _analyze_temporal_distribution(self, references: List[Dict]) -> Dict[int, int]:
        """
        Analyze temporal distribution of citations.
        
        Returns dictionary mapping years to citation counts.
        """
        distribution = {}
        
        for ref in references:
            year = ref.get('year')
            if year:
                distribution[year] = distribution.get(year, 0) + 1
        
        return distribution
    
    def _calculate_citation_diversity(
        self,
        citations: List[ExtractedCitation],
        references: List[Dict]
    ) -> float:
        """
        Calculate citation diversity score.
        
        Proprietary diversity metric measuring breadth of citations.
        Returns score from 0.0 (low diversity) to 1.0 (high diversity).
        """
        if not references:
            return 0.0
        
        # Count unique venues
        venues = set()
        for ref in references:
            venue = ref.get('venue')
            if venue:
                venues.add(venue.lower())
        
        # Count unique authors
        authors = set()
        for ref in references:
            ref_authors = ref.get('authors', [])
            for author in ref_authors:
                authors.add(author.lower())
        
        # Calculate diversity (proprietary formula)
        venue_diversity = min(len(venues) / max(len(references), 1), 1.0)
        author_diversity = min(len(authors) / (len(references) * 2), 1.0)
        
        # Weighted combination
        diversity = venue_diversity * 0.6 + author_diversity * 0.4
        
        return diversity
    
    def _calculate_citation_risk_score(
        self,
        self_citation_rate: float,
        patterns: List[CitationPattern],
        density: float,
        diversity: float
    ) -> float:
        """
        Proprietary risk scoring algorithm for citation behavior.
        
        Returns risk score from 0.0 (low risk) to 1.0 (high risk).
        """
        risk = 0.0
        
        # Self-citation risk (excessive self-citation)
        if self_citation_rate > 0.3:
            risk += 0.3
        elif self_citation_rate > 0.2:
            risk += 0.15
        
        # Pattern risk (suspicious citation patterns)
        suspicious_patterns = [p for p in patterns if p.suspicion_score > 0.5]
        risk += min(len(suspicious_patterns) * 0.15, 0.4)
        
        # Clustering risk (excessive citation clustering)
        if density > 0.7:
            risk += 0.15
        
        # Diversity risk (low citation diversity)
        if diversity < 0.3:
            risk += 0.15
        
        return min(risk, 1.0)
    
    def _generate_recommendations(
        self,
        self_citation_rate: float,
        patterns: List[CitationPattern],
        diversity: float,
        temporal_dist: Dict[int, int]
    ) -> List[str]:
        """Generate recommendations based on citation analysis"""
        recommendations = []
        
        if self_citation_rate > 0.3:
            recommendations.append(
                f"Self-citation rate is high ({self_citation_rate:.1%}). "
                "Consider citing more diverse sources."
            )
        
        if diversity < 0.4:
            recommendations.append(
                "Citation diversity is low. Expand literature review to include "
                "more venues and authors."
            )
        
        if temporal_dist:
            recent_years = [y for y in temporal_dist.keys() if y >= datetime.now().year - 3]
            if not recent_years:
                recommendations.append(
                    "Consider including more recent references (last 3 years)."
                )
        
        suspicious_patterns = [p for p in patterns if p.suspicion_score > 0.6]
        if suspicious_patterns:
            recommendations.append(
                f"Detected {len(suspicious_patterns)} suspicious citation patterns. "
                "Review citation practices for potential manipulation."
            )
        
        return recommendations
