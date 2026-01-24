# X-MPFD-E++: Explainable Multimodal Phishing & Fraud Detection and Reasoning Engine

**Copyright © 2026. All Rights Reserved.Panchadip B & Somyajeet A**

## Overview

X-MPFD-E++ is a sophisticated software framework designed to detect phishing and online fraud by systematically processing heterogeneous digital signals, applying configurable fusion logic, and generating human-interpretable decision rationales.

The software emphasizes **traceability**, **explainability**, and **reproducibility**, making it suitable for security research, compliance auditing, and enterprise deployment.

## Core Design Philosophy

The framework is built on five non-trivial principles:

1. **Multimodality as a software orchestration problem**, not a model problem
2. **Feature provenance as a first-class software artifact**
3. **Fusion policies expressed as executable logic**
4. **Explainability synthesized into structured narratives**
5. **Separation of detection, reasoning, and explanation layers**

This separation itself is copyrightable expression.

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│              X-MPFD-E++ Framework                       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Input → Orchestrator → Features → Fusion → Decision   │
│           ↓              ↓          ↓         ↓        │
│      Provenance      Registry   Policies   Explainer   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Architecture Layers

#### A. Input & Signal Acquisition Layer
Handles heterogeneous sources:
- URLs and lexical strings
- Webpage DOM, HTML, CSS, JavaScript
- Rendered webpage screenshots
- Network-level metadata (optional)

Each input is converted into a canonical signal descriptor.

#### B. Multimodal Signal Orchestrator
**This is the heart of originality.**

Responsibilities:
- Signal normalization across modalities
- Temporal alignment (URL ↔ DOM ↔ visual)
- Noise filtering and redundancy elimination
- Signal validity scoring

Output: A unified **Multimodal Signal Tensor (MST)**

#### C. Feature Provenance & Lineage Tracker
Every extracted feature is tagged with:
- Source modality
- Extraction method
- Transformation history
- Confidence score

This enables:
- Traceable decisions
- Post-hoc audits
- Explanation alignment

#### D. Feature Extraction & Representation Layer
- Lexical feature generators
- Structural feature encoders
- Visual pattern extractors
- Statistical and heuristic features

All features are registered into a **Feature Registry**, preventing duplication and leakage.

#### E. Fusion Policy Engine
**Major Copyright Strength**

Instead of hardcoding models, X-MPFD-E++ defines fusion as policy logic:

Supported policies:
- Early fusion
- Late fusion
- Conditional gated fusion
- Confidence-weighted ensemble fusion

Fusion rules are configurable, versioned, and executable, making them literary code.

#### F. Decision & Risk Scoring Core
Applies fusion outputs to classifiers or rule-based evaluators.

Produces:
- Binary decision (legitimate / phishing)
- Risk probability score
- Uncertainty estimate

#### G. Explanation Synthesis Engine
**Deep & Unique**

Produces:
- Feature-aligned explanations
- Modality-wise contribution summaries
- Natural-language rationales
- Decision confidence narratives

Example:
> "The webpage was flagged as phishing primarily due to abnormal URL entropy and deceptive visual similarity to known financial portals."

#### H. Data Leakage, Bias & Integrity Auditor
- Detects train-test contamination
- Flags distributional shift
- Measures feature dominance bias
- Logs integrity warnings

#### I. Inference API & Integration Layer
- REST-based inference endpoints
- Batch and real-time support
- JSON-based explanation outputs
- Logging and trace export

## Module Structure

```
/x_mpfd_e_plus
 ├── input_signal_manager/         # Signal acquisition & preprocessing
 ├── multimodal_orchestrator/      # Signal orchestration & alignment
 ├── feature_registry/             # Centralized feature catalog
 ├── provenance_lineage_tracker/   # Feature lineage tracking
 ├── lexical_feature_engine/       # Text & URL analysis
 ├── structural_feature_engine/    # DOM & HTML analysis
 ├── visual_feature_engine/        # Screenshot & visual analysis
 ├── fusion_policy_engine/         # Configurable fusion logic
 ├── decision_risk_core/           # Classification & risk scoring
 ├── explanation_synthesis_engine/ # Human-readable explanations
 ├── leakage_bias_auditor/         # Integrity validation
 ├── inference_api/                # REST API endpoints
 ├── audit_logger/                 # Comprehensive logging
 └── report_generator/             # Report creation & export
```

## Installation

### Requirements
- Python 3.8+
- Standard library only (core functionality)
- Optional: beautifulsoup4, PIL for enhanced processing

### Setup

```bash
# Clone or extract the software
cd "X-MPFD-E ++"

# No dependencies required for core functionality
python x_mpfd_cli.py --help
```

## Usage

### Command-Line Interface

```bash
# Analyze a URL
python x_mpfd_cli.py analyze-url "https://example.com" --explain

# Analyze webpage HTML
python x_mpfd_cli.py analyze-html webpage.html --visual screenshot.png

# Batch analysis
python x_mpfd_cli.py batch-analyze urls.txt --output results.json

# Run integrity audit
python x_mpfd_cli.py audit-integrity --check-leakage
```

### Python API

```python
from x_mpfd_e_plus import PhishingDetector

# Initialize detector
detector = PhishingDetector(
    fusion_policy='confidence_weighted',
    explain=True
)

# Analyze URL
result = detector.analyze_url('https://suspicious-site.com')

print(f"Risk Score: {result.risk_score:.2%}")
print(f"Decision: {result.decision}")
print(f"Explanation: {result.explanation}")

# Access detailed provenance
for feature in result.features:
    print(f"{feature.name}: {feature.value}")
    print(f"  Source: {feature.provenance.source_modality}")
    print(f"  Confidence: {feature.confidence}")
```

### Fusion Policy Configuration

```python
from x_mpfd_e_plus.fusion_policy_engine import FusionPolicy

# Define custom fusion policy
policy = FusionPolicy(
    name='custom_ensemble',
    strategy='weighted',
    weights={
        'lexical': 0.35,
        'structural': 0.30,
        'visual': 0.35
    },
    threshold=0.65,
    require_consensus=True
)

detector = PhishingDetector(fusion_policy=policy)
```

## Key Features

### 1. Multimodal Signal Processing
- **Lexical Analysis**: URL structure, domain features, text patterns
- **Structural Analysis**: HTML/DOM structure, JavaScript behavior
- **Visual Analysis**: Screenshot-based similarity detection

### 2. Feature Provenance Tracking
Every feature maintains complete lineage:
```json
{
  "feature_id": "url_entropy",
  "value": 3.847,
  "provenance": {
    "source_modality": "lexical",
    "extraction_method": "shannon_entropy",
    "timestamp": "2026-01-02T10:30:00Z",
    "confidence": 0.95
  },
  "lineage": [
    "raw_url",
    "normalized_url", 
    "entropy_calculation"
  ]
}
```

### 3. Configurable Fusion Policies

**Early Fusion:**
```python
policy = FusionPolicy(strategy='early')
# Combines features before classification
```

**Late Fusion:**
```python
policy = FusionPolicy(strategy='late')
# Independent classification, then ensemble
```

**Conditional Gated Fusion:**
```python
policy = FusionPolicy(
    strategy='gated',
    confidence_threshold=0.8
)
# Only fuses high-confidence signals
```

### 4. Explainability

Natural language explanations generated automatically:

```
Detection Result: PHISHING (Risk: 87%)

Primary Indicators:
• URL exhibits abnormal entropy (3.8 vs expected 2.1)
• Domain age: 3 days (newly registered)
• Visual similarity to PayPal login: 94%
• Missing HTTPS certificate
• Suspicious JavaScript: document.write() injection detected

Confidence: HIGH
Recommendation: Block and quarantine
```

### 5. Integrity Auditing

```python
from x_mpfd_e_plus import IntegrityAuditor

auditor = IntegrityAuditor()

# Check for data leakage
audit_report = auditor.check_leakage(
    train_set=train_data,
    test_set=test_data
)

if audit_report.has_leakage:
    print(f"Warning: {audit_report.contamination_rate:.1%} contamination detected")
```

## Algorithms & Logic

### Proprietary Components

1. **Signal Normalization Algorithms**
   - Rule-based signal standardization
   - Temporal alignment logic
   - Noise filtering heuristics

2. **Feature Extraction Logic**
   - URL entropy calculation
   - DOM tree structural metrics
   - Visual perceptual hashing

3. **Fusion Policy Execution**
   - Configurable weighted averaging
   - Confidence gating logic
   - Consensus mechanisms

4. **Explanation Generation**
   - Feature importance ranking
   - Natural language template synthesis
   - Modality contribution attribution

5. **Integrity Validation**
   - Leakage detection algorithms
   - Bias measurement metrics
   - Distributional shift detection

## Technical Specifications

### Input Formats
- URLs: Plain text strings
- HTML: Raw HTML documents
- Screenshots: PNG, JPG (optional)
- Metadata: JSON descriptors

### Output Formats
- JSON: Structured detection results
- Text: Human-readable reports
- CSV: Batch analysis results
- HTML: Detailed audit reports

### Performance Characteristics
- URL analysis: < 100ms
- HTML analysis: < 500ms
- Visual analysis: < 2s (if enabled)
- Batch processing: 1000+ URLs/hour

## Security & Privacy

- No data retention by default
- All processing local (no external calls)
- Audit logs configurable
- GDPR-compliant design

## Legal & Copyright

### Nature of Work
**Computer Software (Source Code and Associated Documentation)**

### Description
X-MPFD-E++ is an explainable multimodal software framework designed to detect phishing and online fraud by orchestrating heterogeneous digital signals, tracking feature provenance and lineage, applying configurable fusion policies, and synthesizing human-interpretable decision explanations. The software includes modular pipelines for signal processing, feature extraction, decision scoring, explainability generation, and integrity auditing.

### Copyright Protection
This software is protected under copyright law as a literary work. The specific expression of algorithms, the selection and arrangement of modules, the proprietary data structures, and the overall architecture constitute original creative works.

Protected elements include:
- Signal orchestration logic
- Feature provenance tracking system
- Fusion policy execution engine
- Explanation synthesis algorithms
- Integrity audit procedures

### License
See [LICENSE.md](LICENSE.md) for complete terms.

## Citation

When referencing this software in academic work:

```
X-MPFD-E++: Explainable Multimodal Phishing & Fraud Detection and Reasoning Engine.
Copyright © 2026. Version 1.0.0.
```

## Support & Contact

For licensing, technical support, or collaboration:
- **Project**: X-MPFD-E++
- **Version**: 1.0.0
- **Copyright**: © 2026. All Rights Reserved.

---

**X-MPFD-E++ - Explainable Multimodal Phishing & Fraud Detection and Reasoning Engine**

*A copyright-protected software framework for security research and enterprise deployment*

**© 2026. All Rights Reserved.**
