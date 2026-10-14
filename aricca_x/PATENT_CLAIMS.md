# ARICCA-X Patent Claims Specification (Expanded Multi-Signal Architecture)

**ARICCA-X: Deterministic, Machine-Executable Multi-Signal System for Academic Research Integrity & Credibility Verification**

**Patent Application — Full Claims Specification**

**Inventors**: Panchadip B & Somyajeet A  
**Filing Date**: October 2026  
**Priority Date**: January 2, 2026 (v1.0.0 release)  
**Classification**: G06F 40/30 (Semantic Analysis); G06Q 50/20 (Education/Research); G06F 21/64 (Data Integrity Verification); G06F 16/9024 (Graph-based Information Retrieval)

---

## Technical Field and Problems Solved

This invention relates to computerized automated systems for academic research integrity, venue credibility assessment, citation-network forensics, peer-review authenticity verification, and funding mandate compliance auditing.

The invention solves specific technical shortcomings of the prior art:
1. **Absence of Unified Multi-Signal Verification**: Prior art treats venue spoofing, citation cartels, synthetic peer reviews, and open access mandate non-compliance in disjoint technological silos.
2. **Opacity and Non-Reproducibility of Machine-Learning Black Boxes**: ML-based classifiers (e.g., SVMs, transformer encoders, XGBoost stylometry in US9178901B2, US12113828B2, US12361214B2, and Baidya 2026) cannot be audited by institutional bodies, produce probabilistic drift, and carry liability risks in formal integrity adjudications.
3. **Data Completeness Bias (False Neutrals)**: Traditional systems (e.g., AU2012231158B2) substitute default or neutral scores when data sources are absent.
4. **Circumvention by Coordinated Reciprocal Citation Loops**: Standard citation sharpening (e.g., Schreiber 2007) removes only direct self-citations and co-author citations, leaving multi-author reciprocal citation rings undetected.
5. **Decoupled AI Peer-Review Detection**: Prior-art stylometric detectors fail when texts are humanized or when superficial tone contradicts nominal decision outcomes.

---

## CLAIMS

### CLAIM 1: Master Deterministic Multi-Signal Academic Integrity Verification System

A computer-implemented system for automated, auditable verification of academic research integrity, the system comprising:
one or more processors; and
a non-transitory computer-readable memory storing instructions that, when executed by the one or more processors, cause the system to:

**(a)** receive four independent, heterogeneous input data streams associated with an academic publication lifecycle, comprising:
  (i) a publication venue data stream comprising venue identification, website domain identifiers, and Call for Papers (CFP) textual announcements with temporal publication schedules;
  (ii) a directed author citation network stream wherein nodes represent researchers and directed edges represent citation relationships between scholarly works;
  (iii) a peer-review data stream comprising textual review evaluation content and a categorical reviewer recommendation; and
  (iv) a publication metadata stream comprising open access publication route, embargo duration, copyright license classification, repository deposit status, and funding grant acknowledgment identifiers;

**(b)** process each respective input data stream through a dedicated deterministic, non-machine-learning computational module to generate a normalized credibility score, a discrete flag set, and an auditable mathematical record:
  (i) evaluating said publication venue data stream in a **Venue Intelligence Module** by calculating a temporal urgency interval between CFP announcement and submission deadline, computing a Levenshtein edit distance between candidate venue URLs and authenticated academic publisher registry entries, and evaluating indexing veracity using grammatical tense analysis;
  (ii) evaluating said directed citation network stream in a **Researcher Auditing Module** by executing a bounded depth-first search graph traversal to enumerate reciprocal citation loops, decomposing citations into self, co-author, loop, and independent categories, and recomputing a True Independent H-Index and a loop-purged H-Index;
  (iii) evaluating said peer-review data stream in a **Peer-Review Forensics Module** by computing a sentence length coefficient of variation, matching against a predefined deterministic hedging lexicon, evaluating manuscript structural element specificity via regular expressions, and calculating a behavioral alignment between review sentiment polarity and categorical recommendation; and
  (iv) evaluating said publication metadata stream in a **Grant Compliance Engine** by executing machine-readable Boolean rule matrices corresponding to applicable funding mandates to yield rule-level pass/fail indicators and deterministic remediation directives;

**(c)** synthesize the outputs of said dedicated modules in a **Cross-Correlation Engine** configured to:
  (i) apply an Adaptive Dynamic Weighting (ADW) algorithm that redistributes base weight allocations of unobserved streams proportionally over observed streams without fabricating default scores, and computes a closed-form epistemic evidence interval; and
  (ii) execute a Cross-Signal Anomaly Detection (CSAD) algorithm that computes mathematical divergence $D$ between normalized credibility scores of independent modules, and amplifies composite risk proportionally via $Risk' = \min(1, Risk \times (1 + \alpha \cdot g(D, \tau)))$ when divergence exceeds a divergence threshold $\tau$, wherein $\alpha$ is an asymmetric factor penalizing surface-layer facade inflation relative to substrate-layer evidence; and

**(d)** output a deterministic composite risk profile and an auditable, cryptographically verifiable evidence chain for the assessed academic entity;
wherein the entire core pipeline is executed without probabilistic machine-learning inference models.

---

### CLAIM 2: Bifurcated Architecture and Runtime Determinism Enforcement

The system of Claim 1, further comprising a bifurcated architecture separating research development from production execution, comprising:
**(a)** an isolated offline research environment wherein experimental machine-learning models and statistical classifiers analyze empirical corpora to identify risk thresholds;
**(b)** an immutable production rule registry comprising human-approved, sealed production rules defining explicit formulas, Boolean predicates, and numerical thresholds with cryptographically recorded promotion provenance; and
**(c)** an automated determinism runtime guard that inspects loaded runtime libraries prior to pipeline execution and terminates execution upon detecting any probabilistic machine-learning inference library or neural network framework.

---

### CLAIM 3: Adaptive Dynamic Weighting (ADW) with Epistemic Evidence Intervals

The system of Claim 1, wherein the Adaptive Dynamic Weighting (ADW) algorithm comprises:
**(a)** identifying an observed subset of dimensions $A \subseteq K$ having verified data inputs, and designating any unobserved dimension $j \notin A$ as strictly unknown without substituting neutral or default values;
**(b)** calculating an effective weight $w'_i$ for each observed dimension $i \in A$ according to the proportional redistribution formula:
$$w'_i = \frac{w_i}{\sum_{k \in A} w_k}$$
wherein $\sum_{i \in A} w'_i = 1.0$ and $w'_j = 0.0$ for all $j \notin A$;
**(c)** computing an aggregated credibility score $C = \sum_{i \in A} w'_i \cdot s_i$;
**(d)** calculating a closed-form epistemic evidence interval $[L, U]$ bounding prospective true credibility:
$$L = \sum_{i \in A} w_i \cdot s_i$$
$$U = L + \sum_{j \notin A} w_j$$
having an interval width $W = \sum_{j \notin A} w_j$; and
**(e)** triggering an `INSUFFICIENT_EVIDENCE` flag when said interval width $W$ exceeds a predetermined threshold.

---

### CLAIM 4: Layer-Asymmetric Cross-Signal Anomaly Detection (CSAD)

The system of Claim 1, wherein the Cross-Signal Anomaly Detection (CSAD) algorithm comprises:
**(a)** assigning each evaluated credibility signal $s_i \in [0, 1]$ to an architectural evidence layer comprising either:
  (i) a SURFACE layer representing signals that are low-cost to fabricate; or
  (ii) a SUBSTRATE layer representing structural signals that are computationally or organizationally expensive to falsify;
**(b)** for each correlated pair of signals $(s_i, s_j)$, calculating a pairwise divergence magnitude $D_{ij} = |s_i - s_j|$;
**(c)** evaluating an excess divergence function $g(D_{ij}, \tau) = \max\left(0, \frac{D_{ij} - \tau}{1 - \tau}\right)$, wherein $\tau$ is a predetermined divergence threshold;
**(d)** selecting an amplification coefficient $\alpha_{ij} = \alpha_{\text{facade}}$ when the SURFACE-layer signal exceeds the SUBSTRATE-layer signal by more than $\tau$, and $\alpha_{ij} = \alpha_{\text{neutral}}$ otherwise, wherein $\alpha_{\text{facade}} > \alpha_{\text{neutral}}$; and
**(e)** selecting the pair maximizing $\alpha_{ij} \cdot g(D_{ij}, \tau)$ and amplifying composite risk according to:
$$Risk' = \min(1, Risk \times (1 + \alpha^* \cdot g(D^*, \tau)))$$
without executing an artificial intelligence classifier.

---

### CLAIM 5: Venue Intelligence with URL Levenshtein Forensics and Predatory Urgency

The system of Claim 1, wherein the Venue Intelligence Module comprises:
**(a)** extracting a candidate venue domain from a submitted URL and computing a Levenshtein edit distance $d$ between the candidate domain and a registry database of authenticated academic publishers;
**(b)** classifying said candidate domain as a typosquat or lookalike spoof when $1 \le d \le \max(1, \lfloor 0.20 \times L_{\text{reg}} \rfloor)$, wherein $L_{\text{reg}}$ is the character length of the authentic registry domain;
**(c)** parsing Call for Papers announcement dates and submission deadline dates, computing an operational window $\Delta t = t_{\text{deadline}} - t_{\text{announcement}}$, and raising a `PREDATORY_URGENCY` flag when $0 \le \Delta t < 30 \text{ days}$; and
**(d)** executing a Grammatical Tense Analysis (GTA) algorithm on indexing statements to penalize prospective or conditional claims.

---

### CLAIM 6: Grammatical Tense Analysis (GTA) for Venue Indexing Veracity

The system of Claim 5, wherein the Grammatical Tense Analysis (GTA) algorithm comprises:
**(a)** scanning textual claims referencing academic indexing databases;
**(b)** matching verb phrases surrounding indexing keywords against a deterministic tense taxonomy comprising:
  (i) a CONDITIONAL tense receiving a deterministic risk penalty of +0.30;
  (ii) a FUTURE tense receiving a deterministic risk penalty of +0.25;
  (iii) a PRESENT tense receiving a neutral risk penalty of 0.00;
  (iv) a PAST tense receiving a negative risk weight of -0.05; and
  (v) an UNKNOWN tense receiving a slight risk penalty of +0.05;
**(c)** applying an additional penalty of +0.10 when FUTURE or CONDITIONAL tense claims appear on official venue web pages;
**(d)** identifying same-indexer contradictions where a venue asserts both present indexing and prospective indexing; and
**(e)** detecting anachronistic temporal anchors where a claim asserts historical indexing starting in a year exceeding the current calendar year.

---

### CLAIM 7: Temporal Fingerprint Evolution Tracking (TFET)

The system of Claim 1, wherein the Venue Intelligence Module further comprises:
**(a)** generating a multi-dimensional venue fingerprint snapshot $F(T_1)$ at time $T_1$ and a second snapshot $F(T_2)$ at time $T_2 > T_1$, wherein each snapshot comprises CFP risk, website depth, structural completeness, indexing claim count, CFP syntax signature hash, organizer count, and domain ownership identifier;
**(b)** computing a multi-dimensional drift vector $\Delta F = F(T_2) - F(T_1)$;
**(c)** calculating a weighted Euclidean drift magnitude:
$$\|\Delta F\|_W = \sqrt{\frac{\sum_k w_k \cdot (\Delta F_k)^2}{\sum_k w_k}}$$
**(d)** calculating a normalized monthly drift velocity $V = \|\Delta F\|_W \times \frac{30}{\max(1, \text{days}(T_2 - T_1))}$; and
**(e)** raising a `STABILITY_ALERT` when $\|\Delta F\|_W > 0.25$, and raising a `HIJACK_SUSPECTED` alert when domain ownership changes concurrently with syntax signature alteration.

---

### CLAIM 8: Researcher Auditing with Bounded-Depth DFS and Loop-Purged H-Index

The system of Claim 1, wherein the Researcher Auditing Module comprises:
**(a)** constructing a directed author citation graph wherein directed edges $(u, v)$ represent citations from author $u$ to author $v$;
**(b)** executing a bounded depth-first search (DFS) with a maximum depth limit $k = 5$ to enumerate simple directed citation cycles passing through a target author, wherein each simple cycle is enumerated exactly once from its minimal node in lexicographic order;
**(c)** executing a deterministic four-way citation decomposition for citations to the target author:
  (i) `SELF` citations where the target author is listed as a co-author of the citing paper;
  (ii) `CO_AUTHOR` citations where a non-target citing author has co-authored a prior paper with the target author;
  (iii) `LOOP` citations where a citing author is a member of a detected simple citation cycle passing through the target author; and
  (iv) `INDEPENDENT` citations comprising remaining non-self, non-coauthor, non-loop citations;
**(d)** recomputing h-index metrics comprising:
  (i) a standard h-index calculated over all incoming citations;
  (ii) a True Independent H-Index calculated after excluding `SELF` and `CO_AUTHOR` citations; and
  (iii) a loop-purged H-Index calculated after additionally excluding `LOOP` citations;
**(e)** calculating a Citation Independence Ratio $\text{CIR} = \frac{\text{INDEPENDENT} + \text{LOOP}}{\text{TOTAL}}$ and a Loop-Adjusted Citation Independence Ratio $\text{LACIR} = \frac{\text{INDEPENDENT}}{\text{TOTAL}}$; and
**(f)** triggering an inflation alert when either CIR or LACIR falls below 0.30.

---

### CLAIM 9: Peer-Review Forensics via Linguistic Fingerprinting and Behavioral Misalignment

The system of Claim 1, wherein the Peer-Review Forensics Module comprises:
**(a)** tokenizing peer-review text into sentences and words;
**(b)** calculating a coefficient of variation (CV) of sentence word lengths:
$$\text{CV} = \frac{\sigma_{\text{lengths}}}{\mu_{\text{lengths}}}$$
and raising an `ARTIFICIAL_UNIFORMITY` flag when $\text{CV} < 0.20$ for reviews containing at least 3 sentences;
**(c)** calculating a hedging phrase density by matching text against a predetermined academic hedging lexicon and flagging excessive hedging when density exceeds 4.0%;
**(d)** calculating a manuscript specificity score using regular expressions targeting explicit structural elements comprising equations, tables, figures, sections, theorems, algorithms, pages, and lines, and raising a `LOW_SPECIFICITY` flag when references per sentence fall below 0.15;
**(e)** calculating a deterministic sentiment polarity score $P \in [-1.0, 1.0]$:
$$P = \frac{N_{\text{pos}} - N_{\text{neg}}}{\max(1, N_{\text{pos}} + N_{\text{neg}})}$$
based on predetermined positive and negative academic terminology; and
**(f)** evaluating behavioral alignment between polarity $P$ and nominal reviewer recommendation, and triggering a `SENTIMENT_RECOMMENDATION_MISALIGNMENT` alert when $P \ge +0.50$ concurrently with a "Reject" recommendation, or when $P \le -0.50$ concurrently with an "Accept" recommendation.

---

### CLAIM 10: Grant Compliance Verification via Boolean Rule Matrices

The system of Claim 1, wherein the Grant Compliance Engine comprises:
**(a)** maintaining machine-readable Boolean rule matrices defining open access policies for funding mandates comprising NIH, NSF, Plan S, and UKRI;
**(b)** evaluating publication metadata against each rule in the applicable matrix, the rules verifying:
  (i) immediate Gold/Diamond open access route or immediate Green repository deposit with zero embargo;
  (ii) permissible Creative Commons license type;
  (iii) approved institutional, PMC, or NSF-PAR repository deposit status;
  (iv) statutory embargo duration limits; and
  (v) presence of funding agency award numbers in acknowledgments;
**(c)** generating an immutable pass/fail record for each rule evaluation; and
**(d)** generating a deterministic, actionable remediation directive for each failed rule.

---

### CLAIM 11: Six-Phase Strictly Serializable Deterministic Pipeline

A computerized method for academic integrity verification, the method comprising executing six sequential deterministic processing phases:
**(a) Phase 1 (Component Scoring)**: receiving module scores and computing effective weights using the Adaptive Dynamic Weighting (ADW) algorithm of Claim 3;
**(b) Phase 2 (Heuristic Evaluation)**: evaluating domain Boolean heuristic rules and calculating cumulative rule failure penalties;
**(c) Phase 3 (Credibility & Anomaly Aggregation)**: computing composite risk from Phase 1 and Phase 2 outputs and applying the Cross-Signal Anomaly Detection (CSAD) multiplicative risk amplification of Claim 4;
**(d) Phase 4 (Risk Classification)**: mapping composite risk to a four-tier classification comprising low, medium, high, and critical tiers based on fixed numerical thresholds;
**(e) Phase 5 (Recommendation Generation)**: selecting actionable remediation directives mapped to triggered heuristic violations; and
**(f) Phase 6 (Flag Generation & Tamper-Evident Hash Chaining)**: aggregating severity-classified warning flags and recording each phase state in a cryptographically linked SHA-256 audit hash chain;
wherein every intermediate state is canonicalized such that identical inputs yield byte-identical serialized states and bit-identical hash digests.

---

### CLAIM 12: Cryptographic Phase Hash Chain for Tamper-Evident Offline Auditing

The method of Claim 11, wherein recording in said SHA-256 audit hash chain comprises:
**(a)** generating a genesis hash:
$$h_0 = \text{SHA256}(\text{"0"}^{64} \,\|\, \text{pipeline\_id} \,\|\, \text{input\_digest} \,\|\, \text{ruleset\_digest})$$
**(b)** for each phase $i \in \{1, \dots, 6\}$, generating a canonical JSON representation of the complete phase state, calculating a state digest $d_i = \text{SHA256}(\text{canonical\_json}(\text{state}_i))$, and linking the phase record via:
$$h_i = \text{SHA256}(h_{i-1} \,\|\, i \,\|\, \text{phase\_name}_i \,\|\, d_i)$$
and
**(c)** exporting the resulting hash chain, enabling third-party auditors to verify mathematical integrity and absence of tampering without re-running pipeline computation.

---

### CLAIM 13 (Dependent on Claim 1)
The system of Claim 1, wherein phantom reference hallucination is detected in said peer-review data stream by extracting equation and table numerical identifiers cited in the review text and cross-referencing against an actual element manifest of the manuscript under review, raising a hallucination flag when cited elements are absent from the manuscript manifest.

---

### CLAIM 14 (Dependent on Claim 5)
The system of Claim 5, wherein brand embedding spoofing is detected by identifying legitimate publisher trademark tokens embedded within non-conforming second-level domain strings.

---

### CLAIM 15 (Dependent on Claim 8)
The system of Claim 8, wherein said bounded depth-first search graph traversal enforces an execution cycle budget limit to guarantee deterministic upper-bounded execution time on large author citation networks.

---

### CLAIM 16 (Dependent on Claim 1)
A non-transitory computer-readable storage medium comprising instructions that, when executed by a computer, cause the computer to execute the multi-signal academic integrity verification pipeline of Claim 1.

---

### CLAIM 17: Submission Gateway Interdiction Controller (Independent System Claim)

A computerized submission gateway interdiction apparatus for protecting computing and network processing resources from fraudulent manuscript submissions, the apparatus comprising:
a network interface coupled to a communication network;
one or more processors; and
a non-transitory memory storing instructions that, when executed by the one or more processors, cause the apparatus to:
**(a)** intercept an incoming manuscript submission payload and an ingress session token associated with a submitting client session;
**(b)** evaluate the manuscript submission payload through the deterministic multi-signal pipeline of Claim 1 to generate a composite risk score and a closed-form epistemic evidence interval $[L, U]$ having an interval width $W$;
**(c)** execute a dual-threshold evidence-coverage gating rule wherein automated rejection is barred when interval width $W > 0.50$, forcing a quarantine hold;
**(d)** upon determining a RELEASE action code when composite risk is below 0.25 and interval width $W \le 0.50$:
  (i) issue a cryptographically signed HMAC-SHA256 routing authorization token;
  (ii) command an operating system thread scheduler to allocate a pool of compute worker threads for downstream Abstract Syntax Tree generation and manuscript parsing; and
  (iii) commit the submission record to an active editorial queue state;
**(e)** upon determining a HOLD action code when composite risk is between 0.25 and 0.75, or when interval width $W > 0.50$:
  (i) acquire an atomic transactional lock on the submission database record;
  (ii) divert the manuscript submission payload into a segregated sandbox buffer storage partition;
  (iii) suppress allocation of downstream compute worker threads, conserving processor cycle consumption and memory bus bandwidth; and
  (iv) dispatch an asynchronous telemetry request identifying unobserved evidence dimensions; and
**(f)** upon determining a REJECT action code when composite risk is at least 0.75 and interval width $W \le 0.50$:
  (i) push a revocation record to an ingress firewall session table to cryptographically invalidate said ingress session token;
  (ii) transmit a network socket reset packet to sever the client session;
  (iii) purge the segregated sandbox buffer storage partition; and
  (iv) commit an immutable RFC 8785 canonical JSON forensic audit log with a SHA-256 block hash.

---

### CLAIM 18: Computer-Implemented Gateway Interdiction Method (Independent Method Claim)

A computer-implemented method for physical gateway interdiction and compute thread suppression in a manuscript submission platform, the method comprising executing the steps of Claim 17.

---

## 35 U.S.C. § 101 Eligibility Analysis (Alice/Mayo Framework)

| Claim | Specific Technical Improvement | Technological Transformation | Physical Transformation & Concrete Output |
|---|---|---|---|
| **Claim 1** | Four-module multi-signal deterministic architecture combining venue, citation loop DFS, stylometric misalignment, and grant rule matrices. | Eliminates black-box ML drift and data completeness bias through non-ML algebraic formulas. | Generates cryptographically verifiable audit chain and composite risk profile. |
| **Claim 2** | Bifurcated architecture isolating offline research ML models from immutable production rule registries with runtime guard. | Guarantees non-probabilistic production determinism at interpreter level. | Runtime execution interdiction upon detection of unauthorized ML inference modules. |
| **Claim 3** | Adaptive Dynamic Weighting (ADW) with closed-form proportional redistribution and epistemic evidence interval bounding. | Overcomes false-neutral score corruption caused by missing data sources. | Produces mathematically bounded interval $[L, U]$ and width $W$. |
| **Claim 4** | Layer-asymmetric Cross-Signal Anomaly Detection (CSAD) multiplying risk by excess divergence $g(D, \tau)$. | Exposes deceptive bad actors who selectively polish surface signals while neglecting structural substrates. | Deterministically amplifies risk without statistical clustering. |
| **Claim 5-7** | Levenshtein edit distance, predatory window $\Delta t < 30\text{d}$, GTA tense taxonomy, and TFET longitudinal drift $\|\Delta F\|_W$. | Automates forensic detection of hijacked venues and prospective indexing misrepresentations. | Identifies lookalike domains and longitudinal fingerprint mutations. |
| **Claim 8** | Bounded-depth DFS ($k=5$), four-way citation decomposition, True Independent H-Index, loop-purged H-Index, and CIR $<0.30$. | Solves reciprocal colleague collusion undetected by standard self-citation filters. | Restores true unmanipulated bibliometric citation rank. |
| **Claim 9** | Concurrent evaluation of sentence length CV $<0.20$, hedging density, regex element grounding, and sentiment-recommendation misalignment. | Exposes synthetic LLM-generated reviews and corrupt peer review decisions. | Flags behavioral contradiction between verbal praise and rejection outcomes. |
| **Claim 10** | Machine-readable Boolean matrices for NIH, NSF, Plan S, and UKRI open access rules. | Automates legal and contractual grant compliance auditing. | Produces immutable pass/fail records and specific remediation steps. |
| **Claim 11-12** | Six-phase strictly serializable pipeline with canonical serialization and SHA-256 hash chaining. | Guarantees bit-identical reproducible institutional decisions and tamper-evident audit trails. | Enables offline mathematical verification by external judicial or institutional bodies. |

---

**© 2026 Panchadip B & Somyajeet A. All Rights Reserved. Patent Pending.**
