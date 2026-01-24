"""
CFP Extractor - Extracts Call for Papers information from various sources

Implements proprietary extraction algorithms for CFP data.
Copyright (c) 2026. All rights reserved.
"""

import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
from urllib.parse import urlparse


@dataclass
class ExtractedCFP:
    """Structured CFP information"""
    venue_name: Optional[str]
    venue_type: Optional[str]  # "conference" or "journal"
    submission_deadline: Optional[datetime]
    notification_date: Optional[datetime]
    event_date: Optional[datetime]
    location: Optional[str]
    topics: List[str]
    email_contacts: List[str]
    website_url: Optional[str]
    submission_system: Optional[str]
    raw_text: str
    extraction_confidence: float


class CFPExtractor:
    """
    Extracts structured information from Call for Papers documents.
    
    Uses proprietary natural language processing and pattern matching
    algorithms to identify and extract key CFP components.
    """
    
    # Proprietary extraction patterns (copyright-protected)
    DATE_PATTERNS = [
        r'(\w+\s+\d{1,2},?\s+\d{4})',  # January 15, 2026
        r'(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})',  # 01/15/2026 or 15-01-26
        r'(\d{4}[-/]\d{1,2}[-/]\d{1,2})',  # 2026-01-15
    ]
    
    DEADLINE_INDICATORS = [
        r'submission\s+deadline\s*:?\s*',
        r'paper\s+submission\s*:?\s*',
        r'deadline\s*:?\s*',
        r'due\s+date\s*:?\s*'
    ]
    
    VENUE_TYPE_INDICATORS = {
        'conference': [
            r'\bconference\b', r'\bsymposium\b', r'\bworkshop\b',
            r'\bcongress\b', r'\bmeeting\b'
        ],
        'journal': [
            r'\bjournal\b', r'\bperiodical\b', r'\btransactions\b',
            r'\bletters\b', r'\bproceedings\b'
        ]
    }
    
    SUBMISSION_SYSTEMS = [
        r'easychair',
        r'openconf',
        r'edas',
        r'microsoft\s+cmt',
        r'hotcrp'
    ]
    
    def __init__(self):
        """Initialize the CFP extractor with compiled patterns"""
        self.date_patterns = [re.compile(p, re.IGNORECASE) for p in self.DATE_PATTERNS]
        self.deadline_patterns = [re.compile(p, re.IGNORECASE) for p in self.DEADLINE_INDICATORS]
        self.system_patterns = [re.compile(p, re.IGNORECASE) for p in self.SUBMISSION_SYSTEMS]
    
    def extract(self, cfp_text: str, source_url: Optional[str] = None) -> ExtractedCFP:
        """
        Extract structured information from CFP text.
        
        Args:
            cfp_text: The Call for Papers text
            source_url: Optional source URL
            
        Returns:
            ExtractedCFP object with extracted information
        """
        # Extract venue name
        venue_name = self._extract_venue_name(cfp_text)
        
        # Determine venue type
        venue_type = self._determine_venue_type(cfp_text)
        
        # Extract dates
        dates = self._extract_dates(cfp_text)
        
        # Extract location
        location = self._extract_location(cfp_text)
        
        # Extract topics
        topics = self._extract_topics(cfp_text)
        
        # Extract email contacts
        emails = self._extract_emails(cfp_text)
        
        # Extract submission system
        submission_system = self._extract_submission_system(cfp_text)
        
        # Extract website URL
        website = self._extract_website(cfp_text, source_url)
        
        # Calculate extraction confidence
        confidence = self._calculate_extraction_confidence(
            venue_name, venue_type, dates, location, topics, emails
        )
        
        return ExtractedCFP(
            venue_name=venue_name,
            venue_type=venue_type,
            submission_deadline=dates.get('submission'),
            notification_date=dates.get('notification'),
            event_date=dates.get('event'),
            location=location,
            topics=topics,
            email_contacts=emails,
            website_url=website,
            submission_system=submission_system,
            raw_text=cfp_text,
            extraction_confidence=confidence
        )
    
    def _extract_venue_name(self, text: str) -> Optional[str]:
        """Extract venue name using proprietary heuristics"""
        # Look for common patterns
        patterns = [
            r'^([A-Z][^.!?\n]{10,100})\n',  # First line if capitalized
            r'(?:conference|symposium|workshop|journal)\s+on\s+([^.!?\n]+)',
            r'([A-Z]{3,}(?:\s+\d{4})?)\s*[-–—]\s*(?:call|cfp)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
            if match:
                name = match.group(1).strip()
                if 5 < len(name) < 150:
                    return name
        
        return None
    
    def _determine_venue_type(self, text: str) -> Optional[str]:
        """Determine if venue is conference or journal"""
        conf_score = 0
        journal_score = 0
        
        text_lower = text.lower()
        
        for pattern in self.VENUE_TYPE_INDICATORS['conference']:
            if re.search(pattern, text_lower):
                conf_score += 1
        
        for pattern in self.VENUE_TYPE_INDICATORS['journal']:
            if re.search(pattern, text_lower):
                journal_score += 1
        
        if conf_score > journal_score:
            return "conference"
        elif journal_score > conf_score:
            return "journal"
        
        return None
    
    def _extract_dates(self, text: str) -> Dict[str, Optional[datetime]]:
        """Extract important dates from CFP text"""
        dates = {
            'submission': None,
            'notification': None,
            'event': None
        }
        
        # Find all date strings
        date_strings = []
        for pattern in self.date_patterns:
            matches = pattern.findall(text)
            date_strings.extend(matches)
        
        # Try to associate dates with their purpose
        lines = text.split('\n')
        for i, line in enumerate(lines):
            line_lower = line.lower()
            
            # Check for submission deadline
            if any(re.search(p, line_lower) for p in self.deadline_patterns):
                date = self._parse_date_from_line(line, date_strings)
                if date:
                    dates['submission'] = date
            
            # Check for notification date
            if 'notification' in line_lower or 'acceptance' in line_lower:
                date = self._parse_date_from_line(line, date_strings)
                if date:
                    dates['notification'] = date
            
            # Check for event/conference date
            if 'conference date' in line_lower or 'event date' in line_lower:
                date = self._parse_date_from_line(line, date_strings)
                if date:
                    dates['event'] = date
        
        return dates
    
    def _parse_date_from_line(self, line: str, date_strings: List[str]) -> Optional[datetime]:
        """Parse a date from a line of text"""
        for date_str in date_strings:
            if date_str in line:
                try:
                    # Try multiple date formats
                    for fmt in ['%B %d, %Y', '%b %d, %Y', '%m/%d/%Y', '%Y-%m-%d', '%d-%m-%Y']:
                        try:
                            return datetime.strptime(date_str.strip(), fmt)
                        except ValueError:
                            continue
                except Exception:
                    pass
        return None
    
    def _extract_location(self, text: str) -> Optional[str]:
        """Extract venue location using proprietary heuristics"""
        # Look for location patterns
        patterns = [
            r'(?:location|venue|held\s+in|held\s+at)\s*:?\s*([A-Z][^.!?\n]{5,60})',
            r'([A-Z][a-z]+,\s+[A-Z][a-z]+(?:,\s+[A-Z]{2,})?)',  # City, Country
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                location = match.group(1).strip()
                if 3 < len(location) < 100:
                    return location
        
        return None
    
    def _extract_topics(self, text: str) -> List[str]:
        """Extract research topics/themes"""
        topics = []
        
        # Look for topics sections
        topics_section = re.search(
            r'(?:topics|themes|areas|scope)\s*:?\s*\n((?:[-•*]\s*.+\n?)+)',
            text,
            re.IGNORECASE | re.MULTILINE
        )
        
        if topics_section:
            lines = topics_section.group(1).split('\n')
            for line in lines:
                # Clean up bullet points
                topic = re.sub(r'^[-•*]\s*', '', line.strip())
                if topic and len(topic) > 5:
                    topics.append(topic)
        
        return topics[:20]  # Limit to top 20
    
    def _extract_emails(self, text: str) -> List[str]:
        """Extract email addresses"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        return list(set(emails))  # Remove duplicates
    
    def _extract_submission_system(self, text: str) -> Optional[str]:
        """Extract submission management system name"""
        for pattern in self.system_patterns:
            match = pattern.search(text)
            if match:
                return match.group(0).title()
        return None
    
    def _extract_website(self, text: str, source_url: Optional[str]) -> Optional[str]:
        """Extract website URL"""
        if source_url:
            return source_url
        
        # Look for URLs in text
        url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
        urls = re.findall(url_pattern, text)
        
        if urls:
            return urls[0]
        
        return None
    
    def _calculate_extraction_confidence(
        self,
        venue_name: Optional[str],
        venue_type: Optional[str],
        dates: Dict[str, Optional[datetime]],
        location: Optional[str],
        topics: List[str],
        emails: List[str]
    ) -> float:
        """
        Proprietary confidence calculation for extraction quality.
        
        Returns confidence score from 0.0 to 1.0
        """
        score = 0.0
        
        # Component weights
        if venue_name:
            score += 0.25
        if venue_type:
            score += 0.15
        if dates['submission']:
            score += 0.20
        if location:
            score += 0.10
        if topics:
            score += min(len(topics) * 0.02, 0.15)
        if emails:
            score += min(len(emails) * 0.05, 0.15)
        
        return min(score, 1.0)
