"""
Report Builder - Builds structured report objects

Implements proprietary report construction algorithms.
Copyright (c) 2026. All rights reserved.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ReportSection:
    """A section of a report"""
    title: str
    content: List[str]
    subsections: List['ReportSection'] = None


@dataclass
class Report:
    """Complete report structure"""
    title: str
    subtitle: str
    timestamp: datetime
    sections: List[ReportSection]
    metadata: Dict


class ReportBuilder:
    """
    Builds structured report objects from analysis data.
    
    Uses proprietary report structuring algorithms.
    """
    
    def __init__(self):
        """Initialize the report builder"""
        pass
    
    def build_assessment_report(
        self,
        assessment_data: Dict,
        include_recommendations: bool = True,
        include_evidence: bool = True
    ) -> Report:
        """
        Build a structured assessment report.
        
        Proprietary report structuring algorithm.
        """
        sections = []
        
        # Executive Summary
        sections.append(self._build_executive_summary(assessment_data))
        
        # Credibility Analysis
        sections.append(self._build_credibility_section(assessment_data))
        
        # Risk Assessment
        sections.append(self._build_risk_section(assessment_data))
        
        # Detailed Findings
        sections.append(self._build_findings_section(assessment_data))
        
        # Recommendations (optional)
        if include_recommendations:
            sections.append(self._build_recommendations_section(assessment_data))
        
        # Evidence (optional)
        if include_evidence:
            sections.append(self._build_evidence_section(assessment_data))
        
        venue_name = assessment_data.get('venue_name', 'Unknown Venue')
        
        return Report(
            title=f"ARICCA-X Analysis Report: {venue_name}",
            subtitle="Automated Research Integrity, Credibility & Compliance Analysis",
            timestamp=datetime.now(),
            sections=sections,
            metadata={
                'venue_id': assessment_data.get('venue_id', 'unknown'),
                'assessment_timestamp': assessment_data.get('assessment_timestamp'),
                'confidence': assessment_data.get('confidence', 0.0)
            }
        )
    
    def build_comparison_report(self, comparison_data: Dict) -> Report:
        """Build venue comparison report"""
        sections = []
        
        # Overview
        sections.append(ReportSection(
            title="Comparison Overview",
            content=[
                f"Total venues analyzed: {comparison_data.get('total_venues', 0)}",
                f"Average credibility: {comparison_data.get('average_credibility', 0):.2%}",
                f"Average risk: {comparison_data.get('average_risk', 0):.2%}"
            ]
        ))
        
        # Risk Distribution
        risk_dist = comparison_data.get('risk_distribution', {})
        sections.append(ReportSection(
            title="Risk Distribution",
            content=[
                f"Low risk: {risk_dist.get('low', 0)} venues",
                f"Medium risk: {risk_dist.get('medium', 0)} venues",
                f"High risk: {risk_dist.get('high', 0)} venues",
                f"Critical risk: {risk_dist.get('critical', 0)} venues"
            ]
        ))
        
        # Recommendations
        recommended = comparison_data.get('recommended_venues', [])
        if recommended:
            sections.append(ReportSection(
                title="Recommended Venues",
                content=[
                    f"{i+1}. {v['name']} (Score: {v['score']:.2%})"
                    for i, v in enumerate(recommended)
                ]
            ))
        
        return Report(
            title="ARICCA-X Venue Comparison Report",
            subtitle="Multi-Venue Credibility Analysis",
            timestamp=datetime.now(),
            sections=sections,
            metadata=comparison_data
        )
    
    def build_compliance_report(self, compliance_data: Dict) -> Report:
        """Build manuscript compliance report"""
        sections = []
        
        # Summary
        sections.append(ReportSection(
            title="Compliance Summary",
            content=[
                f"Manuscript: {compliance_data.get('manuscript_title', 'Unknown')}",
                f"Status: {compliance_data.get('compilation_status', 'unknown').upper()}",
                f"Compliance Score: {compliance_data.get('compliance_score', 0):.2%}",
                f"Is Compliant: {'YES' if compliance_data.get('is_compliant') else 'NO'}"
            ]
        ))
        
        # Issues
        issues = compliance_data.get('issues', [])
        if issues:
            error_content = []
            warning_content = []
            
            for issue in issues:
                if hasattr(issue, 'severity'):
                    msg = f"[{issue.issue_id}] {issue.message}"
                    if issue.severity == 'error':
                        error_content.append(msg)
                    elif issue.severity == 'warning':
                        warning_content.append(msg)
            
            if error_content:
                sections.append(ReportSection(
                    title="Errors",
                    content=error_content
                ))
            
            if warning_content:
                sections.append(ReportSection(
                    title="Warnings",
                    content=warning_content
                ))
        
        return Report(
            title="ARICCA-X Compliance Report",
            subtitle="Manuscript Compliance Analysis",
            timestamp=datetime.now(),
            sections=sections,
            metadata=compliance_data
        )
    
    def _build_executive_summary(self, data: Dict) -> ReportSection:
        """Build executive summary section"""
        venue_name = data.get('venue_name', 'Unknown')
        risk_level = data.get('risk_level', 'unknown').upper()
        score = data.get('overall_credibility_score', 0.0)
        
        return ReportSection(
            title="Executive Summary",
            content=[
                f"Venue: {venue_name}",
                f"Overall Credibility Score: {score:.2%}",
                f"Risk Level: {risk_level}",
                "",
                self._get_risk_statement(risk_level.lower())
            ]
        )
    
    def _build_credibility_section(self, data: Dict) -> ReportSection:
        """Build credibility analysis section"""
        components = data.get('score_components', {})
        content = ["Score Breakdown:"]
        
        if hasattr(components, 'cfp_risk_score'):
            content.append(f"  • CFP Risk: {components.cfp_risk_score:.2f}")
        if hasattr(components, 'website_credibility_score'):
            content.append(f"  • Website Credibility: {components.website_credibility_score:.2f}")
        if hasattr(components, 'indexing_credibility_score'):
            content.append(f"  • Indexing Credibility: {components.indexing_credibility_score:.2f}")
        
        return ReportSection(
            title="Credibility Analysis",
            content=content
        )
    
    def _build_risk_section(self, data: Dict) -> ReportSection:
        """Build risk assessment section"""
        flags = data.get('flags', [])
        return ReportSection(
            title="Risk Assessment",
            content=flags if flags else ["No critical risk flags identified"]
        )
    
    def _build_findings_section(self, data: Dict) -> ReportSection:
        """Build detailed findings section"""
        heuristic_results = data.get('heuristic_results', [])
        failed = [h for h in heuristic_results if hasattr(h, 'passed') and not h.passed]
        
        content = []
        if failed:
            content.append("Failed Credibility Checks:")
            for h in failed:
                content.append(f"  • {h.name}: {h.description}")
        else:
            content.append("All credibility checks passed successfully.")
        
        return ReportSection(
            title="Detailed Findings",
            content=content
        )
    
    def _build_recommendations_section(self, data: Dict) -> ReportSection:
        """Build recommendations section"""
        recommendations = data.get('recommendations', [])
        return ReportSection(
            title="Recommendations",
            content=recommendations if recommendations else ["No specific recommendations"]
        )
    
    def _build_evidence_section(self, data: Dict) -> ReportSection:
        """Build evidence section"""
        evidence = []
        
        heuristic_results = data.get('heuristic_results', [])
        for h in heuristic_results:
            if hasattr(h, 'evidence') and h.evidence:
                evidence.extend(h.evidence[:3])  # Top 3 per heuristic
        
        return ReportSection(
            title="Supporting Evidence",
            content=evidence[:10] if evidence else ["Analysis based on available data"]
        )
    
    def _get_risk_statement(self, risk_level: str) -> str:
        """Get appropriate risk statement"""
        statements = {
            'low': "This venue appears legitimate with minimal risk indicators.",
            'medium': "This venue shows mixed signals - exercise caution.",
            'high': "This venue shows significant predatory indicators - high risk.",
            'critical': "This venue shows severe predatory characteristics - critical risk. DO NOT submit."
        }
        return statements.get(risk_level, "Risk level could not be determined.")
