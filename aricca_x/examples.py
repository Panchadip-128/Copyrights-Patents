"""
Example Usage of ARICCA-X System

This script demonstrates the core functionality of ARICCA-X.
Copyright (c) 2026. All rights reserved.
"""

import sys
from pathlib import Path
from datetime import date

# Ensure aricca_x is importable whether run from root or within aricca_x directory
_pkg_root = Path(__file__).resolve().parent
sys.path.insert(0, str(_pkg_root.parent))
sys.path.insert(0, str(_pkg_root))

from aricca_x import (
    CredibilityLogicEngine,
    VenueFingerprintBuilder,
    ComplianceCompiler,
    ReportRenderer,
    VenueIntelligenceAnalyzer,
    ResearcherAuditor,
    PeerReviewForensicsAnalyzer,
    GrantComplianceEvaluator,
    PublicationMetadata,
    CrossCorrelationEngine,
    FingerprintSnapshot,
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


def example_5_module_a_venue_intelligence():
    """Example 5: Module A - Venue Intelligence (URL Spoofing, Urgency, GTA, TFET)"""
    print("\n" + "="*80)
    print("EXAMPLE 5: Module A - Venue Intelligence Engine (Patent Claims 1, 2, 6)")
    print("="*80 + "\n")

    analyzer = VenueIntelligenceAnalyzer()

    # 1. URL Spoofing & Brand Embedding detection
    test_urls = [
        "https://ieee.org",
        "https://ieee-conference-2026.org",
        "https://acm-proceedings.net",
    ]
    print("1. Levenshtein & Brand-Embedding URL Auditing:")
    for url in test_urls:
        audit = analyzer.audit_url(url)
        print(f"   URL: {url}")
        print(f"     Match: {audit.classification} | Spoofed: {audit.is_spoofed} | Score: {audit.score:.2f}")

    # 2. Predatory Urgency Window (< 30 days)
    print("\n2. Predatory Urgency Window Analysis:")
    urgency_result = analyzer.evaluate_temporal_urgency(
        announcement_date=date(2026, 3, 1),
        deadline_date=date(2026, 3, 15),
    )
    print(f"   Interval: {urgency_result.interval_days} days | Urgency Score: {urgency_result.urgency_score:.2f}")
    print(f"   Predatory Urgency Flag: {urgency_result.predatory_urgency}")

    # 3. Grammatical Tense Analysis (GTA) on Indexing Claims
    print("\n3. Grammatical Tense Analysis (GTA) on Indexing Claims:")
    claims = [
        {"text": "Papers will be indexed in Scopus", "source": "cfp", "indexer": "Scopus"},
        {"text": "Indexed in IEEE Xplore since 2012", "source": "cfp", "indexer": "IEEE Xplore"},
        {"text": "May be indexed upon committee selection", "source": "website", "indexer": "Springer"},
    ]
    records, gta_score, justification = analyzer.analyze_grammatical_tense(claims)
    print(f"   GTA Veracity Score: {gta_score:.2f} ({justification[0]})")
    for r in records:
        print(f"     Claim: '{r.claim_text}' -> Tense: {r.tense.upper()} (Risk Weight: {r.risk_weight:.2f})")

    # 4. Temporal Fingerprint Evolution Tracking (TFET)
    print("\n4. Temporal Fingerprint Evolution Tracking (TFET):")
    t1 = FingerprintSnapshot(
        timestamp=date(2025, 1, 1),
        cfp_risk_score=0.2,
        website_depth_score=0.8,
        structural_completeness=0.9,
        indexing_claims_count=3,
        cfp_signature_hash="sig_alpha",
        organizer_count=12,
        domain_name="authentic-conf.org",
    )
    t2 = FingerprintSnapshot(
        timestamp=date(2026, 1, 1),
        cfp_risk_score=0.7,
        website_depth_score=0.3,
        structural_completeness=0.4,
        indexing_claims_count=10,
        cfp_signature_hash="sig_beta_mutated",
        organizer_count=3,
        domain_name="hijacked-lookalike-conf.org",
    )
    drift = analyzer.evaluate_tfet(t1, t2)
    print(f"   Weighted Drift Magnitude: {drift.weighted_drift_magnitude:.4f} (Threshold: {drift.stability_threshold})")
    print(f"   Velocity: {drift.drift_velocity_per_month:.6f}/month | Hijack Suspected: {drift.hijack_suspected}")


def example_6_module_b_researcher_auditing():
    """Example 6: Module B - Researcher Auditing & Cartel Detection (Patent Claim 3)"""
    print("\n" + "="*80)
    print("EXAMPLE 6: Module B - Researcher Auditing & Cartel Ring Detection (Patent Claim 3)")
    print("="*80 + "\n")

    auditor = ResearcherAuditor()

    target = "Author_Target"
    pubs = [
        {"paper_id": "P1", "authors": [target, "Coauthor_1"], "citations": [{"citing_authors": ["Coauthor_1"]}, {"citing_authors": ["Member_B"]}, {"citing_authors": ["Independent_X"]}]},
        {"paper_id": "P2", "authors": [target], "citations": [{"citing_authors": [target]}, {"citing_authors": ["Member_C"]}]},
        {"paper_id": "P3", "authors": [target], "citations": [{"citing_authors": ["Member_B"]}, {"citing_authors": ["Member_C"]}]},
    ]
    edges = [
        (target, "Member_B", 3),
        ("Member_B", "Member_C", 3),
        ("Member_C", target, 3),  # 3-cycle passing through target
        ("Independent_X", target, 1),
    ]

    print("Auditing Author across Citation Network...")
    res = auditor.audit(target_author=target, publications=pubs, author_citation_edges=edges)

    print(f"Target Author: {res.target_author}")
    print(f"  Standard H-Index: {res.h_index_standard}")
    print(f"  True Independent H-Index: {res.h_index_true_independent}")
    print(f"  Loop-Purged H-Index: {res.h_index_loop_purged}")
    print(f"  Citation Independence Ratio (CIR): {res.citation_independence_ratio:.2%}")
    print(f"  Loop-Adjusted CIR (LACIR): {res.loop_adjusted_cir:.2%}")
    print(f"  Inflation Alert (CIR < 30%): {res.inflation_alert}")
    print(f"  Loop Inflation Alert: {res.loop_inflation_alert}")
    print(f"  Cartel Citation Loops Detected: {len(res.loops)}")
    for loop in res.loops:
        print(f"    • Loop (length={loop.length}): {' -> '.join(loop.members)}")


def example_7_module_c_peer_review_forensics():
    """Example 7: Module C - Peer Review Forensics (Patent Claim 4)"""
    print("\n" + "="*80)
    print("EXAMPLE 7: Module C - Peer Review Forensics Engine (Patent Claim 4)")
    print("="*80 + "\n")

    analyzer = PeerReviewForensicsAnalyzer()

    synthetic_review = (
        "This paper presents an outstanding and highly innovative method. "
        "The proposed approach is solid and exceptionally well written. "
        "The experiments are rigorous and completely convince the reader. "
        "The contribution is valuable and provides profound insight."
    )

    print("Auditing Review Text (Synthetic Uniformity + Recommendation Misalignment):")
    res = analyzer.analyze(
        review_id="REV_2026_01",
        review_text=synthetic_review,
        recommendation="Reject",
    )

    fp = res.fingerprint
    print(f"Linguistic Fingerprint:")
    print(f"  Sentence Length CV: {fp.sentence_length_cv:.4f} (Unnatural Uniformity: {fp.is_unnaturally_uniform})")
    print(f"  Academic Hedging Density: {fp.hedging_density_percent:.2f}%")
    print(f"  Specificity Score: {fp.specificity_score:.4f}")
    print(f"\nSentiment vs Recommendation Analysis:")
    print(f"  Polarity Score: {res.sentiment_alignment.sentiment_polarity:.2f}")
    print(f"  Stated Recommendation: {res.sentiment_alignment.reviewer_recommendation}")
    print(f"  Behavioral Misalignment Flag: {res.sentiment_alignment.is_misaligned}")
    print(f"  Credibility Signal: {res.credibility_signal:.2f}")
    print(f"  Flags: {res.flags}")


def example_8_module_d_grant_compliance():
    """Example 8: Module D - Machine-Readable Grant Compliance (Patent Claim 1)"""
    print("\n" + "="*80)
    print("EXAMPLE 8: Module D - Grant Compliance Engine (Boolean Rule Matrices, Patent Claim 1)")
    print("="*80 + "\n")

    evaluator = GrantComplianceEvaluator()

    pub = PublicationMetadata(
        publication_id="PUB_2026_NIH",
        title="Deterministic Multi-Signal Integrity Analysis",
        oa_type="gold",
        license="CC-BY",
        embargo_months=0,
        repository_deposited=True,
        pmc_deposited=True,
        grant_acknowledged=True,
        grant_numbers=("NIH-R01-HG012345", "NSF-2026-999"),
    )

    print("Evaluating Publication Metadata against Mandates (NIH, NSF, Plan S, UKRI):")
    res = evaluator.evaluate_publication(pub)

    print(f"Overall Compliance: {'COMPLIANT' if res.overall_compliant else 'NON-COMPLIANT'}")
    print(f"Credibility Signal: {res.credibility_signal:.2%}")
    print(f"Triggered Flags: {res.flags if res.flags else 'None'}")
    print("\nRule-Level Deterministic Verification:")
    for funder_id, f_res in res.funder_results.items():
        print(f"  Funder: {f_res.funder_name} (Compliant: {f_res.is_fully_compliant})")
        for rule in f_res.evaluations:
            status = "[PASS]" if rule.passed else "[FAIL]"
            print(f"    {status} [{rule.rule_id}] {rule.description}")
            if not rule.passed:
                print(f"           Remediation: {rule.remediation_note}")


def example_9_six_phase_pipeline_and_audit_chain():
    """Example 9: Six-Phase Pipeline with ADW, CSAD, and Cryptographic Chaining"""
    print("\n" + "="*80)
    print("EXAMPLE 9: Six-Phase Pipeline with ADW, CSAD & SHA-256 Audit Chaining")
    print("="*80 + "\n")

    engine = CrossCorrelationEngine()

    v_analyzer = VenueIntelligenceAnalyzer()
    v_res = v_analyzer.analyze(
        venue_id="conf_spoof_2026",
        venue_name="International Conf on Computing",
        candidate_url="https://ieee-conf2026.org",
    )

    r_auditor = ResearcherAuditor()
    r_res = r_auditor.audit(
        target_author="Author_Target",
        publications=[
            {"paper_id": "P1", "authors": ["Author_Target"], "citations": [{"citing_authors": ["Author_Target"]}]}
        ],
    )

    rev_analyzer = PeerReviewForensicsAnalyzer()
    rev_res = rev_analyzer.analyze(
        review_id="REV_P1",
        review_text="This paper presents an outstanding and highly innovative method. The proposed approach is solid.",
        recommendation="Accept",
    )

    g_evaluator = GrantComplianceEvaluator()
    g_res = g_evaluator.evaluate_publication(
        PublicationMetadata(
            publication_id="PUB_P1",
            title="Sample Paper",
            oa_type="closed",
            license="Exclusive",
            embargo_months=24,
            repository_deposited=False,
            pmc_deposited=False,
            grant_acknowledged=False,
        )
    )

    print("Executing Six-Phase Pipeline across all 4 deterministic modules...")
    pipeline_res = engine.run_pipeline(
        target_id="ASSESSMENT_2026_001",
        target_type="composite",
        venue_result=v_res,
        researcher_result=r_res,
        peer_review_result=rev_res,
        grant_result=g_res,
    )

    print(f"Target: {pipeline_res.target_id}")
    print(f"Overall Credibility Score: {pipeline_res.overall_credibility_score:.2f}")
    print(f"Total Risk Score (with CSAD): {pipeline_res.total_risk_score:.2f}")
    print(f"Risk Tier: {pipeline_res.risk_level.upper()}")
    print(f"Confidence: {pipeline_res.confidence:.2%}")
    print(f"Epistemic Interval [L, U]: [{pipeline_res.epistemic_interval[0]:.2f}, {pipeline_res.epistemic_interval[1]:.2f}] (Width: {pipeline_res.interval_width:.2f})")
    print(f"CSAD Facade Amplification Applied: {pipeline_res.csad_amplification_applied}")
    
    print("\nTriggered Flags:")
    for flag in pipeline_res.flags:
        print(f"  • {flag}")

    print("\nRecommendations:")
    for rec in pipeline_res.recommendations:
        print(f"  • {rec}")

    print("\nTamper-Evident SHA-256 Audit Chain Verification:")
    audit_chain = pipeline_res.audit_chain
    print(f"  Pipeline ID: {audit_chain['pipeline_id']}")
    print(f"  Phases Recorded: {len(audit_chain['records'])}")
    print(f"  Genesis Input Hash: {audit_chain['input_digest'][:16]}...")
    print(f"  Final Audit Hash: {audit_chain['final_hash'][:16]}...")

    from aricca_x.deterministic_core.audit_chain import verify_exported_chain
    is_valid = verify_exported_chain(audit_chain)
    print(f"  Cryptographic Hash Chain Integrity: {'VERIFIED [OK]' if is_valid else 'COMPROMISED [FAIL]'}")


def main():
    """Run all examples"""
    print("\n")
    print("=" * 80)
    print("ARICCA-X COMPREHENSIVE DEMONSTRATION SUITE".center(80))
    print("Deterministic Multi-Signal Academic Research Integrity Analyzer".center(80))
    print("=" * 80)
    
    try:
        example_1_venue_analysis()
        example_2_venue_comparison()
        example_3_compliance_check()
        example_4_citation_analysis()
        example_5_module_a_venue_intelligence()
        example_6_module_b_researcher_auditing()
        example_7_module_c_peer_review_forensics()
        example_8_module_d_grant_compliance()
        example_9_six_phase_pipeline_and_audit_chain()
        
        print("\n" + "="*80)
        print("ALL 9 ARICCA-X DEMONSTRATION EXAMPLES COMPLETED SUCCESSFULLY")
        print("="*80 + "\n")
        
    except Exception as e:
        print(f"\nError running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

