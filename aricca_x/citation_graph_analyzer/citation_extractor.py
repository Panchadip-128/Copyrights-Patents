"""
Citation Extractor - Extracts citations from manuscript text

Implements proprietary citation extraction algorithms.
Copyright (c) 2026. All rights reserved.
"""

import re
from typing import Dict, List, Set, Tuple
from dataclasses import dataclass


@dataclass
class ExtractedCitation:
    """Represents a citation extracted from text"""
    reference_id: str
    position: int
    context: str
    sentence: str
    citation_type: str  # "support", "contrast", "methodology"


class CitationExtractor:
    """
    Extracts and analyzes citations from manuscript text.
    
    Uses proprietary natural language processing for citation detection.
    """
    
    # Citation patterns (proprietary)
    CITATION_PATTERNS = [
        r'\[(\d+(?:,\s*\d+)*)\]',  # [1], [1,2,3]
        r'\[(\d+-\d+)\]',  # [1-5]
        r'\(([A-Z][a-z]+\s+et\s+al\.,\s*\d{4})\)',  # (Smith et al., 2020)
        r'\(([A-Z][a-z]+\s+and\s+[A-Z][a-z]+,\s*\d{4})\)',  # (Smith and Jones, 2020)
    ]
    
    # Context indicators for citation type
    SUPPORT_INDICATORS = ['shown', 'demonstrated', 'proven', 'validated', 'confirmed']
    CONTRAST_INDICATORS = ['however', 'contrary', 'unlike', 'different', 'contrast']
    METHODOLOGY_INDICATORS = ['method', 'approach', 'technique', 'algorithm', 'using']
    
    def __init__(self):
        """Initialize the citation extractor"""
        self.patterns = [re.compile(p) for p in self.CITATION_PATTERNS]
    
    def extract_citations(
        self,
        text: str,
        references: List[Dict]
    ) -> List[ExtractedCitation]:
        """
        Extract all citations from text.
        
        Args:
            text: Manuscript text
            references: List of references
            
        Returns:
            List of ExtractedCitation objects
        """
        citations = []
        
        # Split into sentences
        sentences = self._split_sentences(text)
        
        for pattern in self.patterns:
            for i, sentence in enumerate(sentences):
                for match in pattern.finditer(sentence):
                    # Extract reference IDs
                    ref_ids = self._parse_reference_ids(match.group(1))
                    
                    for ref_id in ref_ids:
                        # Extract context
                        context = self._extract_context(sentences, i, window=2)
                        
                        # Determine citation type
                        cit_type = self._classify_citation(sentence)
                        
                        citations.append(ExtractedCitation(
                            reference_id=ref_id,
                            position=match.start(),
                            context=context,
                            sentence=sentence,
                            citation_type=cit_type
                        ))
        
        return citations
    
    def _split_sentences(self, text: str) -> List[str]:
        """Split text into sentences"""
        # Simple sentence splitting
        sentences = re.split(r'[.!?]+\s+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def _parse_reference_ids(self, ref_string: str) -> List[str]:
        """Parse reference IDs from citation string"""
        ids = []
        
        # Handle ranges like "1-5"
        if '-' in ref_string and ref_string.replace('-', '').isdigit():
            parts = ref_string.split('-')
            if len(parts) == 2:
                start, end = int(parts[0]), int(parts[1])
                ids.extend(str(i) for i in range(start, end + 1))
        # Handle comma-separated like "1,2,3"
        elif ',' in ref_string:
            ids.extend(i.strip() for i in ref_string.split(',') if i.strip())
        # Single ID
        else:
            ids.append(ref_string.strip())
        
        return ids
    
    def _extract_context(
        self,
        sentences: List[str],
        position: int,
        window: int = 2
    ) -> str:
        """Extract context around citation"""
        start = max(0, position - window)
        end = min(len(sentences), position + window + 1)
        return ' '.join(sentences[start:end])
    
    def _classify_citation(self, sentence: str) -> str:
        """
        Classify citation type based on context.
        
        Proprietary classification algorithm.
        """
        sentence_lower = sentence.lower()
        
        # Check for support indicators
        if any(ind in sentence_lower for ind in self.SUPPORT_INDICATORS):
            return "support"
        
        # Check for contrast indicators
        if any(ind in sentence_lower for ind in self.CONTRAST_INDICATORS):
            return "contrast"
        
        # Check for methodology indicators
        if any(ind in sentence_lower for ind in self.METHODOLOGY_INDICATORS):
            return "methodology"
        
        # Default
        return "support"
