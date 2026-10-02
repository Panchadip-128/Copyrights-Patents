
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
