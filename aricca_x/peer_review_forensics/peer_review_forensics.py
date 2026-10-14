"""
Peer-Review Forensics Module (Module C)

Deterministic linguistic fingerprinting and behavioral alignment analysis
of peer-review text without probabilistic or machine-learning classifiers:

  1. Sentence Length Coefficient of Variation (CV):
     Tokenizes text into sentences and computes sentence word counts:
         CV = stdev(lengths) / mean(lengths)
     Flags ARTIFICIAL_UNIFORMITY if CV < 0.20 (LLMs typically generate unnaturally
     uniform sentence pacing, whereas human reviews exhibit high variance).

  2. Deterministic Hedging Phrase Density:
     Matches against a predefined dictionary of characteristic academic hedge
     phrases:
         hedging_density = (matches / word_count) * 100
     Flags EXCESSIVE_HEDGING if hedging_density > 4.0%.

  3. Manuscript Element Specificity Score:
     Evaluates grounding in manuscript specifics using regular expressions
     for equations, tables, figures, sections, theorems, algorithms, page/line numbers:
         specificity = element_references / sentence_count
     Flags LOW_SPECIFICITY if specificity < 0.15 (indicating generic/hallucinated review).

  4. Lexical Diversity (Type-Token Ratio):
     Evaluates lexical richness across content words.

  5. Sentiment Polarity & Recommendation Misalignment:
     Evaluates sentiment polarity P:
         P = (pos_matches - neg_matches) / max(1, pos_matches + neg_matches)
     where P in [-1.0, 1.0].
     Raises SENTIMENT_DECISION_MISALIGNMENT if:
         - Review text is strongly positive (P >= +0.50) but recommendation is REJECT, or
         - Review text is strongly negative (P <= -0.50) but recommendation is ACCEPT.

All decisions are produced by explicit arithmetic formulas and Boolean rules
carrying human-readable mathematical justification.

Copyright (c) 2026. All rights reserved. Patent Pending.
"""

import math
import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence, Set, Tuple

from ..deterministic_core import DEFAULT_REGISTRY, RuleRegistry, clamp01

# Predefined deterministic hedging patterns
HEDGING_PATTERNS: Tuple[str, ...] = (
    "it seems", "it appears", "perhaps", "possibly", "might consider",
    "could be", "may want", "to some extent", "somewhat", "arguably",
    "it is possible", "one might argue", "it could be argued",
    "there may be", "this might", "this could", "would suggest",
    "tends to", "appears to", "seems to", "likely", "unlikely",
    "roughly", "approximately", "in some cases", "generally speaking",
    "potential merit", "broadly speaking", "could potentially"
)

# Specific manuscript element patterns
SPECIFIC_PATTERNS: Tuple[Tuple[str, str], ...] = (
    ("equation", r"\b(?:equation|eq\.)\s*(?:\(?\d+\)?|\([a-z0-9.]+\))"),
    ("table", r"\b(?:table|tab\.)\s*\d+"),
    ("figure", r"\b(?:figure|fig\.)\s*\d+"),
    ("section", r"\b(?:section|sec\.)\s*(?:\d+(?:\.\d+)*|[A-Z])"),
    ("page", r"\bpage\s*\d+"),
    ("line", r"\bline\s*\d+"),
    ("theorem", r"\b(?:theorem|lemma|proposition|corollary)\s*\d+"),
    ("algorithm", r"\b(?:algorithm|algo\.|step)\s*\d+"),
    ("appendix", r"\b(?:appendix)\s*[A-Z]"),
)

# Deterministic academic sentiment lexicon
POSITIVE_WORDS: Tuple[str, ...] = (
    "excellent", "outstanding", "strong", "solid", "compelling", "novel",
    "innovative", "significant", "important", "valuable", "interesting",
    "well-written", "thorough", "rigorous", "impressive", "clear", "elegant",
    "insightful", "groundbreaking", "convincing", "exemplary"
)

NEGATIVE_WORDS: Tuple[str, ...] = (
    "weak", "poor", "lacking", "insufficient", "flawed", "unclear",
    "confusing", "missing", "inadequate", "superficial", "trivial",
    "unconvincing", "problematic", "wrong", "incorrect", "erroneous",
    "vague", "incomplete", "limited", "unfounded", "unsubstantiated"
)


def tokenize_sentences(text: str) -> List[str]:
    """Tokenize review text into clean sentences, respecting common abbreviations."""
    clean = re.sub(r"\b(?:e\.g\.|i\.e\.|et al\.|Fig\.|Eq\.|Dr\.|Prof\.|vs\.)",
                   lambda m: m.group(0).replace(".", "@"), text)
    splits = re.split(r"[.!?]+", clean)
    sentences = [s.replace("@", ".").strip() for s in splits if len(s.strip()) > 3]
    return sentences


def tokenize_words(text: str) -> List[str]:
    """Tokenize text into lowercase words."""
    return [w.lower() for w in re.findall(r"\b[a-zA-Z0-9'-]+\b", text)]


@dataclass(frozen=True)
class LinguisticFingerprint:
    sentence_count: int
    word_count: int
    avg_sentence_length: float
    sentence_length_variance: float
    sentence_length_stdev: float
    sentence_length_cv: float
    is_unnaturally_uniform: bool
    hedging_matches_count: int
    hedging_density_percent: float
    is_excessive_hedging: bool
    specific_elements_count: int
    specificity_score: float
    is_low_specificity: bool
    type_token_ratio: float


@dataclass(frozen=True)
class SentimentAlignmentResult:
    positive_count: int
    negative_count: int
    sentiment_polarity: float   # in [-1.0, 1.0]
    reviewer_recommendation: str
    is_misaligned: bool
    justification: str


@dataclass
class PeerReviewAuditResult:
    review_id: str
    fingerprint: LinguisticFingerprint
    sentiment_alignment: SentimentAlignmentResult
    phantom_references_detected: bool
    authenticity_verdict: str  # "LIKELY_AUTHENTIC" | "SUSPICIOUS_UNIFORM" | "LIKELY_SYNTHETIC"
    credibility_signal: float  # 1.0 = authentic human, 0.0 = deceptive / synthetic
    flags: List[str] = field(default_factory=list)
    justification: List[str] = field(default_factory=list)


class PeerReviewForensicsAnalyzer:
    """Deterministic analyzer for peer-review authenticity and behavioral alignment."""

    def __init__(self, rules: RuleRegistry = DEFAULT_REGISTRY):
        self.rules = rules
        self.cv_threshold = rules.param("PR-UNIFORMITY", "cv_threshold")
        self.min_sentences = int(rules.param("PR-UNIFORMITY", "min_sentences"))
        self.hedging_threshold = rules.param("PR-HEDGING", "density_threshold")
        self.min_specificity = rules.param("PR-SPECIFICITY", "min_specificity")
        self.polarity_threshold = rules.param("PR-MISALIGNMENT", "polarity_threshold")
        self.pos_polarity_threshold = (
            rules.param("PR-MISALIGNMENT", "pos_polarity_threshold")
            if "pos_polarity_threshold" in rules.get("PR-MISALIGNMENT").as_dict()
            else self.polarity_threshold
        )
        self.neg_polarity_threshold = (
            rules.param("PR-MISALIGNMENT", "neg_polarity_threshold")
            if "neg_polarity_threshold" in rules.get("PR-MISALIGNMENT").as_dict()
            else 0.30
        )

    def extract_fingerprint(self, text: str) -> LinguisticFingerprint:
        """Extract deterministic linguistic features."""
        sentences = tokenize_sentences(text)
        words = tokenize_words(text)
        word_count = len(words)
        sentence_count = len(sentences)

        if sentence_count == 0 or word_count == 0:
            return LinguisticFingerprint(
                sentence_count=0, word_count=0, avg_sentence_length=0.0,
                sentence_length_variance=0.0, sentence_length_stdev=0.0,
                sentence_length_cv=0.0, is_unnaturally_uniform=False,
                hedging_matches_count=0, hedging_density_percent=0.0,
                is_excessive_hedging=False, specific_elements_count=0,
                specificity_score=0.0, is_low_specificity=True,
                type_token_ratio=0.0,
            )

        sentence_lengths = [len(tokenize_words(s)) for s in sentences]
        mean_len = sum(sentence_lengths) / sentence_count
        variance = sum((l - mean_len) ** 2 for l in sentence_lengths) / sentence_count
        stdev = math.sqrt(variance)
        cv = stdev / mean_len if mean_len > 0 else 0.0

        is_uniform = cv < self.cv_threshold if sentence_count >= self.min_sentences else False

        # Hedging count
        lower_text = text.lower()
        hedging_count = sum(len(re.findall(re.escape(p), lower_text)) for p in HEDGING_PATTERNS)
        hedging_density = (hedging_count / word_count) * 100.0
        is_hedging_dense = hedging_density > self.hedging_threshold

        # Specificity count
        specific_count = sum(len(re.findall(p[1], lower_text)) for p in SPECIFIC_PATTERNS)
        specificity = specific_count / sentence_count
        is_low_spec = specificity < self.min_specificity

        # Lexical diversity (TTR)
        unique_words = len(set(words))
        ttr = unique_words / word_count if word_count > 0 else 0.0

        return LinguisticFingerprint(
            sentence_count=sentence_count,
            word_count=word_count,
            avg_sentence_length=mean_len,
            sentence_length_variance=variance,
            sentence_length_stdev=stdev,
            sentence_length_cv=cv,
            is_unnaturally_uniform=is_uniform,
            hedging_matches_count=hedging_count,
            hedging_density_percent=hedging_density,
            is_excessive_hedging=is_hedging_dense,
            specific_elements_count=specific_count,
            specificity_score=specificity,
            is_low_specificity=is_low_spec,
            type_token_ratio=ttr,
        )

    def evaluate_sentiment_alignment(
        self, text: str, recommendation: str
    ) -> SentimentAlignmentResult:
        """Evaluate sentiment polarity and compare against reviewer recommendation."""
        words = tokenize_words(text)
        lower_text = text.lower()

        pos_count = sum(len(re.findall(r"\b" + re.escape(w) + r"\b", lower_text)) for w in POSITIVE_WORDS)
        neg_count = sum(len(re.findall(r"\b" + re.escape(w) + r"\b", lower_text)) for w in NEGATIVE_WORDS)

        total_sentiment = pos_count + neg_count
        polarity = (pos_count - neg_count) / total_sentiment if total_sentiment > 0 else 0.0

        rec_clean = recommendation.strip().lower()

        # Misalignment logic:
        # Strongly positive text (P >= +0.50) with REJECT
        # Critical negative text (P <= -0.30) with ACCEPT
        is_misaligned = False
        justification = ""

        if polarity >= self.pos_polarity_threshold and "reject" in rec_clean:
            is_misaligned = True
            justification = (
                f"Sentiment-Decision Misalignment: Reviewer recommendation is '{recommendation.upper()}' "
                f"despite strongly positive linguistic sentiment polarity P={polarity:+.2f} "
                f"(positive terms={pos_count}, negative terms={neg_count}; threshold >= +{self.pos_polarity_threshold:.2f})"
            )
        elif polarity <= -self.neg_polarity_threshold and ("accept" in rec_clean and "reject" not in rec_clean):
            is_misaligned = True
            justification = (
                f"Sentiment-Decision Misalignment: Reviewer recommendation is '{recommendation.upper()}' "
                f"despite critical linguistic sentiment polarity P={polarity:+.2f} "
                f"(positive terms={pos_count}, negative terms={neg_count}; threshold <= -{self.neg_polarity_threshold:.2f})"
            )
        else:
            justification = (
                f"Sentiment consistent: Polarity P={polarity:+.2f} aligns with decision '{recommendation}'"
            )

        return SentimentAlignmentResult(
            positive_count=pos_count,
            negative_count=neg_count,
            sentiment_polarity=polarity,
            reviewer_recommendation=recommendation,
            is_misaligned=is_misaligned,
            justification=justification,
        )

    def analyze(
        self,
        review_id: str,
        review_text: str,
        recommendation: str = "Accept",
        manuscript_element_ids: Optional[Sequence[str]] = None,
    ) -> PeerReviewAuditResult:
        """Full deterministic audit of peer-review text."""
        fp = self.extract_fingerprint(review_text)
        align = self.evaluate_sentiment_alignment(review_text, recommendation)

        # Phantom references check: does review cite non-existent equations/tables?
        phantom_detected = False
        if manuscript_element_ids is not None:
            # Check if review mentions element IDs not in the manuscript
            text_lower = review_text.lower()
            claimed_eqs = re.findall(r"equation\s*\(?(\d+)\)?", text_lower)
            known_ids = set(manuscript_element_ids)
            for eq in claimed_eqs:
                if f"eq_{eq}" not in known_ids and f"equation_{eq}" not in known_ids and eq not in known_ids:
                    phantom_detected = True
                    break

        # Indicator penalties based on rules
        w_uniform = self.rules.param("PR-INDICATOR-WEIGHTS", "uniform")
        w_hedge = self.rules.param("PR-INDICATOR-WEIGHTS", "hedge_dense")
        w_spec = self.rules.param("PR-INDICATOR-WEIGHTS", "low_specificity")
        w_align = self.rules.param("PR-INDICATOR-WEIGHTS", "misaligned")
        w_phantom = self.rules.param("PR-INDICATOR-WEIGHTS", "phantom_reference")

        penalty = 0.0
        if fp.is_unnaturally_uniform:
            penalty += w_uniform
        if fp.is_excessive_hedging:
            penalty += w_hedge
        if fp.is_low_specificity:
            penalty += w_spec
        if align.is_misaligned:
            penalty += w_align
        if phantom_detected:
            penalty += w_phantom

        credibility_signal = clamp01(1.0 - penalty)

        flags: List[str] = []
        if fp.is_unnaturally_uniform:
            flags.append("PR_UNNATURAL_SENTENCE_UNIFORMITY")
        if fp.is_excessive_hedging:
            flags.append("PR_EXCESSIVE_HEDGING_DENSITY")
        if fp.is_low_specificity:
            flags.append("PR_LOW_MANUSCRIPT_SPECIFICITY")
        if align.is_misaligned:
            flags.append("PR_SENTIMENT_RECOMMENDATION_MISALIGNMENT")
        if phantom_detected:
            flags.append("PR_PHANTOM_REFERENCE_HALLUCINATION")

        if penalty >= 0.50:
            verdict = "LIKELY_SYNTHETIC"
        elif penalty >= 0.25:
            verdict = "SUSPICIOUS_UNIFORM"
        else:
            verdict = "LIKELY_AUTHENTIC"

        justification = [
            f"Peer-Review Forensics for '{review_id}'",
            f"Sentence CV = {fp.sentence_length_cv:.4f} {'<' if fp.is_unnaturally_uniform else '>='} threshold {self.cv_threshold:.2f}",
            f"Hedging density = {fp.hedging_density_percent:.2f}% (threshold {self.hedging_threshold:.1f}%)",
            f"Specificity score = {fp.specificity_score:.4f} (threshold {self.min_specificity:.2f})",
            align.justification,
            f"Authenticity verdict: {verdict} (credibility signal s_review = {credibility_signal:.4f})",
        ]

        return PeerReviewAuditResult(
            review_id=review_id,
            fingerprint=fp,
            sentiment_alignment=align,
            phantom_references_detected=phantom_detected,
            authenticity_verdict=verdict,
            credibility_signal=credibility_signal,
            flags=sorted(flags),
            justification=justification,
        )
