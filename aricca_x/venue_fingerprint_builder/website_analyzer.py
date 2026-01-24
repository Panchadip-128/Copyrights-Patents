"""
Website Analyzer - Analyzes venue websites for credibility assessment

Implements proprietary website analysis algorithms.
Copyright (c) 2026. All rights reserved.
"""

import re
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass
from urllib.parse import urlparse, urljoin
from datetime import datetime


@dataclass
class WebsiteAnalysisResult:
    """Results from website analysis"""
    url: str
    domain: str
    has_ssl: bool
    page_count: int
    pages: List[str]
    max_navigation_depth: int
    sections: List[str]
    has_contact_page: bool
    has_about_page: bool
    has_submission_page: bool
    is_responsive: bool
    domain_age_indicator: Optional[str]
    external_links_count: int
    social_media_presence: List[str]
    credibility_score: float
    analysis_timestamp: datetime


class WebsiteAnalyzer:
    """
    Analyzes academic venue websites for structural and credibility assessment.
    
    Uses proprietary algorithms to evaluate website architecture, content
    organization, and credibility indicators.
    """
    
    # Proprietary classification patterns
    PAGE_TYPE_PATTERNS = {
        'about': [r'/about', r'/overview', r'/introduction'],
        'committee': [r'/committee', r'/organization', r'/team'],
        'submission': [r'/submit', r'/submission', r'/authors'],
        'program': [r'/program', r'/schedule', r'/agenda'],
        'registration': [r'/register', r'/registration', r'/attend'],
        'contact': [r'/contact', r'/reach', r'/inquiry'],
        'cfp': [r'/cfp', r'/call-for-papers', r'/participate'],
        'venue': [r'/venue', r'/location', r'/travel']
    }
    
    SOCIAL_MEDIA_PATTERNS = {
        'twitter': r'twitter\.com/[\w]+',
        'linkedin': r'linkedin\.com/(?:company|in)/[\w-]+',
        'facebook': r'facebook\.com/[\w.]+',
        'youtube': r'youtube\.com/(?:channel|user)/[\w-]+'
    }
    
    def __init__(self):
        """Initialize the website analyzer"""
        self.page_patterns = {
            page_type: [re.compile(p, re.IGNORECASE) for p in patterns]
            for page_type, patterns in self.PAGE_TYPE_PATTERNS.items()
        }
        self.social_patterns = {
            platform: re.compile(pattern, re.IGNORECASE)
            for platform, pattern in self.SOCIAL_MEDIA_PATTERNS.items()
        }
    
    def analyze_website(
        self,
        url: str,
        html_content: Optional[str] = None,
        sitemap: Optional[List[str]] = None
    ) -> WebsiteAnalysisResult:
        """
        Analyze a venue website for credibility indicators.
        
        Args:
            url: Website URL
            html_content: Optional HTML content of main page
            sitemap: Optional list of pages in the site
            
        Returns:
            WebsiteAnalysisResult with analysis findings
        """
        # Parse URL
        parsed = urlparse(url)
        domain = parsed.netloc
        has_ssl = parsed.scheme == 'https'
        
        # Analyze pages
        pages = sitemap if sitemap else []
        page_types = self._classify_pages(pages)
        
        # Calculate navigation depth
        max_depth = self._calculate_navigation_depth(pages)
        
        # Identify sections
        sections = self._identify_sections(html_content or "", pages)
        
        # Check for key pages
        has_contact = 'contact' in page_types
        has_about = 'about' in page_types
        has_submission = 'submission' in page_types
        
        # Analyze responsiveness (from HTML)
        is_responsive = self._check_responsive_design(html_content or "")
        
        # Count external links
        external_links = self._count_external_links(html_content or "", domain)
        
        # Detect social media presence
        social_media = self._detect_social_media(html_content or "")
        
        # Calculate credibility score
        credibility = self._calculate_website_credibility(
            has_ssl, len(pages), has_contact, has_about, has_submission,
            is_responsive, max_depth, external_links, social_media
        )
        
        return WebsiteAnalysisResult(
            url=url,
            domain=domain,
            has_ssl=has_ssl,
            page_count=len(pages),
            pages=pages,
            max_navigation_depth=max_depth,
            sections=list(page_types.keys()),
            has_contact_page=has_contact,
            has_about_page=has_about,
            has_submission_page=has_submission,
            is_responsive=is_responsive,
            domain_age_indicator=None,  # Would require WHOIS lookup
            external_links_count=external_links,
            social_media_presence=social_media,
            credibility_score=credibility,
            analysis_timestamp=datetime.now()
        )
    
    def _classify_pages(self, pages: List[str]) -> Dict[str, List[str]]:
        """Classify pages by type"""
        classified = {}
        
        for page in pages:
            for page_type, patterns in self.page_patterns.items():
                for pattern in patterns:
                    if pattern.search(page):
                        if page_type not in classified:
                            classified[page_type] = []
                        classified[page_type].append(page)
                        break
        
        return classified
    
    def _calculate_navigation_depth(self, pages: List[str]) -> int:
        """
        Calculate maximum navigation depth.
        
        Proprietary algorithm for measuring site structure depth.
        """
        if not pages:
            return 0
        
        max_depth = 0
        for page in pages:
            # Count path segments
            parsed = urlparse(page)
            segments = [s for s in parsed.path.split('/') if s]
            depth = len(segments)
            max_depth = max(max_depth, depth)
        
        return max_depth
    
    def _identify_sections(self, html_content: str, pages: List[str]) -> List[str]:
        """Identify major sections of the website"""
        sections = set()
        
        # From HTML navigation
        nav_patterns = [
            r'<nav[^>]*>(.*?)</nav>',
            r'<menu[^>]*>(.*?)</menu>',
            r'class=["\'](?:nav|menu|navigation)["\'][^>]*>(.*?)</(?:div|ul|nav)>'
        ]
        
        for pattern in nav_patterns:
            matches = re.findall(pattern, html_content, re.DOTALL | re.IGNORECASE)
            for match in matches:
                # Extract link text
                links = re.findall(r'<a[^>]*>(.*?)</a>', match, re.IGNORECASE)
                sections.update(link.strip() for link in links if link.strip())
        
        # From page URLs
        for page in pages:
            parsed = urlparse(page)
            segments = [s for s in parsed.path.split('/') if s]
            if segments:
                sections.add(segments[0])
        
        return list(sections)
    
    def _check_responsive_design(self, html_content: str) -> bool:
        """
        Check for responsive design indicators.
        
        Proprietary heuristics for detecting mobile-friendly design.
        """
        if not html_content:
            return False
        
        # Check for viewport meta tag
        has_viewport = bool(re.search(
            r'<meta[^>]*name=["\']viewport["\']',
            html_content,
            re.IGNORECASE
        ))
        
        # Check for media queries
        has_media_queries = bool(re.search(
            r'@media[^{]*\([^)]*(?:max-width|min-width)',
            html_content,
            re.IGNORECASE
        ))
        
        # Check for responsive frameworks
        has_framework = bool(re.search(
            r'bootstrap|foundation|bulma|tailwind',
            html_content,
            re.IGNORECASE
        ))
        
        return has_viewport or has_media_queries or has_framework
    
    def _count_external_links(self, html_content: str, domain: str) -> int:
        """Count external links in HTML content"""
        if not html_content:
            return 0
        
        # Extract all links
        links = re.findall(r'<a[^>]*href=["\']([^"\']+)["\']', html_content, re.IGNORECASE)
        
        external_count = 0
        for link in links:
            if link.startswith('http'):
                link_domain = urlparse(link).netloc
                if link_domain and link_domain != domain:
                    external_count += 1
        
        return external_count
    
    def _detect_social_media(self, html_content: str) -> List[str]:
        """Detect social media presence"""
        found = []
        
        for platform, pattern in self.social_patterns.items():
            if pattern.search(html_content):
                found.append(platform)
        
        return found
    
    def _calculate_website_credibility(
        self,
        has_ssl: bool,
        page_count: int,
        has_contact: bool,
        has_about: bool,
        has_submission: bool,
        is_responsive: bool,
        max_depth: int,
        external_links: int,
        social_media: List[str]
    ) -> float:
        """
        Proprietary credibility scoring algorithm for websites.
        
        Returns credibility score from 0.0 (low) to 1.0 (high).
        """
        score = 0.0
        
        # SSL/HTTPS (security)
        if has_ssl:
            score += 0.15
        
        # Essential pages
        if has_contact:
            score += 0.15
        if has_about:
            score += 0.10
        if has_submission:
            score += 0.15
        
        # Content depth
        if page_count >= 5:
            score += 0.10
        if page_count >= 10:
            score += 0.05
        
        # Navigation depth (indicates structured content)
        if max_depth >= 2:
            score += 0.10
        if max_depth >= 3:
            score += 0.05
        
        # Responsive design (modern standards)
        if is_responsive:
            score += 0.10
        
        # External links (indicates engagement)
        if 5 <= external_links <= 50:
            score += 0.05
        
        # Social media presence
        if social_media:
            score += min(len(social_media) * 0.02, 0.10)
        
        return min(score, 1.0)
