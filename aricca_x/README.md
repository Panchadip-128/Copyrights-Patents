# ARICCA-X (v2.0) | Enterprise Research Integrity Suite 🛡️

[![Patent Pending](https://img.shields.io/badge/Patent-Pending%20(14%20Claims)-#10b981?style=for-the-badge)](./PATENT_SPECIFICATION_V2.md)
[![Next.js](https://img.shields.io/badge/Next.js-16.3.8-black?style=for-the-badge&logo=next.js)](https://nextjs.org/)
[![Status](https://img.shields.io/badge/Status-Empirically%20Validated-blue?style=for-the-badge)](#empirical-validation-engine)

**ARICCA-X** (Academic Research Integrity & Credibility Correlation Analyzer) is a comprehensive, multi-signal platform designed to protect universities, publishers, and funding agencies from academic fraud.

While the industry rushes toward black-box Machine Learning (which is legally difficult to patent and prone to hallucination), ARICCA-X takes a radically different approach: **A 100% deterministic, mathematically verifiable, and fully patentable pipeline.**

---

## 🏛️ Architecture & Patent Strategy (The "Alice" Advantage)

Under US Patent Law (35 U.S.C. § 101 - *Alice Corp. v. CLS Bank*), generic software or "abstract ideas on a computer" cannot be patented. To survive this, ARICCA-X strictly separates its architecture:

1. **The Core Pipeline (On-Chain):** Uses deterministic algorithms (Bounded DFS graph traversal, strict linguistic formulas, hardcoded rule engines). Because it uses explicit, unconventional mathematical methods rather than a black-box LLM, it is highly patentable.
2. **The ML Sandbox (Off-Chain):** Machine Learning models are used *only* for off-chain research and validation (`ml_verification.py`). Knowledge gained here is manually translated into deterministic rules for the core pipeline.

---

## 🧩 The 4 Core Modules

ARICCA-X v2.0 expands from a single predatory-journal detector into a full enterprise suite governed by **14 distinct patent claims**.

### Module A: Venue Intelligence (Claims 1-5)
Evaluates the credibility of academic conferences and journals.
* **Heuristics:** Evaluates CFP timelines, URL anomalies, and sponsor inconsistencies.
* **Tense Shift Analysis:** Uses rule-based NLP to detect plagiarized or spun conference descriptions.
* **Evolution Tracking:** Computes Levenshtein distance across years to detect hijacked conferences.

### Module B: Researcher Auditing (Claims 6-8)
Detects citation cartels and h-index inflation.
* **Citation Ring Detection:** Executes Bounded Depth-First Search (DFS) on citation graphs to unearth hidden reciprocal citation rings (cartels).
* **Citation Concentration Ratio (CCR):** Mathematically isolates suspicious temporal citation bursts.
* **H-Index Decomposition:** Strips away self-citations and co-author citations to reveal a researcher's "True" Independent H-Index.

### Module C: Peer-Review Forensics (Claims 9-11)
Detects AI-generated peer reviews and sentiment misalignment without relying on LLMs.
* **Linguistic Fingerprinting:** Calculates precise Hedging Density, Specificity Ratio, and Sentence Length Coefficient of Variation (CV).
* **Misalignment Detection:** Maps reviewer sentiment polarity against the final decision (Accept/Reject) to flag conflicting peer reviews.

### Module D: Grant Compliance (Claims 12-13)
Automates funding agency mandate verification.
* **Rule Engine:** Contains structured, machine-readable mandates for Plan S, NIH, NSF, and UKRI.
* **Verification:** Checks embargo periods, OA types (Gold/Green), licensing (CC-BY), and repository deposits to generate auditable compliance reports.

---

## 🧪 Empirical Validation Engine

A patent requires "Reduction to Practice." To prove the mathematical integrity of the system, ARICCA-X includes a massive-scale fuzzer (`empirical_evidence_generator.js`).

**Results from 11,500 fuzzed inputs:**
* **Citation Graphs (1,000):** 0% false negatives in detecting injected citation rings amidst dense network noise.
* **H-Index Portfolios (10,000):** 0 math boundary violations. The decomposed H-index never hallucinated.
* **NLP Extreme Edges (500):** Handled 5,000-word blocks without NaN, zero-division, or memory overflow errors.

---

## 🚀 Getting Started

### Running the Web Application
The ARICCA-X portal is built with Next.js and React.

```bash
cd portal
npm install
npm run dev
```
Navigate to `http://localhost:3000`. Login with:
* **Email:** admin@aricca.com
* **Password:** admin123

### Running the Empirical Tests
To verify the determinism of the algorithms yourself:

```bash
# Run the specific unit tests
node integrity_test.js

# Run the 11,500-input stress test
node empirical_evidence_generator.js
```

### Exploring the ML Sandbox
To conduct experimental machine learning research (kept strictly off-chain):

```bash
python ml_verification.py
```

---
*© 2026 Panchadip B & Somyajeet A. All Rights Reserved. Patent Pending.*
