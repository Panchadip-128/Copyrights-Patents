# UNITED STATES PATENT AND TRADEMARK OFFICE (USPTO) / PCT SPECIFICATION
## PATENT CLAIMS SPECIFICATION

**INVENTION TITLE:**  
DETERMINISTIC MULTIMODAL FUSION ARCHITECTURE FOR ZERO-DAY PHISHING DETECTION, COMPUTATIONAL HARDWARE OPTIMIZATION, AND CRYPTOGRAPHIC FEATURE PROVENANCE TRACKING

**INVENTORS:**  
Panchadip B, Somyajeet A, Sanvi Sharma, Saloni Ruia, Gururaj H L  

**FILING DATE:**  
October 2026  

---

### WHAT IS CLAIMED IS:

#### Claim 1 (Independent Appliance Hardware Claim)
A network security gateway appliance for high-throughput zero-day phishing detection and packet stream processing, comprising:  
a physical network interface configured to ingest high-velocity network packet streams containing uniform resource locator (URL) data;  
a packet reception ring buffer communicatively coupled to the physical network interface;  
at least one central processing unit (CPU);  
a parser worker thread pool executable on the at least one CPU;  
a deterministic feature extraction layer configured to extract lexical, structural, and transport security feature signals from ingested network payloads;  
a deterministic fusion policy engine configured to synthesize extracted feature signals into a composite security decision; and  
a non-transitory hardware execution memory storing instructions that, when executed by the at least one CPU, cause the appliance to:  
(a) execute an upstream lexical analyzer within said deterministic feature extraction layer in a lightweight memory buffer of computational complexity $O(L)$ with respect to string length $L$ to calculate a closed-form Shannon Entropy value $H(U)$ on an ingested uniform resource locator (URL) string or a structural component thereof prior to downstream thread scheduling;  
(b) evaluate whether $H(U)$ exceeds a critical domain-generation threshold $\tau_{dga}$;  
(c) in response to determining that $H(U) > \tau_{dga}$, emit a physical hardware directive to withhold allocation of worker threads from said parser worker thread pool for HyperText Markup Language (HTML) Abstract Syntax Tree (AST) parsing and Document Object Model (DOM) rendering, immediately tear down a Transmission Control Protocol (TCP) socket receive buffer, and drop the associated network packet at the physical network interface, thereby replacing an $O(N)$ tree parsing operation with an $O(L)$ character frequency evaluation followed by an immediate hardware packet drop;  
(d) in response to determining that $H(U) \le \tau_{dga}$, conditionally allocate worker threads from said parser worker thread pool to construct an HTML AST from an ingested payload via said deterministic feature extraction layer, compute a Structural Density Ratio ($SDR = N_{total} / \max(1, D_{max})$), and calculate an anomaly deviation percentage $\Delta SDR$ against a stored legitimate brand baseline $SDR_{baseline}$;  
(e) evaluate extracted feature signals through said deterministic fusion policy engine to emit an auditable security classification;  
(f) append persistent, machine-readable provenance lineage tags comprising 256-bit cryptographic hash signatures to every feature extracted by said deterministic feature extraction layer; and  
(g) execute an explanation synthesis engine configured to map said persistent provenance lineage tags and evaluated Boolean execution branches into an auditable cryptographic decision token without invoking non-deterministic generative artificial intelligence.

---

#### Claim 2 (Dependent System Claim — Lexical Shannon Entropy Scope)
The appliance of claim 1, wherein the upstream lexical analyzer calculates the Shannon Entropy of an evaluated string according to the closed-form equation:  
$$H(U) = -\sum_{i=1}^{n} P(x_i) \log_2 P(x_i)$$  
where $x_i$ represents an individual character in the evaluated string and $P(x_i)$ represents the empirical frequency probability of character $x_i$, wherein the evaluated string is selectively configured as:  
(i) an entire uniform resource locator (URL) string;  
(ii) a concatenated host and path component excluding query string parameters; or  
(iii) a hostname component thereof;  
wherein algorithmic domain generation (DGA) obfuscation is mathematically isolated in real time without querying external static domain reputation databases or executing neural network character embeddings.

---

#### Claim 3 (Dependent System Claim — Structural AST Parsing & SDR)
The appliance of claim 1, wherein the deterministic feature extraction layer parses a HyperText Markup Language (HTML) document into an Abstract Syntax Tree (AST) using a deterministic tag-stack state machine to calculate:  
(a) a total Document Object Model (DOM) node count $N_{total}$;  
(b) a maximum tree depth $D_{max}$; and  
(c) a Structural Density Ratio ($SDR$) defined by the mathematical expression:  
$$SDR = \frac{N_{total}}{\max(1, D_{max})}$$

---

#### Claim 4 (Dependent System Claim — Baseline SDR Deviation)
The appliance of claim 3, wherein the deterministic feature extraction layer evaluates an anomalous credential-harvesting template by calculating a percentage deviation $\Delta SDR$ against an established legitimate brand baseline $SDR_{baseline}$:  
$$\Delta SDR = \frac{|SDR - SDR_{baseline}|}{SDR_{baseline}} \times 100\%$$  
and generates a structural anomaly flag exclusively if $\Delta SDR$ exceeds a predefined threshold percentage $\tau_{sdr}$ and the AST contains at least one password input element.

---

#### Claim 5 (Dependent System Claim — Late Confidence-Weighted Fusion)
The appliance of claim 1, wherein the deterministic fusion policy engine executes a late confidence-weighted fusion algorithm, applying discrete numerical weights $[w_L, w_S, w_M]$ satisfying $\sum w_i = 1.0$ to independently calculated lexical, structural, and visual sub-scores $[S_L, S_S, S_M]$ to compute a final scalar composite risk score:  
$$Risk_{composite} = (w_L \times S_L) + (w_S \times S_S) + (w_M \times S_M)$$  
wherein a classification of phishing is emitted if $Risk_{composite} \ge \tau_{threshold}$.

---

#### Claim 6 (Dependent System Claim — Conditional Gated Fusion & Compute Bypass)
The appliance of claim 1, wherein the deterministic fusion policy engine executes a conditional gated fusion algorithm comprising a multi-stage Boolean gating matrix that:  
(a) evaluates the calculated lexical Shannon Entropy $H(U)$;  
(b) if $H(U)$ exceeds a critical domain-generation threshold $\tau_{dga}$, immediately terminates classification with a decision of algorithmic phishing and dynamically bypasses execution of downstream HTML AST parsing and visual rendering routines, thereby preserving physical processor cycles and memory bandwidth; and  
(c) if $H(U) \le \tau_{dga}$, conditionally invokes HTML AST structural parsing and evaluates structural density deviation $\Delta SDR$.

---

#### Claim 7 (Dependent System Claim — Cryptographic Provenance Tags)
The appliance of claim 1, wherein each persistent provenance lineage tag comprises:  
(a) an identifier of the source modality selected from the group consisting of lexical, structural, visual, and network;  
(b) a string identifier of the deterministic extraction algorithm utilized;  
(c) an ISO-8601 UTC temporal extraction timestamp;  
(d) an immutable parameter state dictionary serialized with sorted canonical keys; and  
(e) a 256-bit Secure Hash Algorithm (SHA-256) cryptographic digest generated over a deterministic colon-delimited canonical serialization of elements (a) through (d).

---

#### Claim 8 (Dependent System Claim — Explanation Synthesis Engine)
The appliance of claim 1, wherein the explanation synthesis engine parses said persistent provenance lineage tags and deterministic Boolean gate execution paths to populate parameterized linguistic templates, outputting a human-readable legal explanation string explicitly detailing the numerical values, threshold boundaries, and bypassed computational routines without invoking non-deterministic generative artificial intelligence or large language models.

---

#### Claim 9 (Dependent System Claim — Strict Determinism & Cross-Architecture Invariance)
The appliance of claim 1, wherein the core inference and fusion pipelines strictly exclude non-deterministic generative neural networks and black-box machine learning weights, and apply discrete numerical quantization to intermediate scores, ensuring identical input bitstreams produce bit-exact identical classification outputs and identical SHA-256 audit hashes across disparate runtime environments and processor architectures.

---

#### Claim 10 (Independent Medium Claim)
A non-transitory computer-readable storage medium having recorded thereon computer-executable instructions that, when executed by one or more processors, cause the one or more processors to execute operations comprising:  
(a) executing an $O(L)$ character-frequency scan on an ingested uniform resource locator (URL) string or a structural component thereof of length $L$ to calculate a Shannon Entropy metric $H(U)$;  
(b) comparing $H(U)$ against a predefined mathematical threshold $\tau_{dga}$;  
(c) if $H(U) > \tau_{dga}$, classifying the URL as algorithmically obfuscated and bypassing downstream HTML document parsing;  
(d) if $H(U) \le \tau_{dga}$, parsing an associated HTML document into an Abstract Syntax Tree to compute a Structural Density Ratio ($SDR = N_{total} / D_{max}$); and  
(e) evaluating said calculated metrics through a deterministic Boolean gating matrix to produce an auditable classification output.

---

#### Claim 11 (Dependent Medium Claim — Multimodal Signal Tensor Construction)
The medium of claim 10, wherein the operations further comprise normalizing disparate lexical, structural, and visual signals into a unified Multimodal Signal Tensor (MST) comprising discrete vector fields $[V_L, V_S, V_M]$ with verified channel completeness scoring.

---

#### Claim 12 (Dependent Medium Claim — Early Fusion Matrix Algebra)
The medium of claim 10, wherein the operations further comprise executing an early fusion matrix projection by mapping a continuous normalized feature vector derived from $H(U)$ and $SDR$ through a projection weight vector to compute a scalar risk metric prior to threshold boundary evaluation.

---

#### Claim 13 (Dependent Medium Claim — Deterministic Visual/TLS Geometry)
The medium of claim 10, wherein the operations further comprise evaluating visual and transport security metadata by verifying Transport Layer Security (TLS) certificate authority trust, self-signed flag states, and form-action destination host alignment without executing convolutional neural network image classification models.

---

#### Claim 14 (Dependent Medium Claim — Canonical JSON Evidence Schema)
The medium of claim 10, wherein the operations further comprise generating a tamper-evident audit report conforming to a canonical JavaScript Object Notation (JSON) schema, comprising the classification decision, scalar risk score, list of bypassed computational routines, cryptographic feature provenance dictionary, and a SHA-256 block hash.

---

#### Claim 15 (Independent Method Claim — Hardware Optimization in Security Appliances)
A computer-implemented method for hardware optimization and execution cycle preservation in network security appliances, comprising:  
(a) receiving an incoming network packet containing an alphanumeric uniform resource locator (URL);  
(b) executing an $O(L)$ character-frequency extraction on the URL or a structural component thereof of length $L$ in a first memory buffer to calculate a Shannon Entropy value $H(U)$;  
(c) determining whether $H(U)$ satisfies an upstream hardware bypass condition $H(U) > \tau_{dga}$;  
(d) in response to satisfying the hardware bypass condition, immediately generating an appliance block instruction and dynamically withholding allocation of hardware threads for HyperText Markup Language (HTML) Abstract Syntax Tree (AST) parsing and Document Object Model (DOM) rendering, thereby replacing an $O(N)$ tree parsing operation with an $O(L)$ character-frequency evaluation and an immediate hardware packet drop; and  
(e) in response to failing to satisfy the hardware bypass condition, allocating hardware threads to parse downstream HTML payloads and compute structural density deviation metrics.

---
*END OF FORMAL PATENT CLAIMS SPECIFICATION*
