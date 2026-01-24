"""
Syntax Pattern Detector - Detects linguistic patterns in CFP documents

Implements proprietary pattern recognition for academic venue analysis.
Copyright (c) 2026. All rights reserved.
"""

import re
from typing import Dict, List, Tuple
from dataclasses import dataclass
from enum import Enum


class PatternCategory(Enum):
    """Categories of detected patterns"""
    URGENCY = "urgency"
    LEGITIMACY = "legitimacy"
    PROFESSIONALISM = "professionalism"
    TECHNICAL = "technical"
    CONTACT = "contact"
    FINANCIAL = "financial"


@dataclass
class DetectedPattern:
    """Represents a detected pattern in text"""
    category: PatternCategory
    pattern_text: str
    confidence: float
    position: int
    context: str


class SyntaxPatternDetector:
    """
    Detects and categorizes syntax patterns in Call for Papers documents.
    
    Uses proprietary pattern matching algorithms and heuristics specifically
    designed for academic venue credibility assessment.
    """
    
    # Proprietary pattern library (copyright-protected)
    PATTERN_LIBRARY = {
        PatternCategory.URGENCY: [
            (r'\b(extended|deadline\s+extended)\b', 0.7, "Deadline extension"),
            (r'\b(last\s+call|final\s+reminder)\b', 0.8, "Final call language"),
            (r'\b(submit\s+now|act\s+quickly)\b', 0.9, "Action urgency"),
        ],
        PatternCategory.LEGITIMACY: [
            (r'\b(indexed\s+by|scopus|web\s+of\s+science)\b', 0.9, "Major indexing claim"),
            (r'\b(peer[\s-]review|double[\s-]blind)\b', 0.8, "Review process mention"),
            (r'\b(conference\s+proceedings|journal\s+publication)\b', 0.7, "Publication type"),
        ],
        PatternCategory.PROFESSIONALISM: [
            (r'\b(program\s+committee|technical\s+committee)\b', 0.8, "Committee structure"),
            (r'\b(keynote|invited\s+speaker|plenary)\b', 0.7, "Speaker mentions"),
            (r'\b(call\s+for\s+papers|submission\s+guidelines)\b', 0.6, "Standard CFP language"),
        ],
        PatternCategory.TECHNICAL: [
            (r'\b(LaTeX|BibTeX|IEEE\s+format|ACM\s+format)\b', 0.8, "Technical format"),
            (r'\b(page\s+limit|word\s+count|submission\s+portal)\b', 0.7, "Submission requirements"),
            (r'\b(camera[\s-]ready|copyright\s+form)\b', 0.6, "Publication process"),
        ],
        PatternCategory.CONTACT: [
            (r'@[a-zA-Z0-9.-]+\.(edu|ac\.[a-z]{2})', 0.9, "Academic email"),
            (r'@[a-zA-Z0-9.-]+\.(com|net|org)', 0.4, "Commercial email"),
            (r'\b(contact|inquiry|questions)\s*:', 0.6, "Contact section"),
        ],
        PatternCategory.FINANCIAL: [
            (r'\b(registration\s+fee|publication\s+fee|processing\s+fee)\b', 0.7, "Fee mention"),
            (r'\b(early\s+bird|discount|waiver)\b', 0.5, "Fee incentives"),
            (r'\b(\$|USD|EUR|GBP)\s*\d+', 0.8, "Specific fee amount"),
        ]
    }
    
    def __init__(self):
        """Initialize the pattern detector with compiled patterns"""
        self.compiled_patterns = {}
        for category, patterns in self.PATTERN_LIBRARY.items():
            self.compiled_patterns[category] = [
                (re.compile(pattern, re.IGNORECASE), confidence, description)
                for pattern, confidence, description in patterns
            ]
    
    def detect_patterns(self, text: str, min_confidence: float = 0.5) -> List[DetectedPattern]:
        """
        Detect all patterns in the given text.
        
        Args:
            text: Text to analyze
            min_confidence: Minimum confidence threshold for pattern detection
            
        Returns:
            List of DetectedPattern objects
        """
        detected = []
        
        for category, patterns in self.compiled_patterns.items():
            for compiled_pattern, confidence, description in patterns:
                if confidence < min_confidence:
                    continue
                
                for match in compiled_pattern.finditer(text):
                    # Extract context (50 chars before and after)
                    start = max(0, match.start() - 50)
                    end = min(len(text), match.end() + 50)
                    context = text[start:end]
                    
                    detected.append(DetectedPattern(
                        category=category,
                        pattern_text=match.group(0),
                        confidence=confidence,
                        position=match.start(),
                        context=context
                    ))
        
        # Sort by position
        detected.sort(key=lambda x: x.position)
        
        return detected
    
    def analyze_pattern_distribution(self, text: str) -> Dict[PatternCategory, int]:
        """
        Analyze the distribution of pattern categories in text.
        
        Returns:
            Dictionary mapping categories to occurrence counts
        """
        patterns = self.detect_patterns(text)
        distribution = {category: 0 for category in PatternCategory}
        
        for pattern in patterns:
            distribution[pattern.category] += 1
        
        return distribution
    
    def calculate_legitimacy_indicators(self, text: str) -> Dict[str, float]:
        """
        Proprietary legitimacy scoring based on pattern distribution.
        
        Returns:
            Dictionary of legitimacy indicators with scores 0.0-1.0
        """
        distribution = self.analyze_pattern_distribution(text)
        patterns = self.detect_patterns(text)
        
        # Calculate weighted scores
        legitimacy_score = min(distribution[PatternCategory.LEGITIMACY] * 0.2, 1.0)
        professionalism_score = min(distribution[PatternCategory.PROFESSIONALISM] * 0.15, 1.0)
        technical_score = min(distribution[PatternCategory.TECHNICAL] * 0.15, 1.0)
        
        # Negative indicators
        urgency_penalty = min(distribution[PatternCategory.URGENCY] * 0.1, 0.5)
        
        # Contact quality
        contact_patterns = [p for p in patterns if p.category == PatternCategory.CONTACT]
        academic_contacts = sum(1 for p in contact_patterns if 'Academic email' in p.context)
        contact_score = min(academic_contacts * 0.3, 1.0)
        
        return {
            'legitimacy_score': legitimacy_score,
            'professionalism_score': professionalism_score,
            'technical_score': technical_score,
            'contact_quality_score': contact_score,
            'urgency_penalty': urgency_penalty,
            'overall_indicator': max(0.0, (legitimacy_score + professionalism_score + 
                                          technical_score + contact_score - urgency_penalty) / 4.0)
        }
    
    def extract_key_phrases(self, text: str, top_n: int = 10) -> List[Tuple[str, PatternCategory, float]]:
        """
        Extract top key phrases from text based on pattern detection.
        
        Returns:
            List of (phrase, category, confidence) tuples
        """
        patterns = self.detect_patterns(text)
        
        # Sort by confidence
        patterns.sort(key=lambda x: x.confidence, reverse=True)
        
        # Return top N unique phrases
        seen = set()
        key_phrases = []
        
        for pattern in patterns:
            if pattern.pattern_text.lower() not in seen and len(key_phrases) < top_n:
                seen.add(pattern.pattern_text.lower())
                key_phrases.append((
                    pattern.pattern_text,
                    pattern.category,
                    pattern.confidence
                ))
        
        return key_phrases
