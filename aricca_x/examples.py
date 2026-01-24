"""
Example Usage of ARICCA-X System

This script demonstrates the core functionality of ARICCA-X.
Copyright (c) 2026. All rights reserved.
"""

from aricca_x import (
    CredibilityLogicEngine,
    VenueFingerprintBuilder,
    ComplianceCompiler,
    ReportRenderer
)


def example_1_venue_analysis():
    """Example 1: Analyze a research venue"""
    print("\n" + "="*80)
    print("EXAMPLE 1: Venue Credibility Analysis")
    print("="*80 + "\n")
    
    # Initialize engine
    engine = CredibilityLogicEngine()
    renderer = ReportRenderer()
    
    # Sample venue data
    venue_data = {
        'venue_name': 'International Conference on Advanced Computing 2026',
        'venue_id': 'icac2026'
    }
    
    # Sample CFP analysis results
    cfp_data = {
        'overall_cfp_risk': 0.25,
        'syntax_score': 0.85,
        'professionalism_score': 0.90,
        'urgency_indicators': [],
        'suspicious_patterns': [],
        'language_quality_score': 0.88,
        'contact_legitimacy_score': 0.85
    }
    
    # Sample website analysis results
    website_data = {
        'credibility_score': 0.82,
        'has_ssl': True,
        'has_contact_page': True,
        'has_about_page': True,
        'page_count': 15,
        'max_navigation_depth': 3,
        'is_responsive': True
    }
    
    # Perform assessment
    print("Analyzing venue credibility...")
    assessment = engine.assess_credibility(
        venue_data=venue_data,
        cfp_data=cfp_data,
        website_data=website_data
    )
    
    # Display results
    print(f"\nVenue: {assessment.venue_name}")
    print(f"Overall Credibility Score: {assessment.overall_credibility_score:.2%}")
    print(f"Risk Level: {assessment.risk_level.upper()}")
    print(f"Assessment Confidence: {assessment.confidence:.2%}")
    
    print("\nScore Components:")
    components = assessment.score_components
    print(f"  • CFP Risk: {components.cfp_risk_score:.2f}")
    print(f"  • Website Credibility: {components.website_credibility_score:.2f}")
    print(f"  • Contact Legitimacy: {components.contact_legitimacy_score:.2f}")
    
    if assessment.flags:
        print("\nWarning Flags:")
        for flag in assessment.flags:
            print(f"  {flag}")
    
    if assessment.recommendations:
        print("\nRecommendations:")
        for rec in assessment.recommendations[:3]:
            print(f"  • {rec}")
    
    # Generate detailed report
    print("\n" + "-"*80)
    print("Generating detailed report...")
    report = renderer.render_assessment_report(
        assessment.__dict__,
        output_format='text',
        include_recommendations=True
    )
    
    # Save report
    with open('venue_analysis_report.txt', 'w', encoding='utf-8') as f:
        f.write(report)
    print("Report saved to: venue_analysis_report.txt")


def example_2_venue_comparison():
    """Example 2: Compare multiple venues"""
    print("\n" + "="*80)
    print("EXAMPLE 2: Multi-Venue Comparison")
    print("="*80 + "\n")
    
    engine = CredibilityLogicEngine()
    
    # Sample venues with different risk levels
    venues = [
        {
            'venue_name': 'IEEE Conference on Software Engineering',
            'venue_id': 'ieee_cse',
            'cfp_data': {
                'overall_cfp_risk': 0.15,
                'contact_legitimacy_score': 0.95
            },
            'website_data': {
                'credibility_score': 0.92,
                'has_ssl': True,
                'page_count': 20
            }
        },
        {
            'venue_name': 'International Conference on Computing',
            'venue_id': 'icc',
            'cfp_data': {
                'overall_cfp_risk': 0.45,
                'contact_legitimacy_score': 0.60
            },
            'website_data': {
                'credibility_score': 0.55,
                'has_ssl': False,
                'page_count': 5
            }
        },
        {
            'venue_name': 'ACM Symposium on Applied Computing',
            'venue_id': 'acm_sac',
            'cfp_data': {
                'overall_cfp_risk': 0.20,
                'contact_legitimacy_score': 0.90
            },
            'website_data': {
                'credibility_score': 0.88,
                'has_ssl': True,
                'page_count': 18
            }
        }
    ]
    
    print(f"Analyzing {len(venues)} venues...")
    assessments = engine.batch_assess(venues)
    
    print("\nIndividual Assessments:")
    for assessment in assessments:
        print(f"\n  {assessment.venue_name}")
        print(f"    Score: {assessment.overall_credibility_score:.2%}")
        print(f"    Risk:  {assessment.risk_level.upper()}")
    
    # Compare venues
    print("\n" + "-"*80)
    print("Generating comparison analysis...")
    comparison = engine.compare_venues(assessments)
    
    print(f"\nComparison Summary:")
    print(f"  Average Credibility: {comparison['average_credibility']:.2%}")
    print(f"  Average Risk: {comparison['average_risk']:.2%}")
    
    print(f"\nRisk Distribution:")
    for level, count in comparison['risk_distribution'].items():
        print(f"  {level.capitalize()}: {count} venues")
    
    print(f"\nBest Venue:")
    print(f"  {comparison['best_venue']['name']}")
    print(f"  Score: {comparison['best_venue']['score']:.2%}")
    
    print(f"\nRecommended Venues:")
    for venue in comparison['recommended_venues']:
        print(f"  • {venue['name']} ({venue['score']:.2%})")


def example_3_compliance_check():
    """Example 3: Check manuscript compliance"""
    print("\n" + "="*80)
    print("EXAMPLE 3: Manuscript Compliance Check")
    print("="*80 + "\n")
    
    # Note: This example demonstrates the API
    # In real usage, you'd provide an actual manuscript file
    
    from aricca_x.compliance_compiler import CompilerConfiguration
    
    config = CompilerConfiguration(
        check_formatting=True,
        check_references=True,
        check_structure=True,
        check_metadata=True,
        strict_mode=False,
        style_guide='IEEE'
    )
    
    compiler = ComplianceCompiler(config)
    
    print("Compliance compiler initialized")
    print(f"  Style Guide: {config.style_guide}")
    print(f"  Strict Mode: {config.strict_mode}")
    print(f"  Checks Enabled:")
    print(f"    • Formatting: {config.check_formatting}")
    print(f"    • References: {config.check_references}")
    print(f"    • Structure: {config.check_structure}")
    print(f"    • Metadata: {config.check_metadata}")
    
    print("\nNote: To use with actual manuscript:")
    print("  report = compiler.compile('paper.pdf', 'pdf')")
    print("  if report.is_compliant:")
    print("      print('Manuscript is compliant!')")
    print("  else:")
    print("      for issue in report.issues:")
    print("          print(f'{issue.severity}: {issue.message}')")


def example_4_citation_analysis():
    """Example 4: Analyze citation patterns"""
    print("\n" + "="*80)
    print("EXAMPLE 4: Citation Pattern Analysis")
    print("="*80 + "\n")
    
    from aricca_x import CitationGraphAnalyzer
    
    analyzer = CitationGraphAnalyzer()
    
    # Sample manuscript text with citations
    sample_text = """
    Recent advances in machine learning [1,2] have shown promising results.
    Building on previous work [3], we propose a novel approach.
    The methodology described in [4] was adapted for our study.
    Several researchers [5,6,7] have explored similar techniques.
    """
    
    # Sample references
    sample_references = [
        {'authors': ['Smith', 'Jones'], 'year': 2022, 'venue': 'Nature'},
        {'authors': ['Brown'], 'year': 2021, 'venue': 'Science'},
        {'authors': ['Davis', 'Wilson'], 'year': 2020, 'venue': 'Nature'},
        {'authors': ['Taylor'], 'year': 2023, 'venue': 'IEEE Trans'},
        {'authors': ['Anderson'], 'year': 2019, 'venue': 'ACM SIGKDD'},
        {'authors': ['Lee', 'Chen'], 'year': 2022, 'venue': 'NeurIPS'},
        {'authors': ['Martinez'], 'year': 2021, 'venue': 'ICML'}
    ]
    
    print("Analyzing citation network...")
    analysis = analyzer.analyze(
        manuscript_text=sample_text,
        references=sample_references,
        author_names=['Researcher', 'Coauthor']
    )
    
    print(f"\nCitation Statistics:")
    print(f"  Total Citations: {analysis.total_citations}")
    print(f"  Unique Citations: {analysis.unique_citations}")
    print(f"  Self-Citations: {analysis.self_citations}")
    print(f"  Self-Citation Rate: {analysis.self_citation_rate:.1%}")
    
    print(f"\nCitation Quality Metrics:")
    print(f"  Citation Diversity: {analysis.author_citation_diversity:.2f}")
    print(f"  Network Density: {analysis.citation_network_density:.2f}")
    print(f"  Risk Score: {analysis.risk_score:.2f}")
    
    if analysis.citation_clusters:
        print(f"\nCitation Clusters Found: {len(analysis.citation_clusters)}")
    
    if analysis.suspicious_patterns:
        print(f"\nSuspicious Patterns:")
        for pattern in analysis.suspicious_patterns:
            print(f"  • {pattern.pattern_type}: {pattern.description}")
    
    if analysis.recommendations:
        print(f"\nRecommendations:")
        for rec in analysis.recommendations:
            print(f"  • {rec}")


def main():
    """Run all examples"""
    print("\n")
    print("╔" + "═"*78 + "╗")
    print("║" + " "*78 + "║")
    print("║" + "ARICCA-X DEMONSTRATION EXAMPLES".center(78) + "║")
    print("║" + "Automated Research Integrity, Credibility & Compliance Analyzer".center(78) + "║")
    print("║" + " "*78 + "║")
    print("╚" + "═"*78 + "╝")
    
    try:
        example_1_venue_analysis()
        example_2_venue_comparison()
        example_3_compliance_check()
        example_4_citation_analysis()
        
        print("\n" + "="*80)
        print("ALL EXAMPLES COMPLETED SUCCESSFULLY")
        print("="*80 + "\n")
        
    except Exception as e:
        print(f"\nError running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
