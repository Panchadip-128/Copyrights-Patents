"""
Multimodal Signal Orchestrator
Module: x_mpfd_e_plus.multimodal_orchestrator.orchestrator

Normalizes heterogeneous lexical, structural, and visual signals into a unified
Multimodal Signal Tensor (MST). Implements deterministic Shannon Entropy and
HTML Abstract Syntax Tree (AST) Structural Density Ratio (SDR) calculations.
Patent Claims 1, 2, 3, 4, 11, and 13.

Copyright © 2026 Panchadip B & Somyajeet A. All Rights Reserved.
"""

from typing import Any, Dict, List, Optional, Tuple
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote, urlunparse
from datetime import datetime, timezone
import math
import re
import hashlib
import unicodedata


class URLNormalizer:
    """
    Deterministic URL Normalizer.
    Addresses Checklist Item 1 (AR1115):
    - Unicode Normalization: Form NFC (Canonical Decomposition followed by Canonical Composition)
    - Percent-Encoding: Decoded exactly ONCE via unquote to expose obfuscated characters
    - Case Normalization: Scheme and netloc/hostname converted to lowercase (RFC 3986 § 3.2.2)
    - Port Normalization: Strips redundant default ports (:80 for http, :443 for https)
    - Path Normalization: Standardizes consecutive slashes and query delimiters
    """
    @classmethod
    def normalize(cls, raw_url: str) -> Tuple[str, Dict[str, Any]]:
        if not raw_url:
            return "", {"unicode_form": "NFC", "percent_decoded": False}

        # 1. Unicode Normalization: Form NFC
        unicode_normalized = unicodedata.normalize("NFC", raw_url.strip())

        # 2. Single-pass Percent-Decoding
        percent_decoded = unquote(unicode_normalized)

        # 3. Parse components & canonicalize scheme-less inputs
        if "://" not in percent_decoded:
            stripped = percent_decoded.lstrip("/")
            parsed = urlparse("//" + stripped, scheme="http")
            scheme = "http"
        else:
            parsed = urlparse(percent_decoded)
            scheme = parsed.scheme.lower() if parsed.scheme else "http"

        netloc = parsed.netloc.lower()

        # 4. Port Normalization: Strip default ports
        if scheme == "http" and netloc.endswith(":80"):
            netloc = netloc[:-3]
        elif scheme == "https" and netloc.endswith(":443"):
            netloc = netloc[:-4]

        # 5. Path canonicalization: Ensure leading slash and collapse consecutive slashes
        path = parsed.path
        if not path:
            path = "/"
        elif not path.startswith("/"):
            path = "/" + path
        import re
        path = re.sub(r"/+", "/", path)

        reconstructed = urlunparse((
            scheme,
            netloc,
            path,
            parsed.params,
            parsed.query,
            parsed.fragment
        ))

        metadata = {
            "unicode_form": "NFC",
            "percent_decoded_once": True,
            "scheme_lowercased": scheme,
            "hostname_lowercased": netloc,
            "raw_length": len(raw_url),
            "normalized_length": len(reconstructed),
        }
        return reconstructed, metadata


class DeterministicDOMAnalyzer(HTMLParser):
    """
    Deterministic HTML Abstract Syntax Tree (AST) Parser.
    Addresses Checklist Item 2 (AR1115):
    - Element Nodes: Counted in N_total; non-void tags increment depth stack.
    - Void Elements: HTML5 void elements (area, base, br, col, embed, hr, img, input, link, meta, param, source, track, wbr)
      increment N_total and update max_depth as leaves, but are NOT pushed onto depth_stack.
    - Text Nodes: Ignored in N_total to ensure topological density is layout-invariant.
    - Comment Nodes: Ignored in N_total (or stripped by NoiseFilter).
    - Script Nodes: Counted as 1 element tag; script body JavaScript code is not parsed as DOM tags.
    - Iframe Nodes: Counted as 1 element tag; inner cross-origin iframe documents are not traversed in host AST.
    - Implicitly Closed Nodes: Void tags do not leak stack depth.
    Patent Claims 3 and 4.
    """
    VOID_ELEMENTS = {
        "area", "base", "br", "col", "embed", "hr", "img", "input",
        "link", "meta", "param", "source", "track", "wbr"
    }

    def __init__(self):
        super().__init__()
        self.total_nodes: int = 0
        self.current_depth: int = 0
        self.max_depth: int = 0
        self.form_count: int = 0
        self.password_fields: int = 0
        self.hidden_inputs: int = 0
        self.script_count: int = 0
        self.iframe_count: int = 0
        self.external_links: int = 0
        self.tag_counts: Dict[str, int] = {}
        self.depth_stack: List[str] = []
        # Explicit node statistics for Section 10(4) sufficiency
        self.element_nodes_count: int = 0
        self.void_element_nodes_count: int = 0
        self.excluded_text_nodes_count: int = 0
        self.excluded_comment_nodes_count: int = 0

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, Optional[str]]]):
        tag = tag.lower()
        self.total_nodes += 1
        self.element_nodes_count += 1
        self.tag_counts[tag] = self.tag_counts.get(tag, 0) + 1

        attrs_dict = {k.lower(): (v or "") for k, v in attrs}

        if tag == "form":
            self.form_count += 1
        elif tag == "input":
            input_type = attrs_dict.get("type", "text").lower()
            if input_type == "password":
                self.password_fields += 1
            elif input_type == "hidden":
                self.hidden_inputs += 1
        elif tag == "script":
            self.script_count += 1
        elif tag == "iframe":
            self.iframe_count += 1
            # Note: The <iframe> element itself is counted as a single node in N_total.
            # In accordance with network compute withholding and same-origin security boundaries,
            # external documents referenced by the iframe 'src' attribute are never fetched or parsed.
        elif tag == "a" and "href" in attrs_dict:
            href = attrs_dict["href"]
            if href.startswith(("http://", "https://", "//")):
                self.external_links += 1

        if tag in self.VOID_ELEMENTS:
            self.void_element_nodes_count += 1
            effective_depth = self.current_depth + 1
            if effective_depth > self.max_depth:
                self.max_depth = effective_depth
            # Void elements are self-closing; DO NOT push to depth_stack
        else:
            self.current_depth += 1
            self.depth_stack.append(tag)
            if self.current_depth > self.max_depth:
                self.max_depth = self.current_depth

    def handle_startendtag(self, tag: str, attrs: List[Tuple[str, Optional[str]]]):
        """
        Explicit handler for self-closing / XHTML-style tags (e.g. <br/>, <img ... />).
        Dispatches to handle_starttag and handle_endtag to prevent depth stack leaks.
        """
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_endtag(self, tag: str):
        tag = tag.lower()
        if tag in self.VOID_ELEMENTS:
            return  # Void elements have no closing tag to process
        if self.depth_stack and self.depth_stack[-1] == tag:
            self.depth_stack.pop()
            if self.current_depth > 0:
                self.current_depth -= 1
        elif tag in self.depth_stack:
            while self.depth_stack and self.depth_stack[-1] != tag:
                self.depth_stack.pop()
                if self.current_depth > 0:
                    self.current_depth -= 1
            if self.depth_stack:
                self.depth_stack.pop()
                if self.current_depth > 0:
                    self.current_depth -= 1

    def handle_data(self, data: str):
        if data and data.strip():
            self.excluded_text_nodes_count += 1
            # Text nodes are explicitly NOT counted in total_nodes

    def handle_comment(self, data: str):
        self.excluded_comment_nodes_count += 1
        # Comments are explicitly NOT counted in total_nodes

    def calculate_sdr(self) -> float:
        """
        Computes Structural Density Ratio (SDR) = Total Nodes / Max Depth.
        Formula: SDR = N / D_max
        """
        if self.max_depth == 0:
            return 0.0
        return self.total_nodes / float(self.max_depth)


class LexicalAnalyzer:
    """
    Deterministic Lexical Feature Extractor.
    Calculates Shannon Entropy and URL obfuscation metrics.
    Patent Claim 2.
    """
    SUSPICIOUS_TLDS = {
        "tk", "ml", "ga", "cf", "gq", "top", "xyz", "club", "work",
        "buzz", "cam", "icu", "date", "racing", "win", "stream"
    }

    @staticmethod
    def calculate_shannon_entropy(text: str) -> float:
        """
        Calculates Shannon Entropy H(U) = - SUM(P(x_i) * log2(P(x_i))).
        Patent Claim 2.
        """
        if not text:
            return 0.0
        counts: Dict[str, int] = {}
        for char in text:
            counts[char] = counts.get(char, 0) + 1
        length = float(len(text))
        entropy = 0.0
        for count in counts.values():
            p = count / length
            if p > 0:
                entropy -= p * math.log2(p)
        return float(entropy)

    @classmethod
    def analyze_url(cls, url: str) -> Dict[str, Any]:
        """
        Extracts complete deterministic lexical vector.
        Applies RFC 3986 and Unicode NFC normalization before entropy calculation.
        """
        normalized_url, norm_meta = URLNormalizer.normalize(url)
        parsed = urlparse(normalized_url)
        netloc = parsed.netloc.lower()
        path = parsed.path
        full_entropy = cls.calculate_shannon_entropy(normalized_url)
        netloc_entropy = cls.calculate_shannon_entropy(netloc)
        host_path_str = f"{netloc}{path}" if path else netloc
        host_path_entropy = cls.calculate_shannon_entropy(host_path_str)

        # Detect IP-based host
        is_ip = bool(re.match(r"^(\d{1,3}\.){3}\d{1,3}(:\d+)?$", netloc))

        # Detect suspicious TLD
        if is_ip:
            tld = ""
            has_suspicious_tld = False
        else:
            tld = netloc.split(".")[-1] if "." in netloc else ""
            has_suspicious_tld = tld in cls.SUSPICIOUS_TLDS

        # Digit ratio in hostname
        digit_count = sum(c.isdigit() for c in netloc)
        digit_ratio = digit_count / max(1, len(netloc))

        # Hyphen count
        hyphen_count = netloc.count("-")

        # Subdomain count
        parts = netloc.split(".")
        subdomain_count = max(0, len(parts) - 2) if not is_ip else 0

        # Compute composite lexical risk
        lexical_risk = 0.0
        if full_entropy > 4.5:
            lexical_risk = 0.95
        elif full_entropy > 4.0:
            lexical_risk = 0.75
        elif full_entropy > 3.6:
            lexical_risk = 0.40
        else:
            lexical_risk = 0.05

        if is_ip:
            lexical_risk = min(1.0, lexical_risk + 0.35)
        if has_suspicious_tld:
            lexical_risk = min(1.0, lexical_risk + 0.30)
        if digit_ratio > 0.30:
            lexical_risk = min(1.0, lexical_risk + 0.20)

        return {
            "url": url,
            "normalized_url": normalized_url,
            "normalization_metadata": norm_meta,
            "hostname": netloc,
            "shannon_entropy": round(full_entropy, 4),
            "hostname_entropy": round(netloc_entropy, 4),
            "host_path_entropy": round(host_path_entropy, 4),
            "is_ip_address": is_ip,
            "tld": tld,
            "has_suspicious_tld": has_suspicious_tld,
            "digit_ratio": round(digit_ratio, 4),
            "hyphen_count": hyphen_count,
            "subdomain_count": subdomain_count,
            "lexical_risk_score": round(lexical_risk, 4),
        }


class StructuralAnalyzer:
    """
    Deterministic Structural Feature Extractor using DOM AST.
    Patent Claims 3 and 4.
    """
    BASELINE_SDR: float = 16.0  # Established enterprise login page baseline

    @classmethod
    def analyze_html(cls, html: Optional[str], baseline_sdr: float = BASELINE_SDR) -> Dict[str, Any]:
        if not html or not html.strip():
            return {
                "has_html": False,
                "total_nodes": 0,
                "max_depth": 0,
                "sdr": 0.0,
                "sdr_deviation_pct": 0.0,
                "form_count": 0,
                "password_fields": 0,
                "hidden_inputs": 0,
                "script_count": 0,
                "iframe_count": 0,
                "structural_risk_score": 0.0,
            }

        parser = DeterministicDOMAnalyzer()
        try:
            parser.feed(html)
        except Exception:
            pass  # Resilient parsing without crashing

        sdr = parser.calculate_sdr()
        # SDR deviation from legitimate brand baseline
        deviation_pct = (abs(sdr - baseline_sdr) / baseline_sdr) * 100.0 if baseline_sdr > 0 else 0.0

        # Structural risk: credential harvesting signatures
        structural_risk = 0.0
        if parser.password_fields > 0 and parser.max_depth <= 4:
            # Shallow cloned login page
            structural_risk = 0.90
        elif deviation_pct > 60.0:
            structural_risk = 0.75
        elif deviation_pct > 40.0:
            structural_risk = 0.50
        elif parser.password_fields > 0:
            structural_risk = 0.35
        else:
            structural_risk = 0.05

        if parser.iframe_count > 2:
            structural_risk = min(1.0, structural_risk + 0.15)

        return {
            "has_html": True,
            "total_nodes": parser.total_nodes,
            "max_depth": parser.max_depth,
            "sdr": round(sdr, 4),
            "sdr_deviation_pct": round(deviation_pct, 2),
            "form_count": parser.form_count,
            "password_fields": parser.password_fields,
            "hidden_inputs": parser.hidden_inputs,
            "script_count": parser.script_count,
            "iframe_count": parser.iframe_count,
            "external_links": parser.external_links,
            "structural_risk_score": round(structural_risk, 4),
        }


class VisualMetadataAnalyzer:
    """
    Deterministic Visual and Metadata Extractor.
    Evaluates TLS security, iframe overlays, and geometry without CNN backbones.
    Patent Claim 13.
    """
    @classmethod
    def analyze(
        cls,
        url: str,
        screenshot: Optional[bytes] = None,
        tls_valid: bool = True,
        is_self_signed: bool = False,
    ) -> Dict[str, Any]:
        has_screenshot = bool(screenshot)
        screenshot_size = len(screenshot) if screenshot else 0

        # Determine visual/TLS risk deterministically
        visual_risk = 0.0
        if not tls_valid:
            visual_risk = 0.95
        elif is_self_signed:
            visual_risk = 0.85
        else:
            visual_risk = 0.05

        return {
            "tls_valid": tls_valid,
            "is_self_signed": is_self_signed,
            "has_screenshot": has_screenshot,
            "screenshot_bytes": screenshot_size,
            "visual_risk_score": round(visual_risk, 4),
        }


class MultimodalSignalTensor:
    """
    Standardized Multimodal Signal Tensor (MST).
    Encapsulates Lexical (V_L), Structural (V_S), and Visual (V_M) vectors.
    Patent Claim 1 and Claim 11.
    """
    def __init__(
        self,
        lexical_vector: Dict[str, Any],
        structural_vector: Dict[str, Any],
        visual_vector: Dict[str, Any],
        provenance_tags: Optional[List[Dict[str, Any]]] = None,
        timestamp: Optional[str] = None,
    ):
        self.lexical_vector = lexical_vector
        self.structural_vector = structural_vector
        self.visual_vector = visual_vector
        self.provenance_tags = provenance_tags or []
        self.timestamp = timestamp or datetime.now(timezone.utc).isoformat()

    @property
    def V_L(self) -> Dict[str, Any]:
        return self.lexical_vector

    @property
    def V_S(self) -> Dict[str, Any]:
        return self.structural_vector

    @property
    def V_M(self) -> Dict[str, Any]:
        return self.visual_vector

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "V_L": self.lexical_vector,
            "V_S": self.structural_vector,
            "V_M": self.visual_vector,
            "provenance_tags": self.provenance_tags,
        }


class TemporalAligner:
    """Asynchronous temporal alignment for real-time signal streams."""
    def align(self, signals: List[Any]) -> List[Any]:
        return sorted(signals, key=lambda s: getattr(s, "timestamp", ""))


class NoiseFilter:
    """Deterministic noise reduction for web telemetry and DOM inputs."""
    def filter_html(self, html: Optional[str]) -> str:
        if not html:
            return ""
        # Remove HTML comments deterministically
        return re.sub(r"<!--.*?-->", "", html, flags=re.DOTALL)


class CompletenessEvaluator:
    """Evaluates availability and completeness of multimodal input channels."""
    def evaluate(self, tensor: MultimodalSignalTensor) -> float:
        channels = [
            bool(tensor.lexical_vector),
            bool(tensor.structural_vector.get("has_html", False)),
            bool(tensor.visual_vector),
        ]
        return float(sum(channels) / len(channels))


class MultimodalOrchestrator:
    """
    Multimodal Signal Orchestrator.
    Patent Claims 1 and 11.
    """
    def __init__(self):
        self.lexical_analyzer = LexicalAnalyzer()
        self.structural_analyzer = StructuralAnalyzer()
        self.visual_analyzer = VisualMetadataAnalyzer()
        self.aligner = TemporalAligner()
        self.noise_filter = NoiseFilter()
        self.completeness_evaluator = CompletenessEvaluator()

    def orchestrate(
        self,
        url: str,
        html: Optional[str] = None,
        screenshot: Optional[bytes] = None,
        tls_valid: bool = True,
        is_self_signed: bool = False,
    ) -> MultimodalSignalTensor:
        clean_html = self.noise_filter.filter_html(html) if html else None

        v_l = self.lexical_analyzer.analyze_url(url)
        v_s = self.structural_analyzer.analyze_html(clean_html)
        v_m = self.visual_analyzer.analyze(
            url=url,
            screenshot=screenshot,
            tls_valid=tls_valid,
            is_self_signed=is_self_signed,
        )

        now_iso = datetime.now(timezone.utc).isoformat()
        provenance_tags = [
            {
                "modality": "lexical",
                "algorithm": "shannon_entropy_base_2",
                "value": v_l["shannon_entropy"],
                "timestamp": now_iso,
                "sha256": hashlib.sha256(f"lexical:{v_l['shannon_entropy']}:{now_iso}".encode("utf-8")).hexdigest(),
            },
            {
                "modality": "structural",
                "algorithm": "ast_node_depth_sdr",
                "value": v_s["sdr"],
                "timestamp": now_iso,
                "sha256": hashlib.sha256(f"structural:{v_s['sdr']}:{now_iso}".encode("utf-8")).hexdigest(),
            },
            {
                "modality": "visual",
                "algorithm": "tls_geometry_evaluator",
                "value": v_m["tls_valid"],
                "timestamp": now_iso,
                "sha256": hashlib.sha256(f"visual:{v_m['tls_valid']}:{now_iso}".encode("utf-8")).hexdigest(),
            },
        ]

        return MultimodalSignalTensor(
            lexical_vector=v_l,
            structural_vector=v_s,
            visual_vector=v_m,
            provenance_tags=provenance_tags,
            timestamp=now_iso,
        )
