"""
Compliance Compiler - Main compilation module for manuscript compliance

Implements proprietary compilation algorithms for manuscript analysis.
Copyright (c) 2026. All rights reserved.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
from .manuscript_parser import ManuscriptParser, ParsedManuscript
from .compliance_checker import ComplianceChecker, ComplianceIssue
from .compilation_report_generator import CompilationReportGenerator, CompilationReport


@dataclass
class CompilerConfiguration:
    """Configuration for the compliance compiler"""
    check_formatting: bool = True
    check_references: bool = True
    check_structure: bool = True
    check_metadata: bool = True
    strict_mode: bool = False
    style_guide: str = "IEEE"  # IEEE, ACM, APA, etc.


class ComplianceCompiler:
    """
    Compiles and validates manuscript submissions for compliance.
    
    This proprietary system converts author submissions into an intermediate
    representation and runs rule-based compliance checks similar to a
    software compiler.
    """
    
    def __init__(self, config: Optional[CompilerConfiguration] = None):
        """
        Initialize the compliance compiler.
        
        Args:
            config: Optional compiler configuration
        """
        self.config = config or CompilerConfiguration()
        self.parser = ManuscriptParser()
        self.checker = ComplianceChecker(self.config.style_guide)
        self.report_generator = CompilationReportGenerator()
    
    def compile(
        self,
        manuscript_path: str,
        manuscript_format: str = "pdf"
    ) -> CompilationReport:
        """
        Compile manuscript and generate compliance report.
        
        This is the main entry point that orchestrates the entire
        compilation process.
        
        Args:
            manuscript_path: Path to manuscript file
            manuscript_format: Format of manuscript ("pdf", "latex", "docx")
            
        Returns:
            CompilationReport with all findings
        """
        # Phase 1: Parse manuscript
        parsed_manuscript = self.parser.parse(manuscript_path, manuscript_format)
        
        # Phase 2: Run compliance checks
        issues = []
        
        if self.config.check_formatting:
            issues.extend(self.checker.check_formatting(parsed_manuscript))
        
        if self.config.check_references:
            issues.extend(self.checker.check_references(parsed_manuscript))
        
        if self.config.check_structure:
            issues.extend(self.checker.check_structure(parsed_manuscript))
        
        if self.config.check_metadata:
            issues.extend(self.checker.check_metadata(parsed_manuscript))
        
        # Phase 3: Generate compilation report
        report = self.report_generator.generate_report(
            manuscript=parsed_manuscript,
            issues=issues,
            config=self.config
        )
        
        return report
    
    def compile_batch(
        self,
        manuscript_paths: List[str],
        manuscript_format: str = "pdf"
    ) -> List[CompilationReport]:
        """
        Compile multiple manuscripts in batch.
        
        Args:
            manuscript_paths: List of manuscript file paths
            manuscript_format: Format of manuscripts
            
        Returns:
            List of CompilationReport objects
        """
        reports = []
        
        for path in manuscript_paths:
            try:
                report = self.compile(path, manuscript_format)
                reports.append(report)
            except Exception as e:
                # Create error report
                error_report = self.report_generator.generate_error_report(
                    manuscript_path=path,
                    error_message=str(e)
                )
                reports.append(error_report)
        
        return reports
    
    def get_compliance_summary(self, report: CompilationReport) -> Dict[str, any]:
        """
        Get a summary of compliance status.
        
        Args:
            report: CompilationReport to summarize
            
        Returns:
            Dictionary with summary statistics
        """
        return {
            'total_issues': len(report.issues),
            'errors': sum(1 for i in report.issues if i.severity == 'error'),
            'warnings': sum(1 for i in report.issues if i.severity == 'warning'),
            'info': sum(1 for i in report.issues if i.severity == 'info'),
            'compliance_score': report.compliance_score,
            'is_compliant': report.is_compliant,
            'compilation_status': report.compilation_status
        }
