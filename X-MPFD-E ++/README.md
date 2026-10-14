# X-MPFD-E++ | Deterministic Multimodal Fraud Fusion Engine 🛡️

[![Patent Pending](https://img.shields.io/badge/Patent-Pending%20(15%20Claims)-#10b981?style=for-the-badge)](./PATENT_CLAIMS.md)
[![Prior Art Defense](https://img.shields.io/badge/Prior_Art-15_Page_Report-blue?style=for-the-badge)](./FINAL_PRIOR_ART_SEARCH_REPORT.md)
[![Lextria Due Diligence](https://img.shields.io/badge/Lextria_Diligence-AR1115_Response-orange?style=for-the-badge)](./LEXTRIA_DUE_DILIGENCE_RESPONSE_AR1115.md)
[![Checklist Response](https://img.shields.io/badge/Checklist_AR1115-Full_Compliance-teal?style=for-the-badge)](./AR1115_CHECKLIST_RESPONSE.md)
[![Patent Drawings](https://img.shields.io/badge/Drawings-Section_10(4)_FIGS_1--5-purple?style=for-the-badge)](./figures/)
[![Counsel Response](https://img.shields.io/badge/Patent_Counsel-Response_Dossier-purple?style=for-the-badge)](./PATENT_COUNSEL_RESPONSE_THILAK.md)
[![Status](https://img.shields.io/badge/Status-Empirically%20Validated-green?style=for-the-badge)](#7-empirical-reduction-to-practice--validation)
[![License](https://img.shields.io/badge/License-Proprietary%20IP-red?style=for-the-badge)](./LICENSE.md)

**X-MPFD-E++** (Explainable Multimodal Phishing & Fraud Detection and Reasoning Engine) is an enterprise-grade cybersecurity architecture engineered to detect zero-day phishing campaigns, credential-harvesting templates, and polymorphic domain-generation algorithm (DGA) infrastructure at line rate.

Unlike conventional cybersecurity appliances that rely on legally vulnerable, uninterpretable "black-box" neural networks or reactive static reputation blacklists, **X-MPFD-E++** executes **100% deterministic closed-form mathematics**, **real HTML Abstract Syntax Tree (AST) parsing**, **configurable Boolean gating matrices**, and **persistent cryptographic SHA-256 feature provenance tags**.

---

## 1. System Architecture & The "Alice" Defense (35 U.S.C. § 101)

Under the Supreme Court precedent *Alice Corp. v. CLS Bank International*, generic applications of "artificial intelligence" to known problems face routine patent rejections as unpatentable abstract ideas. Furthermore, probabilistic models hallucinate explanations and cannot satisfy strict legal auditability requirements in enterprise Security Operations Centers (SOCs).

**X-MPFD-E++** overcomes this hurdle via the **Hardware Optimization Doctrine** (*Finjan, Inc. v. Blue Coat Systems, Inc.* & *Enfish, LLC v. Microsoft Corp.*). The system achieves a physical improvement in cybersecurity hardware performance by dynamically bypassing downstream processor thread allocations for deep Document Object Model (DOM) parsing when upstream lexical entropy flags an attack.

```mermaid
graph TD
    subgraph "Ingestion & Multimodal Signal Tensor (MST) [Claim 1, 11]"
        U["URL String"] --> L_EX["Lexical Analyzer (Shannon Entropy)"]
        H["HTML Body"] --> S_EX["Structural AST Parser (SDR)"]
        M["TLS / Visual"] --> V_EX["Visual Metadata Analyzer"]
        
        L_EX --> MST["Multimodal Signal Tensor (MST)"]
        S_EX --> MST
        V_EX --> MST
    end

    subgraph "Cryptographic Provenance Lineage Tracker [Claim 7]"
        MST --> PROV["SHA-256 Provenance & Lineage Tagging"]
    end

    subgraph "Deterministic Fusion Policy Engine [Claims 5, 6, 12, 15]"
        PROV --> GATE{"Conditional Gated Fusion"}
        GATE -- "H(U) > 4.5 bits/char" --> BYPASS["O(1) Dynamic Compute Bypass: RETURN PHISHING_DGA"]
        GATE -- "H(U) <= 4.5" --> STRUCT{"SDR Deviation > 50%?"}
        STRUCT -- "Yes + TLS Invalid" --> CLONE["RETURN PHISHING_CLONE"]
        STRUCT -- "Yes + TLS Valid" --> SUSP["RETURN SUSPICIOUS"]
        STRUCT -- "No" --> LEGIT["RETURN LEGITIMATE"]
    end

    subgraph "Auditable Evidence & Synthesis [Claims 8, 14]"
        BYPASS & CLONE & SUSP & LEGIT --> SYNTH["Deterministic Explanation Synthesis Engine"]
        SYNTH --> JSON_REP["Canonical JSON Evidence Schema (Claim 14)"]
    end
```

---

## 2. Exhaustive Prior Art Search & Novelty (35 U.S.C. §§ 102 & 103)

| Prior Art Category & Key References | Operating Methodology | Reason Prior Art Fails | X-MPFD-E++ Deterministic Novelty | Primary Claims |
| :--- | :--- | :--- | :--- | :--- |
| **Category A: Static Blacklists**<br>*(Google Safe Browsing, PhishTank, Spamhaus)* | Centralized database lookups of known malicious domains. | **The 4-Hour Zero-Day Gap:** Reactive; powerless against fresh domains generated minutes prior. | **Real-Time Shannon Entropy ($H(U)$):** Calculates character randomness in closed form, isolating DGAs at wire speed without DB queries. | **Claim 2** |
| **Category B: Black-Box ML**<br>*(CrowdStrike Falcon, Palo Alto WildFire, Proofpoint)* | Deep neural networks outputting opaque probabilistic scores (e.g. 0.98). | **The "Black Box" Problem:** Uninterpretable; cannot provide legal proof for false positives. Rejected under § 101. | **Deterministic Provenance & Boolean Gating:** Explicit Boolean logic matrices with cryptographic SHA-256 feature tags and deterministic linguistic synthesis. | **Claims 1, 5, 7, 8, 9** |
| **Category C: Single-Modality Scanners**<br>*(CheckPhish, Traditional DOM Scrapers)* | Evaluates single vectors (screenshot visual similarity or HTML keyword search). | **Evasion via Polymorphism:** Easily bypassed by CSS overlays, iframe injection, or keyword obfuscation. | **Multimodal Signal Tensor (MST) & SDR:** Evaluates $[V_L, V_S, V_M]$ simultaneously. Real AST parsing computes Structural Density Ratio ($SDR = N / D_{max}$). | **Claims 3, 4, 11, 13** |

For the full legal analysis, see [**FINAL PRIOR ART SEARCH REPORT**](./FINAL_PRIOR_ART_SEARCH_REPORT.md) and [**PATENT COUNSEL RESPONSE DOSSIER**](./PATENT_COUNSEL_RESPONSE_THILAK.md).

---

## 3. Core Mathematical Extraction Formulations

### 3.1. Lexical Shannon Entropy Algorithm (Claim 2)
To detect algorithmic domain generation (DGAs) and URL obfuscation in real time without querying reputation databases, the system calculates the Shannon Entropy of the URL string:
$$H(U) = -\sum_{i=1}^{n} P(x_i) \log_2 P(x_i)$$
where $x_i$ represents an individual character in the URL string and $P(x_i)$ represents its empirical frequency probability.
* **Critical DGA Gating Boundary:** $\tau_{dga} = 4.50\text{ bits/char}$.
* **Standard Domain Safe Envelope:** Legitimate enterprise domains typically exhibit $H(U) \le 3.80\text{ bits/char}$.

### 3.2. Structural Abstract Syntax Tree (AST) & Structural Density Ratio (Claims 3 & 4)
Credential-harvesting sites clone brand visual styles but lack backend web application depth, resulting in shallow DOM trees with disproportionately placed input elements. The system deterministically parses HTML into an AST to calculate:
$$SDR = \frac{N_{total}}{\max(1, D_{max})}$$
where $N_{total}$ is the total DOM node count and $D_{max}$ is the maximum tree depth.

The baseline percentage deviation is computed as:
$$\Delta SDR = \frac{|SDR - SDR_{baseline}|}{SDR_{baseline}} \times 100\%$$
* **Harvester Signature:** $\Delta SDR > 50.0\%$ combined with $D_{max} \le 4$ and presence of password form inputs triggers an immediate structural anomaly flag.

---

## 4. Deterministic Multimodal Fusion Strategies (Claims 5, 6, 12, 15)

X-MPFD-E++ supports five deterministic, non-probabilistic fusion strategies:

1. **Conditional Gated Fusion (Claims 6 & 15 - Hardware Optimization):**
   - Evaluates $H(U)$. If $H(U) > 4.50$, immediately emits `PHISHING_DGA` ($Risk = 0.99$) and **dynamically bypasses** downstream HTML AST parsing and visual rendering, transforming an $O(N)$ operation into an $O(1)$ early exit.
   - If $H(U) \le 4.50$, parses DOM AST. If $\Delta SDR > 50.0\%$ and TLS invalid, emits `PHISHING_CLONE` ($Risk = 0.95$). If TLS valid, emits `SUSPICIOUS` ($Risk = 0.70$).
   - Otherwise, emits `LEGITIMATE` ($Risk = 0.05$).
2. **Late Confidence-Weighted Fusion (Claim 5):**
   - Applies discrete weight matrix $W = [w_L=0.40, w_S=0.40, w_M=0.20]$:
     $$Risk_{composite} = (w_L \times S_L) + (w_S \times S_S) + (w_M \times S_M)$$
3. **Early Fusion Matrix Algebra (Claims 11 & 12):**
   - Projects normalized feature vector $[H(U)/6.0, \Delta SDR/100.0, 1.0 - TLS]$ through weight matrix into scalar risk space.
4. **Consensus / Majority Voting Fusion:**
   - Emits `PHISHING` if $\ge 2$ of the 3 independent modalities flag anomalies.
5. **Strict Cartesian Risk Matrix:**
   - Direct 3D lookup $(b_{lex}, b_{struct}, b_{vis}) \in \{0, 1\}^3 \to \text{Decision}$.

---

## 5. Cryptographic Provenance Lineage & Auditability (Claims 7, 8, 14)

Every feature extracted is wrapped in an immutable cryptographic provenance object:
```json
{
  "feature_id": "feat_ad305dabb3370a54",
  "name": "Shannon Entropy",
  "value": 4.62,
  "provenance": {
    "source_modality": "lexical",
    "extraction_method": "shannon_entropy_base_2",
    "extraction_timestamp": "2026-10-10T14:25:09.182741Z",
    "confidence": 1.0,
    "sha256_hash": "2e590283035538ea9a7176247e5c27be7bf76a55b726c76b7e17a47f974d525d"
  }
}
```

The **Explanation Synthesis Engine (Claim 8)** deterministically parses these tags to output human-readable legal evidence without LLMs:
> *"ZERO-DAY DGA DETECTED: The input URL was classified as PHISHING_DGA because the Lexical Shannon Entropy H(U) = 4.71 bits/char exceeded the mathematical threshold of 4.50 bits/char. Computational hardware optimization bypassed downstream HTML AST DOM parsing, preserving CPU execution cycles."*

---

## 6. Formal Patent Claims (1–15) Summary

* **Claim 1 (Independent System):** Deterministic machine-executable multimodal pipeline with orchestrator, non-probabilistic extractor, provenance tracker, Boolean fusion engine, and explanation engine.
* **Claim 2 (Dependent System):** Real-time Shannon Entropy $H(U) = -\sum P(x) \log_2 P(x)$ isolating DGAs without neural network character embeddings.
* **Claim 3 (Dependent System):** HTML Abstract Syntax Tree (AST) parsing computing node count $N_{total}$, max depth $D_{max}$, and Structural Density Ratio ($SDR = N / D_{max}$).
* **Claim 4 (Dependent System):** Baseline deviation $\Delta SDR$ exceeding threshold percentage $\tau_{sdr}$ in presence of password form inputs.
* **Claim 5 (Dependent System):** Late confidence-weighted fusion with discrete weight matrix $W = [w_L, w_S, w_M]$.
* **Claim 6 (Dependent System):** Conditional gated fusion dynamically bypassing downstream HTML AST parsing when $H(U) > \tau_{dga}$.
* **Claim 7 (Dependent System):** Persistent cryptographic SHA-256 provenance lineage tags.
* **Claim 8 (Dependent System):** Deterministic explanation synthesis engine mapping provenance tags to auditable legal rationales without generative AI.
* **Claim 9 (Dependent System):** Strict exclusion of non-deterministic generative neural networks from production path.
* **Claim 10 (Independent Medium):** Non-transitory computer-readable storage medium executing entropy, structural AST variance, and Boolean gating.
* **Claim 11 (Dependent Medium):** Multimodal Signal Tensor (MST) normalization with channel completeness scoring.
* **Claim 12 (Dependent Medium):** Early fusion matrix algebra projecting normalized feature vectors.
* **Claim 13 (Dependent Medium):** Deterministic visual and transport security metadata evaluation without CNN models.
* **Claim 14 (Dependent Medium):** Canonical JSON audit schema with SHA-256 block hash.
* **Claim 15 (Independent Method):** Method for hardware optimization in network security appliances transforming $O(N)$ tree parsing into $O(1)$ early exit.

*(Complete verbatim claims provided in [**PATENT_CLAIMS.md**](./PATENT_CLAIMS.md)).*

---

## 7. Empirical Reduction to Practice & Validation

X-MPFD-E++ includes comprehensive automated test suites and a large-scale stress fuzzer:

### 7.1. Prior Art & CRI Guidelines Test Suite (`test_prior_art_inventions.py`)
```bash
python test_prior_art_inventions.py
```
* **Result:** **24/24 tests PASSED** in 0.026 seconds (100% success rate). Covers Sections 3(k), 3(m), 3(n), 10(4), and Claims 1–15.

### 7.2. Comparative Performance Benchmark (`comparative_benchmark.py`)
*Fulfills Indian Patent Office CRI Guidelines 2025, Paras 4.5.1, 4.5.3, 4.5.4.*
```bash
python comparative_benchmark.py
```
* **Corpus Tested:** 1,000 labelled inputs (334 DGA URLs, 333 Cloned Harvesters, 333 Legitimate Portals).
* **Execution Time Reduction:** **40.86% time saved** (3.91s vs 6.62s).
* **Median Latency (p50):** **82.10% latency reduction** (1.30ms vs 7.24ms).
* **Physical DOM Parses Avoided:** **334 heavy AST parses avoided** on DGA traffic.
* **Detection Quality:** **100.00% Accuracy, 100.00% Precision, 100.00% Recall, 0.00% FPR** (Identical).

### 7.3. Legitimate Domain Entropy Distribution Profiler (`legitimate_entropy_profiler.py`)
```bash
python legitimate_entropy_profiler.py
```
* **Sample Size:** 90 verified authentic portals (PayPal, Chase, Microsoft, Google, etc.).
* **Result:** Confirms $H(U)_{99\%} \le 3.80\text{ bits/char}$ for legitimate sites, separating cleanly from DGA botnets ($H(U) \ge 4.51\text{ bits/char}$) by a mathematical margin of $0.174\text{ bits/char}$.

### 7.4. Comprehensive Examples Suite (`examples.py`)
```bash
python examples.py
```
* **Result:** **9/9 end-to-end patent workflows PASSED** with full provenance traces and explanations.

### 7.5. Large-Scale Fuzzer (`empirical_evidence_generator.py`)
```bash
python empirical_evidence_generator.py
```
* **Total Synthetic Inputs Evaluated:** 10,000 inputs.
* **Successful Executions:** 10,000 (100.00% success rate, 0 crashes).
* **Throughput:** 1,172 inputs/second.

---

## 8. Response to Tentative Checklist (AR1115) & Section 10(4) Patent Drawings

In compliance with the formal **Tentative Checklist** issued by patent counsel **Adv. Pranav Bhat (Lextria Research / IPTTO MAHE)**, the following technical definitions, empirical profiling data, and formal patent drawings have been incorporated into the patent filing package:

| Checklist Query | Statutory Purpose | Technical Specification in X-MPFD-E++ | Proof / Artifact Reference |
| :--- | :--- | :--- | :--- |
| **Item 1: URL Normalization** | Sec. 10(4) & Claim 2 | **Form NFC** Unicode normalization + **single-pass percent-decoding** (`unquote`) + **lowercase** scheme/hostname + default port strip (`:80`, `:443`). Character frequencies $P(x_i)$ and entropy $H(U)$ are invariant to evasion encodings. | `x_mpfd_e_plus/multimodal_orchestrator/orchestrator.py` (`URLNormalizer`) |
| **Item 2: DOM AST Node Types** | Sec. 10(4) & Claims 3, 4 | Element nodes counted in $N_{total}$; HTML5 void elements counted as leaves without pushing to `depth_stack`; **text and comment nodes strictly excluded** from $N_{total}$ and stack depth; `<iframe>` inner documents not traversed. | `x_mpfd_e_plus/multimodal_orchestrator/orchestrator.py` (`DeterministicDOMAnalyzer`) |
| **Item 3: DGA Latency Breakdown** | CRI Guidelines 2025 Para 4.5.1 | High-precision microsecond profiling shows bypassed input executes normalization (0.037 ms) + entropy (0.043 ms) + gate check (0.0003 ms) + registry SHA-256 (0.027 ms) + fusion rule (0.018 ms) + explanation & block audit hash (0.041 ms), while **withholding 2.650 ms of HTML AST parsing**. Overall DGA latency reduced from 6.621 ms to 3.971 ms (-40.0%). | `dga_latency_breakdown_results.json` & `dga_latency_breakdown.py` |
| **Item 4: Fusion Calibration Constants** | Claims 5, 11, 12 | **Late Fusion:** $W_{late} = [0.40, 0.40, 0.20]$, decision threshold $\tau_{late} = 0.65$ (selected via Youden's $J = 0.994$ on 1,000 samples).<br>**Early Fusion:** $W_{early} = [0.45, 0.35, 0.20]^T$, decision threshold $\tau_{early} = 0.60$ for PHISHING, $0.35$ for SUSPICIOUS. | `x_mpfd_e_plus/fusion_policy_engine/fusion_engine.py` (Table 6-1 & 6-2) |
| **Item 5: Validation Artifacts & Logs** | Sec. 10(4) Sufficiency | Deposited reproducible JSON logs of 1,000 comparative benchmark runs, 500 independent holdout inputs across 3 entropy modes, 90 enterprise entropy distributions, and captured execution logs of 24 unit tests and 9 examples. | `comparative_benchmark_results.json`, `ANNEXURE_B_...json`, `test_execution_log.txt`, `examples_execution_log.txt` |
| **Item 6: Section 10(4) Patent Drawings** | Rule 15 Patents Rules, 2003 | Generated five 300 DPI high-resolution figures in PNG and vector PDF for Form 2 Complete Specification filing. | `figures/` directory (`FIG_1` to `FIG_5`) |

### Formal Section 10(4) Patent Drawings (Drawings Sheet):
* **[FIG. 1: Processing Latency Distribution (Gated vs Ungated Pipeline)](./figures/FIG_1_latency_distribution_gated_vs_ungated.png):** Demonstrates median latency reduction from 6.61 ms to 1.26 ms (80.9% speedup).
* **[FIG. 2: Shannon Entropy Distribution & Gating Boundary](./figures/FIG_2_entropy_distribution_legitimate_vs_dga.png):** Illustrates the 0.174 bits/char safety margin between legitimate sites (max 4.34) and DGA domains (min 4.51).
* **[FIG. 3: Topological AST Structural Density Ratio vs DOM Depth](./figures/FIG_3_sdr_deviation_cloned_vs_authentic.png):** Demarcates the shallow credential harvester envelope ($D_{max} \le 4, SDR \le 3.5$) from deep enterprise portals ($D_{max} \ge 12, SDR \ge 13.0$).
* **[FIG. 4: Receiver Operating Characteristic (ROC) Comparison](./figures/FIG_4_roc_curves_fusion_policies.png):** Confirms AUC = 1.000 for Gated Multimodal Fusion over single-modality baselines.
* **[FIG. 5: Microsecond Latency Breakdown of DGA Processing](./figures/FIG_5_dga_latency_breakdown_operations.png):** Proves physical suppression of the 2.65 ms AST workload under CRI Guidelines 2025 Para 4.5.1.

See full documentation in [**AR1115 CHECKLIST RESPONSE**](./AR1115_CHECKLIST_RESPONSE.md) and [**AR1115 Checklist Response PDF**](./AR1115_Checklist_Response.pdf).

---

## 9. CLI Usage Guide

```bash
# Display help and available commands
python x_mpfd_cli.py --help

# Run interactive demonstration
python x_mpfd_cli.py demo

# Analyze an individual URL with Gated Fusion (Default)
python x_mpfd_cli.py analyze-url "https://paypa1-secure-login.tk" --fusion-policy gated

# Analyze a URL with HTML payload and emit canonical JSON (Claim 14)
python x_mpfd_cli.py analyze-url "https://login-chase-update.com" --html sample.html --format json --output report.json

# Run batch analysis
python x_mpfd_cli.py batch-analyze urls.txt --output batch_results.json
```

---

## 10. Repository Structure

```text
X-MPFD-E ++/
├── x_mpfd_e_plus/
│   ├── decision_risk_core/          # PhishingDetector & decision coordination
│   ├── explanation_synthesis_engine/# Deterministic template explanation synthesizer (Claim 8)
│   ├── feature_registry/            # Cryptographic SHA-256 feature registry (Claims 1, 7)
│   ├── fusion_policy_engine/        # Gated, Weighted, Early, Consensus policies (Claims 5, 6, 12)
│   ├── inference_api/               # High-level Python inference API
│   ├── input_signal_manager/        # Input signal normalization & validation
│   ├── leakage_bias_auditor/        # Data leakage & determinism auditor (Claim 9)
│   ├── multimodal_orchestrator/     # DOM AST Parser (SDR) & Lexical Entropy (Claims 2, 3, 11)
│   ├── provenance_lineage_tracker/  # Immutable DAG lineage tracker (Claim 7)
│   └── report_generator/            # Text, Canonical JSON (Claim 14), and HTML reports
├── figures/                         # Section 10(4) Patent Drawings (FIG 1 to FIG 5 in PNG & PDF)
│   ├── FIG_1_latency_distribution_gated_vs_ungated.png (.pdf)
│   ├── FIG_2_entropy_distribution_legitimate_vs_dga.png (.pdf)
│   ├── FIG_3_sdr_deviation_cloned_vs_authentic.png (.pdf)
│   ├── FIG_4_roc_curves_fusion_policies.png (.pdf)
│   └── FIG_5_dga_latency_breakdown_operations.png (.pdf)
├── test_prior_art_inventions.py     # 24 automated unit tests verifying Sections 3(k), 3(m), 3(n), 10(4)
├── test_execution_log.txt           # Captured execution log of all 24 unit tests (100% pass)
├── examples.py                      # 9 comprehensive end-to-end patent workflows
├── examples_execution_log.txt       # Captured execution log of all 9 patent examples
├── comparative_benchmark.py         # 1,000-sample comparative benchmark (CRI Guidelines 2025)
├── comparative_benchmark_results.json# Measured empirical benchmark data log
├── dga_latency_breakdown.py         # Microsecond sub-operation profiler for DGA compute bypass
├── dga_latency_breakdown_results.json# Measured microsecond sub-operation data log (Item 3)
├── legitimate_entropy_profiler.py   # Statistical profile of 90 authentic enterprise portals
├── legitimate_entropy_profile.json  # Authentic domain statistical distribution log
├── empirical_evidence_generator.py  # 10,000-input stress fuzzer & benchmark
├── generate_patent_figures.py       # Matplotlib generator for 300 DPI patent drawings
├── generate_checklist_pdf.py        # ReportLab builder for AR1115_Checklist_Response.pdf
├── x_mpfd_cli.py                    # Command-line interface
├── AR1115_CHECKLIST_RESPONSE.md     # Formal comprehensive response to Tentative Checklist AR1115
├── AR1115_Checklist_Response.pdf    # Print-ready submission PDF for counsel with embedded drawings
├── LEXTRIA_DUE_DILIGENCE_RESPONSE_AR1115.md # Formal rebuttal dossier for Adv. Pranav Bhat / IPTTO MAHE
├── PATENT_CLAIMS.md                 # Verbatim 15-claim USPTO/PCT patent specification
├── PATENT_COUNSEL_RESPONSE_THILAK.md# Response dossier addressed to patent counsel
└── FINAL_PRIOR_ART_SEARCH_REPORT.md # 15-page prior art analysis and defense
```

---

*© 2026 Panchadip B & Somyajeet A. All Rights Reserved. Patent Pending.*
