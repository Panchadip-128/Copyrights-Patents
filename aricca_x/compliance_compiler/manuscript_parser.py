"""
Manuscript Parser - Parses manuscripts into intermediate representation

Implements proprietary parsing algorithms for various manuscript formats.
Copyright (c) 2026. All rights reserved.
"""

import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path


@dataclass
class ManuscriptSection:
    """Represents a section of the manuscript"""
    title: str
    level: int  # 1 for main sections, 2 for subsections, etc.
    content: str
    line_start: int
    line_end: int
    word_count: int


@dataclass
class ManuscriptReference:
    """Represents a bibliographic reference"""
    ref_id: str
    raw_text: str
    authors: List[str]
    title: Optional[str]
    year: Optional[int]
    venue: Optional[str]
    citation_count: int = 0


@dataclass
class ManuscriptMetadata:
    """Metadata extracted from manuscript"""
    title: Optional[str] = None
    authors: List[str] = field(default_factory=list)
    affiliations: List[str] = field(default_factory=list)
    abstract: Optional[str] = None
    keywords: List[str] = field(default_factory=list)
    page_count: int = 0
    word_count: int = 0


@dataclass
class ParsedManuscript:
    """Complete intermediate representation of a manuscript"""
    file_path: str
    file_format: str
    metadata: ManuscriptMetadata
    sections: List[ManuscriptSection]
    references: List[ManuscriptReference]
    figures_count: int
    tables_count: int
    equations_count: int
    citation_count: int
    raw_text: str
    parse_timestamp: datetime
    parse_confidence: float


class ManuscriptParser:
    """
    Parses manuscripts into structured intermediate representation.
    
    Implements proprietary parsing algorithms for PDF, LaTeX, and DOCX formats.
    """
    
    # Proprietary section detection patterns
    SECTION_PATTERNS = [
        # Numbered sections: "1. Introduction"
        r'^(\d+\.?\d*)\s+([A-Z][^\n]{3,80})\s*$',
        # Roman numerals: "I. Introduction"
        r'^([IVX]+\.)\s+([A-Z][^\n]{3,80})\s*$',
        # Letter sections: "A. Introduction"
        r'^([A-Z]\.)\s+([A-Z][^\n]{3,80})\s*$',
    ]
    
    # Reference patterns
    REFERENCE_PATTERNS = [
        # [1] Author et al., "Title", Venue, Year
        r'\[(\d+)\]\s+([^,]+),\s+"([^"]+)",\s+([^,]+),\s+(\d{4})',
        # Author et al. (Year). Title. Venue.
        r'([^.]+)\s+\((\d{4})\)\.\s+([^.]+)\.\s+([^.]+)\.',
    ]
    
    def __init__(self):
        """Initialize the manuscript parser"""
        self.section_patterns = [re.compile(p, re.MULTILINE) for p in self.SECTION_PATTERNS]
        self.reference_patterns = [re.compile(p) for p in self.REFERENCE_PATTERNS]
    
    def parse(self, file_path: str, file_format: str) -> ParsedManuscript:
        """
        Parse manuscript file into intermediate representation.
        
        Args:
            file_path: Path to manuscript file
            file_format: Format ("pdf", "latex", "docx")
            
        Returns:
            ParsedManuscript object
        """
        # Extract raw text based on format
        raw_text = self._extract_text(file_path, file_format)
        
        # Parse metadata
        metadata = self._parse_metadata(raw_text)
        
        # Parse sections
        sections = self._parse_sections(raw_text)
        
        # Parse references
        references = self._parse_references(raw_text)
        
        # Count elements
        figures_count = self._count_figures(raw_text)
        tables_count = self._count_tables(raw_text)
        equations_count = self._count_equations(raw_text)
        citation_count = self._count_citations(raw_text)
        
        # Calculate parse confidence
        confidence = self._calculate_parse_confidence(
            metadata, sections, references
        )
        
        return ParsedManuscript(
            file_path=file_path,
            file_format=file_format,
            metadata=metadata,
            sections=sections,
            references=references,
            figures_count=figures_count,
            tables_count=tables_count,
            equations_count=equations_count,
            citation_count=citation_count,
            raw_text=raw_text,
            parse_timestamp=datetime.now(),
            parse_confidence=confidence
        )
    
    def _extract_text(self, file_path: str, file_format: str) -> str:
        """
        Extract text from manuscript file.
        
        Note: In a real implementation, this would use libraries like:
        - PyPDF2 or pdfplumber for PDF
        - Direct reading for LaTeX
        - python-docx for DOCX
        """
        # Placeholder implementation
        if Path(file_path).exists():
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    return f.read()
            except Exception:
                return ""
        return ""
    
    def _parse_metadata(self, text: str) -> ManuscriptMetadata:
        """Parse manuscript metadata"""
        metadata = ManuscriptMetadata()
        
        # Extract title (usually first major line)
        lines = [l.strip() for l in text.split('\n') if l.strip()]
        if lines:
            # Find first substantial line (likely title)
            for line in lines[:10]:
                if 20 < len(line) < 200 and not line.startswith(('Abstract', 'Keywords')):
                    metadata.title = line
                    break
        
        # Extract abstract
        abstract_match = re.search(
            r'(?:abstract|ABSTRACT)\s*[:\-]?\s*\n?(.*?)(?:\n\n|keywords|introduction)',
            text,
            re.IGNORECASE | re.DOTALL
        )
        if abstract_match:
            metadata.abstract = abstract_match.group(1).strip()
        
        # Extract keywords
        keywords_match = re.search(
            r'(?:keywords|KEYWORDS)\s*[:\-]?\s*\n?(.+?)(?:\n\n|\n[A-Z])',
            text,
            re.IGNORECASE | re.DOTALL
        )
        if keywords_match:
            keywords_text = keywords_match.group(1)
            # Split by commas, semicolons, or newlines
            metadata.keywords = [
                k.strip() for k in re.split(r'[,;\n]', keywords_text)
                if k.strip()
            ]
        
        # Count pages and words (approximate)
        metadata.page_count = text.count('\f') + 1  # Form feed character
        metadata.word_count = len(text.split())
        
        # Extract authors (look for email patterns or author sections)
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text[:2000])  # Look in first 2000 chars
        if emails:
            metadata.authors = [f"Author <{email}>" for email in emails[:5]]
        
        return metadata
    
    def _parse_sections(self, text: str) -> List[ManuscriptSection]:
        """Parse document sections"""
        sections = []
        lines = text.split('\n')
        
        # Find section headers
        for i, line in enumerate(lines):
            for pattern in self.section_patterns:
                match = pattern.match(line.strip())
                if match:
                    section_num = match.group(1)
                    section_title = match.group(2)
                    
                    # Determine section level
                    if '.' in section_num:
                        level = section_num.count('.') + 1
                    else:
                        level = 1
                    
                    # Find section content (until next section)
                    content_lines = []
                    j = i + 1
                    while j < len(lines):
                        next_line = lines[j].strip()
                        # Check if it's another section
                        is_section = any(p.match(next_line) for p in self.section_patterns)
                        if is_section:
                            break
                        content_lines.append(lines[j])
                        j += 1
                    
                    content = '\n'.join(content_lines)
                    
                    sections.append(ManuscriptSection(
                        title=section_title,
                        level=level,
                        content=content,
                        line_start=i,
                        line_end=j,
                        word_count=len(content.split())
                    ))
                    
                    break
        
        return sections
    
    def _parse_references(self, text: str) -> List[ManuscriptReference]:
        """Parse bibliographic references"""
        references = []
        
        # Find references section
        ref_section_match = re.search(
            r'(?:references|bibliography|works cited)\s*\n(.*?)(?:\n\n\n|$)',
            text,
            re.IGNORECASE | re.DOTALL
        )
        
        if not ref_section_match:
            return references
        
        ref_text = ref_section_match.group(1)
        
        # Extract individual references
        # Split by reference numbers like [1], [2], etc.
        ref_splits = re.split(r'\n\[(\d+)\]', ref_text)
        
        for i in range(1, len(ref_splits), 2):
            if i + 1 < len(ref_splits):
                ref_id = ref_splits[i]
                ref_content = ref_splits[i + 1].strip()
                
                # Parse reference components
                authors = self._extract_authors(ref_content)
                title = self._extract_title(ref_content)
                year = self._extract_year(ref_content)
                
                references.append(ManuscriptReference(
                    ref_id=ref_id,
                    raw_text=ref_content,
                    authors=authors,
                    title=title,
                    year=year,
                    venue=None
                ))
        
        return references
    
    def _extract_authors(self, ref_text: str) -> List[str]:
        """Extract author names from reference text"""
        # Simple heuristic: names before the first comma or period
        match = re.match(r'^([^,.]+(?:,\s*[^,.]+)*)[,.]', ref_text)
        if match:
            authors_text = match.group(1)
            # Split by "and" or comma
            authors = re.split(r'\s+and\s+|,\s*', authors_text)
            return [a.strip() for a in authors if a.strip()]
        return []
    
    def _extract_title(self, ref_text: str) -> Optional[str]:
        """Extract title from reference text"""
        # Look for text in quotes
        match = re.search(r'"([^"]+)"', ref_text)
        if match:
            return match.group(1)
        return None
    
    def _extract_year(self, ref_text: str) -> Optional[int]:
        """Extract publication year from reference text"""
        match = re.search(r'\b(19|20)\d{2}\b', ref_text)
        if match:
            return int(match.group(0))
        return None
    
    def _count_figures(self, text: str) -> int:
        """Count figures in manuscript"""
        return len(re.findall(r'(?:figure|fig\.)\s+\d+', text, re.IGNORECASE))
    
    def _count_tables(self, text: str) -> int:
        """Count tables in manuscript"""
        return len(re.findall(r'table\s+\d+', text, re.IGNORECASE))
    
    def _count_equations(self, text: str) -> int:
        """Count equations in manuscript"""
        # Look for equation markers
        equation_markers = len(re.findall(r'\$\$.*?\$\$', text, re.DOTALL))
        equation_markers += len(re.findall(r'\\begin\{equation\}', text))
        return equation_markers
    
    def _count_citations(self, text: str) -> int:
        """Count in-text citations"""
        # Count citation patterns like [1], [2,3], etc.
        return len(re.findall(r'\[\d+(?:,\s*\d+)*\]', text))
    
    def _calculate_parse_confidence(
        self,
        metadata: ManuscriptMetadata,
        sections: List[ManuscriptSection],
        references: List[ManuscriptReference]
    ) -> float:
        """
        Calculate confidence in parse results.
        
        Proprietary confidence scoring algorithm.
        """
        confidence = 0.0
        
        # Metadata completeness
        if metadata.title:
            confidence += 0.2
        if metadata.abstract:
            confidence += 0.2
        if metadata.keywords:
            confidence += 0.1
        
        # Structure completeness
        if len(sections) >= 4:  # Typical: Intro, Methods, Results, Conclusion
            confidence += 0.3
        elif len(sections) >= 2:
            confidence += 0.15
        
        # References presence
        if len(references) >= 10:
            confidence += 0.2
        elif len(references) >= 5:
            confidence += 0.1
        
        return min(confidence, 1.0)
