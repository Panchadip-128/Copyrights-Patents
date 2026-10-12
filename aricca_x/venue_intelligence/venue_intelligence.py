"""
Venue Intelligence Module (Module A)

Evaluates the credibility and authenticity of publication venues (conferences
and journals) using purely deterministic algorithms:

  1. Predatory Urgency Detection:
     Calculates interval between Call for Papers (CFP) announcement and
     submission deadline:
         interval_days = submission_deadline - cfp_announcement
     Raises PREDATORY_URGENCY flag when interval_days < 30 days.

  2. Registry URL Spoofing & Typosquatting Detection:
     Computes deterministic Levenshtein edit distance between candidate URL
     domain and legitimate publisher/indexing registry URLs (IEEE, ACM,
     Springer, Elsevier, Nature, Wiley, etc.):
         d = Levenshtein(candidate_domain, registry_domain)
     Flags TYPOSQUAT / SPOOF when edit distance indicates lookalike domain.

  3. Grammatical Tense Analysis (GTA):
     Classifies indexing statements and CFP commitments into tense classes:
         CONDITIONAL (+0.30 risk) - e.g. "may be indexed", "subject to approval"
         FUTURE      (+0.25 risk) - e.g. "will be indexed", "planning to submit"
         PRESENT     ( 0.00 risk) - e.g. "is indexed", "currently listed in"
         PAST        (-0.05 risk) - e.g. "has been indexed since 2018"
         UNKNOWN     (+0.05 risk) - unclassified phrasing
     Applies website location penalty (+0.10) for future/conditional claims on
     official venue portals, contradiction penalties, and anachronistic anchor detection.

  4. Temporal Fingerprint Evolution Tracking (TFET):
     Compares multi-dimensional fingerprints F(T1) and F(T2):
         Delta_F = F(T2) - F(T1)
         ||Delta_F||_W = sqrt( sum_k w_k * Delta_F_k^2 / sum_k w_k )
     Raises STABILITY_ALERT when ||Delta_F||_W exceeds operational stability threshold (0.25).

Copyright (c) 2026. All rights reserved. Patent Pending.
"""

import math
import re
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Dict, List, Mapping, Optional, Sequence, Set, Tuple

from ..deterministic_core import DEFAULT_REGISTRY, RuleRegistry, clamp01


def levenshtein_distance(s1: str, s2: str) -> int:
    """Deterministic Levenshtein edit distance between two strings."""
    s1, s2 = s1.lower().strip(), s2.lower().strip()
    if s1 == s2:
        return 0
    if not s1:
        return len(s2)
    if not s2:
        return len(s1)

    previous_row = list(range(len(s2) + 1))
    for i, c1 in enumerate(s1):
        current_row = [i + 1] + [0] * len(s2)
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row[j + 1] = min(insertions, deletions, substitutions)
        previous_row = current_row
    return previous_row[-1]


def extract_domain(url: str) -> str:
    """Extract clean domain/host from URL or domain string."""
    clean = re.sub(r"^https?://", "", url.strip().lower())
    clean = clean.split("/")[0].split("?")[0].split(":")[0]
    if clean.startswith("www."):
        clean = clean[4:]
    return clean


# Curated legitimate registry domains
LEGITIMATE_REGISTRIES: Dict[str, str] = {
    "ieee.org": "IEEE",
    "acm.org": "ACM",
    "springer.com": "Springer",
    "elsevier.com": "Elsevier",
    "nature.com": "Nature Publishing Group",
    "wiley.com": "Wiley",
    "sciencedirect.com": "ScienceDirect",
    "cell.com": "Cell Press",
    "pnas.org": "PNAS",
    "plos.org": "PLOS",
    "biorxiv.org": "bioRxiv",
    "medrxiv.org": "medRxiv",
    "arxiv.org": "arXiv",
}


@dataclass(frozen=True)
class UrlAuditResult:
    candidate_domain: str
    target_registry: Optional[str]
    organization: Optional[str]
    edit_distance: int
    is_exact_match: bool
    is_spoofed: bool
    classification: str   # "VERIFIED_REGISTRY" | "LOOKALIKE_SPOOF" | "UNRELATED_DOMAIN"
    score: float          # 1.0 = verified legitimate, 0.0 = spoof/typosquat, 0.7 = standard custom domain
    justification: str


@dataclass(frozen=True)
class TenseAnalysisRecord:
    indexer_name: str
    claim_text: str
    source: str           # "cfp" | "website" | "email"
    tense: str            # "past" | "present" | "future" | "conditional" | "unknown"
    risk_weight: float
    is_anachronistic: bool
    evidence: str


@dataclass(frozen=True)
class TemporalIntegrityResult:
    announcement_date: Optional[date]
    deadline_date: Optional[date]
    interval_days: Optional[int]
    predatory_urgency: bool
    urgency_score: float   # 1.0 = safe interval, 0.0 = extreme predatory urgency (<30 days)
    justification: str


@dataclass(frozen=True)
class FingerprintSnapshot:
    timestamp: date
    cfp_risk_score: float
    website_depth_score: float
    structural_completeness: float
    indexing_claims_count: float
    cfp_signature_hash: str
    organizer_count: int
    domain_name: str


@dataclass
class TFETDriftReport:
    drift_vector: Dict[str, float]
    weighted_drift_magnitude: float
    stability_threshold: float
    stability_alert: bool
    drift_velocity_per_month: float
    hijack_suspected: bool
    temporal_risk_adjustment: float
    mutations: List[str]
    justification: List[str] = field(default_factory=list)


@dataclass
class VenueIntelligenceResult:
    venue_id: str
    venue_name: str
    url_audit: UrlAuditResult
    temporal_integrity: TemporalIntegrityResult
    tense_analysis: List[TenseAnalysisRecord]
    tense_credibility_score: float
    tfet_drift: Optional[TFETDriftReport]
    credibility_signal: float
    flags: List[str] = field(default_factory=list)
    justification: List[str] = field(default_factory=list)


class VenueIntelligenceAnalyzer:
    """Deterministic analyzer for publication venue credibility."""

    def __init__(self, rules: RuleRegistry = DEFAULT_REGISTRY):
        self.rules = rules
        self.min_urgency_days = int(rules.param("VI-URGENCY", "min_interval_days"))
        self.typosquat_ratio = rules.param("VI-SPOOF", "relative_ratio")
        self.typosquat_floor = int(rules.param("VI-SPOOF", "absolute_floor"))
        self.tfet_threshold = rules.param("TFET", "stability_threshold")

    def audit_url(self, candidate_url: str) -> UrlAuditResult:
        """Deterministic Levenshtein evaluation against legitimate registry domains."""
        candidate = extract_domain(candidate_url)
        if not candidate:
            return UrlAuditResult(
                candidate_domain="",
                target_registry=None,
                organization=None,
                edit_distance=-1,
                is_exact_match=False,
                is_spoofed=False,
                classification="UNKNOWN",
                score=0.5,
                justification="Empty or invalid candidate URL provided",
            )

        # Check exact matches
        for reg_domain, org in LEGITIMATE_REGISTRIES.items():
            if candidate == reg_domain or candidate.endswith("." + reg_domain):
                return UrlAuditResult(
                    candidate_domain=candidate,
                    target_registry=reg_domain,
                    organization=org,
                    edit_distance=0,
                    is_exact_match=True,
                    is_spoofed=False,
                    classification="VERIFIED_REGISTRY",
                    score=self.rules.param("VI-URL-SCORES", "verified_registry"),
                    justification=f"Domain verified as official registry of {org} ({reg_domain})",
                )

        # Look for edit distance anomalies / typosquats against all legitimate registries
        closest_reg = None
        closest_org = None
        min_dist = 999
        cand_base = candidate.split(".")[0]

        for reg_domain, org in LEGITIMATE_REGISTRIES.items():
            reg_base = reg_domain.split(".")[0]
            # Test both full domain and primary domain label
            d_full = levenshtein_distance(candidate, reg_domain)
            d_base = levenshtein_distance(cand_base, reg_base)
            d = min(d_full, d_base)

            if d < min_dist:
                min_dist = d
                closest_reg = reg_domain
                closest_org = org

        # Rule evaluation: typosquat threshold based on registry domain length
        if closest_reg:
            threshold = max(self.typosquat_floor, int(len(closest_reg.split(".")[0]) * self.typosquat_ratio))
            if 1 <= min_dist <= threshold:
                return UrlAuditResult(
                    candidate_domain=candidate,
                    target_registry=closest_reg,
                    organization=closest_org,
                    edit_distance=min_dist,
                    is_exact_match=False,
                    is_spoofed=True,
                    classification="LOOKALIKE_SPOOF",
                    score=self.rules.param("VI-URL-SCORES", "typosquat"),
                    justification=(
                        f"Domain '{candidate}' is a spoofed lookalike of {closest_org} "
                        f"('{closest_reg}') with Levenshtein distance d={min_dist} <= threshold={threshold}"
                    ),
                )

        # Brand embedding check (e.g. "ieee-conference-fake.com")
        for reg_domain, org in LEGITIMATE_REGISTRIES.items():
            reg_base = reg_domain.split(".")[0]
            if len(reg_base) >= 4 and reg_base in candidate:
                return UrlAuditResult(
                    candidate_domain=candidate,
                    target_registry=reg_domain,
                    organization=org,
                    edit_distance=len(candidate) - len(reg_base),
                    is_exact_match=False,
                    is_spoofed=True,
                    classification="BRAND_EMBEDDING_SPOOF",
                    score=self.rules.param("VI-URL-SCORES", "brand_embedding"),
                    justification=(
                        f"Domain '{candidate}' fraudulently embeds authentic brand token '{reg_base}' ({org})"
                    ),
                )

        return UrlAuditResult(
            candidate_domain=candidate,
            target_registry=None,
            organization=None,
            edit_distance=min_dist,
            is_exact_match=False,
            is_spoofed=False,
            classification="UNRELATED_DOMAIN",
            score=self.rules.param("VI-URL-SCORES", "unrelated"),
            justification=f"Independent domain '{candidate}'; no brand impersonation detected",
        )

    def evaluate_temporal_urgency(
        self, announcement_date: Optional[date], deadline_date: Optional[date]
    ) -> TemporalIntegrityResult:
        """Deterministic evaluation of CFP urgency interval."""
        if announcement_date is None or deadline_date is None:
            return TemporalIntegrityResult(
                announcement_date=announcement_date,
                deadline_date=deadline_date,
                interval_days=None,
                predatory_urgency=False,
                urgency_score=0.5,
                justification="Dates missing; temporal integrity UNKNOWN",
            )

        interval = (deadline_date - announcement_date).days
        is_predatory = 0 <= interval < self.min_urgency_days

        if interval < 0:
            urgency_score = 0.0
            justification = f"Anomalous negative interval ({interval} days): deadline precedes announcement"
        elif is_predatory:
            # Scaled penalty: 0 days = 0.0, 29 days = 0.48
            urgency_score = max(0.0, (interval / self.min_urgency_days) * 0.5)
            justification = (
                f"Predatory Urgency: CFP window is {interval} days (< statutory threshold of {self.min_urgency_days} days)"
            )
        else:
            # Healthy window (>= 30 days)
            urgency_score = min(1.0, 0.5 + min(0.5, (interval - self.min_urgency_days) / 60.0))
            justification = f"Healthy CFP window of {interval} days (>= {self.min_urgency_days} days threshold)"

        return TemporalIntegrityResult(
            announcement_date=announcement_date,
            deadline_date=deadline_date,
            interval_days=interval,
            predatory_urgency=is_predatory,
            urgency_score=clamp01(urgency_score),
            justification=justification,
        )

    def analyze_grammatical_tense(
        self, statements: Sequence[Mapping[str, str]]
    ) -> Tuple[List[TenseAnalysisRecord], float, List[str]]:
        """
        Rule-based Grammatical Tense Analysis (GTA) of indexing & review claims.
        """
        records: List[TenseAnalysisRecord] = []
        justification: List[str] = []
        current_year = date.today().year

        conditional_patterns = [
            r"\b(?:may|might|could|would)\s+(?:be\s+)?(?:indexed|included|listed|submitted)",
            r"\b(?:possibly|potentially)\s+(?:indexed|included)",
            r"\bsubject\s+to\s+(?:indexing|inclusion|approval)",
        ]
        future_patterns = [
            r"\b(?:will|shall|going\s+to)\s+(?:be\s+)?(?:indexed|included|submitted|listed)",
            r"\b(?:planning|aiming|intending)\s+to\s+(?:submit|apply|index)",
            r"\bto\s+be\s+(?:indexed|submitted|included)",
            r"\bapplied?\s+for\s+(?:indexing|inclusion)",
            r"\bunder\s+(?:review|consideration|evaluation)\s+for",
        ]
        past_patterns = [
            r"\b(?:was|were|has\s+been|had\s+been)\s+(?:indexed|included|listed)",
            r"\bindexed\s+.*?\bsince\s+(\d{4})\b",
            r"\bsince\s+(\d{4})\b",
        ]

        present_patterns = [
            r"\b(?:is|are)\s+(?:indexed|included|listed|covered|abstracted)",
            r"\bcurrently\s+(?:indexed|included|listed)",
            r"\bindexed\s+(?:in|by)\b",
        ]

        total_penalty = 0.0
        seen_tenses_by_indexer: Dict[str, Set[str]] = {}

        for item in statements:
            text = item.get("text", "").lower()
            indexer = item.get("indexer", "General").title()
            source = item.get("source", "cfp").lower()

            tense = "unknown"
            weight = self.rules.param("GTA-WEIGHTS", "unknown")
            is_anachronistic = False

            if any(re.search(p, text) for p in conditional_patterns):
                tense = "conditional"
                weight = self.rules.param("GTA-WEIGHTS", "conditional")
            elif any(re.search(p, text) for p in future_patterns):
                tense = "future"
                weight = self.rules.param("GTA-WEIGHTS", "future")
            elif any(re.search(p, text) for p in past_patterns):
                tense = "past"
                weight = self.rules.param("GTA-WEIGHTS", "past")
                # Check for anachronistic year
                year_match = re.search(r"\bsince\s+(\d{4})\b", text)
                if year_match:
                    claim_year = int(year_match.group(1))
                    if claim_year > current_year:
                        is_anachronistic = True
                        weight += self.rules.param("GTA-WEIGHTS", "impossible_anchor_penalty")
            elif any(re.search(p, text) for p in present_patterns):
                tense = "present"
                weight = self.rules.param("GTA-WEIGHTS", "present")

            # Website location penalty
            if source == "website" and tense in ("future", "conditional"):
                weight += self.rules.param("GTA-WEIGHTS", "website_location_penalty")

            seen_tenses_by_indexer.setdefault(indexer, set()).add(tense)
            total_penalty += max(0.0, weight)

            evidence_str = f"Tense={tense.upper()} (weight {weight:+.2f}) on {source.upper()}"
            if is_anachronistic:
                evidence_str += " [ANACHRONISTIC FUTURE ANCHOR]"

            records.append(
                TenseAnalysisRecord(
                    indexer_name=indexer,
                    claim_text=item.get("text", ""),
                    source=source,
                    tense=tense,
                    risk_weight=weight,
                    is_anachronistic=is_anachronistic,
                    evidence=evidence_str,
                )
            )

        # Check same-indexer contradictions (e.g. claiming both present and future for Scopus)
        for indexer, tenses in seen_tenses_by_indexer.items():
            if "present" in tenses and ("future" in tenses or "conditional" in tenses):
                contra_penalty = self.rules.param("GTA-WEIGHTS", "contradiction_penalty")
                total_penalty += contra_penalty
                justification.append(
                    f"Contradiction detected for '{indexer}': venue claims both present and prospective status (+{contra_penalty:.2f} penalty)"
                )

        credibility_score = clamp01(1.0 - min(1.0, total_penalty))
        justification.append(
            f"GTA analyzed {len(records)} claim statement(s): aggregate tense credibility = {credibility_score:.4f}"
        )

        return records, credibility_score, justification

    def evaluate_tfet(
        self, t1: FingerprintSnapshot, t2: FingerprintSnapshot
    ) -> TFETDriftReport:
        """
        Temporal Fingerprint Evolution Tracking (TFET) comparing multi-dimensional
        fingerprints between time T1 and T2.
        """
        days_diff = max(1, (t2.timestamp - t1.timestamp).days)

        # 1. CFP risk drift
        d_cfp = abs(t2.cfp_risk_score - t1.cfp_risk_score)
        # 2. Website structural drift
        d_web = abs(t2.website_depth_score - t1.website_depth_score)
        # 3. Completeness drift
        d_comp = abs(t2.structural_completeness - t1.structural_completeness)
        # 4. Indexing claims drift
        d_claims = abs(t2.indexing_claims_count - t1.indexing_claims_count) / max(1.0, t1.indexing_claims_count + t2.indexing_claims_count)
        # 5. CFP syntax signature drift (binary)
        d_sig = 1.0 if t1.cfp_signature_hash != t2.cfp_signature_hash else 0.0
        # 6. Organizer turnover
        d_org = abs(t2.organizer_count - t1.organizer_count) / max(1.0, t1.organizer_count + t2.organizer_count)
        # 7. Domain change (hijack indicator)
        d_domain = 1.0 if t1.domain_name.lower() != t2.domain_name.lower() else 0.0

        drift_vector = {
            "cfp_risk": d_cfp,
            "website_depth": d_web,
            "structural_completeness": d_comp,
            "indexing_claims": d_claims,
            "cfp_signature": d_sig,
            "organizer_continuity": d_org,
            "ownership": d_domain,
        }

        weights = {
            "cfp_risk": self.rules.param("TFET", "w_cfp_risk"),
            "website_depth": self.rules.param("TFET", "w_website_depth"),
            "structural_completeness": self.rules.param("TFET", "w_structural_completeness"),
            "indexing_claims": self.rules.param("TFET", "w_indexing_claims"),
            "cfp_signature": self.rules.param("TFET", "w_cfp_signature"),
            "organizer_continuity": self.rules.param("TFET", "w_organizer_continuity"),
            "ownership": self.rules.param("TFET", "w_ownership"),
        }

        # Weighted Euclidean norm: ||Delta_F||_W = sqrt( sum w_k * Delta_F_k^2 / sum w_k )
        numerator = sum(weights[k] * (drift_vector[k] ** 2) for k in drift_vector)
        denominator = sum(weights.values())
        norm = math.sqrt(numerator / denominator) if denominator > 0 else 0.0

        # Monthly velocity
        velocity = norm * (30.0 / days_diff)
        stability_alert = norm > self.tfet_threshold
        hijack_suspected = d_domain > 0 and (d_sig > 0 or d_claims > 0.5)

        mutations: List[str] = []
        if d_domain > 0:
            mutations.append(f"Domain changed from '{t1.domain_name}' to '{t2.domain_name}'")
        if d_sig > 0:
            mutations.append("CFP syntax signature altered completely")
        if d_cfp > 0.20:
            mutations.append(f"CFP risk score shifted by {d_cfp:.2f}")
        if d_claims > 0.30:
            mutations.append(f"Indexing claims modified substantially ({d_claims:.2f})")

        adj_gain = self.rules.param("TFET", "adjustment_gain")
        adj_cap = self.rules.param("TFET", "adjustment_cap")
        hijack_bonus = self.rules.param("TFET", "hijack_bonus")

        risk_adj = min(adj_cap, norm * adj_gain) if stability_alert else 0.0
        if hijack_suspected:
            risk_adj = min(adj_cap, risk_adj + hijack_bonus)

        justification = [
            f"TFET compared snapshots across {days_diff} days (T1: {t1.timestamp} -> T2: {t2.timestamp})",
            f"Weighted drift magnitude ||Delta_F||_W = {norm:.4f} "
            f"{'>' if stability_alert else '<='} operational threshold {self.tfet_threshold:.2f}",
            f"Drift velocity: {velocity:.4f} / month",
        ]
        if hijack_suspected:
            justification.append("CRITICAL: Domain and signature shift indicate prospective hijacked journal takeover")

        return TFETDriftReport(
            drift_vector=drift_vector,
            weighted_drift_magnitude=norm,
            stability_threshold=self.tfet_threshold,
            stability_alert=stability_alert,
            drift_velocity_per_month=velocity,
            hijack_suspected=hijack_suspected,
            temporal_risk_adjustment=risk_adj,
            mutations=mutations,
            justification=justification,
        )

    def analyze(
        self,
        venue_id: str,
        venue_name: str,
        candidate_url: str = "",
        announcement_date: Optional[date] = None,
        deadline_date: Optional[date] = None,
        indexing_claims: Optional[Sequence[Mapping[str, str]]] = None,
        t1_snapshot: Optional[FingerprintSnapshot] = None,
        t2_snapshot: Optional[FingerprintSnapshot] = None,
    ) -> VenueIntelligenceResult:
        """Full deterministic audit of venue intelligence stream."""
        url_audit = self.audit_url(candidate_url)
        urgency = self.evaluate_temporal_urgency(announcement_date, deadline_date)
        tense_records, tense_score, gta_just = self.analyze_grammatical_tense(indexing_claims or [])

        tfet_report = None
        if t1_snapshot and t2_snapshot:
            tfet_report = self.evaluate_tfet(t1_snapshot, t2_snapshot)

        # Module sub-signal weights
        w_url = self.rules.param("VI-SUBSIGNAL-WEIGHTS", "url")
        w_temp = self.rules.param("VI-SUBSIGNAL-WEIGHTS", "temporal")
        w_claims = self.rules.param("VI-SUBSIGNAL-WEIGHTS", "claims")

        credibility = (
            w_url * url_audit.score
            + w_temp * urgency.urgency_score
            + w_claims * tense_score
        ) / (w_url + w_temp + w_claims)

        if tfet_report and tfet_report.stability_alert:
            credibility = max(0.0, credibility - tfet_report.temporal_risk_adjustment)

        flags: List[str] = []
        if urgency.predatory_urgency:
            flags.append("VI_PREDATORY_URGENCY")
        if url_audit.is_spoofed:
            flags.append(f"VI_URL_SPOOF_{url_audit.classification}")
        if any(r.tense in ("future", "conditional") for r in tense_records):
            flags.append("VI_GTA_PROSPECTIVE_INDEXING_CLAIM")
        if any(r.is_anachronistic for r in tense_records):
            flags.append("VI_GTA_ANACHRONISTIC_ANCHOR")
        if tfet_report and tfet_report.stability_alert:
            flags.append("VI_TFET_STABILITY_ALERT")
        if tfet_report and tfet_report.hijack_suspected:
            flags.append("VI_TFET_HIJACK_SUSPECTED")

        justification = [
            f"Venue Intelligence assessment for '{venue_name}' ({venue_id})",
            f"URL analysis: {url_audit.justification}",
            f"Temporal urgency: {urgency.justification}",
            *gta_just,
        ]
        if tfet_report:
            justification.extend(tfet_report.justification)
        justification.append(f"Composite venue credibility signal s_venue = {credibility:.4f}")

        return VenueIntelligenceResult(
            venue_id=venue_id,
            venue_name=venue_name,
            url_audit=url_audit,
            temporal_integrity=urgency,
            tense_analysis=tense_records,
            tense_credibility_score=tense_score,
            tfet_drift=tfet_report,
            credibility_signal=credibility,
            flags=sorted(flags),
            justification=justification,
        )
