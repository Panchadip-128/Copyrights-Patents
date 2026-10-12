#!/usr/bin/env python3
"""
ARICCA-X Main CLI Entry Point

Automated Research Integrity, Credibility & Compliance Analyzer - Extended Edition

Multi-signal deterministic verification:
  - Module A: Venue Intelligence (Levenshtein URL spoofing, Predatory Urgency, GTA, TFET)
  - Module B: Researcher Auditing (bounded-DFS loops, True Independent H-Index, CIR)
  - Module C: Peer-Review Forensics (sentence CV, hedging density, specificity, misalignment)
  - Module D: Grant Compliance (Boolean rule matrices: NIH, NSF, Plan S, UKRI)
  - 6-Phase Cross-Correlation Engine with ADW, CSAD, and tamper-evident audit hash chains.

Copyright (c) 2026. All rights reserved. Patent Pending.
"""

import argparse
import json
import sys
from datetime import date, datetime
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from aricca_x import (
    DEFAULT_REGISTRY,
    CompositeRiskProfile,
    CrossCorrelationEngine,
    GrantComplianceEvaluator,
    PeerReviewForensicsAnalyzer,
    PublicationMetadata,
    ResearcherAuditor,
    VenueIntelligenceAnalyzer,
    adaptive_decay_weighting,
    cross_signal_anomaly_detection,
    # Backward compatible classes
    CitationGraphAnalyzer,
    ComplianceCompiler,
    CredibilityLogicEngine,
    ReportRenderer,
    RiskExplanationGenerator,
    VenueFingerprintBuilder,
)


class ARRICCAX:
    """Main ARICCA-X coordinator providing both legacy and patent-extended interfaces."""

    def __init__(self):
        # 4 Dedicated deterministic modules
        self.venue_analyzer = VenueIntelligenceAnalyzer()
        self.researcher_auditor = ResearcherAuditor()
        self.peer_review_analyzer = PeerReviewForensicsAnalyzer()
        self.grant_evaluator = GrantComplianceEvaluator()
        self.correlation_engine = CrossCorrelationEngine()

        # Legacy components
        self.credibility_engine = CredibilityLogicEngine()
        self.fingerprint_builder = VenueFingerprintBuilder()
        self.compliance_compiler = ComplianceCompiler()
        self.citation_analyzer = CitationGraphAnalyzer()
        self.risk_generator = RiskExplanationGenerator()
        self.report_renderer = ReportRenderer()

    def audit_venue_intelligence(
        self,
        venue_name: str,
        website_url: str = "",
        announcement_date: str = "",
        deadline_date: str = "",
        indexing_claims: list = None,
    ):
        """Execute Module A: Venue Intelligence deterministic audit."""
        print(f"\n{'='*80}")
        print(f"ARICCA-X Module A: Venue Intelligence Audit for '{venue_name}'")
        print(f"{'='*80}\n")

        d_ann = datetime.strptime(announcement_date, "%Y-%m-%d").date() if announcement_date else None
        d_dead = datetime.strptime(deadline_date, "%Y-%m-%d").date() if deadline_date else None

        result = self.venue_analyzer.analyze(
            venue_id=venue_name.lower().replace(" ", "_"),
            venue_name=venue_name,
            candidate_url=website_url,
            announcement_date=d_ann,
            deadline_date=d_dead,
            indexing_claims=indexing_claims or [],
        )

        print(f"URL Classification:       {result.url_audit.classification} (score: {result.url_audit.score:.2f})")
        print(f"  Domain Audited:         {result.url_audit.candidate_domain or 'None'}")
        print(f"  Justification:          {result.url_audit.justification}")
        print(f"\nTemporal Urgency Check:   {'PREDATORY URGENCY' if result.temporal_integrity.predatory_urgency else 'HEALTHY'}")
        print(f"  CFP Interval:           {result.temporal_integrity.interval_days} days (Urgency score: {result.temporal_integrity.urgency_score:.2f})")
        print(f"  Justification:          {result.temporal_integrity.justification}")
        print(f"\nGrammatical Tense (GTA):  Credibility score: {result.tense_credibility_score:.2f}")
        for r in result.tense_analysis:
            print(f"  [{r.indexer_name}] {r.evidence}: \"{r.claim_text}\"")
        print(f"\nComposite Venue Signal:   s_venue = {result.credibility_signal:.4f}")
        print(f"Active Flags:             {', '.join(result.flags) if result.flags else 'None'}")
        return result

    def audit_researcher(
        self,
        target_author: str,
        publications: list,
        citation_edges: list = None,
    ):
        """Execute Module B: Researcher Auditing deterministic citation loop audit."""
        print(f"\n{'='*80}")
        print(f"ARICCA-X Module B: Researcher Auditing for '{target_author}'")
        print(f"{'='*80}\n")

        result = self.researcher_auditor.audit(
            target_author=target_author,
            publications=publications,
            author_citation_edges=citation_edges,
        )

        print(f"Target Author:            {result.target_author}")
        print(f"Total Citations Audited:  {result.total_citations} across {result.publication_count} publication(s)")
        print(f"  Self-citations:         {result.self_citations}")
        print(f"  Co-author citations:    {result.coauthor_citations}")
        print(f"  Loop citations:         {result.loop_citations}")
        print(f"  Independent citations:  {result.independent_citations}")
        print(f"\nH-Index Decomposition:")
        print(f"  Standard h-index:       {result.h_index_standard}")
        print(f"  True Independent h:     {result.h_index_true_independent}")
        print(f"  Loop-purged h-index:    {result.h_index_loop_purged}")
        cir_str = f"{result.citation_independence_ratio:.2f}" if result.citation_independence_ratio is not None else "N/A"
        lacir_str = f"{result.loop_adjusted_cir:.2f}" if result.loop_adjusted_cir is not None else "N/A"
        print(f"\nCitation Independence:    CIR = {cir_str} | LACIR = {lacir_str}")
        print(f"  Inflation Alert (<0.30):{'TRIGGERED' if result.inflation_alert else 'Normal'}")
        print(f"  Detected Loops (max=5): {len(result.loops)} loop(s)")
        for l in result.loops:
            print(f"    Loop path: {' -> '.join(l.members)} -> {l.members[0]} (length={l.length})")
        print(f"\nResearcher Signal:        s_researcher = {result.credibility_signal if result.credibility_signal is not None else 'UNKNOWN'}")
        print(f"Active Flags:             {', '.join(result.flags) if result.flags else 'None'}")
        return result

    def audit_peer_review(
        self,
        review_id: str,
        review_text: str,
        recommendation: str = "Accept",
    ):
        """Execute Module C: Peer-Review Forensics deterministic linguistic audit."""
        print(f"\n{'='*80}")
        print(f"ARICCA-X Module C: Peer-Review Forensics for '{review_id}'")
        print(f"{'='*80}\n")

        result = self.peer_review_analyzer.analyze(
            review_id=review_id,
            review_text=review_text,
            recommendation=recommendation,
        )

        fp = result.fingerprint
        print(f"Linguistic Fingerprint:")
        print(f"  Sentences / Words:      {fp.sentence_count} / {fp.word_count}")
        print(f"  Sentence Length CV:     {fp.sentence_length_cv:.4f} (Threshold < 0.20: {'UNNATURAL UNIFORMITY' if fp.is_unnaturally_uniform else 'Natural variation'})")
        print(f"  Hedging Density:        {fp.hedging_density_percent:.2f}% (Threshold > 4.0%: {'EXCESSIVE HEDGING' if fp.is_excessive_hedging else 'Normal'})")
        print(f"  Manuscript Specificity: {fp.specificity_score:.4f} (Threshold < 0.15: {'GENERIC REVIEW' if fp.is_low_specificity else 'Grounded'})")
        print(f"  Type-Token Ratio (TTR): {fp.type_token_ratio:.4f}")
        print(f"\nSentiment-Decision Alignment:")
        print(f"  Sentiment Polarity:     P = {result.sentiment_alignment.sentiment_polarity:+.2f}")
        print(f"  Recommendation:         {result.sentiment_alignment.reviewer_recommendation}")
        print(f"  Status:                 {'MISALIGNED ANOMALY' if result.sentiment_alignment.is_misaligned else 'Consistent'}")
        print(f"\nReview Authenticity:      {result.authenticity_verdict}")
        print(f"Review Signal:            s_review = {result.credibility_signal:.4f}")
        print(f"Active Flags:             {', '.join(result.flags) if result.flags else 'None'}")
        return result

    def verify_grants(
        self,
        publication: PublicationMetadata,
        funders: list = None,
    ):
        """Execute Module D: Grant Compliance Boolean rule verification."""
        print(f"\n{'='*80}")
        print(f"ARICCA-X Module D: Grant Compliance Audit for '{publication.publication_id}'")
        print(f"{'='*80}\n")

        result = self.grant_evaluator.evaluate_publication(
            publication=publication,
            applicable_funders=funders or ["plans", "nih", "nsf", "ukri"],
        )

        print(f"Publication:              {publication.title}")
        print(f"Overall Compliance:       {'100% COMPLIANT' if result.overall_compliant else 'NON-COMPLIANT RULES DETECTED'}")
        print(f"Grant Compliance Signal:  s_grant = {result.credibility_signal:.4f}")
        for funder_key, f_res in result.funder_results.items():
            print(f"\n  Funder: {f_res.funder_name} [{f_res.passed_rules_count}/{f_res.total_rules_count} Passed]")
            for ev in f_res.evaluations:
                status = "PASS" if ev.passed else "FAIL"
                print(f"    [{status}] {ev.rule_id}: {ev.description} ({ev.observed_value})")
                if not ev.passed:
                    print(f"           REMEDIATION: {ev.remediation_note}")
        print(f"\nActive Flags:             {', '.join(result.flags) if result.flags else 'None'}")
        return result

    def run_six_phase_pipeline(
        self,
        target_id: str,
        target_type: str = "composite",
        venue_result=None,
        researcher_result=None,
        peer_review_result=None,
        grant_result=None,
    ) -> CompositeRiskProfile:
        """Run the comprehensive six-phase cross-correlation pipeline."""
        print(f"\n{'='*80}")
        print(f"ARICCA-X Six-Phase Deterministic Pipeline Assessment: '{target_id}'")
        print(f"{'='*80}\n")

        profile = self.correlation_engine.run_pipeline(
            target_id=target_id,
            target_type=target_type,
            venue_result=venue_result,
            researcher_result=researcher_result,
            peer_review_result=peer_review_result,
            grant_result=grant_result,
        )

        for line in profile.mathematical_justification:
            print(f"  • {line}")

        print(f"\nComposite Credibility:   {profile.overall_credibility_score:.4f}")
        print(f"Composite Risk Score:    {profile.total_risk_score:.4f} --> RISK TIER: {profile.risk_level.upper()}")
        print(f"Confidence Assessment:   {profile.confidence:.4f} (Interval: [{profile.epistemic_interval[0]:.4f}, {profile.epistemic_interval[1]:.4f}])")
        print(f"CSAD Amplified:          {'YES (Cross-signal divergence threshold exceeded)' if profile.csad_amplification_applied else 'No (signals coherent)'}")
        print(f"Tamper-Evident Digest:   {profile.audit_chain['final_hash']}")
        print(f"\nActionable Recommendations:")
        for rec in profile.recommendations:
            print(f"  --> {rec}")

        return profile

    # Backward compatibility methods
    def analyze_venue(self, venue_name: str, cfp_file: str = None, website_url: str = None, output_format: str = "text"):
        return self.audit_venue_intelligence(venue_name=venue_name, website_url=website_url or "")

    def check_compliance(self, manuscript_path: str, manuscript_format: str = "pdf", style_guide: str = "IEEE", output_format: str = "text"):
        report = self.compliance_compiler.compile(manuscript_path=manuscript_path, manuscript_format=manuscript_format)
        formatted = self.report_renderer.render_compliance_report(report.__dict__, output_format=output_format)
        print(formatted)
        return report

    def analyze_citations(self, manuscript_path: str, output_format: str = "text"):
        sample_text = "This study [1] builds upon previous work [2,3]."
        sample_refs = [
            {'authors': ['Smith'], 'year': 2020, 'venue': 'Journal A'},
            {'authors': ['Jones'], 'year': 2021, 'venue': 'Conference B'},
            {'authors': ['Brown'], 'year': 2019, 'venue': 'Journal A'},
        ]
        analysis = self.citation_analyzer.analyze(manuscript_text=sample_text, references=sample_refs, author_names=['Researcher'])
        print(f"\nCitation Analysis Results:\n  Total: {analysis.total_citations}\n  Self-citation rate: {analysis.self_citation_rate:.1%}\n  Risk score: {analysis.risk_score:.2f}")
        return analysis


def main():
    parser = argparse.ArgumentParser(
        description="ARICCA-X: Deterministic Multi-Signal Academic Integrity Verification System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", help="Available audit commands")

    # Command: venue-intelligence
    vp = subparsers.add_parser("venue-intelligence", help="Audit venue credibility, Levenshtein spoofing, urgency and GTA")
    vp.add_argument("venue_name", help="Name of venue")
    vp.add_argument("--url", default="", help="Candidate venue website URL")
    vp.add_argument("--announced", default="", help="CFP announcement date (YYYY-MM-DD)")
    vp.add_argument("--deadline", default="", help="Submission deadline date (YYYY-MM-DD)")

    # Command: researcher-audit
    rp = subparsers.add_parser("researcher-audit", help="Audit researcher citation loops, True Independent H-Index and CIR")
    rp.add_argument("author_name", help="Name of target researcher")

    # Command: peer-review
    prp = subparsers.add_parser("peer-review", help="Audit peer review text for artificial uniformity and misalignment")
    prp.add_argument("review_text", help="Reviewer text content or file path")
    prp.add_argument("--decision", default="Accept", help="Recommendation (Accept/Reject/Minor/Major)")

    # Command: grant-compliance
    gp = subparsers.add_parser("grant-compliance", help="Evaluate publication metadata against funding mandates (NIH/NSF/Plan S/UKRI)")
    gp.add_argument("title", help="Publication title")
    gp.add_argument("--oa", default="closed", help="Open access type (gold/diamond/green/closed)")
    gp.add_argument("--license", default="Publisher", help="License type (CC-BY/CC-BY-SA/Publisher)")
    gp.add_argument("--embargo", type=int, default=18, help="Embargo duration in months")

    # Command: pipeline
    pip = subparsers.add_parser("pipeline", help="Run the full 6-phase cross-correlation engine demonstration")
    pip.add_argument("--id", default="DEMO_INTEGRITY_AUDIT_2026", help="Assessment target ID")

    # Legacy commands
    subparsers.add_parser("analyze-venue", help="Legacy analyze venue")
    subparsers.add_parser("check-compliance", help="Legacy check compliance")
    subparsers.add_parser("analyze-citations", help="Legacy analyze citations")

    args = parser.parse_args()
    aricca = ARRICCAX()

    if args.command == "venue-intelligence":
        sample_claims = [
            {"text": "Papers will be indexed in Scopus and Web of Science subject to final review", "source": "website", "indexer": "Scopus"},
            {"text": "All accepted contributions are indexed in IEEE Xplore since 2015", "source": "cfp", "indexer": "IEEE Xplore"},
        ]
        aricca.audit_venue_intelligence(
            venue_name=args.venue_name,
            website_url=args.url,
            announcement_date=args.announced,
            deadline_date=args.deadline,
            indexing_claims=sample_claims,
        )
    elif args.command == "researcher-audit":
        # Demonstrate bounded-DFS loop detection + CIR decomposition
        sample_pubs = [
            {"paper_id": "P1", "authors": [args.author_name, "Colleague_A"], "citations": [{"citing_authors": ["Colleague_A"]}, {"citing_authors": ["Author_B"]}, {"citing_authors": ["Independent_X"]}]},
            {"paper_id": "P2", "authors": [args.author_name], "citations": [{"citing_authors": [args.author_name]}, {"citing_authors": ["Author_B"]}]},
            {"paper_id": "P3", "authors": [args.author_name], "citations": [{"citing_authors": ["Author_B"]}, {"citing_authors": ["Independent_Y"]}]},
        ]
        sample_edges = [
            (args.author_name, "Author_B", 3),
            ("Author_B", "Author_C", 2),
            ("Author_C", args.author_name, 2),  # 3-cycle loop!
            ("Independent_X", args.author_name, 1),
        ]
        aricca.audit_researcher(target_author=args.author_name, publications=sample_pubs, citation_edges=sample_edges)
    elif args.command == "peer-review":
        text = args.review_text
        if Path(text).exists():
            text = Path(text).read_text(encoding="utf-8")
        aricca.audit_peer_review(review_id="REV_001", review_text=text, recommendation=args.decision)
    elif args.command == "grant-compliance":
        pub = PublicationMetadata(
            publication_id="PUB_001",
            title=args.title,
            oa_type=args.oa,
            license=args.license,
            embargo_months=args.embargo,
            repository_deposited=True,
            pmc_deposited=False,
            grant_acknowledged=True,
            grant_numbers=("NIH-R01-HG001234",),
        )
        aricca.verify_grants(publication=pub)
    elif args.command == "pipeline" or not args.command:
        # Full integrated demonstration of all four streams feeding into 6-phase pipeline
        v_res = aricca.venue_analyzer.analyze(
            venue_id="icict_2026",
            venue_name="International Conf on Innovative Computing (Spoofed)",
            candidate_url="https://ieee-icict2026.org",  # Typosquat / brand embedding!
            announcement_date=date(2026, 3, 1),
            deadline_date=date(2026, 3, 18),  # 17 days -> Predatory Urgency!
            indexing_claims=[{"text": "All submissions will be indexed in Scopus", "source": "website", "indexer": "Scopus"}],
        )

        r_res = aricca.researcher_auditor.audit(
            target_author="Dr. Cartel",
            publications=[
                {"paper_id": "P1", "authors": ["Dr. Cartel"], "citations": [{"citing_authors": ["Dr. Cartel"]}, {"citing_authors": ["Member_B"]}]},
                {"paper_id": "P2", "authors": ["Dr. Cartel"], "citations": [{"citing_authors": ["Member_C"]}]},
            ],
            author_citation_edges=[
                ("Dr. Cartel", "Member_B", 3),
                ("Member_B", "Member_C", 3),
                ("Member_C", "Dr. Cartel", 3),  # Loop passing through target!
            ],
        )

        pr_res = aricca.peer_review_analyzer.analyze(
            review_id="REV_789",
            review_text=(
                "This paper presents an outstanding and innovative contribution to the field. "
                "The methodology is solid, rigorous, and extremely well-written throughout. "
                "The experimental results appear quite convincing and highly significant."
            ),
            recommendation="Reject",  # Critical sentiment misalignment!
        )

        g_res = aricca.grant_evaluator.evaluate_publication(
            publication=PublicationMetadata(
                publication_id="PUB_999",
                title="Deceptive Research Article",
                oa_type="closed",
                license="Publisher-Exclusive",
                embargo_months=24,
                repository_deposited=False,
                pmc_deposited=False,
                grant_acknowledged=False,
            )
        )

        aricca.run_six_phase_pipeline(
            target_id=args.id if hasattr(args, "id") else "DEMO_INTEGRITY_AUDIT_2026",
            target_type="multi_stream_composite",
            venue_result=v_res,
            researcher_result=r_res,
            peer_review_result=pr_res,
            grant_result=g_res,
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
