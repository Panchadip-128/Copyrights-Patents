"""
Compliance Checker - Checks manuscript compliance against style guides

Implements proprietary compliance checking algorithms.
Copyright (c) 2026. All rights reserved.
"""

import re
from typing import List, Dict
from dataclasses import dataclass
from enum import Enum
from .manuscript_parser import ParsedManuscript, ManuscriptSection


class IssueSeverity(Enum):
    """Severity levels for compliance issues"""
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass
class ComplianceIssue:
    """Represents a compliance issue found in the manuscript"""
    issue_id: str
    severity: str
    category: str
    message: str
    location: str
    line_number: int = 0
    suggestion: str = ""


class ComplianceChecker:
    """
    Checks manuscripts for compliance with formatting and style guidelines.
    
    Implements proprietary rule-based checking algorithms.
    """
    
    # Proprietary style guide rules (copyright-protected)
    STYLE_GUIDES = {
        'IEEE': {
            'max_pages': 8,
            'max_title_length': 150,
            'min_abstract_words': 150,
            'max_abstract_words': 250,
            'required_sections': ['introduction', 'conclusion', 'references'],
            'min_references': 10,
            'citation_style': 'numbered'
        },
        'ACM': {
            'max_pages': 10,
            'max_title_length': 200,
            'min_abstract_words': 150,
            'max_abstract_words': 300,
            'required_sections': ['introduction', 'related work', 'conclusion', 'references'],
            'min_references': 15,
            'citation_style': 'numbered'
        }
    }
    
    def __init__(self, style_guide: str = "IEEE"):
        """Initialize compliance checker with style guide"""
        self.style_guide = style_guide
        self.rules = self.STYLE_GUIDES.get(style_guide, self.STYLE_GUIDES['IEEE'])
    
    def check_formatting(self, manuscript: ParsedManuscript) -> List[ComplianceIssue]:
        """Check formatting compliance"""
        issues = []
        
        # Check page count
        if manuscript.metadata.page_count > self.rules['max_pages']:
            issues.append(ComplianceIssue(
                issue_id="FMT001",
                severity=IssueSeverity.ERROR.value,
                category="formatting",
                message=f"Page count ({manuscript.metadata.page_count}) exceeds maximum ({self.rules['max_pages']})",
                location="document",
                suggestion=f"Reduce document to {self.rules['max_pages']} pages or fewer"
            ))
        
        # Check title length
        if manuscript.metadata.title:
            title_len = len(manuscript.metadata.title)
            if title_len > self.rules['max_title_length']:
                issues.append(ComplianceIssue(
                    issue_id="FMT002",
                    severity=IssueSeverity.WARNING.value,
                    category="formatting",
                    message=f"Title length ({title_len}) exceeds recommended maximum ({self.rules['max_title_length']})",
                    location="title",
                    suggestion="Consider shortening the title"
                ))
        
        # Check abstract length
        if manuscript.metadata.abstract:
            abstract_words = len(manuscript.metadata.abstract.split())
            if abstract_words < self.rules['min_abstract_words']:
                issues.append(ComplianceIssue(
                    issue_id="FMT003",
                    severity=IssueSeverity.WARNING.value,
                    category="formatting",
                    message=f"Abstract is too short ({abstract_words} words, minimum {self.rules['min_abstract_words']})",
                    location="abstract",
                    suggestion="Expand abstract to provide more detail"
                ))
            elif abstract_words > self.rules['max_abstract_words']:
                issues.append(ComplianceIssue(
                    issue_id="FMT004",
                    severity=IssueSeverity.WARNING.value,
                    category="formatting",
                    message=f"Abstract is too long ({abstract_words} words, maximum {self.rules['max_abstract_words']})",
                    location="abstract",
                    suggestion="Condense abstract to key points"
                ))
        
        return issues
    
    def check_references(self, manuscript: ParsedManuscript) -> List[ComplianceIssue]:
        """Check reference compliance"""
        issues = []
        
        # Check reference count
        ref_count = len(manuscript.references)
        if ref_count < self.rules['min_references']:
            issues.append(ComplianceIssue(
                issue_id="REF001",
                severity=IssueSeverity.WARNING.value,
                category="references",
                message=f"Reference count ({ref_count}) below recommended minimum ({self.rules['min_references']})",
                location="references",
                suggestion="Add more references to support your work"
            ))
        
        # Check for references without years
        for ref in manuscript.references:
            if not ref.year:
                issues.append(ComplianceIssue(
                    issue_id="REF002",
                    severity=IssueSeverity.WARNING.value,
                    category="references",
                    message=f"Reference [{ref.ref_id}] missing publication year",
                    location=f"reference {ref.ref_id}",
                    suggestion="Add publication year to reference"
                ))
        
        # Check citation-reference consistency
        if manuscript.citation_count > len(manuscript.references):
            issues.append(ComplianceIssue(
                issue_id="REF003",
                severity=IssueSeverity.ERROR.value,
                category="references",
                message=f"More in-text citations ({manuscript.citation_count}) than references ({len(manuscript.references)})",
                location="references",
                suggestion="Ensure all cited works are in reference list"
            ))
        
        return issues
    
    def check_structure(self, manuscript: ParsedManuscript) -> List[ComplianceIssue]:
        """Check document structure compliance"""
        issues = []
        
        # Check for required sections
        section_titles_lower = [s.title.lower() for s in manuscript.sections]
        
        for required_section in self.rules['required_sections']:
            if not any(required_section in title for title in section_titles_lower):
                issues.append(ComplianceIssue(
                    issue_id="STR001",
                    severity=IssueSeverity.ERROR.value,
                    category="structure",
                    message=f"Required section missing: {required_section.title()}",
                    location="document structure",
                    suggestion=f"Add {required_section.title()} section"
                ))
        
        # Check section ordering (Introduction should be first major section)
        if manuscript.sections:
            first_section = manuscript.sections[0].title.lower()
            if 'introduction' not in first_section and 'intro' not in first_section:
                issues.append(ComplianceIssue(
                    issue_id="STR002",
                    severity=IssueSeverity.WARNING.value,
                    category="structure",
                    message="First major section should be Introduction",
                    location="section 1",
                    suggestion="Ensure Introduction is the first major section"
                ))
        
        # Check for very short sections
        for section in manuscript.sections:
            if section.word_count < 50 and section.level == 1:
                issues.append(ComplianceIssue(
                    issue_id="STR003",
                    severity=IssueSeverity.INFO.value,
                    category="structure",
                    message=f"Section '{section.title}' is very short ({section.word_count} words)",
                    location=f"section '{section.title}'",
                    suggestion="Consider expanding or merging this section"
                ))
        
        return issues
    
    def check_metadata(self, manuscript: ParsedManuscript) -> List[ComplianceIssue]:
        """Check metadata compliance"""
        issues = []
        
        # Check for missing title
        if not manuscript.metadata.title:
            issues.append(ComplianceIssue(
                issue_id="META001",
                severity=IssueSeverity.ERROR.value,
                category="metadata",
                message="Document title is missing",
                location="metadata",
                suggestion="Add document title"
            ))
        
        # Check for missing abstract
        if not manuscript.metadata.abstract:
            issues.append(ComplianceIssue(
                issue_id="META002",
                severity=IssueSeverity.ERROR.value,
                category="metadata",
                message="Abstract is missing",
                location="metadata",
                suggestion="Add abstract section"
            ))
        
        # Check for keywords
        if not manuscript.metadata.keywords:
            issues.append(ComplianceIssue(
                issue_id="META003",
                severity=IssueSeverity.WARNING.value,
                category="metadata",
                message="Keywords are missing",
                location="metadata",
                suggestion="Add 3-5 keywords"
            ))
        elif len(manuscript.metadata.keywords) < 3:
            issues.append(ComplianceIssue(
                issue_id="META004",
                severity=IssueSeverity.INFO.value,
                category="metadata",
                message=f"Only {len(manuscript.metadata.keywords)} keywords provided (3-5 recommended)",
                location="metadata",
                suggestion="Add more keywords"
            ))
        
        return issues
