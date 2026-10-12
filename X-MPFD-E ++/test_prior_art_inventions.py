"""
Automated Prior Art & Patent Claims Verification Test Suite
Repository: X-MPFD-E++
Document: 35 U.S.C. Section 101/102/103 Empirical Verification
Patent Claims: 1 through 15

Verifies deterministic algorithms against prior art references:
- Category A: Static Blacklists (Google Safe Browsing, PhishTank)
- Category B: Black-Box ML Classifiers (CrowdStrike, Proofpoint)
- Category C: Single-Modality Scanners (CheckPhish)

Copyright © 2026 Panchadip B & Somyajeet A. All Rights Reserved.
"""

import sys
import os
import unittest
import math
import json
import hashlib
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).parent))

from x_mpfd_e_plus import (
    PhishingDetector,
    MultimodalOrchestrator,
    FusionPolicyEngine,
    FusionPolicy,
    FusionStrategy,
    ExplanationSynthesizer,
    IntegrityAuditor,
    InferenceAPI,
)
from x_mpfd_e_plus.multimodal_orchestrator.orchestrator import (
    LexicalAnalyzer,
    StructuralAnalyzer,
    DeterministicDOMAnalyzer,
    VisualMetadataAnalyzer,
)
from x_mpfd_e_plus.feature_registry.registry import (
    FeatureRegistry,
    FeatureCategory,
    FeatureProvenance,
    ProvenanceLineageTracker,
)
from x_mpfd_e_plus.report_generator import ReportGenerator


class TestClaim2LexicalShannonEntropy(unittest.TestCase):
    """
    CLAIM 2: Real-time Shannon Entropy H(U) calculation isolates DGAs
    without database lookups, overcoming the 4-hour zero-day blacklist gap.
    """
    def test_shannon_entropy_mathematical_precision(self):
        # A single character string has entropy 0.0
        self.assertEqual(LexicalAnalyzer.calculate_shannon_entropy("aaaaaaa"), 0.0)

        # Two equally distributed characters have entropy 1.0
        self.assertAlmostEqual(LexicalAnalyzer.calculate_shannon_entropy("abababab"), 1.0, places=4)

        # Natural legitimate URL
        legit_url = "https://paypal.com"
        legit_entropy = LexicalAnalyzer.calculate_shannon_entropy(legit_url)
        self.assertLess(legit_entropy, 4.0, f"Legitimate URL entropy should be <= 4.0, got {legit_entropy}")

        # High-entropy algorithmic DGA string
        dga_url = "https://xq889z-1bka98z-p09927xb-q77.phishgate-auth-update.xyz/login?id=99283748234"
        dga_entropy = LexicalAnalyzer.calculate_shannon_entropy(dga_url)
        self.assertGreater(dga_entropy, 4.5, f"DGA URL entropy should be > 4.5, got {dga_entropy}")

    def test_lexical_analyzer_vector_extraction(self):
        url = "https://paypa1-update.tk/secure/auth"
        vec = LexicalAnalyzer.analyze_url(url)
        self.assertIn("shannon_entropy", vec)
        self.assertFalse(vec["is_ip_address"])
        self.assertEqual(vec["tld"], "tk")
        self.assertTrue(vec["has_suspicious_tld"])
        self.assertGreater(vec["lexical_risk_score"], 0.30)


class TestClaims3And4StructuralASTandSDR(unittest.TestCase):
    """
    CLAIMS 3 & 4: Deterministic HTML AST parsing, Maximum Tree Depth (D_max),
    and Structural Density Ratio (SDR = N / D_max) identify cloned harvester pages.
    """
    def test_ast_parsing_and_sdr_calculation(self):
        html_sample = """
        <!DOCTYPE html>
        <html>
            <head><title>Test Page</title></head>
            <body>
                <div id="main">
                    <form action="/login" method="POST">
                        <input type="text" name="user"/>
                        <input type="password" name="pwd"/>
                        <input type="hidden" name="token" value="abc"/>
                        <button type="submit">Sign In</button>
                    </form>
                </div>
            </body>
        </html>
        """
        parser = DeterministicDOMAnalyzer()
        parser.feed(html_sample)

        self.assertGreater(parser.total_nodes, 5)
        self.assertGreater(parser.max_depth, 3)
        self.assertEqual(parser.form_count, 1)
        self.assertEqual(parser.password_fields, 1)
        self.assertEqual(parser.hidden_inputs, 1)

        sdr = parser.calculate_sdr()
        expected_sdr = parser.total_nodes / float(parser.max_depth)
        self.assertAlmostEqual(sdr, expected_sdr, places=4)

    def test_cloned_harvester_shallow_sdr_deviation(self):
        # Shallow phishing clone: very few wrapper tags, but has a password field
        shallow_phish_html = """
        <html>
            <body>
                <form action="http://attacker.com/steal">
                    <input type="password" name="password" />
                </form>
            </body>
        </html>
        """
        res = StructuralAnalyzer.analyze_html(shallow_phish_html, baseline_sdr=16.0)
        self.assertTrue(res["has_html"])
        self.assertEqual(res["password_fields"], 1)
        self.assertLessEqual(res["max_depth"], 4)
        self.assertGreater(res["sdr_deviation_pct"], 50.0)
        self.assertGreaterEqual(res["structural_risk_score"], 0.75)


class TestClaims6And15ConditionalGatedFusionHardwareOptimization(unittest.TestCase):
    """
    CLAIMS 6 & 15: Hardware Optimization in Cybersecurity Appliances.
    Dynamically bypassing deep HTML AST parsing and visual rendering
    based on superficial string entropy H(U) > 4.5.
    """
    def test_gated_fusion_hardware_compute_bypass(self):
        detector = PhishingDetector(fusion_policy="gated")

        # High-entropy DGA URL
        high_entropy_url = "https://99az-qwer-18274b-zk991p-xxm8172.dga-botnet-fraud.xyz/verify?token=89234872938472"
        # Large complex HTML page that should be bypassed
        huge_html = "<html><body>" + "<div><span>deep node</span></div>" * 500 + "</body></html>"

        result = detector.analyze_url(url=high_entropy_url, html=huge_html, tls_valid=True)

        self.assertEqual(result.decision, "PHISHING_DGA")
        self.assertEqual(result.confidence, "HIGH")
        self.assertGreaterEqual(result.risk_score, 0.95)
        self.assertTrue(result.hardware_compute_bypassed, "Hardware compute bypass must be TRUE for H(U) > 4.5")
        self.assertIn("structural_dom_ast", result.bypassed_modalities)
        self.assertIn("visual_rendering", result.bypassed_modalities)

    def test_gated_fusion_normal_pipeline_flow(self):
        detector = PhishingDetector(fusion_policy="gated")
        legit_url = "https://www.chase.com/personal/banking"
        legit_html = "<html><body>" + "<div><section><p>content</p></section></div>" * 20 + "</body></html>"

        result = detector.analyze_url(url=legit_url, html=legit_html, tls_valid=True)
        self.assertEqual(result.decision, "LEGITIMATE")
        self.assertFalse(result.hardware_compute_bypassed)
        self.assertLessEqual(result.risk_score, 0.10)

    def test_gated_fusion_hostname_entropy_avoids_query_token_false_positives(self):
        """
        Validates configurable scope in Claims 1, 2, 10, 15:
        Computing H(U) on hostname rather than full URL prevents false positives
        on legitimate portals carrying long hex session tokens in query parameters.
        """
        token_url = "https://www.discover.com/online-banking?session_id=8049d7b1ca1d1e089ebe1f467499978613ae71db&client=auth"
        legit_html = "<html><body>" + "<div><section><p>banking</p></section></div>" * 20 + "</body></html>"

        # Scope: URL (Full string entropy is ~4.89 > 4.50 -> trips gate)
        detector_url = PhishingDetector(fusion_policy="gated", entropy_scope="url")
        res_url = detector_url.analyze_url(url=token_url, html=legit_html, tls_valid=True)
        self.assertTrue(res_url.hardware_compute_bypassed)

        # Scope: Hostname (Hostname entropy is ~3.33 < 3.80 -> avoids gate, allocates threads, correctly LEGITIMATE)
        detector_host = PhishingDetector(fusion_policy="gated", entropy_scope="hostname", entropy_threshold=3.80)
        res_host = detector_host.analyze_url(url=token_url, html=legit_html, tls_valid=True)
        self.assertFalse(res_host.hardware_compute_bypassed)
        self.assertEqual(res_host.decision, "LEGITIMATE")


class TestClaims51112MultimodalFusionStrategies(unittest.TestCase):
    """
    CLAIMS 5, 11, & 12: Late Confidence-Weighted, Early Matrix Algebra,
    and Consensus Voting fusion policies.
    """
    def setUp(self):
        self.fusion_engine = FusionPolicyEngine()

    def test_late_confidence_weighted_fusion(self):
        policy = self.fusion_engine.get_policy("confidence_weighted")
        self.fusion_engine.set_policy(policy)

        # Test weighted execution: lexical=0.8, structural=0.8, visual=0.8 -> Risk=0.8
        res = self.fusion_engine.execute(
            entropy=4.2,
            sdr_deviation=65.0,
            tls_valid=False,
            url="https://phish.com",
            lexical_risk=0.80,
            structural_risk=0.80,
            visual_risk=0.80,
        )
        self.assertEqual(res.decision, "PHISHING")
        self.assertAlmostEqual(res.risk_score, 0.80, places=2)
        self.assertEqual(res.policy_name, "confidence_weighted")

    def test_early_fusion_matrix_algebra(self):
        policy = self.fusion_engine.get_policy("early_fusion")
        self.fusion_engine.set_policy(policy)

        res = self.fusion_engine.execute(
            entropy=4.8,
            sdr_deviation=80.0,
            tls_valid=False,
            url="https://early-matrix-test.com",
        )
        self.assertEqual(res.decision, "PHISHING")
        self.assertGreater(res.risk_score, 0.60)
        self.assertEqual(res.policy_name, "early_fusion")

    def test_consensus_majority_voting(self):
        policy = self.fusion_engine.get_policy("consensus_fusion")
        self.fusion_engine.set_policy(policy)

        # 2 of 3 modalities flagged: entropy > 4.0, sdr > 40.0, tls valid -> 2 votes -> PHISHING
        res = self.fusion_engine.execute(
            entropy=4.2,
            sdr_deviation=55.0,
            tls_valid=True,
            url="https://consensus-test.com",
        )
        self.assertEqual(res.decision, "PHISHING")
        self.assertEqual(res.risk_score, 0.90)


class TestClaim7CryptographicProvenanceLineage(unittest.TestCase):
    """
    CLAIM 7: Cryptographic SHA-256 Provenance Lineage Tags and Tamper Detection.
    """
    def test_sha256_provenance_tag_immutability(self):
        registry = FeatureRegistry()
        feat = registry.register_feature(
            name="URL Entropy",
            category=FeatureCategory.LEXICAL,
            value=4.35,
            source_modality="lexical",
            extraction_method="shannon_entropy_base_2",
            confidence=1.0,
            parameters={"threshold": 4.0},
        )
        prov = feat.provenance
        self.assertEqual(len(prov.sha256_hash), 64, "Provenance hash must be valid SHA-256 (64 hex characters)")

        # Verify hash matches canonical payload
        canonical_str = f"{prov.source_modality}:{prov.extraction_method}:{prov.extraction_timestamp}:{prov.confidence}:{json.dumps(prov.parameters, sort_keys=True)}"
        expected_hash = hashlib.sha256(canonical_str.encode("utf-8")).hexdigest()
        self.assertEqual(prov.sha256_hash, expected_hash)

    def test_provenance_lineage_tracker_dag(self):
        tracker = ProvenanceLineageTracker()
        lineage = tracker.create_lineage(source_signal_id="sig_url_001")
        tracker.track_extraction(lineage, "url_parse", "raw_components")
        tracker.track_transformation(lineage, "entropy_calc", 4.35)

        audit = tracker.audit_lineage("feat_test_001", lineage)
        self.assertEqual(audit["transformation_count"], 2)
        self.assertTrue(audit["is_complete"])


class TestClaim8ExplanationSynthesisEngine(unittest.TestCase):
    """
    CLAIM 8: Non-probabilistic Explanation Synthesis Engine mapping
    provenance tags to auditable decision rationales without generative AI.
    """
    def test_deterministic_explanation_generation(self):
        synthesizer = ExplanationSynthesizer()
        provenance_tags = [{"modality": "lexical", "value": 4.62}]

        dossier = synthesizer.synthesize(
            decision="PHISHING_DGA",
            risk_score=0.99,
            policy_name="gated_fusion",
            provenance_tags=provenance_tags,
            entropy=4.62,
            sdr=12.0,
            sdr_deviation=25.0,
            tls_valid=True,
            password_fields=0,
            bypassed=True,
        )

        rationale = dossier["human_readable_rationale"]
        self.assertIn("PHISHING_DGA", rationale)
        self.assertIn("4.62", rationale)
        self.assertIn("bypassed downstream HTML AST DOM parsing", rationale)
        self.assertTrue(dossier["is_pure_deterministic"])
        self.assertFalse(dossier["llm_inference_used"])
        self.assertEqual(len(dossier["sha256_explanation_hash"]), 64)


class TestClaims191014PipelineDeterminismAndAliceDefense(unittest.TestCase):
    """
    CLAIMS 1, 9, 10, & 14: System Determinism, Alice Section 101 Defense,
    and Canonical JSON Schema Generation.
    """
    def test_bit_for_bit_determinism(self):
        detector = PhishingDetector(fusion_policy="gated")
        url = "https://paypa1-security-check.com/update"
        html = "<html><body><form><input type='password' /></form></body></html>"

        res1 = detector.analyze_url(url=url, html=html, tls_valid=False)
        res2 = detector.analyze_url(url=url, html=html, tls_valid=False)

        self.assertEqual(res1.decision, res2.decision)
        self.assertEqual(res1.risk_score, res2.risk_score)
        self.assertEqual(res1.confidence, res2.confidence)
        self.assertEqual(res1.explanation, res2.explanation)
        self.assertEqual(res1.sha256_audit_hash, res2.sha256_audit_hash)

    def test_claim_9_cross_architecture_bit_exact_determinism(self):
        """
        CLAIM 9: Bit-exact determinism across runtime environments and architectures.
        Verifies that discrete quantization (4 decimal places) eliminates IEEE-754 sub-epsilon
        floating-point variances (e.g. x86-64 vs ARM64 NEON), ensuring bit-exact SHA-256 audit hashes.
        """
        from x_mpfd_e_plus.fusion_policy_engine.fusion_engine import AnalysisResult

        # Case 1: Fresh detector instances produce identical hashes
        det1 = PhishingDetector(fusion_policy="gated", entropy_scope="hostname", entropy_threshold=3.80)
        det2 = PhishingDetector(fusion_policy="gated", entropy_scope="hostname", entropy_threshold=3.80)
        url = "https://portal.bank-security-update.com/login"
        html = "<html><body><form action='/post'><input type='password'/></form></body></html>"

        r1 = det1.analyze_url(url=url, html=html, tls_valid=False)
        r2 = det2.analyze_url(url=url, html=html, tls_valid=False)

        self.assertEqual(r1.decision, r2.decision)
        self.assertEqual(r1.risk_score, r2.risk_score)
        self.assertEqual(r1.sha256_audit_hash, r2.sha256_audit_hash)

        # Case 2: Sub-epsilon float noise (+-1e-14) simulates x86 vs ARM64 FPU differences
        base_score = 0.950000000000001
        arm_noise_score = base_score + 1e-14
        x86_noise_score = base_score - 1e-14

        res_arm = AnalysisResult(decision="PHISHING", risk_score=arm_noise_score, confidence="HIGH", policy_name="gated")
        res_x86 = AnalysisResult(decision="PHISHING", risk_score=x86_noise_score, confidence="HIGH", policy_name="gated")

        self.assertEqual(res_arm.sha256_audit_hash, res_x86.sha256_audit_hash,
                         "Quantization must produce bit-exact SHA-256 hash despite sub-epsilon float variance")
        self.assertEqual(res_arm.to_dict()["risk_score"], 0.95)
        self.assertEqual(res_x86.to_dict()["risk_score"], 0.95)

    def test_claim_14_canonical_json_report(self):
        detector = PhishingDetector(fusion_policy="gated")
        res = detector.analyze_url(url="https://paypal.com", tls_valid=True)

        gen = ReportGenerator()
        json_report = gen.generate_json_report(res)
        parsed = json.loads(json_report)

        self.assertEqual(parsed["schema_version"], "1.0.0-patent-claim-14")
        self.assertEqual(parsed["decision"], "LEGITIMATE")
        self.assertIn("sha256_audit_hash", parsed)
        self.assertTrue(parsed["determinism_guarantee"]["deterministic_closed_form"])
        self.assertFalse(parsed["determinism_guarantee"]["llm_inference_used"])


class TestSection3nAuditVerificationAndTamperDetection(unittest.TestCase):
    """
    SECTION 3(n) CRI GUIDELINES 2025: Cryptographic Verification & Replay Function.
    Proves that the JSON evidence report and explanations serve an active verification
    function capable of detecting tamper attempts.
    """
    def test_audit_verification_of_valid_report(self):
        from x_mpfd_e_plus.provenance_lineage_tracker import AuditVerifier
        detector = PhishingDetector(fusion_policy="gated")
        res = detector.analyze_url(url="https://paypal.com", tls_valid=True)

        gen = ReportGenerator()
        report_json = gen.generate_json_report(res)

        verifier = AuditVerifier()
        is_valid, msg, details = verifier.verify_report(report_json)
        self.assertTrue(is_valid, f"Verification failed: {msg}")
        self.assertIn("AUDIT_VERIFIED", msg)
        self.assertFalse(details.get("tampered", True))

    def test_tamper_detection_when_recorded_value_altered(self):
        from x_mpfd_e_plus.provenance_lineage_tracker import AuditVerifier
        detector = PhishingDetector(fusion_policy="gated")
        res = detector.analyze_url(url="https://paypal.com", tls_valid=True)

        gen = ReportGenerator()
        report_json = gen.generate_json_report(res)
        parsed = json.loads(report_json)

        # Adversary alters feature parameters (e.g. changing Shannon Entropy threshold from 4.50 to 9.99)
        for feat in parsed["feature_provenance_registry"]:
            if feat["name"] == "Shannon Entropy":
                feat["provenance"]["parameters"]["threshold"] = 9.99  # Tampering with recorded parameters!

        tampered_json = json.dumps(parsed)
        verifier = AuditVerifier()
        is_valid, msg, details = verifier.verify_report(tampered_json)

        self.assertFalse(is_valid, "Verifier must detect tampering when parameters are modified!")
        self.assertIn("TAMPER_DETECTED", msg)
        self.assertGreater(len(details["mismatches"]), 0)

    def test_deterministic_decision_replay(self):
        from x_mpfd_e_plus.provenance_lineage_tracker import AuditVerifier
        detector = PhishingDetector(fusion_policy="gated")
        res = detector.analyze_url(url="https://paypal.com", tls_valid=True)

        gen = ReportGenerator()
        report_json = gen.generate_json_report(res)

        verifier = AuditVerifier()
        replayed, msg, details = verifier.replay_decision(report_json)
        self.assertTrue(replayed, f"Replay failed: {msg}")
        self.assertEqual(details["original_decision"], details["replayed_decision"])
        self.assertTrue(details["is_deterministic"])


class TestSection3mSystemControlDirectivesAndRuleExecution(unittest.TestCase):
    """
    SECTION 3(m) CRI GUIDELINES 2025: Appliance Hardware Directives & Table 6-1/6-2 Rules.
    Proves that decision rules directly control the parser and renderer within the system.
    """
    def test_hardware_directive_withhold_on_dga(self):
        detector = PhishingDetector(fusion_policy="gated")
        dga_url = "https://ax99-qzk184p-9x882b7-k2991.phishgate-auth-update.xyz/token?id=99283748234"
        res = detector.analyze_url(url=dga_url)

        self.assertEqual(res.decision, "PHISHING_DGA")
        self.assertEqual(res.system_control_directive, "WITHHOLD_PARSER_AND_RENDERER")
        self.assertEqual(res.rule_id, "RULE_TABLE_6_1_GATE_DGA_SUPPRESSION")

    def test_hardware_directive_isolate_on_cloned_harvester(self):
        detector = PhishingDetector(fusion_policy="gated")
        shallow_html = "<html><body><form><input type='password' /></form></body></html>"
        res = detector.analyze_url(url="https://phish-bank.com", html=shallow_html, tls_valid=False)

        self.assertEqual(res.decision, "PHISHING_CLONE")
        self.assertEqual(res.system_control_directive, "ISOLATE_CREDENTIAL_FORM")
        self.assertEqual(res.rule_id, "RULE_TABLE_6_1_GATE_CLONE_CONFIRMED")

    def test_table_6_2_complete_cartesian_8_cell_matrix(self):
        engine = FusionPolicyEngine()
        policy = engine.get_policy("strict_matrix")
        engine.set_policy(policy)

        # Test Cell 1: (1, 1, 1) -> PHISHING
        r1 = engine.execute(entropy=4.8, sdr_deviation=80.0, tls_valid=False, url="")
        self.assertEqual(r1.decision, "PHISHING")
        self.assertEqual(r1.rule_id, "RULE_TABLE_6_2_CELL_1_ALL_FLAGS")

        # Test Cell 2: (1, 1, 0) -> PHISHING
        r2 = engine.execute(entropy=4.8, sdr_deviation=80.0, tls_valid=True, url="")
        self.assertEqual(r2.decision, "PHISHING")
        self.assertEqual(r2.rule_id, "RULE_TABLE_6_2_CELL_2_LEX_STRUCT")

        # Test Cell 5: (1, 0, 0) -> SUSPICIOUS
        r5 = engine.execute(entropy=4.8, sdr_deviation=10.0, tls_valid=True, url="")
        self.assertEqual(r5.decision, "SUSPICIOUS")
        self.assertEqual(r5.rule_id, "RULE_TABLE_6_2_CELL_5_LEX_ONLY")

        # Test Cell 8: (0, 0, 0) -> LEGITIMATE
        r8 = engine.execute(entropy=3.2, sdr_deviation=10.0, tls_valid=True, url="")
        self.assertEqual(r8.decision, "LEGITIMATE")
        self.assertEqual(r8.rule_id, "RULE_TABLE_6_2_CELL_8_ALL_CLEAN")


class TestSection10MissingModalityHandling(unittest.TestCase):
    """
    SECTION 10(4) SUFFICIENCY & ENABLEMENT: Missing Modality Degradation Rules.
    """
    def test_missing_html_modality_handling(self):
        detector = PhishingDetector(fusion_policy="gated")
        # URL with no HTML provided (e.g. socket timeout)
        res_valid_tls = detector.analyze_url(url="https://paypal.com", html=None, tls_valid=True)
        self.assertEqual(res_valid_tls.decision, "LEGITIMATE")
        self.assertEqual(res_valid_tls.rule_id, "RULE_TABLE_6_1_MISSING_HTML_SAFE")

        res_invalid_tls = detector.analyze_url(url="https://paypal.com", html=None, tls_valid=False)
        self.assertEqual(res_invalid_tls.decision, "SUSPICIOUS")
        self.assertEqual(res_invalid_tls.rule_id, "RULE_TABLE_6_1_MISSING_HTML_TLS_INVALID")

    def test_consensus_voting_with_two_modalities(self):
        engine = FusionPolicyEngine()
        policy = engine.get_policy("consensus_fusion")
        engine.set_policy(policy)

        # Missing HTML: 2 modalities available (Lexical + Visual)
        # Both flag anomaly -> 2/2 -> PHISHING
        r1 = engine.execute(entropy=4.8, sdr_deviation=0.0, tls_valid=False, url="", has_html=False)
        self.assertEqual(r1.decision, "PHISHING")

        # 1 flags anomaly -> 1/2 -> SUSPICIOUS
        r2 = engine.execute(entropy=4.8, sdr_deviation=0.0, tls_valid=True, url="", has_html=False)
        self.assertEqual(r2.decision, "SUSPICIOUS")

        # 0 flag anomaly -> 0/2 -> LEGITIMATE
        r3 = engine.execute(entropy=3.2, sdr_deviation=0.0, tls_valid=True, url="", has_html=False)
        self.assertEqual(r3.decision, "LEGITIMATE")


if __name__ == "__main__":
    unittest.main(verbosity=2)
