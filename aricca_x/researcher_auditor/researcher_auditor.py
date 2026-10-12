"""
Researcher Auditing Module (Module B)

Deterministic citation-network audit of an individual researcher:

  1. Bounded-depth DFS enumeration of directed author citation loops
     (2 <= loop length <= max_depth, preferred max_depth = 5).  Each simple
     cycle is enumerated exactly once, starting from its minimum node, so the
     result is canonical and order-independent.
  2. Four-way citation decomposition relative to the target author, applied
     in strict priority order:
         SELF        target is an author of the citing paper
         CO_AUTHOR   a citing author has co-authored with the target
         LOOP        a citing author is a member of a detected citation loop
                     that passes through the target
         INDEPENDENT none of the above
  3. Index family:
         h_standard           all citations
         h_true_independent   excludes SELF and CO_AUTHOR (True Independent H-Index)
         h_loop_purged        additionally excludes LOOP citations
  4. Ratios:
         CIR   = (INDEPENDENT + LOOP) / total     -> INFLATION_ALERT if < 0.30
         LACIR = INDEPENDENT / total              -> LOOP_INFLATION_ALERT if < 0.30

Distinguishing feature: Schreiber (2007) removes self/co-author citations but
expressly notes the sharpened index "can still be inflated by reciprocal
citing between colleagues".  The loop-purged index closes exactly that gap by
coupling the graph-cycle result to the h-index recomputation.  Unlike Kojaku
et al. (2021, journal-level null model) and Spanakis et al. (2026, isolation
forest), no statistical model or ML classifier is used.

Copyright (c) 2026. All rights reserved. Patent Pending.
"""

from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Mapping, Optional, Sequence, Set, Tuple

from ..deterministic_core import DEFAULT_REGISTRY, RuleRegistry

SELF = "self"
CO_AUTHOR = "co_author"
LOOP = "loop"
INDEPENDENT = "independent"


def h_index(citation_counts: Iterable[int]) -> int:
    """Largest h such that h papers have at least h citations each."""
    h = 0
    for rank, count in enumerate(sorted(citation_counts, reverse=True), start=1):
        if count >= rank:
            h = rank
        else:
            break
    return h


@dataclass(frozen=True)
class CitationLoop:
    members: Tuple[str, ...]          # canonical rotation: starts at the minimum node
    length: int
    bottleneck_weight: int            # min edge weight around the loop
    edges: Tuple[Tuple[str, str, int], ...]


class _CycleBudgetExceeded(Exception):
    pass


class AuthorCitationGraph:
    """Directed, weighted author -> author citation graph."""

    def __init__(self) -> None:
        self._adjacency: Dict[str, Dict[str, int]] = {}

    def add_citation(self, citing_author: str, cited_author: str, count: int = 1) -> None:
        citing_author, cited_author = citing_author.strip(), cited_author.strip()
        if not citing_author or not cited_author or citing_author == cited_author:
            return  # self-citations are handled by the decomposition, not as graph loops
        self._adjacency.setdefault(citing_author, {})
        self._adjacency.setdefault(cited_author, {})
        self._adjacency[citing_author][cited_author] = (
            self._adjacency[citing_author].get(cited_author, 0) + int(count)
        )

    def nodes(self) -> List[str]:
        return sorted(self._adjacency)

    def successors(self, node: str) -> List[Tuple[str, int]]:
        return sorted(self._adjacency.get(node, {}).items())

    def weight(self, citing_author: str, cited_author: str) -> int:
        return self._adjacency.get(citing_author, {}).get(cited_author, 0)

    @property
    def edge_count(self) -> int:
        return sum(len(v) for v in self._adjacency.values())

    @classmethod
    def from_edges(cls, edges: Iterable) -> "AuthorCitationGraph":
        graph = cls()
        for edge in edges:
            if isinstance(edge, Mapping):
                graph.add_citation(edge["from"], edge["to"], int(edge.get("count", 1)))
            else:
                citing, cited = edge[0], edge[1]
                graph.add_citation(citing, cited, int(edge[2]) if len(edge) > 2 else 1)
        return graph

    @classmethod
    def from_publications(cls, publications: Sequence[Mapping]) -> "AuthorCitationGraph":
        graph = cls()
        for pub in publications:
            cited_authors = sorted(set(pub.get("authors", [])))
            for citation in pub.get("citations", []):
                for citing in sorted(set(citation.get("citing_authors", []))):
                    for cited in cited_authors:
                        graph.add_citation(citing, cited, 1)
        return graph

    def find_loops(self, max_depth: int = 5, through: Optional[str] = None,
                   max_cycles: int = 10000) -> Tuple[List[CitationLoop], bool]:
        """
        Bounded-depth DFS enumeration of simple directed cycles.

        A cycle is reported only from its minimum node (in sorted order) and the
        DFS only extends to nodes greater than that start node, so every cycle
        is produced exactly once.  Recursion depth never exceeds max_depth.
        Returns (loops, truncated).
        """
        if max_depth < 2:
            return [], False
        order = {node: idx for idx, node in enumerate(self.nodes())}
        loops: List[CitationLoop] = []

        def record(path: List[str]) -> None:
            edges = tuple(
                (path[i], path[(i + 1) % len(path)], self.weight(path[i], path[(i + 1) % len(path)]))
                for i in range(len(path))
            )
            loops.append(CitationLoop(
                members=tuple(path),
                length=len(path),
                bottleneck_weight=min(e[2] for e in edges),
                edges=edges,
            ))
            if len(loops) >= max_cycles:
                raise _CycleBudgetExceeded()

        def dfs(start: str, current: str, path: List[str], on_path: Set[str]) -> None:
            for successor, _ in self.successors(current):
                if successor == start and len(path) >= 2:
                    record(path)
                elif (order[successor] > order[start] and successor not in on_path
                      and len(path) < max_depth):
                    path.append(successor)
                    on_path.add(successor)
                    dfs(start, successor, path, on_path)
                    on_path.discard(successor)
                    path.pop()

        truncated = False
        try:
            for start in self.nodes():
                dfs(start, start, [start], {start})
        except _CycleBudgetExceeded:
            truncated = True

        if through is not None:
            loops = [loop for loop in loops if through in loop.members]
        return loops, truncated


@dataclass
class ResearcherAuditResult:
    target_author: str
    publication_count: int
    total_citations: int
    self_citations: int
    coauthor_citations: int
    loop_citations: int
    independent_citations: int
    h_index_standard: int
    h_index_true_independent: int
    h_index_loop_purged: int
    citation_independence_ratio: Optional[float]
    loop_adjusted_cir: Optional[float]
    inflation_alert: bool
    loop_inflation_alert: bool
    loops: List[CitationLoop]
    loop_members: List[str]
    loops_truncated: bool
    max_depth: int
    credibility_signal: Optional[float]
    flags: List[str] = field(default_factory=list)
    justification: List[str] = field(default_factory=list)
    per_publication: List[Dict] = field(default_factory=list)


class ResearcherAuditor:
    """Runs the deterministic researcher audit."""

    def __init__(self, rules: RuleRegistry = DEFAULT_REGISTRY):
        self.max_depth = int(rules.param("RA-DFS", "max_depth"))
        self.max_cycles = int(rules.param("RA-DFS", "max_cycles"))
        self.alert_threshold = rules.param("RA-CIR", "alert_threshold")
        self.healthy_reference = rules.param("RA-CIR", "healthy_reference")

    @staticmethod
    def classify_citation(citing_authors: Iterable[str], target: str,
                          coauthors: Set[str], loop_members: Set[str]) -> str:
        citing = {a.strip() for a in citing_authors}
        if target in citing:
            return SELF
        if citing & coauthors:
            return CO_AUTHOR
        if citing & loop_members:
            return LOOP
        return INDEPENDENT

    def audit(self, target_author: str, publications: Sequence[Mapping],
              author_citation_edges: Optional[Iterable] = None) -> ResearcherAuditResult:
        target = target_author.strip()
        own_pubs = sorted(
            (p for p in publications if target in {a.strip() for a in p.get("authors", [])}),
            key=lambda p: str(p.get("paper_id", "")),
        )
        coauthors = {
            a.strip() for p in own_pubs for a in p.get("authors", []) if a.strip() != target
        }

        graph = (AuthorCitationGraph.from_edges(author_citation_edges)
                 if author_citation_edges is not None
                 else AuthorCitationGraph.from_publications(publications))
        loops, truncated = graph.find_loops(self.max_depth, through=target, max_cycles=self.max_cycles)
        loop_members = sorted({m for loop in loops for m in loop.members if m != target})
        loop_member_set = set(loop_members)

        totals = {SELF: 0, CO_AUTHOR: 0, LOOP: 0, INDEPENDENT: 0}
        per_pub: List[Dict] = []
        all_counts, tih_counts, lp_counts = [], [], []
        for pub in own_pubs:
            buckets = {SELF: 0, CO_AUTHOR: 0, LOOP: 0, INDEPENDENT: 0}
            for citation in pub.get("citations", []):
                category = self.classify_citation(
                    citation.get("citing_authors", []), target, coauthors, loop_member_set
                )
                buckets[category] += 1
            for key in totals:
                totals[key] += buckets[key]
            total = sum(buckets.values())
            all_counts.append(total)
            tih_counts.append(buckets[LOOP] + buckets[INDEPENDENT])
            lp_counts.append(buckets[INDEPENDENT])
            per_pub.append({"paper_id": pub.get("paper_id", ""), "total": total, **buckets})

        total_citations = sum(totals.values())
        h_std, h_tih, h_lp = h_index(all_counts), h_index(tih_counts), h_index(lp_counts)

        justification = [
            f"Bounded DFS (max_depth={self.max_depth}) over {len(graph.nodes())} authors / "
            f"{graph.edge_count} edges -> {len(loops)} loop(s) through '{target}'",
            f"Decomposition: self={totals[SELF]}, co-author={totals[CO_AUTHOR]}, "
            f"loop={totals[LOOP]}, independent={totals[INDEPENDENT]} (total={total_citations})",
            f"h_standard={h_std}, h_true_independent={h_tih}, h_loop_purged={h_lp}",
        ]

        flags: List[str] = []
        if total_citations > 0:
            cir = (totals[INDEPENDENT] + totals[LOOP]) / total_citations
            lacir = totals[INDEPENDENT] / total_citations
            inflation = cir < self.alert_threshold
            loop_inflation = lacir < self.alert_threshold
            justification.append(
                f"CIR = ({totals[INDEPENDENT]} + {totals[LOOP]}) / {total_citations} = {cir:.4f}"
                f" {'<' if inflation else '>='} {self.alert_threshold:.2f}"
            )
            justification.append(
                f"LACIR = {totals[INDEPENDENT]} / {total_citations} = {lacir:.4f}"
                f" {'<' if loop_inflation else '>='} {self.alert_threshold:.2f}"
            )
            retention = (h_lp / h_std) if h_std > 0 else 1.0
            signal = 0.6 * min(1.0, lacir / self.healthy_reference) + 0.4 * retention
            justification.append(
                f"s_researcher = 0.6*min(1, {lacir:.4f}/{self.healthy_reference:.2f}) + "
                f"0.4*({h_lp}/{h_std if h_std else 1}) = {signal:.4f}"
            )
        else:
            cir = lacir = None
            inflation = loop_inflation = False
            signal = None
            justification.append("No citations: CIR/LACIR UNKNOWN, researcher signal UNKNOWN")

        if inflation:
            flags.append("RA_INFLATION_ALERT")
        if loop_inflation:
            flags.append("RA_LOOP_INFLATION_ALERT")
        if loops:
            flags.append("RA_CITATION_LOOP_DETECTED")
        if h_std - h_lp >= 2:
            flags.append("RA_H_INDEX_INFLATION")
        if truncated:
            flags.append("RA_LOOP_ENUMERATION_TRUNCATED")

        return ResearcherAuditResult(
            target_author=target,
            publication_count=len(own_pubs),
            total_citations=total_citations,
            self_citations=totals[SELF],
            coauthor_citations=totals[CO_AUTHOR],
            loop_citations=totals[LOOP],
            independent_citations=totals[INDEPENDENT],
            h_index_standard=h_std,
            h_index_true_independent=h_tih,
            h_index_loop_purged=h_lp,
            citation_independence_ratio=cir,
            loop_adjusted_cir=lacir,
            inflation_alert=inflation,
            loop_inflation_alert=loop_inflation,
            loops=loops,
            loop_members=loop_members,
            loops_truncated=truncated,
            max_depth=self.max_depth,
            credibility_signal=signal,
            flags=sorted(flags),
            justification=justification,
            per_publication=per_pub,
        )
