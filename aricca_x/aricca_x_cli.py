#!/usr/bin/env python3
"""
ARICCA-X Main CLI Entry Point

Automated Research Integrity, Credibility & Compliance Analyzer - Extended Edition

Copyright (c) 2026. All rights reserved.
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from aricca_x import (
    CredibilityLogicEngine,
    VenueFingerprintBuilder,
    ComplianceCompiler,
    CitationGraphAnalyzer,
    RiskExplanationGenerator,
    ReportRenderer
)


class ARRICCAX:
    """
    Main ARICCA-X Application Class
    
    Coordinates all analysis modules and provides unified interface.
    """
    
    def __init__(self):
        """Initialize ARICCA-X system"""
        self.credibility_engine = CredibilityLogicEngine()
        self.fingerprint_builder = VenueFingerprintBuilder()
        self.compliance_compiler = ComplianceCompiler()
        self.citation_analyzer = CitationGraphAnalyzer()
        self.risk_generator = RiskExplanationGenerator()
        self.report_renderer = ReportRenderer()
    
    def analyze_venue(
        self,
        venue_name: str,
        cfp_file: str = None,
        website_url: str = None,
        output_format: str = "text"
    ):
        """Analyze a research venue for credibility"""
        print(f"\n{'='*80}")
        print(f"ARICCA-X: Analyzing venue '{venue_name}'")
        print(f"{'='*80}\n")
        
        # Prepare venue data
        venue_data = {
            'venue_name': venue_name,
            'venue_id': venue_name.lower().replace(' ', '_')
        }
        
        # TODO: In full implementation, parse CFP and analyze website
        # For now, use sample data
        print("Note: Using demonstration mode with sample analysis")
        
        cfp_data = {
            'overall_cfp_risk': 0.3,
            'urgency_indicators': ['extended deadline'],
            'suspicious_patterns': [],
            'contact_legitimacy_score': 0.8
        }
        
        website_data = {
            'credibility_score': 0.75,
            'has_ssl': True,
            'has_contact_page': True,
            'page_count': 8
        }
        
        # Perform assessment
        print("Running credibility assessment...")
        assessment = self.credibility_engine.assess_credibility(
            venue_data=venue_data,
            cfp_data=cfp_data,
            website_data=website_data
        )
        
        # Generate explanation
        print("Generating risk explanation...")
        explanation = self.risk_generator.generate_explanation(
            assessment.__dict__
        )
        
        # Render report
        print("Rendering report...\n")
        report = self.report_renderer.render_assessment_report(
            assessment.__dict__,
            output_format=output_format
        )
        
        print(report)
        
        return assessment
    
    def check_compliance(
        self,
        manuscript_path: str,
        manuscript_format: str = "pdf",
        style_guide: str = "IEEE",
        output_format: str = "text"
    ):
        """Check manuscript compliance"""
        print(f"\n{'='*80}")
        print(f"ARICCA-X: Checking manuscript compliance")
        print(f"File: {manuscript_path}")
        print(f"Style Guide: {style_guide}")
        print(f"{'='*80}\n")
        
        # Compile manuscript
        print("Compiling manuscript...")
        report = self.compliance_compiler.compile(
            manuscript_path=manuscript_path,
            manuscript_format=manuscript_format
        )
        
        # Render report
        print("Generating compliance report...\n")
        formatted_report = self.report_renderer.render_compliance_report(
            report.__dict__,
            output_format=output_format
        )
        
        print(formatted_report)
        
        return report
    
    def analyze_citations(
        self,
        manuscript_path: str,
        output_format: str = "text"
    ):
        """Analyze citation patterns in manuscript"""
        print(f"\n{'='*80}")
        print(f"ARICCA-X: Analyzing citation patterns")
        print(f"File: {manuscript_path}")
        print(f"{'='*80}\n")
        
        # TODO: Extract manuscript text and references
        # For demonstration, use sample data
        print("Note: Using demonstration mode with sample data\n")
        
        sample_text = "This study [1] builds upon previous work [2,3]."
        sample_refs = [
            {'authors': ['Smith'], 'year': 2020, 'venue': 'Journal A'},
            {'authors': ['Jones'], 'year': 2021, 'venue': 'Conference B'},
            {'authors': ['Brown'], 'year': 2019, 'venue': 'Journal A'}
        ]
        
        # Analyze citations
        print("Analyzing citation network...")
        analysis = self.citation_analyzer.analyze(
            manuscript_text=sample_text,
            references=sample_refs,
            author_names=['Researcher']
        )
        
        # Display results
        print("\nCitation Analysis Results:")
        print(f"  Total citations: {analysis.total_citations}")
        print(f"  Unique citations: {analysis.unique_citations}")
        print(f"  Self-citation rate: {analysis.self_citation_rate:.1%}")
        print(f"  Citation diversity: {analysis.author_citation_diversity:.2f}")
        print(f"  Risk score: {analysis.risk_score:.2f}")
        
        if analysis.recommendations:
            print("\nRecommendations:")
            for rec in analysis.recommendations:
                print(f"  • {rec}")
        
        return analysis


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="ARICCA-X: Automated Research Integrity, Credibility & Compliance Analyzer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze a venue
  python aricca_x_cli.py analyze-venue "ICICT 2026" --cfp cfp.txt

  # Check manuscript compliance
  python aricca_x_cli.py check-compliance paper.pdf --style IEEE

  # Analyze citations
  python aricca_x_cli.py analyze-citations paper.pdf

Copyright (c) 2026. All rights reserved.
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Analyze venue command
    venue_parser = subparsers.add_parser('analyze-venue', help='Analyze a research venue')
    venue_parser.add_argument('venue_name', help='Name of the venue to analyze')
    venue_parser.add_argument('--cfp', help='Path to Call for Papers file')
    venue_parser.add_argument('--website', help='URL of venue website')
    venue_parser.add_argument('--format', default='text', choices=['text', 'html', 'json', 'markdown'],
                             help='Output format (default: text)')
    venue_parser.add_argument('--output', help='Output file path')
    
    # Check compliance command
    compliance_parser = subparsers.add_parser('check-compliance', help='Check manuscript compliance')
    compliance_parser.add_argument('manuscript', help='Path to manuscript file')
    compliance_parser.add_argument('--style', default='IEEE', choices=['IEEE', 'ACM', 'APA'],
                                   help='Style guide (default: IEEE)')
    compliance_parser.add_argument('--format', default='text', choices=['text', 'html', 'json'],
                                   help='Output format (default: text)')
    compliance_parser.add_argument('--output', help='Output file path')
    
    # Analyze citations command
    citations_parser = subparsers.add_parser('analyze-citations', help='Analyze citation patterns')
    citations_parser.add_argument('manuscript', help='Path to manuscript file')
    citations_parser.add_argument('--format', default='text', choices=['text', 'html', 'json'],
                                  help='Output format (default: text)')
    citations_parser.add_argument('--output', help='Output file path')
    
    # Version command
    parser.add_argument('--version', action='version', version='ARICCA-X v1.0.0')
    
    args = parser.parse_args()
    
    # Initialize ARICCA-X
    aricca = ARRICCAX()
    
    # Execute command
    if args.command == 'analyze-venue':
        result = aricca.analyze_venue(
            venue_name=args.venue_name,
            cfp_file=args.cfp,
            website_url=args.website,
            output_format=args.format
        )
    
    elif args.command == 'check-compliance':
        result = aricca.check_compliance(
            manuscript_path=args.manuscript,
            style_guide=args.style,
            output_format=args.format
        )
    
    elif args.command == 'analyze-citations':
        result = aricca.analyze_citations(
            manuscript_path=args.manuscript,
            output_format=args.format
        )
    
    else:
        parser.print_help()
        return 1
    
    print(f"\n{'='*80}")
    print("Analysis complete!")
    print(f"{'='*80}\n")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
