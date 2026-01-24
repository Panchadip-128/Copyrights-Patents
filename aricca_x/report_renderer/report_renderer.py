"""
Report Renderer - Generates formatted reports in various output formats

Implements proprietary report rendering algorithms.
Copyright (c) 2026. All rights reserved.
"""

from typing import Dict, Optional
from datetime import datetime
from .report_builder import ReportBuilder, Report
from .template_engine import TemplateEngine
from .export_handler import ExportHandler, ExportFormat


class ReportRenderer:
    """
    Generates formatted reports in multiple output formats.
    
    Implements proprietary rendering algorithms for HTML, PDF, JSON, and text.
    """
    
    def __init__(self):
        """Initialize the report renderer"""
        self.builder = ReportBuilder()
        self.template_engine = TemplateEngine()
        self.export_handler = ExportHandler()
    
    def render_assessment_report(
        self,
        assessment_data: Dict,
        output_format: str = "text",
        include_recommendations: bool = True,
        include_evidence: bool = True
    ) -> str:
        """
        Render a complete assessment report.
        
        Args:
            assessment_data: Assessment data dictionary
            output_format: Output format ("text", "html", "json", "markdown")
            include_recommendations: Include recommendations section
            include_evidence: Include evidence section
            
        Returns:
            Formatted report string
        """
        # Build report structure
        report = self.builder.build_assessment_report(
            assessment_data,
            include_recommendations,
            include_evidence
        )
        
        # Render using appropriate template
        if output_format == "html":
            return self.template_engine.render_html(report)
        elif output_format == "json":
            return self.export_handler.export_json(report)
        elif output_format == "markdown":
            return self.template_engine.render_markdown(report)
        else:  # text
            return self.template_engine.render_text(report)
    
    def render_comparison_report(
        self,
        comparison_data: Dict,
        output_format: str = "text"
    ) -> str:
        """
        Render a venue comparison report.
        
        Args:
            comparison_data: Comparison data from credibility engine
            output_format: Output format
            
        Returns:
            Formatted comparison report
        """
        report = self.builder.build_comparison_report(comparison_data)
        
        if output_format == "html":
            return self.template_engine.render_html(report)
        elif output_format == "json":
            return self.export_handler.export_json(report)
        else:
            return self.template_engine.render_text(report)
    
    def render_compliance_report(
        self,
        compliance_data: Dict,
        output_format: str = "text"
    ) -> str:
        """
        Render a manuscript compliance report.
        
        Args:
            compliance_data: Compliance compilation report data
            output_format: Output format
            
        Returns:
            Formatted compliance report
        """
        report = self.builder.build_compliance_report(compliance_data)
        
        if output_format == "html":
            return self.template_engine.render_html(report)
        elif output_format == "json":
            return self.export_handler.export_json(report)
        else:
            return self.template_engine.render_text(report)
    
    def save_report(
        self,
        report_content: str,
        output_path: str,
        format: ExportFormat = ExportFormat.TEXT
    ) -> bool:
        """
        Save report to file.
        
        Args:
            report_content: Rendered report content
            output_path: Output file path
            format: Export format
            
        Returns:
            Success boolean
        """
        return self.export_handler.save_to_file(report_content, output_path, format)
