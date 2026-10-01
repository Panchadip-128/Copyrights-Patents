# PATENT SPECIFICATION
**Title of Invention:** SYSTEM AND METHOD FOR DETERMINISTIC, NON-ML ACADEMIC VENUE CREDIBILITY ASSESSMENT VIA ADAPTIVE DECAY WEIGHTING AND TEMPORAL FINGERPRINT EVOLUTION

**Inventors:** Panchadip B., Somyajeet A.
**Date:** October 2026
**Status:** Patent Pending

---

## 1. FIELD OF THE INVENTION
The present invention relates generally to computational assessment systems, and more particularly to a deterministic, non-machine-learning-based system and method for evaluating the credibility, integrity, and compliance of academic publication venues using adaptive weight redistribution, cross-signal anomaly detection, and temporal fingerprint evolution tracking.

## 2. BACKGROUND OF THE INVENTION
The proliferation of academic publication venues has led to a significant increase in "predatory" or deceptive publishers that exploit the open-access model for financial gain while lacking rigorous peer review. Existing methods for detecting such venues typically rely on one of two paradigms:
1. Static blacklists or whitelists (e.g., Beall's List), which are subjective, manually maintained, and rapidly become obsolete as venues change names or structures.
2. Machine Learning (ML) classification systems, which rely on black-box neural networks. These ML systems suffer from algorithmic opacity, are highly susceptible to adversarial evasion (where deceptive venues modify text slightly to bypass classifiers), and cannot provide the deterministic, auditable evidence required by institutional compliance boards.

Therefore, there is a need in the art for a computational system that can dynamically assess venue credibility using transparent, reproducible, and deterministic logic without relying on opaque ML models. Furthermore, there is a need for a system capable of detecting sophisticated deceptive practices, such as contradictory claims across different data modalities (e.g., website claims vs. indexing metadata) and deceptive grammatical framing of indexing statuses.

## 3. SUMMARY OF THE INVENTION
The present invention (embodied in the ARICCA-X system) overcomes the limitations of the prior art by providing a deterministic, multi-phase computational pipeline. The system introduces several novel technical methodologies:
- **Adaptive Decay Weighting (ADW):** A mechanism that dynamically redistributes the scoring weights of missing data dimensions to available dimensions, preventing deceptive venues from artificially inflating their scores by hiding information.
- **Cross-Signal Anomaly Detection (CSAD):** A computational method for calculating the divergence between independent evaluation vectors (e.g., Call for Papers risk vs. Infrastructure quality) and applying a mathematically defined risk amplification penalty when divergence exceeds a predefined threshold.
- **Grammatical Tense Analysis (GTA):** A linguistic processing engine that eschews standard keyword matching in favor of temporal framing classification, computationally distinguishing between legitimate present-tense indexing claims (e.g., "is indexed in") and deceptive future/conditional claims (e.g., "will be indexed in").
- **Temporal Fingerprint Evolution Tracking (TFET):** A method for acquiring and comparing multi-dimensional venue metadata snapshots at different time intervals ($T_1$ and $T_2$) to calculate a quantitative aggregate drift vector, thereby identifying structural mutations indicative of predatory behavior.

## 4. DETAILED DESCRIPTION OF THE PREFERRED EMBODIMENTS

### 4.1 System Architecture
The system executes a strictly deterministic, six-phase pipeline:
1. **Component Analysis:** Independent scoring of structural dimensions (CFP, Website, Indexing, Contact).
2. **Heuristic Evaluation:** Boolean logic gates assessing critical thresholds (e.g., acceptance rate guarantees).
3. **Credibility Calculation:** Integration of Component and Heuristic scores via Adaptive Decay Weighting and Cross-Signal Anomaly Detection.
4. **Risk Classification:** Mapping of continuous credibility scores to discrete risk tiers.
5. **Recommendation Generation:** Rule-based generation of actionable compliance steps.
6. **Flagging:** Generation of auditable exception alerts based on dimensional failures.

### 4.2 UI and Demonstrability
The system is coupled with a web-based testing apparatus (`aricca_x_ui.html`) that allows human operators and patent examiners to visually step through the deterministic logic. The UI provides real-time visualization of the Adaptive Decay Weighting redistributions and renders the calculated divergences in the Cross-Signal Anomaly Detection engine.

## 5. CLAIMS

What is claimed is:

**1. A computational method for deterministic evaluation of digital venues, comprising:**
- receiving multi-dimensional input data associated with an academic venue;
- calculating independent credibility scores for each dimension;
- detecting the absence of data in one or more dimensions;
- executing an Adaptive Decay Weighting (ADW) algorithm to proportionally redistribute the predetermined weights of the absent dimensions to the available dimensions; and
- calculating an aggregate score using the dynamically redistributed weights, thereby preventing false-neutral baseline scores resulting from omitted data.

**2. A system for detecting contradictory digital assertions via Cross-Signal Anomaly Detection (CSAD), comprising:**
- a scoring engine configured to map disparate data signals into normalized vectors;
- a comparator module that calculates the mathematical divergence between pairs of independent vectors (e.g., infrastructure credibility vs. indexing claims); and
- a penalty application module that automatically applies a proportional risk amplification coefficient to a final assessment score if the calculated divergence exceeds a predefined threshold, without utilizing machine learning classifiers.

**3. A method for algorithmic verification of deceptive indexing claims via Grammatical Tense Analysis (GTA), comprising:**
- extracting statements referencing academic indexing databases;
- applying regex-based linguistic parsing to classify the temporal intent of the statement into discrete categories including at least: present, past, future, and conditional;
- assigning specific risk penalties based on the temporal classification, wherein future and conditional classifications receive higher penalty weightings than present and past classifications; and
- aggregating said penalties into a deterministic risk score.

**4. A method for quantifying longitudinal venue degradation via Temporal Fingerprint Evolution Tracking (TFET), comprising:**
- acquiring a first multi-dimensional structural fingerprint of a digital venue at time $T_1$;
- acquiring a second multi-dimensional structural fingerprint of said venue at time $T_2$;
- calculating a multi-dimensional drift vector representing the quantitative difference between $T_1$ and $T_2$ fingerprints; and
- triggering an anomalous mutation alert if the calculated drift vector exceeds an operational stability threshold.

**5. A deterministic, non-machine-learning computational pipeline for generating auditable compliance reports, configured to execute serially:**
- (a) a component scoring phase;
- (b) a boolean heuristic evaluation phase;
- (c) a credibility calculation phase incorporating ADW and CSAD;
- (d) a risk classification phase;
- (e) a rule-based recommendation phase; and
- (f) a flag generation phase;
wherein the state of the data structures at the conclusion of each phase is strictly serializable, thereby generating a mathematically reproducible chain of evidence for institutional auditing.
