"""
Compilation Report Generator - Generates compliance compilation reports

Implements proprietary report generation algorithms.
Copyright (c) 2026. All rights reserved.
"""

from typing import List, Dict, Optional
from dataclasses import dataclass, field
from datetime import datetime
from .manuscript_parser import ParsedManuscript
from .compliance_checker import ComplianceIssue


@dataclass
class CompilationReport:
    """Complete compilation report for a manuscript"""
    manuscript_path: str
    manuscript_title: Optional[str]
    compilation_status: str  # "success", "warning", "error"
    is_compliant: bool
    compliance_score: float
    issues: List[ComplianceIssue]
    statistics: Dict[str, any]
    generation_timestamp: datetime
    error_summary: Dict[str, int] = field(default_factory=dict)
    warning_summary: Dict[str, int] = field(default_factory=dict)


class CompilationReportGenerator:
    """
    Generates compilation reports for manuscript compliance analysis.
    
    Implements proprietary report generation and formatting algorithms.
    """
    
    def __init__(self):
        """Initialize the report generator"""
        pass
    
    def generate_report(
        self,
        manuscript: ParsedManuscript,
        issues: List[ComplianceIssue],
        config: any
    ) -> CompilationReport:
        """
        Generate a comprehensive compilation report.
        
        Args:
            manuscript: Parsed manuscript
            issues: List of compliance issues found
            config: Compiler configuration
            
        Returns:
            CompilationReport object
        """
        # Categorize issues
        errors = [i for i in issues if i.severity == 'error']
        warnings = [i for i in issues if i.severity == 'warning']
        infos = [i for i in issues if i.severity == 'info']
        
        # Determine compilation status
        if errors:
            status = "error"
            is_compliant = False
        elif warnings:
            status = "warning"
            is_compliant = not config.strict_mode
        else:
            status = "success"
            is_compliant = True
        
        # Calculate compliance score
        compliance_score = self._calculate_compliance_score(
            manuscript, errors, warnings, infos
        )
        
        # Generate statistics
        statistics = self._generate_statistics(manuscript, issues)
        
        # Generate summaries
        error_summary = self._categorize_issues(errors)
        warning_summary = self._categorize_issues(warnings)
        
        return CompilationReport(
            manuscript_path=manuscript.file_path,
            manuscript_title=manuscript.metadata.title,
            compilation_status=status,
            is_compliant=is_compliant,
            compliance_score=compliance_score,
            issues=issues,
            statistics=statistics,
            generation_timestamp=datetime.now(),
            error_summary=error_summary,
            warning_summary=warning_summary
        )
    
    def generate_error_report(
        self,
        manuscript_path: str,
        error_message: str
    ) -> CompilationReport:
        """Generate a report for compilation errors"""
        return CompilationReport(
            manuscript_path=manuscript_path,
            manuscript_title=None,
            compilation_status="error",
            is_compliant=False,
            compliance_score=0.0,
            issues=[ComplianceIssue(
                issue_id="FATAL001",
                severity="error",
                category="compilation",
                message=f"Compilation failed: {error_message}",
                location="document",
                suggestion="Check file format and accessibility"
            )],
            statistics={},
            generation_timestamp=datetime.now()
        )
    
    def _calculate_compliance_score(
        self,
        manuscript: ParsedManuscript,
        errors: List[ComplianceIssue],
        warnings: List[ComplianceIssue],
        infos: List[ComplianceIssue]
    ) -> float:
        """
        Proprietary compliance scoring algorithm.
        
        Returns score from 0.0 (non-compliant) to 1.0 (fully compliant).
        """
        # Start with perfect score
        score = 1.0
        
        # Deduct for errors (major impact)
        score -= len(errors) * 0.15
        
        # Deduct for warnings (moderate impact)
        score -= len(warnings) * 0.05
        
        # Deduct for info issues (minor impact)
        score -= len(infos) * 0.01
        
        # Bonus for good practices
        if manuscript.metadata.abstract:
            score += 0.05
        if len(manuscript.metadata.keywords) >= 3:
            score += 0.03
        if len(manuscript.references) >= 15:
            score += 0.05
        if len(manuscript.sections) >= 5:
            score += 0.03
        
        return max(0.0, min(score, 1.0))
    
    def _generate_statistics(
        self,
        manuscript: ParsedManuscript,
        issues: List[ComplianceIssue]
    ) -> Dict[str, any]:
        """Generate statistics about the manuscript and issues"""
        return {
            'manuscript': {
                'pages': manuscript.metadata.page_count,
                'words': manuscript.metadata.word_count,
                'sections': len(manuscript.sections),
                'references': len(manuscript.references),
                'figures': manuscript.figures_count,
                'tables': manuscript.tables_count,
                'equations': manuscript.equations_count,
                'citations': manuscript.citation_count
            },
            'issues': {
                'total': len(issues),
                'errors': sum(1 for i in issues if i.severity == 'error'),
                'warnings': sum(1 for i in issues if i.severity == 'warning'),
                'info': sum(1 for i in issues if i.severity == 'info')
            },
            'parse_quality': {
                'confidence': manuscript.parse_confidence,
                'has_title': manuscript.metadata.title is not None,
                'has_abstract': manuscript.metadata.abstract is not None,
                'has_keywords': len(manuscript.metadata.keywords) > 0
            }
        }
    
    def _categorize_issues(self, issues: List[ComplianceIssue]) -> Dict[str, int]:
        """Categorize issues by category"""
        categories = {}
        for issue in issues:
            category = issue.category
            categories[category] = categories.get(category, 0) + 1
        return categories
    
    def format_report_text(self, report: CompilationReport) -> str:
        """
        Format report as human-readable text.
        
        Proprietary formatting algorithm.
        """
        lines = []
        
        # Header
        lines.append("=" * 80)
        lines.append("ARICCA-X COMPLIANCE COMPILATION REPORT")
        lines.append("=" * 80)
        lines.append("")
        
        # Manuscript info
        lines.append(f"Manuscript: {report.manuscript_path}")
        if report.manuscript_title:
            lines.append(f"Title: {report.manuscript_title}")
        lines.append(f"Compilation Status: {report.compilation_status.upper()}")
        lines.append(f"Compliance Score: {report.compliance_score:.2%}")
        lines.append(f"Is Compliant: {'YES' if report.is_compliant else 'NO'}")
        lines.append("")
        
        # Statistics
        if report.statistics:
            lines.append("DOCUMENT STATISTICS")
            lines.append("-" * 40)
            ms = report.statistics.get('manuscript', {})
            lines.append(f"  Pages: {ms.get('pages', 0)}")
            lines.append(f"  Words: {ms.get('words', 0)}")
            lines.append(f"  Sections: {ms.get('sections', 0)}")
            lines.append(f"  References: {ms.get('references', 0)}")
            lines.append(f"  Figures: {ms.get('figures', 0)}")
            lines.append(f"  Tables: {ms.get('tables', 0)}")
            lines.append("")
        
        # Issues
        if report.issues:
            lines.append(f"ISSUES FOUND: {len(report.issues)}")
            lines.append("-" * 40)
            
            # Group by severity
            for severity in ['error', 'warning', 'info']:
                severity_issues = [i for i in report.issues if i.severity == severity]
                if severity_issues:
                    lines.append(f"\n{severity.upper()}S: {len(severity_issues)}")
                    for issue in severity_issues:
                        lines.append(f"  [{issue.issue_id}] {issue.message}")
                        if issue.location != "document":
                            lines.append(f"      Location: {issue.location}")
                        if issue.suggestion:
                            lines.append(f"      Suggestion: {issue.suggestion}")
                        lines.append("")
        else:
            lines.append("NO ISSUES FOUND - EXCELLENT!")
            lines.append("")
        
        # Footer
        lines.append("=" * 80)
        lines.append(f"Report generated: {report.generation_timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("=" * 80)
        
        return '\n'.join(lines)
