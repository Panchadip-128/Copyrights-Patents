
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
