"""
CFP Analyzer - Main analyzer for Call for Papers documents

Implements proprietary analysis algorithms for CFP structure and content.
Copyright (c) 2026. All rights reserved.
"""

import re
from typing import Dict, List, Set, Tuple
from dataclasses import dataclass
from datetime import datetime


@dataclass
class CFPAnalysisResult:
    """Structured result from CFP analysis"""
    venue_name: str
    syntax_score: float
    professionalism_score: float
    urgency_indicators: List[str]
    suspicious_patterns: List[str]
    language_quality_score: float
    deadline_pressure_score: float
    contact_legitimacy_score: float
    overall_cfp_risk: float
    analysis_timestamp: datetime


class CFPAnalyzer:
    """
    Analyzes Call for Papers documents using proprietary rule-based algorithms.
    
    This analyzer implements a unique scoring methodology based on linguistic patterns,
    structural analysis, and credibility heuristics specifically designed for academic
    venue evaluation.
    """
    
    # Proprietary pattern definitions (copyright-protected expression)
    URGENCY_PATTERNS = [
        r'(?i)\b(hurry|urgent|limited|extended|last\s+chance|final\s+call)\b',
        r'(?i)\b(don\'t\s+miss|act\s+now|immediate|quick|fast\s+track)\b',
        r'(?i)\b(ends\s+soon|running\s+out|limited\s+time)\b'
    ]
    
    SUSPICIOUS_PATTERNS = [
        r'(?i)\b(guaranteed\s+acceptance|100%\s+acceptance|no\s+rejection)\b',
        r'(?i)\b(pay\s+first|payment\s+required|fee\s+mandatory)\b',
        r'(?i)\b(all\s+papers\s+accepted|every\s+paper\s+published)\b',
        r'(?i)\b(easy\s+acceptance|quick\s+publication)\b'
    ]
    
    PROFESSIONALISM_KEYWORDS = {
        'positive': ['peer-review', 'double-blind', 'committee', 'proceedings', 'indexing'],
        'negative': ['cheap', 'easy', 'quick', 'guaranteed', 'no-rejection']
    }
    
    def __init__(self):
        self.compiled_urgency = [re.compile(p) for p in self.URGENCY_PATTERNS]
        self.compiled_suspicious = [re.compile(p) for p in self.SUSPICIOUS_PATTERNS]
    
    def analyze(self, cfp_text: str, venue_name: str = "Unknown") -> CFPAnalysisResult:
        """
        Performs comprehensive CFP analysis using proprietary algorithms.
        
        Args:
            cfp_text: The Call for Papers text to analyze
            venue_name: Name of the venue (optional)
            
        Returns:
            CFPAnalysisResult containing detailed analysis metrics
        """
        # Extract urgency indicators
        urgency_indicators = self._detect_urgency(cfp_text)
        urgency_score = len(urgency_indicators) / 10.0  # Normalize to 0-1
        
        # Extract suspicious patterns
        suspicious = self._detect_suspicious_patterns(cfp_text)
        
        # Calculate syntax and professionalism scores
        syntax_score = self._calculate_syntax_score(cfp_text)
        professionalism_score = self._calculate_professionalism_score(cfp_text)
        
        # Evaluate language quality
        language_quality = self._evaluate_language_quality(cfp_text)
        
        # Check contact legitimacy
        contact_legitimacy = self._evaluate_contact_legitimacy(cfp_text)
        
        # Calculate overall risk (proprietary formula)
        overall_risk = self._calculate_overall_risk(
            urgency_score,
            len(suspicious),
            syntax_score,
            professionalism_score,
            language_quality,
            contact_legitimacy
        )
        
        return CFPAnalysisResult(
            venue_name=venue_name,
            syntax_score=syntax_score,
            professionalism_score=professionalism_score,
            urgency_indicators=urgency_indicators,
            suspicious_patterns=suspicious,
            language_quality_score=language_quality,
            deadline_pressure_score=min(urgency_score, 1.0),
            contact_legitimacy_score=contact_legitimacy,
            overall_cfp_risk=overall_risk,
            analysis_timestamp=datetime.now()
        )
    
    def _detect_urgency(self, text: str) -> List[str]:
        """Detects urgency indicators in CFP text"""
        found = []
        for pattern in self.compiled_urgency:
            matches = pattern.findall(text)
            found.extend(matches)
        return list(set(found))  # Remove duplicates
    
    def _detect_suspicious_patterns(self, text: str) -> List[str]:
        """Detects suspicious patterns indicating predatory behavior"""
        found = []
        for pattern in self.compiled_suspicious:
            matches = pattern.findall(text)
            found.extend(matches)
        return list(set(found))
    
    def _calculate_syntax_score(self, text: str) -> float:
        """
        Proprietary syntax quality scoring algorithm.
        
        Returns score from 0.0 (poor) to 1.0 (excellent)
        """
        if not text:
            return 0.0
        
        # Count sentences
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if not sentences:
            return 0.0
        
        # Calculate metrics
        avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences)
        
        # Penalize extreme lengths
        length_score = 1.0
        if avg_sentence_length < 5 or avg_sentence_length > 40:
            length_score = 0.5
        
        # Check for proper capitalization
        capitalization_score = sum(1 for s in sentences if s[0].isupper()) / len(sentences)
        
        # Check for grammatical markers
        has_articles = len(re.findall(r'\b(the|a|an)\b', text, re.IGNORECASE)) > 0
        has_conjunctions = len(re.findall(r'\b(and|but|or|nor|for|yet|so)\b', text, re.IGNORECASE)) > 0
        
        grammar_score = (int(has_articles) + int(has_conjunctions)) / 2.0
        
        # Combined score (proprietary weighting)
        final_score = (length_score * 0.3 + capitalization_score * 0.4 + grammar_score * 0.3)
        
        return min(final_score, 1.0)
    
    def _calculate_professionalism_score(self, text: str) -> float:
        """
        Proprietary professionalism scoring algorithm.
        
        Returns score from 0.0 (unprofessional) to 1.0 (highly professional)
        """
        text_lower = text.lower()
        
        # Count positive and negative keywords
        positive_count = sum(text_lower.count(kw) for kw in self.PROFESSIONALISM_KEYWORDS['positive'])
        negative_count = sum(text_lower.count(kw) for kw in self.PROFESSIONALISM_KEYWORDS['negative'])
        
        # Proprietary scoring formula
        if positive_count + negative_count == 0:
            return 0.5  # Neutral
        
        score = positive_count / (positive_count + negative_count + 1)
        
        # Penalize for negative keywords
        penalty = negative_count * 0.1
        
        return max(0.0, min(score - penalty, 1.0))
    
    def _evaluate_language_quality(self, text: str) -> float:
        """
        Evaluates overall language quality using proprietary heuristics.
        
        Returns score from 0.0 (poor) to 1.0 (excellent)
        """
        if not text:
            return 0.0
        
        # Check for excessive punctuation
        punct_ratio = len(re.findall(r'[!?]{2,}', text)) / max(len(text), 1)
        excessive_punct_penalty = min(punct_ratio * 10, 0.3)
        
        # Check for ALL CAPS
        words = text.split()
        all_caps_ratio = sum(1 for w in words if w.isupper() and len(w) > 2) / max(len(words), 1)
        caps_penalty = min(all_caps_ratio * 0.5, 0.3)
        
        # Check for spelling indicators (repeated letters)
        spelling_issues = len(re.findall(r'(\w)\1{2,}', text))
        spelling_penalty = min(spelling_issues * 0.05, 0.2)
        
        # Base score
        base_score = 1.0
        
        return max(0.0, base_score - excessive_punct_penalty - caps_penalty - spelling_penalty)
    
    def _evaluate_contact_legitimacy(self, text: str) -> float:
        """
        Evaluates legitimacy of contact information using proprietary rules.
        
        Returns score from 0.0 (suspicious) to 1.0 (legitimate)
        """
        score = 0.5  # Start neutral
        
        # Check for institutional email domains
        institutional_domains = re.findall(r'@([a-zA-Z0-9.-]+\.edu|[a-zA-Z0-9.-]+\.ac\.[a-z]{2})', text)
        if institutional_domains:
            score += 0.3
        
        # Check for suspicious email domains
        suspicious_domains = re.findall(r'@(gmail\.com|yahoo\.com|hotmail\.com|outlook\.com)', text)
        if suspicious_domains:
            score -= 0.2
        
        # Check for phone numbers
        has_phone = bool(re.search(r'\+?\d{1,3}[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}', text))
        if has_phone:
            score += 0.1
        
        # Check for physical address indicators
        has_address = bool(re.search(r'\b(street|avenue|road|building|suite|floor)\b', text, re.IGNORECASE))
        if has_address:
            score += 0.1
        
        return max(0.0, min(score, 1.0))
    
    def _calculate_overall_risk(
        self,
        urgency_score: float,
        suspicious_count: int,
        syntax_score: float,
        professionalism_score: float,
        language_quality: float,
        contact_legitimacy: float
    ) -> float:
        """
        Proprietary risk calculation formula.
        
        This formula is a unique expression of copyright-protected logic.
        
        Returns risk score from 0.0 (low risk) to 1.0 (high risk)
        """
        # Weighted components (proprietary weighting scheme)
        urgency_risk = urgency_score * 0.20
        suspicious_risk = min(suspicious_count * 0.15, 0.40)
        syntax_risk = (1.0 - syntax_score) * 0.10
        professionalism_risk = (1.0 - professionalism_score) * 0.15
        language_risk = (1.0 - language_quality) * 0.10
        contact_risk = (1.0 - contact_legitimacy) * 0.15
        
        # Aggregate risk (proprietary formula)
        total_risk = (
            urgency_risk +
            suspicious_risk +
            syntax_risk +
            professionalism_risk +
            language_risk +
            contact_risk
        )
        
        return min(total_risk, 1.0)
