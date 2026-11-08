# ARICCA-X | Coverage-Gated Submission Admission Control & Deterministic Academic Integrity Suite

[![Status](https://img.shields.io/badge/Tests-8%2F8%20Passing%20(100%25)-10b981?style=for-the-badge)](./test_prior_art_inventions.py)
[![Benchmarks](https://img.shields.io/badge/Benchmarks-100%25%20Hardware%20Verified-blue?style=for-the-badge)](./test_checklist_empirical_benchmarks.py)
[![Determinism](https://img.shields.io/badge/Runtime-Zero%20ML%20%2F%20100%25%20Deterministic-indigo?style=for-the-badge)](./deterministic_core/determinism_guard.py)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%20--%203.14-3776ab?style=for-the-badge&logo=python)](https://python.org)

**ARICCA-X** (*Coverage-Gated Submission Control & Multi-Signal Academic Integrity Correlation System*) is a deterministic, machine-executable network admission and forensic correlation platform that protects publishing gateways, universities, and funding agencies from predatory/hijacked venues, reciprocal citation cartels, synthetic peer-review manipulation, and grant mandate violations.

Unlike subjective editorial checklists or probabilistic machine-learning "black boxes," ARICCA-X intercepts incoming submission payloads **before** allocating downstream parsing/editorial worker threads, evaluates available evidence under a pinned rule registry without substituting fake neutral (`0.50`) placeholders for missing data, enforces an **epistemic coverage gate** ($W > 0.50$), actuates physical session/thread/quarantine state transitions, and seals all phase states into a self-verifying **genesis-bound SHA-256 hash chain**.

---

## Quick Reference Guide (Plain-English Summary of Exact Production Behavior)

This summary is designed so both technical engineers and non-technical reviewers / patent drafters can verify the **exact production rules, parameters, and benchmarks** at a glance without reading source code:

1. **Flexible Multi-Unit Architecture (`>= 2` Active Analysis Units):**
   - The correlation engine operates across **any plurality ($\ge 2$) of active analysis units** selected from four implemented modules: **Venue Intelligence** (base weight `0.30`), **Researcher Auditing** (`0.25`), **Peer-Review Forensics** (`0.25`), and **Grant Compliance** (`0.20`). Missing or unapplicable modules are marked `missing` (`None`) — **never** filled with `0.50` placeholders.
2. **Epistemic Missing-Evidence Interval ($[L, U]$) & Dual Coverage Gate ($W > 0.50$):**
   - Observed weights are proportionally redistributed ($w'_i = w_i / \sum_{k \in A} w_k$), while missing evidence weight forms the **interval width** $W = U - L = \sum_{j \notin A} w_j$.
   - **Coverage Safeguard (`gateway_controller.py`):** Whenever $W > 0.50$, **BOTH `RELEASE` and `REJECT` actions are strictly barred** and overridden to **`HOLD` (Quarantine)**. A payload with $>50\%$ missing evidence can neither slip into the editorial queue nor be unfairly auto-rejected.
3. **Gateway Resource & Session Actuation (`gateway_controller.py`):**
   - Incoming payloads are held **without allocating worker threads** until admission evaluation finishes:
     - **`RELEASE`** ($\text{Risk} < 0.25$ and $W \le 0.50$): Issues an HMAC-SHA256 signed route token, commits to the editorial queue, and allocates worker threads (`4` threads per released payload).
     - **`HOLD`** ($0.25 \le \text{Risk} < 0.75$, or **any** risk when $W > 0.50$): Allocates **`0` worker threads**, locks the transaction state, diverts payload bytes into an isolated quarantine memory buffer, and emits a missing-evidence request list.
     - **`REJECT`** ($\text{Risk} \ge 0.75$ and $W \le 0.50$): Allocates **`0` worker threads**, deletes the client session token from the active proxy session table, emits a connection reset signal (`TCP_RST`), and purges buffered payload bytes.
4. **Directional Surface-vs.-Substrate Facade Amplification (`csad.py` & `rules.py`):**
   - **Surface Layer (manipulable outward signals):** **BOTH `venue` AND `peer_review`** belong to the `SURFACE` layer.
   - **Substrate Layer (historical/statutory record signals):** **`researcher` AND `grant`** belong to the `SUBSTRATE` layer.
   - **Exact Production Constants (`rules.py` L210):** Divergence threshold $\tau = 0.35$; **facade amplification $\alpha_{\text{facade}} = 0.60$** (applied when a `SURFACE` module score exceeds a `SUBSTRATE` module score); **non-facade amplification $\alpha_{\text{neutral}} = 0.20$** otherwise (**3× directional asymmetry**).
5. **Self-Contained Tamper-Evident Audit Chain (`audit_chain.py` & `canonical.py`):**
   - Binds a genesis record $H_0$ (over frozen input snapshot digest + pinned `RuleRegistry` digest) through linear SHA-256 phase links $H_1 \dots H_6$ using deterministic sorted-key, zero-whitespace, ASCII-escaped, 6-decimal-rounded canonical JSON (`canonical.py`).
   - Integrity and deterministic replay (`verify_exported_chain()`) operate **100% standalone/offline** without requiring an external third-party RFC 3161 Time-Stamp Authority (external TSA anchoring is supported purely as an optional deployment extension).
6. **Three Additional Hardware/Algorithmic Safeguards Implemented in Production Code:**
   - **Runtime Determinism Guard (`determinism_guard.py`):** Inspects loaded Python runtime modules (`sys.modules`) prior to execution and aborts with `DeterminismViolation` if any prohibited probabilistic/ML library (`torch`, `tensorflow`, `sklearn`, `transformers`, `xgboost`, `lightgbm`, `catboost`, `jax`, `onnxruntime`, etc.) is resident in memory.
   - **Bounded Canonical Citation-Cycle DFS (`researcher_auditor.py`):** Enumerates simple directed citation cycles of length $2 \le k \le 5$ from each cycle's minimum canonical node under a hard budget $C_{\max} = 10,000$ (setting `loops_truncated = True` if reached), partitioning citations into 4 mutually exclusive classes (`self`, `co-author`, `loop`, `independent`) to compute the **Loop-Purged H-Index ($h_{\text{lp}}$)** and **Loop-Adjusted Citation Independence Ratio ($\text{LACIR} < 0.30$)**.
   - **TFET Compound Hijack Detector (`venue_intelligence.py`):** Distinguishes general longitudinal drift ($\|\Delta \mathbf{F}\|_W > 0.25$) from **domain/journal hijacking**, raising `hijack_suspected = True` only on the compound condition: **domain ownership change AND (`cfp_signature` hash change OR `indexing_claims` shift $> 0.50$)**.

---

## 1. End-to-End Coverage-Gated System Architecture

```mermaid
flowchart TD
    Client["Client Device (Payload + Session Token)"] --> GW["Submission Gateway Ingress (Hold Payload, 0 Worker Threads)"]
    GW --> Snap["Frozen Evidence Snapshot (Unavailable Records Marked Missing)"]
    Rules["Pinned RuleRegistry (Sealed Parameters + SHA-256 Digest)"] --> Guard["Runtime Determinism Guard (Blocks ML Libraries in Memory)"]
    Snap --> Guard
    Guard --> M1["Venue Intelligence (Surface Layer, w=0.30)"]
    Guard --> M2["Peer-Review Forensics (Surface Layer, w=0.25)"]
    Guard --> M3["Researcher Auditing (Substrate Layer, w=0.25)"]
    Guard --> M4["Grant Compliance (Substrate Layer, w=0.20)"]
    M1 & M2 & M3 & M4 --> ADW["Phase 1: Observed-Set Weighting (ADW) & Epistemic Interval [L, U], Width W"]
    ADW --> Heur["Phase 2: Boolean Domain Heuristic Penalties"]
    Heur --> CSAD["Phase 3: Asymmetric CSAD Amplification (alpha_facade=0.60 vs alpha_neutral=0.20)"]
    CSAD --> Tier["Phase 4-5: Risk Tier (<0.25, [0.25,0.75), >=0.75) & Remediation Flags"]
    Tier --> Gate{"Coverage Safeguard: Is Interval Width W > 0.50?"}
    Gate -- "Yes (Bar RELEASE & REJECT)" --> Hold["HOLD: 0 Worker Threads + Quarantine Buffer + Missing-Evidence Request"]
    Gate -- "No (Sufficient Coverage)" --> Act{"Risk Class"}
    Act -- "< 0.25" --> Rel["RELEASE: Issue Signed HMAC Route Token + Allocate Worker Threads"]
    Act -- "0.25 to < 0.75" --> Hold
    Act -- ">= 0.75" --> Rej["REJECT: 0 Worker Threads + Delete Session Token + TCP_RST + Purge Buffer"]
    Rel & Hold & Rej --> Chain["Phase 6: Genesis-Bound SHA-256 Audit Chain (H_0 -> H_6) + Replay Verifier"]
```

---

## 2. Exact Production Formulas & Sealed Registry Parameters (`deterministic_core/rules.py`)

Every parameter below is cryptographically sealed in `DEFAULT_REGISTRY` ([`deterministic_core/rules.py`](./deterministic_core/rules.py)) and bound into the genesis hash $H_0$:

### 2.1. Observed-Set Weighting (ADW) & Epistemic Bounds (`deterministic_core/adw.py`)
Given active modules $K$ with normalized base weights $\sum_{k \in K} w_k = 1$ (`venue=0.30`, `researcher=0.25`, `peer_review=0.25`, `grant=0.20`) and observed subset $A = \{k \in K \mid s_k \text{ is available}\}$:
- **Observed Coverage:** $C_{\text{obs}} = \sum_{k \in A} w_k$.
  - If $C_{\text{obs}} = 0$ (no modules available): combined score is `None` (`unknown`) and interval width $W = 1.0$.
  - If $C_{\text{obs}} > 0$: redistributed weights $w'_i = \frac{w_i}{C_{\text{obs}}}$ for $i \in A$ ($w'_j = 0$ for $j \notin A$), and combined score $S = \sum_{i \in A} w'_i s_i$.
- **Closed-Form Epistemic Interval $[L, U]$:**
  $$L = \sum_{i \in A} w_i s_i, \qquad W = \sum_{j \notin A} w_j = 1 - C_{\text{obs}}, \qquad U = L + W$$
  Because every missing score lies in $[0, 1]$, the true full-information composite score $s_{\text{true}}$ is **mathematically guaranteed** to satisfy $s_{\text{true}} \in [L, U]$ (`100.00%` containment, `0.0000` out-of-bounds error). When $W > 0.50$, `ADW_INSUFFICIENT_EVIDENCE` is raised and the gateway bars both `RELEASE` and `REJECT`.

### 2.2. Cross-Signal Anomaly Detection (CSAD) (`deterministic_core/csad.py`)
- **Layer Partition (`cross_correlation_engine.py` L221–226):**
  - `SURFACE = {"venue", "peer_review"}`
  - `SUBSTRATE = {"researcher", "grant"}`
- **Base & Penalized Risk:** $\text{Risk}_0 = 1 - S$; Boolean heuristic penalties add `+0.15` (critical), `+0.08` (high), `+0.04` (medium), `+0.02` (low), capped at `1.0` to form $\text{Risk}_1$.
- **Pairwise Excess Divergence ($\tau = 0.35$):** For every observed pair $(i, j)$ with $D_{ij} = |s_i - s_j| > \tau$:
  $$g(D_{ij}, \tau) = \frac{D_{ij} - \tau}{1 - \tau}$$
- **Directional Amplification Factor:**
  $$\alpha_{ij} = \begin{cases} 0.60 \; (\alpha_{\text{facade}}) & \text{if one module is in SURFACE, the other is in SUBSTRATE, and } s_{\text{surface}} > s_{\text{substrate}} \\ 0.20 \; (\alpha_{\text{neutral}}) & \text{otherwise} \end{cases}$$
- **Amplified Risk:** Using $\gamma^* = \max_{i < j} \alpha_{ij} \cdot g(D_{ij}, \tau)$:
  $$\text{Risk}_2 = \min\!\left(1.0,\; \text{Risk}_1 \times (1 + \gamma^*)\right)$$

### 2.3. Venue Intelligence (`venue_intelligence/venue_intelligence.py`)
- **13 Authenticated Publisher Domains:** `ieee.org`, `acm.org`, `springer.com`, `elsevier.com`, `nature.com`, `wiley.com`, `sciencedirect.com`, `cell.com`, `pnas.org`, `plos.org`, `biorxiv.org`, `medrxiv.org`, `arxiv.org`.
- **Stem-Scaled Levenshtein Typosquat Detection (`VI-SPOOF`):** Flags `TYPOSQUAT` (`score = 0.0`) when $1 \le D_{\text{Lev}}(\text{candidate}, \text{registry\_stem}) \le \max(1, \lfloor 0.20 \times \text{len}(\text{registry\_stem}) \rfloor)$ (edit distance `1` to `2` depending on stem length). Brand-substring embedding on unauthorized domains receives `score = 0.10`; unrelated domains receive `0.70`; verified registries receive `1.00`.
- **CFP Announcement-to-Deadline Schedule Score (`VI-URGENCY`):** For $\Delta t = t_{\text{deadline}} - t_{\text{announce}}$ (in days):
  - $\Delta t \le 0$: `0.00` (inverted/impossible dates)
  - $0 < \Delta t < 14$: `0.05` (`PREDATORY_URGENCY` flagged for all $0 \le \Delta t < 30$)
  - $14 \le \Delta t < 30$: `0.20` (`PREDATORY_URGENCY` flagged)
  - $\Delta t \ge 30$: linear ramp from `0.50` at 30 days to `1.00` at 90+ days: $\min\!\left(1.0,\; 0.5 + \min\!\left(0.5, \frac{\Delta t - 30}{60}\right)\right)$.
- **Grammatical Tense Analysis (`GTA-WEIGHTS`):** Conditional `+0.30`, Future `+0.25`, Unknown `+0.05`, Present `0.00`, Past `-0.05` (corroborated bonus); website future/conditional location penalty `+0.10`; same-indexer tense contradiction `+0.20`; anachronistic `"since YYYY"` ($Y > Y_{\text{current}}$) `+0.30`.
- **Temporal Fingerprint Evolution Tracking (`TFET`):** 7 weighted dimensions (`cfp_risk=0.15`, `website_depth=0.10`, `structural_completeness=0.10`, `indexing_claims=0.25`, `cfp_signature=0.10`, `organizer_continuity=0.15`, `ownership=0.15`). Raises `stability_alert` when $\|\Delta \mathbf{F}\|_W > 0.25$, and raises `hijack_suspected` iff `d_domain > 0 and (d_sig > 0 or d_claims > 0.50)`.

### 2.4. Researcher Auditing (`researcher_auditor/researcher_auditor.py`)
- **Bounded Canonical DFS (`RA-DFS`):** Enumerates simple directed author cycles of length $2 \le k \le 5$ starting only from each cycle's lexicographically smallest node, capped at $C_{\max} = 10,000$ cycles (`loops_truncated = True` if reached).
- **4-Way Citation Partition & Loop-Purged H-Index:** Partitions incoming citations into mutually exclusive `SELF`, `COAUTHOR`, `LOOP`, and `INDEPENDENT` sets. Computes Standard H-index ($h$), True Independent H-index ($h_{\text{tih}}$), Loop-Purged H-index ($h_{\text{lp}}$ over `INDEPENDENT` only), $\text{CIR} = (C_{\text{ind}} + C_{\text{loop}}) / C_{\text{total}}$, and $\text{LACIR} = C_{\text{ind}} / C_{\text{total}}$ (alerting when $\text{CIR} < 0.30$ or $\text{LACIR} < 0.30$).

### 2.5. Peer-Review Forensics (`peer_review_forensics/peer_review_forensics.py`)
- **Sentence-Length Uniformity (`PR-UNIFORMITY`):** Evaluates population $\text{CV} = \sigma / \mu$ when sentence count $\ge 3$; flags synthetic uniformity when $\text{CV} < 0.20$.
- **Academic Hedging Lexicon (`PR-HEDGING`):** 29 closed-set phrases; $\text{Density} = 100 \times \text{matches} / \text{words}$ (flags $> 4.0$, with warning tier above `2.0`).
- **Manuscript-Element Specificity (`PR-SPECIFICITY`):** 9 compiled regex patterns (`section`, `figure`, `table`, `equation`, `theorem/lemma`, `algorithm`, `page`, `line`, `citation [n]`); $\text{Specificity} = \text{total\_element\_matches} / \text{sentence\_count}$ (flags $< 0.15$).
- **Dual Asymmetric Sentiment-Decision Misalignment (`PR-MISALIGNMENT`):** 42 polarity tokens (21 positive, 21 negative) with optional 3-word preceding negation inversion (`not`, `never`, `no`, `neither`, `barely`, `hardly`, `scarcely`, `seldom`), $P = (N_{\text{pos}} - N_{\text{neg}}) / (N_{\text{pos}} + N_{\text{neg}})$. Flags misalignment when:
  - Recommendation is **`Reject`** while $P \ge +0.50$, OR
  - Recommendation is **`Accept`** while $P \le -0.30$.

### 2.6. Grant Compliance (`grant_compliance/grant_compliance.py` & `policies/*.json`)
- Deterministic Boolean and three-valued Kleene (`TRUE`, `FALSE`, `UNKNOWN`) mandate evaluation with actionable remediation directives for **NIH**, **NSF**, **Plan S (cOAlition S)**, and **UKRI**, backed by content-hashed versioned JSON policy definitions in [`grant_compliance/policies/`](./grant_compliance/policies/).

---

## 3. Verified Hardware Empirical Benchmarks ("With vs. Without")

All benchmark figures below are directly reproducible from [`comparative_benchmark.py`](./comparative_benchmark.py), [`test_checklist_empirical_benchmarks.py`](./test_checklist_empirical_benchmarks.py), and [`real_world_validation.py`](./real_world_validation.py) (raw logs archived in [`comparative_benchmark_results.json`](./comparative_benchmark_results.json), [`checklist_empirical_results.json`](./checklist_empirical_results.json), and [`real_world_validation_results.json`](./real_world_validation_results.json)).

* **Test Hardware:** 15 W AMD Ryzen 5 7530U / AMD64 Family 25 Model 80 (6 physical cores / 12 threads), 15.31 GB RAM, Windows 11 64-bit, Python 3.14.2. *(Note: Deterministic accuracy, containment, recall, thread-count, and byte-size metrics are 100% seed-invariant; wall-clock microsecond/millisecond latencies come from a single recorded benchmark run on the stated hardware and vary slightly across runs).*

### Table 1 — Observed-Set Weighting (ADW) vs. Neutral `0.50` Placeholder Substitution (`N = 1,000` Trials)
Evaluated across three missing-evidence tiers: **Tier 1** (`1` of `4` modalities missing = `25%`), **Tier 2** (`2` of `4` missing = `50%`), and **Tier 3** (`3` of `4` missing = `75%`):

| Metric | Baseline (Static `0.50` Substitution) | ARICCA-X ADW (`adw.py`, Interval $[L, U]$) | Improvement / Technical Effect |
| :--- | :---: | :---: | :--- |
| **Mean Absolute Error (MAE) vs. Out-of-Bounds Error** | `0.0812` | **`0.0000`** (`[L, U]` out-of-bounds error) | **`100%` elimination** of uncalibrated point-estimate distortion (`dist(s_true, [L, U]) = 0`) |
| **Maximum Point Error Distortion** | `0.2940` | **`0.0000`** (`[L, U]` out-of-bounds error) | Eliminates worst-case `29.4%` scoring error |
| **False Neutral Rate** (Extreme $s_{\text{true}} \le 0.25$ or $\ge 0.75$ masked into `[0.40, 0.60]`) | `2.00%` of all `1,000` trials (`25.97%` of extreme-score cases; `68.18%` at Tier 3) | **`0.00%`** (`0 / 1,000`; explicitly gated by interval width $W$) | **`100%` elimination** of false-neutral masking |
| **Ground-Truth Containment Rate** ($s_{\text{true}} \in [L, U]$) | `0.00%` (Point estimate only; no bounds) | **`100.00%`** (`1,000 / 1,000`) | Provable mathematical enclosure across all `1,000` trials |
| **Mean Uncertainty Width $W = U - L$** | `0.0000` (Unreported; hidden uncertainty) | **`0.4876`** (`0.20–0.30` at Tier 1; `0.70–0.80` at Tier 3) | Quantifies exact missing-evidence mass (`1 - coverage`) |
| **Execution Latency per Input** | `3.57 µs` (`2.47 – 3.57 µs` across runs) | **`36.16 µs`** (`25.60 – 36.16 µs` across runs) | Sub-40 µs deterministic interval calculation |

### Table 2 — Asymmetric CSAD (`0.60 / 0.20`) vs. Simple Weighted Averaging (`N = 1,000` Trials: `500` Facade + `500` Coherent Controls)
| Metric | Baseline (Weighted Average Only) | ARICCA-X Asymmetric CSAD (`csad.py`) | Improvement / Technical Effect |
| :--- | :---: | :---: | :--- |
| **Mean Composite Risk Score on Facade Attacks** | `0.4802` (Misclassified as Moderate Risk) | **`0.6899`** (Correctly Elevated to High/Critical Risk) | **`+0.2097` (`+43.7%`)** risk amplification on facade inputs |
| **Facade Attack False Pass Rate** (`Risk < 0.50` / Low-Moderate) | `78.40%` (`392 / 500` facade attacks missed) | **`0.00%`** (`0 / 500` missed; `100%` elevated to High/Critical) | **`100%` elimination** of missed facade attacks (`392` caught) |
| **Automated Critical Rejection Rate (`Risk >= 0.75`)** | `0.00%` (`0 / 500`) | **`8.60%`** (Immediate critical interdiction; remaining `91.40%` held at High Risk `[0.61, 0.75)`) | Catches severe facade asymmetry that weighted averaging completely misses |
| **False Alarm Rate on Coherent Inputs** (Over-penalization) | `0.00%` | **`0.00%`** (`0 / 500`) | Zero false positives on consistent legitimate submissions |
| **Execution Latency per Evaluation** | `1.00 µs` (`0.53 – 1.00 µs` across runs) | **`55.61 µs`** (`39.03 – 55.61 µs` across runs) | Sub-60 µs deterministic calculation |

*(Note: Under a `Risk >= 0.70` interdiction threshold against extreme facade profiles, Asymmetric CSAD interdicts `473 / 500` (`94.6%`) with mean risk `0.7647` vs. `166 / 500` (`33.2%`) for symmetric $\alpha = 0.20$ and `0 / 500` (`0.0%`) for weighted averaging).*

### Table 3 — Cryptographic SHA-256 Audit Chain Tamper Detection (`N = 3,000` Adversarial Tamper Attempts)
| Attack / Tamper Vector (`1,000` trials each) | Baseline (Standard Unhashed JSON Logs) | ARICCA-X SHA-256 Audit Chain (`audit_chain.py`) | Mean Verification Latency (Specification / Latest JSON Run) | Storage Overhead per 6-Phase Record |
| :--- | :---: | :---: | :---: | :---: |
| **Altered Intermediate Phase State** (Post-hoc score edit) | `0.00%` (`0 / 1,000` detected) | **`100.00%`** (`1,000 / 1,000` detected) | **`166.19 µs`** (`119.11 µs` latest run) | **`2,457.0 bytes`** (`~2.40 KB`) |
| **Deleted Phase Record** (Dropping a failed check phase) | `0.00%` (`0 / 1,000` detected) | **`100.00%`** (`1,000 / 1,000` detected) | **`123.37 µs`** (`126.18 µs` latest run) | Included in `2.40 KB` chain |
| **Reordered Phase Sequence** (Swapping execution order) | `0.00%` (`0 / 1,000` detected) | **`100.00%`** (`1,000 / 1,000` detected) | **`122.41 µs`** (`95.55 µs` latest run) | Included in `2.40 KB` chain |

### Table 4 — Bounded Canonical DFS ($2 \le k \le 5, C_{\max}=10,000$) Across Graph Sizes & Measured Unbounded $K_{12}$ Baseline
| Graph Scale / Cartel Topology | Cycles Enumerated | Execution Time (Specification / Latest JSON Run) | Peak Memory (`tracemalloc`) | Cycle Precision / False-Alert Rate | Injected Ring Recall ($k \in \{2,3,4,5\}$) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **`50` Nodes (`148` edges)** | `11` | **`0.780 ms`** (`0.756 ms` latest run) | **`9.66 KB`** | `36.36%` / `63.64%` | **`100.0%`** (`4 / 4`) |
| **`100` Nodes (`301` edges)** | `9` | **`0.883 ms`** (`0.941 ms` latest run) | **`10.62 KB`** | `44.44%` / `55.56%` | **`100.0%`** (`4 / 4`) |
| **`250` Nodes (`765` edges)** | `9` | **`1.910 ms`** (`1.655 ms` latest run) | **`14.10 KB`** | `44.44%` / `55.56%` | **`100.0%`** (`4 / 4`) |
| **`500` Nodes (`1,486` edges)** | `13` | **`5.822 ms`** (`3.303 ms` latest run) | **`28.48 KB`** | `30.77%` / `69.23%` | **`100.0%`** (`4 / 4`) |
| **`1,000` Nodes (`2,989` edges)** | `9` | **`6.723 ms`** (`6.066 ms` latest run) | **`61.77 KB`** | `44.44%` / `55.56%` | **`100.0%`** (`4 / 4`) |
| **Dense $K_{12}$ (`12` nodes, `132` edges) — ARICCA-X Bounded ($k \le 5, C_{\max}=10,000$)** | **`10,000`** (`truncated=True`) | **`325.26 ms`** | **`6,205.5 KB` (`6.06 MB`)** | Deterministic halt at budget ceiling | Explicit `truncated=True` flag |
| **Dense $K_{12}$ (`12` nodes, `132` edges) — Unbounded DFS (Emergency Cap `100,000`)** | `100,000` (`aborted=True`) | `5,012.96 ms` (`5.01 s`) | `114,851.2 KB` (`112.16 MB`) | **`15.41×` speedup & `94.60%` RAM reduction** | Prevents memory exhaustion |

### Table 5 — Replay Determinism, Compliance Logic, Coverage Safeguard & Gateway Resource Benchmark (`1,000` Submissions: `300 RELEASE`, `400 HOLD`, `300 REJECT`)
| System Invariant / Gateway Benchmark | Sample Size | Baseline (Unprotected / Unbounded Pipeline) | ARICCA-X Measured Result | Technical Effect |
| :--- | :---: | :---: | :---: | :--- |
| **Bit-Exact Replay Verification** | `1,000` replays | Non-deterministic drift across runs | **`1,000 / 1,000` (`100.0%`)** bit-identical (`736.57 – 816.25 µs`) | Zero floating-point or dictionary-order drift |
| **Three-Valued Kleene Compliance Logic** | `1,000` vectors | Binary crash or false pass on `UNKNOWN` | **`1,000 / 1,000` (`100.0%`)** exact truth-table match (`0` exceptions) | Prevents missing metadata from crashing or bypassing compliance |
| **Evidence Coverage Safeguard ($W > 0.50$)** | `250` high-risk sparse inputs | `250 / 250` (`100.0%`) wrongfully auto-rejected | **`0 / 250` (`0.0%`)** wrongfully rejected (**`100.0%` routed to `HOLD`**) | Eliminates false auto-rejection of incomplete submissions |
| **Downstream Worker Thread Allocation** | `1,000` submissions (`4` threads/job) | `4,000` threads (`100.0%` allocated) | **`1,200` threads** (`30.0%` allocated; **`70.0%` thread suppression**) | Prevents thread-pool starvation from `HOLD` (`400`) and `REJECT` (`300`) traffic |
| **Ingress Session Revocation (`TCP_RST`)** | `300` high-confidence `REJECT` inputs | `0` sessions revoked (connections persist) | **`300 / 300` (`100.0%`)** revoked in **`0.28 ms`** (`244.87 – 280.0 µs` across runs) | Sub-millisecond session table severance |

### Table 6 — Dual-Corpus Validation: Real-World Scholarly Entities & Controlled 500/1,000-Trial Threshold Separation
1. **Real-World Scholarly Corpus (`real_world_validation.py` -> [`real_world_validation_results.json`](./real_world_validation_results.json), `18.33 ms`, `100.0%` Accuracy):**
   - **5 Venues (`5/5` = `100.0%`):** Flagship `IEEE_TSE` (`182-day` CFP window, score `0.985`) and `ACM_SIGCOMM` (`139-day` CFP window, score `0.985`) vs. documented predatory venues `WASET` (`17-day` window $< 30\text{d}$, score `0.470`), `OMICS` (`19-day` window $< 30\text{d}$, score `0.495`), and `ieee-conference-2026.org` brand-embedding spoof (`14-day` window, score `0.305`).
   - **4 Peer Reviews (`4/4` = `100.0%`):** 2 authentic OpenReview/ICLR human reviews (`CV = 0.4853, 0.3118`, hedging `0.0%`, specificity `1.1667, 1.0000` -> `AUTHENTIC_HUMAN`) vs. 2 GPT-4/Claude synthetic reviews (`CV = 0.0487, 0.1806`, hedging `6.15%–31.58%`, specificity `0.0000` -> `SUSPICIOUS_OR_SYNTHETIC`).
   - **2 Author Citation Topologies (`2/2` = `100.0%`):** Independent scholar (`LACIR = 85.71%`, `h_lp = 2`) vs. 3-author reciprocal ring (`LACIR = 0.00%` vs deceptive traditional `CIR = 83.33%`, `h = 2 -> h_lp = 0`).
   - **2 Grant Compliance Records (`2/2` = `100.0%`):** Compliant NIH PMC Gold OA (`PMC9876543`, `0` violations) vs. closed 18-month embargo record (`4` violations, `11` remediations).
2. **Reproducible Controlled Threshold Separation & Mathematical Invariant Benchmarks ([`test_checklist_empirical_benchmarks.py`](./test_checklist_empirical_benchmarks.py) -> [`checklist_empirical_results.json`](./checklist_empirical_results.json), `seed=606`):**

| Benchmark Suite | Sample Size | Measured Outcome | Mean Latency |
| :--- | :---: | :--- | :---: |
| **H-Index & LACIR Monotonicity Invariants** ($0 \le h_{\text{lp}} \le h_{\text{tih}} \le h_{\text{std}}$, $\text{LACIR} \le \text{CIR}$) | `1,000` portfolios | **`1,000 / 1,000` (`100.0%` satisfied, `0` violations)** | Sub-ms / portfolio |
| **Controlled Peer-Review Separation + Boundary Stress** (`250` anchored human vs. `250` hedged/uniform/misaligned + up to `5,000`-word edge inputs) | `500 + 3` inputs | **`100.0%` sensitivity (`250/250`), `100.0%` specificity (`250/250`), `0` exceptions** | **`1,058.68 µs`** (`1.06 ms`) |
| **Controlled Venue Separation** (`250` authenticated registry venues $\Delta t \in [45, 180]\text{d}$ vs. `250` spoofed/predatory venues $\Delta t \in [5, 28]\text{d}$) | `500` venues | **`100.0%` legit pass (`250/250`), `100.0%` predatory interdiction (`250/250`)** | **`980.88 µs`** (`0.98 ms`) |

---

## 4. Repository Structure & Quick Verification Commands

```text
aricca_x/
├── deterministic_core/          # Sealed RuleRegistry, ADW, CSAD, Canonical JSON, AuditChain, DeterminismGuard
├── submission_gateway/          # Coverage-Gated Admission Controller (RELEASE / HOLD / REJECT actuation)
├── cross_correlation_engine/    # 6-Phase Serializable Multi-Signal Pipeline
├── venue_intelligence/          # Levenshtein Spoofing, CFP Schedule Ramp, GTA, TFET Hijack Detection
├── researcher_auditor/          # Bounded Canonical DFS (2<=k<=5, C_max=10,000) & Loop-Purged H-Index
├── peer_review_forensics/       # Sentence CV, 29 Hedging Phrases, 9 Specificity Regexes, Dual Sentiment Bounds
├── grant_compliance/            # NIH, NSF, Plan S, UKRI Boolean Evaluators + grant_compliance/policies/*.json
├── portal/                      # Next.js Interactive Dashboard UI
├── test_prior_art_inventions.py # 8 Automated Patent-Claim Verification Suites
├── comparative_benchmark.py     # Hardware Benchmark: ADW, CSAD, Audit Chain ("With vs. Without")
├── test_checklist_empirical_benchmarks.py # Hardware Benchmark: Tamper, DFS, Replay, Coverage Gate, Gateway Threads
└── real_world_validation.py     # Real-World Corpus Validation Suite
```

### Run All Verification & Benchmark Suites
```bash
cd aricca_x
python test_prior_art_inventions.py
python comparative_benchmark.py
python test_checklist_empirical_benchmarks.py
python real_world_validation.py
```

---

## 5. Institutional Affiliation & Notice
**School of Computer Engineering, Manipal Institute of Technology Bengaluru, Manipal Academy of Higher Education (MAHE).**  
Patent Pending. All rights reserved. See [`LICENSE.md`](./LICENSE.md) for evaluation terms.
