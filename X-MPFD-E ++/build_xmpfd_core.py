import os
import math
from pathlib import Path

BASE_DIR = Path("d:/Copyrights/X-MPFD-E ++/x_mpfd_e_plus")

# Create directories
directories = [
    "fusion_policy_engine",
    "decision_risk_core",
    "explanation_synthesis_engine",
    "leakage_bias_auditor",
    "inference_api",
    "report_generator"
]

for d in directories:
    (BASE_DIR / d).mkdir(exist_ok=True)
    (BASE_DIR / d / "__init__.py").touch()

# Write decision_risk_core/detector.py
detector_code = """
import math
from ..fusion_policy_engine.fusion_engine import FusionPolicyEngine

class PhishingDetector:
    def __init__(self, fusion_policy='gated', explain=True):
        self.fusion_engine = FusionPolicyEngine()
        self.fusion_engine.set_policy(self.fusion_engine.get_policy(fusion_policy))
        self.explain = explain

    def analyze_url(self, url, html=None, screenshot=None):
        # 1. Lexical Extraction (Shannon Entropy)
        entropy = self._calculate_entropy(url)
        
        # 2. Structural Extraction (SDR)
        sdr_deviation = 0.0
        if html:
            sdr_deviation = self._calculate_sdr_deviation(html)
            
        # 3. Visual/TLS (Stub)
        tls_valid = True
        
        # Run Fusion Policy
        return self.fusion_engine.execute(entropy, sdr_deviation, tls_valid, url)

    def _calculate_entropy(self, url):
        prob_dict = {}
        for char in url:
            prob_dict[char] = prob_dict.get(char, 0) + 1
        entropy = 0.0
        for count in prob_dict.values():
            p = count / len(url)
            entropy -= p * math.log2(p)
        return entropy
        
    def _calculate_sdr_deviation(self, html):
        # Simulated deviation based on length for demonstration
        if len(html) < 500:
            return 80.0 # High deviation (shallow clone)
        return 10.0
"""
with open(BASE_DIR / "decision_risk_core" / "detector.py", "w") as f:
    f.write(detector_code)


# Write fusion_policy_engine/fusion_engine.py
fusion_code = """
class FusionPolicy:
    def __init__(self, name, strategy, weights=None, threshold=0.5):
        self.name = name
        self.strategy = strategy
        self.weights = weights
        self.threshold = threshold

class FusionStrategy:
    pass

class AnalysisResult:
    def __init__(self, decision, risk_score, confidence, features=None, explanation=""):
        self.decision = decision
        self.risk_score = risk_score
        self.confidence = confidence
        self.features = features or []
        self.explanation = explanation

class FusionPolicyEngine:
    def __init__(self):
        self.current_policy = None
        
    def get_policy(self, name):
        if name == 'gated_fusion' or name == 'gated':
            return FusionPolicy('gated', 'gated')
        return FusionPolicy(name, 'weighted')
        
    def set_policy(self, policy):
        self.current_policy = policy
        
    def execute(self, entropy, sdr, tls, url):
        features = [
            type('Feature', (), {'name': 'Lexical Entropy', 'value': entropy, 'provenance': type('Prov', (), {'source_modality': 'lexical', 'confidence': 1.0})()})(),
            type('Feature', (), {'name': 'SDR Deviation', 'value': sdr, 'provenance': type('Prov', (), {'source_modality': 'structural', 'confidence': 0.95})()})()
        ]
        
        # GATED FUSION LOGIC (from patent)
        if entropy > 4.0:
            return AnalysisResult("PHISHING_DGA", 0.99, "HIGH", features, f"Lexical entropy ({entropy:.2f}) exceeds mathematical threshold of 4.0. Structural compute bypassed.")
        else:
            if sdr > 50.0:
                if not tls:
                    return AnalysisResult("PHISHING_CLONE", 0.95, "HIGH", features, f"SDR deviation ({sdr:.1f}%) confirms structural anomaly.")
                else:
                    return AnalysisResult("SUSPICIOUS", 0.70, "MEDIUM", features, f"SDR deviation elevated, but TLS valid.")
            else:
                return AnalysisResult("LEGITIMATE", 0.05, "HIGH", features, "Entropy and structural parameters within normal bounds.")
"""
with open(BASE_DIR / "fusion_policy_engine" / "fusion_engine.py", "w") as f:
    f.write(fusion_code)


# Write explanation_synthesis_engine/explainer.py
explainer_code = """
class ExplanationSynthesizer:
    pass
"""
with open(BASE_DIR / "explanation_synthesis_engine" / "explainer.py", "w") as f:
    f.write(explainer_code)

# Write leakage_bias_auditor/auditor.py
auditor_code = """
class IntegrityAuditor:
    pass
"""
with open(BASE_DIR / "leakage_bias_auditor" / "auditor.py", "w") as f:
    f.write(auditor_code)

# Write inference_api/api.py
api_code = """
class InferenceAPI:
    pass
"""
with open(BASE_DIR / "inference_api" / "api.py", "w") as f:
    f.write(api_code)

# Write report_generator/report_generator.py (CLI needs it)
report_gen_code = """
class ReportGenerator:
    def generate_text_report(self, result):
        report = []
        report.append("==================================================")
        report.append(f"DECISION: {result.decision}")
        report.append(f"RISK SCORE: {result.risk_score:.2%}")
        report.append(f"CONFIDENCE: {result.confidence}")
        report.append("==================================================")
        report.append("MATHEMATICAL EXPLANATION:")
        report.append(result.explanation)
        report.append("--------------------------------------------------")
        report.append("FEATURE PROVENANCE:")
        for f in result.features:
            report.append(f"- {f.name}: {f.value:.2f} [Source: {f.provenance.source_modality}]")
        return chr(10).join(report)
        
    def generate_json_report(self, result):
        return "{}"
        
    def generate_html_report(self, result):
        return "<html></html>"
"""
with open(BASE_DIR / "report_generator" / "__init__.py", "w") as f:
    f.write(report_gen_code)

print("Scaffolded X-MPFD-E++ logic modules successfully.")
