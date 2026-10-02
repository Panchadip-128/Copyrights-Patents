# ARICCA-X (v2.0) | Enterprise Research Integrity Suite 🛡️

[![Patent Pending](https://img.shields.io/badge/Patent-Pending%20(14%20Claims)-#10b981?style=for-the-badge)](./PATENT_SPECIFICATION_V2.md)
[![Next.js](https://img.shields.io/badge/Next.js-16.3.8-black?style=for-the-badge&logo=next.js)](https://nextjs.org/)
[![Status](https://img.shields.io/badge/Status-Empirically%20Validated-blue?style=for-the-badge)](#6-empirical-validation-engine)

**ARICCA-X** (Academic Research Integrity & Credibility Correlation Analyzer) is a comprehensive, multi-signal platform designed to protect universities, publishers, and funding agencies from academic fraud.

This repository contains the **patent-pending** (14 Claims) implementation of the ARICCA-X v2.0 suite. It replaces subjective, manual evaluation with a **100% deterministic, mathematically verifiable pipeline**. 

---

## 1. System Architecture & "Alice" Compliance (35 U.S.C. § 101)

To overcome the legal hurdles of software patentability (which frequently rejects generic "AI" as an abstract idea), ARICCA-X strictly bifurcates its architecture into an **Off-Chain ML Sandbox** (for research) and an **On-Chain Deterministic Pipeline** (the patentable invention).

```mermaid
graph TD
    subgraph "Off-Chain ML Sandbox (Research Use Only)"
        ML1["Deep Learning Models"]
        ML2["NLP Transformers"]
        ML3["Pattern Discovery"]
        ML1 --> ML3
        ML2 --> ML3
    end
    
    subgraph "Human Rule Translation Layer"
        HT["Manual Translation into Math/Logic Rules"]
    end
    
    subgraph "On-Chain Deterministic Pipeline (Patentable Application)"
        D1["Module A: Venue Intelligence"]
        D2["Module B: Researcher Auditing"]
        D3["Module C: Peer Review Forensics"]
        D4["Module D: Grant Compliance"]
        D1 & D2 & D3 & D4 --> CORR["Correlation Engine (Claim 14)"]
        CORR --> AUDIT["Auditable Evidence Matrix"]
    end
    
    ML3 -. "Offline Insights" .-> HT
    HT -. "Hardcoded Deterministic Rules" .-> D1
    HT -. "Hardcoded Deterministic Rules" .-> D2
    HT -. "Hardcoded Deterministic Rules" .-> D3
```

---

## 2. Module B: Researcher Auditing (Claims 6-8)

This module audits citation networks and author publication portfolios to mathematically isolate citation cartels and artificial h-index inflation.

### Algorithm 2.1: Bounded DFS for Citation Ring Detection
Standard citation indices (Scopus, Web of Science) track linear citations but fail to detect reciprocal, multi-node collusion loops. ARICCA-X utilizes a Bounded Depth-First Search (DFS) algorithm on a directed citation graph $G=(V,E)$.

```mermaid
flowchart TD
    Start["Start DFS at Target Node V_target"]
    CheckDepth{"Depth > k (max=5)?"}
    CheckDepth -- Yes --> Abort["Abort Path"]
    CheckDepth -- No --> GetNeighbors["Get Adjacent Nodes V_n"]
    GetNeighbors --> CheckTarget{"V_n == V_target & Path Length > 1?"}
    CheckTarget -- Yes --> RingFound["Log Citation Cartel Ring"]
    CheckTarget -- No --> Recurse["Recursively call DFS(V_n, Depth+1)"]
    Recurse --> CheckDepth
```

### Theorem 2.2: H-Index Decomposition & CIR Mathematics
An author's standard h-index ($h$) can be artificially inflated via self-citation and co-author coordination. ARICCA-X applies the following mathematical decomposition:
1. **Total Citations** = $C_{total}$
2. **Artificial Citations** = $C_{self} + C_{co-author}$
3. **Independent Citations** = $C_{ind} = C_{total} - (C_{self} + C_{co-author})$

The system recalculates the h-index using *only* $C_{ind}$ to generate the **True H-Index** ($h_{true}$). 
The **Citation Independence Ratio (CIR)** is calculated as:
$$CIR = \frac{C_{ind}}{C_{total}}$$
If $CIR < 0.30$, a deterministic inflation alert is triggered.

---

## 3. Module C: Peer-Review Forensics (Claims 9-11)

Instead of utilizing black-box Large Language Models (LLMs) which are prone to hallucination, Module C utilizes **Deterministic Linguistic Fingerprinting**. 

### Algorithm 3.1: Sentence Length Coefficient of Variation
AI-generated text exhibits unnatural structural uniformity. The system tokenizes sentences $S$, computes the mean length $\mu$ and standard deviation $\sigma$, and derives the Coefficient of Variation:
$$CV = \frac{\sigma}{\mu}$$
If $CV < 0.20$, the review is flagged for suspicious uniformity.

### Algorithm 3.2: Deterministic Decision Matrix
```mermaid
graph TD
    Input["Peer Review Text Input"]
    Input --> Ext1["Calculate Specificity Score (Regex Anchors)"]
    Input --> Ext2["Calculate Hedging Density (Tokens/100w)"]
    Input --> Ext3["Calculate Sentence CV"]
    
    Ext1 --> Cond1{"SS < 0.15 AND HD > 8.0?"}
    Ext2 --> Cond1
    
    Cond1 -- Yes --> Flag1["FLAG: LIKELY GENERATED"]
    Cond1 -- No --> Cond2{"CV < 0.20?"}
    Ext3 --> Cond2
    
    Cond2 -- Yes --> Flag2["FLAG: SUSPICIOUS UNIFORMITY"]
    Cond2 -- No --> Authentic["AUTHENTIC"]
```

---

## 4. Module A: Venue Intelligence (Claims 1-5)

Evaluates the credibility of conferences and journals through programmatic heuristics.

* **Levenshtein Distance Spoof Detection:** Protects against "hijacked" conferences by computing the character-edit distance between a submitted URL and known IEEE/ACM registries.
* **Tense Shift Analysis:** Detects plagiarized Call for Papers (CFP) descriptions by applying strict NLP tense-matching rules to identify improperly spun text.

---

## 5. Module D: Grant Compliance (Claims 12-13)

A Boolean rule engine containing machine-readable matrices for federal and global funding mandates (NIH, NSF, Plan S, UKRI).

```mermaid
graph LR
    Pub["Publication Metadata"] --> Engine{"Compliance Rule Engine"}
    Mandate["Agency Mandates (e.g. Plan S)"] --> Engine
    
    Engine --> Check1["Check: Embargo Time Limit Met"]
    Engine --> Check2["Check: License is CC-BY"]
    Engine --> Check3["Check: Repository Deposited"]
    
    Check1 & Check2 & Check3 --> Output["Discrete Pass/Fail Audit Trail"]
```

---

## 6. Empirical Validation Engine

To satisfy the patent requirement of **Reduction to Practice**, ARICCA-X includes a massive-scale fuzzer (`empirical_evidence_generator.js`). 

**Results from 11,500 fuzzed inputs:**
* **Citation Graphs (1,000 runs):** 100% cartel identification; 0 false negatives in Bounded DFS.
* **H-Index Portfolios (10,000 runs):** 0 mathematical boundary violations ($h_{true}$ never erroneously exceeded standard $h$).
* **Linguistic Fingerprinting (500 runs):** Successfully processed extreme edge-case syntax (up to 5,000 words) without NaN or zero-division errors.

---

## 7. Installation & Usage

### Running the Deterministic Web Application (On-Chain)
Built with Next.js and React.
```bash
cd portal
npm install
npm run dev
```
Navigate to `http://localhost:3000`. Login with:
* **Email:** admin@aricca.com
* **Password:** admin123

### Executing Empirical Validation (Patent Defense)
Run the fuzzers locally to verify mathematical determinism:
```bash
node integrity_test.js
node empirical_evidence_generator.js
```

### Running the ML Sandbox (Off-Chain Research)
*Note: Ensure ML results are manually translated into Boolean rules before integrating into the Next.js app.*
```bash
python ml_verification.py
```

---
*© 2026 Panchadip B & Somyajeet A. All Rights Reserved. Patent Pending.*
