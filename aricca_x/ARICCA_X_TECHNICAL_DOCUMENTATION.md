# ARICCA-X: COMPREHENSIVE TECHNICAL SPECIFICATION & PRIOR ART SEARCH REPORT
**Version:** 2.0 | **Date:** October 2026 | **Inventors:** Panchadip B & Somyajeet A

---

## 1. ABSTRACT
Disclosed is a deterministic, multi-signal enterprise platform (ARICCA-X) for auditing academic research integrity. The system provides a mathematically verifiable pipeline evaluating venue credibility, researcher citation cartels, peer-review authenticity, and funding mandate compliance. To ensure patentability under 35 U.S.C. § 101, the core pipeline eschews non-deterministic Machine Learning (ML) models in favor of explicit algorithms, including Bounded Depth-First Search (DFS) for citation graph analysis, H-Index decomposition mathematics, and deterministic linguistic fingerprinting for review authenticity.

---

## 2. FIELD OF THE INVENTION
The present invention generally relates to data processing systems and software architecture for academic informatics. More specifically, it relates to algorithmic verification of scientific publications, citation networks, and compliance engines.

---

## 3. BACKGROUND OF THE INVENTION & PRIOR ART SEARCH REPORT

The explosion of predatory publishing, citation cartels, and AI-generated peer reviews has created a crisis in academic integrity. However, existing prior art fails to provide a unified, deterministic, and scalable solution.

### 3.1. Prior Art Category 1: Predatory Journal Databases
**Existing Solutions:** Cabell’s Predatory Reports, Beall’s List (Defunct).
*   **Methodology:** Rely on subjective human curation, crowdsourcing, and manual application of static criteria to categorize journals.
*   **Prior Art Deficiencies:** Human curation cannot scale with the rapid generation of spoofed or "hijacked" conferences. Furthermore, static lists are inherently subjective and legally precarious.
*   **Novelty of the Present Invention (Claims 1-5):** ARICCA-X programmatically analyzes conference attributes using objective metrics. It utilizes Levenshtein distance computations across temporal snapshots to detect hijacked URL spoofs and rule-based NLP to detect plagiarized Call for Papers (CFP) texts, removing human subjectivity entirely.

### 3.2. Prior Art Category 2: Citation Tracking & Indexing
**Existing Solutions:** Dimensions.ai, Scopus, Web of Science, Google Scholar.
*   **Methodology:** These databases aggregate metadata, index references, and compute standard bibliometrics, such as the h-index (Hirsch, 2005) or the i10-index.
*   **Prior Art Deficiencies:** They treat all citations as equal. They do not programmatically audit the *independence* of the citations. A researcher orchestrating a "citation cartel" with colleagues will appear highly cited and legitimate on these platforms.
*   **Novelty of the Present Invention (Claims 6-8):** ARICCA-X introduces automated **Citation Ring Detection** via Bounded Depth-First Search (DFS) traversing directed citation graphs to identify reciprocal loops. Additionally, it introduces **H-Index Decomposition**, mathematically isolating self-citations, co-author citations, and same-institution citations to compute a "Citation Independence Ratio (CIR)" and a "True Independent H-Index."

### 3.3. Prior Art Category 3: AI-Generated Text Detection
**Existing Solutions:** Turnitin, GPTZero, Originality.ai.
*   **Methodology:** Utilize black-box Machine Learning, specifically large language models (LLMs) and transformer architectures, to predict text origin based on probability distributions (perplexity and burstiness).
*   **Prior Art Deficiencies:** ML models suffer from hallucinations, false positives against non-native English speakers, and lack a deterministic, auditable evidence chain. When a university challenges a flagged review, an ML model cannot provide a concrete mathematical justification.
*   **Novelty of the Present Invention (Claims 9-11):** ARICCA-X relies on **Deterministic Linguistic Fingerprinting**. It uses strict mathematical formulas (e.g., Coefficient of Variation in sentence length, Boolean regex matching for specificity) to establish whether a peer review is authentic. This ensures every flagged review is accompanied by a concrete, human-readable mathematical justification.

### 3.4. Prior Art Category 4: Compliance Tracking
**Existing Solutions:** Sherpa Romeo.
*   **Methodology:** Provides a lookup database of publisher open-access policies.
*   **Prior Art Deficiencies:** It places the burden of logic on the human compliance officer to map the publisher policy against specific, complex funding mandates (e.g., Plan S vs. NIH).
*   **Novelty of the Present Invention (Claims 12-13):** ARICCA-X contains a **Publication-Level Rule Engine**. It consumes machine-readable mandates and executes a deterministic Boolean verification against each specific publication, outputting a precise compliance/non-compliance audit trail per paper.

---

## 4. DETAILED DESCRIPTION OF THE PREFERRED EMBODIMENTS

### 4.1. The "Alice" Defense Strategy: Architectural Separation
A critical aspect of the present invention is its structure specifically designed to satisfy the requirements of 35 U.S.C. § 101. Generative AI and ML classifiers are frequently classified as "abstract ideas." 

To overcome this, ARICCA-X implements a bifurcated architecture:
1.  **The On-Chain Deterministic Pipeline:** The production system deployed to end-users. It strictly uses Boolean logic, rule engines, and graph theory mathematics.
2.  **The Off-Chain ML Sandbox:** An isolated local environment where Deep Learning models are empirically validated against historical data. The ML outputs are never directly fed to the user. Instead, insights are translated by human operators into deterministic rules (e.g., "The ML model found AI uses 'perhaps' frequently; we now hardcode a hedging density rule of >8.0 per 100 words into the Deterministic Pipeline").

### 4.2. Module A: Venue Intelligence Engine
The system evaluates a venue $V$ based on a set of programmatic heuristics $H = \{h_1, h_2, ... h_n\}$.
1.  **Temporal Integrity:** Evaluates the delta between CFP announcement $T_{cfp}$ and submission deadline $T_{sub}$. If $\Delta T < \tau_{min}$ (where $\tau_{min}$ is 30 days), a "Predatory Urgency" flag is raised.
2.  **URL Spoofing:** Applies Levenshtein distance $lev(s_1, s_2)$ between the submitted conference URL and known legitimate IEEE/ACM registries.

### 4.3. Module B: Researcher Auditing Engine (DFS & H-Index)
**Bounded DFS Graph Traversal (Claim 6):**
Let a citation network be a directed graph $G = (V, E)$, where $V$ represents authors and $E$ represents a citation from $V_i$ to $V_j$.
To detect a cartel for a target author $V_{target}$, the system executes a Bounded DFS with max depth $k=5$:
```text
function findRings(source, target, depth_limit):
    if depth > depth_limit: return null
    if current == target AND path_length > 1: return path
    for neighbor in get_citations(current):
        findRings(neighbor, target, depth + 1)
```
This isolates hidden reciprocal rings (e.g., $V_a \rightarrow V_b \rightarrow V_c \rightarrow V_a$) that standard citation indexes ignore.

**H-Index Decomposition Mathematics (Claim 8):**
Let $P$ be a set of publications for an author, sorted by citation count in descending order.
*   Standard h-index $h$: The maximum value such that at least $h$ papers have $\ge h$ citations.
*   The system decomposes total citations $C_{total}$ into Self-Citations ($C_{s}$), Co-Author Citations ($C_{ca}$), and Independent Citations ($C_{ind}$).
*   **True H-Index ($h_{true}$):** Calculated by running the h-index algorithm exclusively on $C_{ind}$.
*   **Citation Independence Ratio (CIR):** $CIR = C_{ind} / C_{total}$. If $CIR < 0.30$, the system generates a mathematically verifiable inflation alert.

### 4.4. Module C: Peer-Review Forensics (Deterministic NLP)
The engine consumes a peer review text $T$ and extracts deterministic features:
1.  **Sentence Length Variance (Claim 9a):** Tokenizes sentences $S$. Computes the mean length $\mu$ and standard deviation $\sigma$. Calculates the Coefficient of Variation: $CV = \sigma / \mu$. AI-generated text typically yields $CV < 0.20$ (unnaturally uniform).
2.  **Hedging Density (Claim 9b):** Scans $T$ against a strict array of hedging tokens $W_h$ (e.g., "it appears", "might consider"). Density $D_h = (Count(W_h) / Length(T)) * 100$.
3.  **Specificity Score (Claim 9c):** Applies Regex matching for specific manuscript anchors (e.g., "Equation 4", "Table 2").
4.  **Sentiment Alignment (Claim 11):** Maps positive tokens ($P$) and negative tokens ($N$) to calculate Polarity = $(P-N)/(P+N)$. If Polarity is strongly positive ($>0.6$) but the recommendation is "Reject", a misalignment flag is raised.

### 4.5. Module D: Grant Compliance Engine
A deterministic verification matrix for federal funding mandates.
1.  **Input:** Publication metadata $M$ (Embargo length, OA Type, License, Repository Status).
2.  **Mandate DB:** Contains logic checks for agencies (e.g., `PlanS_Rule1: OA == Gold AND License == CC-BY`).
3.  **Execution:** $M$ is evaluated against all rules in the target mandate. The engine outputs an array of discrete Pass/Fail records with human-readable remediation strings.

---

## 5. REDUCTION TO PRACTICE & EMPIRICAL VALIDATION
The mathematical viability of the deterministic engines was validated through a large-scale automated fuzzing protocol (Stress Test Version 1.0.0).

**Test Parameters:** 11,500 total varied inputs.
1.  **Citation Graphs:** 1,000 synthetic directed graphs (10-50 nodes) with injected cartels. **Result:** 100% cartel identification; 0 false negatives.
2.  **H-Index Portfolios:** 10,000 extreme publication portfolios with randomized citation distribution. **Result:** 0 mathematical boundary violations ($h_{true}$ never erroneously exceeded standard $h$).
3.  **Linguistic Fingerprinting:** 500 massive text blocks (up to 5,000 words) with extreme edge-case syntax. **Result:** 0 processing crashes; NaN/zero-division safe.
**Conclusion:** The system is empirically proven to be robust, deterministic, and functionally reduced to practice.

---

## 6. PATENT CLAIMS

**1.** A deterministic, machine-executable method for multi-signal academic integrity verification, comprising: 
(a) a venue intelligence module; (b) a researcher auditing module utilizing directed graph traversal; (c) a peer-review forensics module utilizing non-probabilistic linguistic feature extraction; (d) a grant compliance rule engine; and (e) a correlation engine generating a composite integrity matrix.

**2.** The method of claim 1, wherein the researcher auditing module computes a Citation Concentration Ratio (CCR) identifying temporal citation bursts within a 90-day bound.

**3.** The method of claim 1, wherein the researcher auditing module executes a Bounded Depth-First Search (DFS) on a directed citation graph to identify reciprocal citation rings up to depth *k*.

**4.** The method of claim 1, wherein the researcher auditing module performs self-citation and co-author citation decomposition to compute a True Independent H-Index.

**5.** The method of claim 1, wherein the peer-review forensics module calculates a Coefficient of Variation (CV) of sentence lengths to detect artificially uniform, generated text.

*(Note: Claims 6-14 map to the extended permutations described in PATENT_SPECIFICATION_V2.md)*

---
*END OF REPORT*
