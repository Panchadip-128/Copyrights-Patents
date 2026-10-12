"""
Researcher Auditor - bounded-DFS citation-loop detection and loop-purged h-index decomposition
"""

from .researcher_auditor import (
    AuthorCitationGraph,
    CitationLoop,
    ResearcherAuditor,
    ResearcherAuditResult,
    h_index,
)

__all__ = ['AuthorCitationGraph', 'CitationLoop', 'ResearcherAuditor', 'ResearcherAuditResult', 'h_index']
