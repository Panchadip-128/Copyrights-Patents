"""
Graph Builder - Builds citation graphs from extracted data

Implements proprietary graph construction algorithms.
Copyright (c) 2026. All rights reserved.
"""

from typing import Dict, List, Set, Tuple, Optional
from dataclasses import dataclass, field


@dataclass
class CitationGraph:
    """Represents a citation network graph"""
    nodes: Set[str]  # Reference IDs
    edges: List[Tuple[str, str]]  # (from_ref, to_ref) pairs
    node_attributes: Dict[str, Dict] = field(default_factory=dict)
    edge_attributes: Dict[Tuple[str, str], Dict] = field(default_factory=dict)
    
    def add_node(self, node_id: str, attributes: Optional[Dict] = None):
        """Add node to graph"""
        self.nodes.add(node_id)
        if attributes:
            self.node_attributes[node_id] = attributes
    
    def add_edge(
        self,
        from_node: str,
        to_node: str,
        attributes: Optional[Dict] = None
    ):
        """Add edge to graph"""
        self.edges.append((from_node, to_node))
        if attributes:
            self.edge_attributes[(from_node, to_node)] = attributes
    
    def get_neighbors(self, node_id: str) -> List[str]:
        """Get neighbors of a node"""
        neighbors = []
        for from_node, to_node in self.edges:
            if from_node == node_id:
                neighbors.append(to_node)
            elif to_node == node_id:
                neighbors.append(from_node)
        return neighbors
    
    def get_degree(self, node_id: str) -> int:
        """Get degree of a node"""
        return len(self.get_neighbors(node_id))


class GraphBuilder:
    """
    Builds citation graphs from citation data.
    
    Implements proprietary graph construction and analysis algorithms.
    """
    
    def __init__(self):
        """Initialize the graph builder"""
        pass
    
    def build_graph(
        self,
        citations: List[any],
        references: List[Dict]
    ) -> CitationGraph:
        """
        Build citation graph from citations and references.
        
        Args:
            citations: List of ExtractedCitation objects
            references: List of reference dictionaries
            
        Returns:
            CitationGraph object
        """
        graph = CitationGraph(nodes=set(), edges=[])
        
        # Add nodes (references)
        ref_map = {str(i+1): ref for i, ref in enumerate(references)}
        
        for ref_id, ref in ref_map.items():
            attributes = {
                'title': ref.get('title', ''),
                'year': ref.get('year'),
                'authors': ref.get('authors', []),
                'venue': ref.get('venue', '')
            }
            graph.add_node(ref_id, attributes)
        
        # Add edges (co-citations and coupling)
        self._add_co_citation_edges(graph, citations)
        self._add_bibliographic_coupling_edges(graph, references)
        
        return graph
    
    def _add_co_citation_edges(self, graph: CitationGraph, citations: List[any]):
        """
        Add co-citation edges (refs cited together in same context).
        
        Proprietary co-citation analysis.
        """
        # Group citations by context
        context_citations = {}
        
        for citation in citations:
            context = citation.context[:100]  # Use first 100 chars as key
            if context not in context_citations:
                context_citations[context] = []
            context_citations[context].append(citation.reference_id)
        
        # Create edges for co-citations
        for context, ref_ids in context_citations.items():
            if len(ref_ids) > 1:
                # Create edges between all pairs
                for i, ref1 in enumerate(ref_ids):
                    for ref2 in ref_ids[i+1:]:
                        if ref1 in graph.nodes and ref2 in graph.nodes:
                            graph.add_edge(ref1, ref2, {'type': 'co-citation'})
    
    def _add_bibliographic_coupling_edges(
        self,
        graph: CitationGraph,
        references: List[Dict]
    ):
        """
        Add bibliographic coupling edges (refs sharing citations).
        
        Proprietary bibliographic coupling algorithm.
        """
        # In a real implementation, this would analyze the references
        # within each reference to find shared citations
        # For now, we'll use a simplified version based on shared venues
        
        venue_refs = {}
        for i, ref in enumerate(references):
            venue = ref.get('venue', '').lower()
            if venue:
                if venue not in venue_refs:
                    venue_refs[venue] = []
                venue_refs[venue].append(str(i+1))
        
        # Create edges between refs in same venue (simplified coupling)
        for venue, ref_ids in venue_refs.items():
            if len(ref_ids) > 1:
                for i, ref1 in enumerate(ref_ids):
                    for ref2 in ref_ids[i+1:]:
                        if ref1 in graph.nodes and ref2 in graph.nodes:
                            # Only add if not already connected
                            if (ref1, ref2) not in graph.edges and (ref2, ref1) not in graph.edges:
                                graph.add_edge(ref1, ref2, {'type': 'coupling'})
