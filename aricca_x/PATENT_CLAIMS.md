# ARICCA-X Patent Claims

**ARICCA-X: Automated Research Integrity, Credibility & Compliance Analyzer**

**Patent Application — Claims Specification**

**Inventors**: Panchadip B & Somyajeet A  
**Filing Date**: October 2026  
**Priority Date**: January 2, 2026 (v1.0.0 release)

---

## Preamble: Technical Problem Addressed

The automated assessment of academic research venue credibility presents specific
technical challenges that distinguish it from general-purpose text classification
or risk scoring:

1. **Heterogeneous Signal Integration**: Credibility signals come from fundamentally
   different data modalities (natural language text, website structure, graph topology,
   database records) that cannot be meaningfully combined by prior-art weighted averaging.

2. **Deceptive Signal Correlation**: Sophisticated predatory venues invest selectively
   in visible signals (e.g., professional-looking CFP text) while neglecting correlated
   indicators (e.g., website infrastructure), creating cross-signal anomalies invisible
   to single-dimension analysis.

3. **Temporal Behavioral Evolution**: Predatory venues evolve their deception over time,
   rendering static-snapshot analysis unreliable. No prior art performs longitudinal
   fingerprint comparison.

4. **Claim Phrasing Deception**: Predatory venues use grammatical tense manipulation
   ("will be indexed" vs. "is indexed") to imply credentials they do not possess.
   Prior art detects keyword *presence* but does not analyze *temporal framing*.

5. **Data Completeness Bias**: Prior-art scoring systems produce false-neutral outputs
   when data sources are unavailable, masking risk from incomplete assessments.

---

## CLAIM 1: Adaptive Decay Weighting System for Multi-Signal Credibility Assessment

A computer-implemented method for assessing the credibility of a research venue,
the method comprising:

**(a)** receiving, by a processor, a plurality of heterogeneous input signals about
a research venue, the signals comprising at least two of: (i) a Call for Papers (CFP)
textual analysis signal, (ii) a website structural analysis signal, (iii) an indexing
claim verification signal, (iv) a contact legitimacy signal, (v) an organizational
structure signal, and (vi) a publication history signal;

**(b)** determining, for each signal, a data availability indicator representing
whether that signal is based on real data or on a neutral default;

**(c)** computing, using an Adaptive Decay Weighting algorithm, an effective weight
for each available signal by:
  - (c1) calculating a total available base weight as the sum of base weights for
    all signals with positive data availability indicators;
  - (c2) calculating a total absent base weight as the sum of base weights for all
    signals with negative data availability indicators;
  - (c3) for each available signal, computing an effective weight equal to:
    `base_weight + (base_weight / total_available_weight) × total_absent_weight`,
    thereby redistributing the full weight budget proportionally among available
    signals rather than discarding absent-signal weight;
  - (c4) applying a data-absence penalty to a risk score proportional to the number
    of absent data sources;

**(d)** computing a weighted risk score by applying the effective weights to the
signal scores; and

**(e)** outputting a deterministic credibility assessment that is invariant to
evaluation order and reproducible given identical inputs.

**Claim 1 Novelty Statement**: Unlike prior-art systems that use fixed-weight
averaging (where absent data defaults to neutral 0.5 scores), the Adaptive Decay
Weighting algorithm dynamically redistributes weight budget to prevent false-neutral
assessments when data is incomplete, while simultaneously penalizing confidence —
solving the specific technical problem of data completeness bias.

---

## CLAIM 2: Cross-Signal Anomaly Detection for Deceptive Venue Identification

A computer-implemented method for detecting deceptive research venues, the method
comprising:

**(a)** computing, by a processor, independent credibility scores for a plurality of
correlated signal pairs derived from different data modalities of a research venue;

**(b)** maintaining a predefined signal correlation matrix that identifies pairs of
signals expected to co-vary in legitimate venues (e.g., CFP professionalism and
website quality; indexing credibility and organizational structure);

**(c)** for each correlated signal pair in the matrix:
  - computing a divergence magnitude as the absolute difference between the two
    signals' credibility scores;
  - comparing the divergence magnitude against a predefined anomaly divergence
    threshold;
  - when the divergence exceeds the threshold, generating a CrossSignalAnomaly
    data structure containing: the signal identifiers, their respective scores,
    the divergence magnitude, an anomaly type classification
    (quality_mismatch | claim_contradiction | temporal_inconsistency), and a risk
    amplification factor computed as:
    `(divergence - threshold) × amplification_coefficient`;

**(d)** aggregating the risk amplification factors from all detected anomalies; and

**(e)** applying the aggregated risk amplification to the base credibility score,
thereby increasing the risk assessment for venues exhibiting cross-signal
inconsistencies characteristic of deceptive behavior.

**Claim 2 Novelty Statement**: No prior art performs pairwise divergence analysis
between correlated venue credibility signals across different data modalities.
This claim addresses the specific technical problem that sophisticated predatory
venues selectively invest in one visible signal while neglecting correlated ones —
a deception pattern that is mathematically invisible to single-signal analysis
or simple aggregation.

---

## CLAIM 3: Grammatical Tense Analysis for Indexing Claim Veracity Classification

A computer-implemented method for evaluating the veracity of academic indexing
claims in textual documents, the method comprising:

**(a)** extracting, by a processor, text segments containing references to academic
database indexers from a document;

**(b)** for each extracted text segment, classifying the grammatical tense of the
indexing claim by matching verb phrase patterns surrounding indexing-related
keywords against a hierarchical tense classification taxonomy comprising:
  - **CONDITIONAL** tense (highest suspicion): patterns indicating uncertainty
    (e.g., "may be indexed", "could be included", "subject to approval");
  - **FUTURE** tense (high suspicion): patterns indicating prospective action
    (e.g., "will be indexed", "planning to submit", "under consideration for");
  - **PAST** tense (low suspicion): patterns indicating historical state
    (e.g., "was indexed", "has been indexed since [year]");
  - **PRESENT** tense (neutral): patterns indicating current state
    (e.g., "is indexed", "currently listed in");
  - **UNKNOWN** (slight suspicion): no clear tense detected;

**(c)** applying tense-specific risk weights to each classified claim, wherein
CONDITIONAL and FUTURE tense claims receive risk weights of 0.30 and 0.25
respectively, and PAST tense claims receive a negative risk weight of -0.05;

**(d)** combining the tense-based risk with pattern-based suspicion scoring and
vagueness detection to produce a composite veracity suspicion score; and

**(e)** outputting a formal ClaimVeracity classification enum value
(VERIFIED | UNVERIFIED | SUSPICIOUS | FALSE | PENDING) for each claim.

**Claim 3 Novelty Statement**: Prior art in predatory venue detection identifies
the *presence* of indexer mentions in text. This claim introduces a specific
technical improvement: analyzing the *grammatical temporal framing* of those
mentions to distinguish between factual statements of current indexing status
and deceptive implications of future or conditional indexing. This addresses the
specific real-world deception technique where venues claim "will be submitted to
Scopus" to imply Scopus indexing.

---

## CLAIM 4: Temporal Fingerprint Evolution Tracking for Longitudinal Venue Monitoring

A computer-implemented method for monitoring the behavioral evolution of a research
venue over time, the method comprising:

**(a)** generating, by a processor, a first structured venue fingerprint at a first
time T1, the fingerprint comprising: a CFP syntax signature hash, a CFP risk score,
a website depth score, a structural completeness score, a set of claimed indexers,
a set of organizer names, and a composite fingerprint hash;

**(b)** generating a second structured venue fingerprint at a second time T2 > T1
for the same venue;

**(c)** computing a multi-dimensional drift analysis by comparing the two fingerprints
across at least five independent dimensions:
  - (c1) **CFP Risk Drift**: absolute change in CFP risk score;
  - (c2) **Website Structural Drift**: average of website depth score change and
    structural completeness change;
  - (c3) **Indexing Claim Drift**: ratio of added/removed indexer claims to total
    unique claims across both fingerprints;
  - (c4) **CFP Signature Drift**: binary indicator of whether the CFP syntax
    signature hash has changed;
  - (c5) **Organizer Continuity Drift**: complement of the Jaccard similarity
    between previous and current organizer name sets;

**(d)** flagging specific dimension-level changes exceeding predefined thresholds
as "fingerprint mutations", each mutation comprising: the dimension name, previous
and current values, drift magnitude, and drift direction;

**(e)** computing an aggregate drift magnitude as a weighted sum of all dimension
drifts; and

**(f)** deriving a temporal risk adjustment factor from the aggregate drift magnitude,
wherein drift exceeding 0.3 produces a positive risk adjustment of
`min(aggregate_drift × 0.5, 0.25)`, and drift below 0.3 produces zero adjustment.

**Claim 4 Novelty Statement**: All prior art in venue credibility assessment
operates on static snapshots. This claim introduces a specific technical system for
*longitudinal* venue monitoring that detects behavioral evolution — addressing the
real-world problem that sophisticated predatory venues continuously adapt their
deception. The multi-dimensional drift analysis with mutation flagging provides a
specific technical solution that no prior art teaches.

---

## CLAIM 5: Deterministic Multi-Phase Credibility Assessment Pipeline with Auditable Intermediate Representations

A system for assessing research venue credibility, the system comprising:

**(a)** a processor; and

**(b)** a non-transitory computer-readable storage medium storing instructions that,
when executed by the processor, cause the system to perform a six-phase deterministic
assessment pipeline:

  - **Phase 1 (Component Scoring)**: computing independent credibility scores for a
    plurality of data modalities using the Adaptive Decay Weighting system of Claim 1;
  - **Phase 2 (Heuristic Evaluation)**: evaluating a set of at least seven
    domain-specific heuristic rules, each producing an independently auditable
    HeuristicResult data structure containing: rule name, pass/fail status,
    importance classification (critical | high | medium | low), evidence list,
    and score impact factor;
  - **Phase 3 (Credibility Calculation)**: combining Phase 1 and Phase 2 outputs
    using a two-tier weighted aggregation formula:
    `credibility = component_score × 0.60 + heuristic_score × 0.40`,
    where heuristic_score is computed by starting from 1.0 and deducting
    importance-weighted penalties for each failed heuristic;
  - **Phase 4 (Risk Classification)**: mapping the credibility score to a four-tier
    risk classification (low | medium | high | critical);
  - **Phase 5 (Recommendation Generation)**: producing actionable remediation
    recommendations based on specific score component thresholds and failed heuristic
    patterns; and
  - **Phase 6 (Flag Generation)**: producing severity-classified warning flags
    triggered by critical heuristic failures and extreme score values;

wherein each phase produces independently serializable intermediate data structures
that constitute a complete audit trail, and wherein the entire pipeline is
**deterministic**: identical inputs always produce bit-identical outputs regardless
of execution environment, time, or evaluation order.

**Claim 5 Novelty Statement**: This claim addresses the specific technical problem
that ML-based credibility systems are non-reproducible black boxes unsuitable for
institutional decision-making. The six-phase pipeline with independently auditable
intermediate representations provides a specific, unconventional technical architecture
that guarantees deterministic reproducibility while maintaining multi-dimensional
analysis depth — a technical improvement over both ML-based systems (non-reproducible)
and simple rule-based checklists (single-dimensional).

---

## Dependent Claims

### Claim 6 (dependent on Claim 1)
The method of Claim 1, wherein the Adaptive Decay Weighting algorithm further
comprises detecting Cross-Signal Anomalies as described in Claim 2, and applying
the anomaly risk amplification to the weighted risk score prior to risk classification.

### Claim 7 (dependent on Claim 3)
The method of Claim 3, further comprising cross-referencing the claim location
source (CFP document | venue website | email communication) with the tense
classification, wherein FUTURE or CONDITIONAL tense claims appearing on venue
websites receive an additional suspicion penalty of 0.10 relative to the same
tense appearing in CFP documents.

### Claim 8 (dependent on Claim 4)
The method of Claim 4, further comprising storing a time-series of fingerprints
for each monitored venue and computing trend indicators (improving | stable |
deteriorating) based on the direction of drift across three or more consecutive
fingerprint comparisons.

### Claim 9 (dependent on Claim 5)
The system of Claim 5, wherein the six-phase pipeline is integrated with a
compiler-architecture manuscript compliance checker that converts electronic
manuscripts into intermediate representations and applies deterministic
format-validation rules to produce compiler-style diagnostic reports.

### Claim 10 (dependent on Claims 1-5)
A computer-implemented system combining Claims 1 through 5, further comprising
a report renderer that serializes the complete assessment pipeline output —
including adaptive weights, cross-signal anomalies, tense classifications,
fingerprint mutations, and audit-trail intermediate representations — into
human-readable multi-format reports (text, HTML, JSON, Markdown) with
embedded evidence chains linking each risk flag to its originating data source.

---

## § 101 Survival Notes

Each independent claim (1-5) is drafted to survive the **Alice/Mayo** two-step test:

| Claim | Technical Problem Solved | Specific Technical Mechanism | Not "Just an Abstract Idea" Because |
|-------|-------------------------|------------------------------|--------------------------------------|
| 1 | Data completeness bias in multi-signal scoring | Adaptive weight redistribution + absence penalty | Improves computer scoring accuracy with specific mathematical formula |
| 2 | Cross-signal deception invisible to single-signal analysis | Pairwise divergence against correlation matrix | Novel signal comparison technique with no prior art analog |
| 3 | Grammatical tense manipulation in claims | Hierarchical tense classification taxonomy | Specific NLP mechanism, not general "analyzing text" |
| 4 | Temporal behavioral evolution in deceptive entities | Multi-dimensional fingerprint drift analysis | Longitudinal data structure comparison, not "monitoring" generically |
| 5 | Non-reproducibility of ML-based assessment | Six-phase deterministic pipeline with audit trail | Specific architectural improvement to computer processing |

---

**© 2026 Panchadip B & Somyajeet A. All Rights Reserved. Patent Pending.**
