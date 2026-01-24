# ARICCA-X Architecture Documentation

**Copyright © 2026. All Rights Reserved.**

## System Overview

ARICCA-X implements a multi-layer reasoning engine using proprietary rule-based algorithms. This document describes the copyright-protected architectural design.

## Core Architecture Principles

### 1. Deterministic Design
- No machine learning components
- Fully reproducible outputs
- Explicit rule-based logic
- Transparent scoring formulas

### 2. Modular Structure
- Seven independent modules
- Well-defined interfaces
- Separation of concerns
- Reusable components

### 3. Copyright-Protected Expression
- Unique algorithm implementations
- Proprietary data structures
- Original scoring formulas
- Custom template designs

## Module Dependencies

```
┌─────────────────────────────────────────────────────────┐
│                    ARICCA-X CLI                         │
└─────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ Credibility  │    │ Compliance   │    │  Citation    │
│    Logic     │    │  Compiler    │    │   Graph      │
│   Engine     │    │              │    │  Analyzer    │
└──────────────┘    └──────────────┘    └──────────────┘
        │                                        │
        ├────────────────────────────────────────┤
        │                                        │
        ▼                                        ▼
┌──────────────┐                        ┌──────────────┐
│   Venue      │                        │     Risk     │
│ Fingerprint  │                        │ Explanation  │
│   Builder    │                        │  Generator   │
└──────────────┘                        └──────────────┘
        │                                        │
        │                                        │
        └────────────┬───────────────────────────┘
                     │
                     ▼
             ┌──────────────┐
             │    Report    │
             │   Renderer   │
             └──────────────┘
                     │
                     ▼
             [Output Files]
```

## Data Flow

### Venue Analysis Pipeline

```
CFP Document → CFP Parser → Syntax Analysis → Pattern Detection
                                                      │
Website URL  → Web Scraper → Structure Analysis →────┤
                                                      │
                                                      ▼
                                            Fingerprint Generator
                                                      │
                                                      ▼
                                            Credibility Engine
                                                      │
                                                      ▼
                                            Risk Assessment
                                                      │
                                                      ▼
                                            Report Generation
```

### Manuscript Analysis Pipeline

```
Manuscript → Parser → Intermediate Representation
                              │
                              ▼
                      Compliance Checker
                              │
                              ├→ Format Rules
                              ├→ Reference Rules
                              ├→ Structure Rules
                              └→ Metadata Rules
                              │
                              ▼
                      Issue Collection
                              │
                              ▼
                      Report Generator
```

## Proprietary Algorithms

### 1. CFP Risk Scoring Formula

```python
# Copyright-protected formula
risk = (
    urgency_score * 0.20 +
    suspicious_count * 0.15 +
    (1 - syntax_score) * 0.10 +
    (1 - professionalism_score) * 0.15 +
    (1 - language_quality) * 0.10 +
    (1 - contact_legitimacy) * 0.15
)
```

**Proprietary Elements**:
- Specific weight values
- Component selection
- Combination methodology

### 2. Credibility Calculation

```python
# Copyright-protected formula
credibility = (
    component_score * 0.60 +
    heuristic_score * 0.40
)

component_score = weighted_sum([
    cfp_credibility * 0.25,
    website_credibility * 0.20,
    indexing_credibility * 0.20,
    contact_legitimacy * 0.15,
    org_structure * 0.10,
    pub_history * 0.10
])
```

**Proprietary Elements**:
- Weight distribution
- Component breakdown
- Aggregation method

### 3. Fingerprint Generation

```python
# Copyright-protected algorithm
fingerprint_hash = SHA256(
    venue_id +
    cfp_signature +
    website_depth +
    indexers_string +
    organizers_string
)

cfp_signature = MD5(
    f"syn:{syntax_score:.2f}|"
    f"pro:{professionalism_score:.2f}|"
    f"urg:{urgency_count}|"
    f"sus:{suspicious_count}"
)
```

**Proprietary Elements**:
- Signature component selection
- Hashing methodology
- Format specification

### 4. Citation Risk Assessment

```python
# Copyright-protected formula
citation_risk = (
    self_citation_penalty +
    pattern_risk +
    clustering_risk +
    diversity_risk
)

# Proprietary thresholds
if self_citation_rate > 0.3:
    self_citation_penalty = 0.3
elif self_citation_rate > 0.2:
    self_citation_penalty = 0.15
```

**Proprietary Elements**:
- Risk component definitions
- Threshold values
- Penalty calculation

## Data Structures

### VenueFingerprint (Proprietary)

```python
@dataclass
class VenueFingerprint:
    venue_id: str
    venue_name: str
    cfp_syntax_signature: str          # Proprietary hash
    cfp_risk_score: float
    website_depth_score: float
    structural_completeness: float
    claimed_indexers: List[str]
    indexing_verification_status: Dict
    organizer_recurrence_score: float  # Proprietary metric
    fingerprint_hash: str              # Unique identifier
    generation_timestamp: datetime
```

### CredibilityAssessment (Proprietary)

```python
@dataclass
class CredibilityAssessment:
    overall_credibility_score: float   # Proprietary calculation
    risk_level: str                    # Proprietary categorization
    score_components: ScoreComponents  # Proprietary breakdown
    heuristic_results: List[HeuristicResult]
    confidence: float
    recommendations: List[str]         # Generated advice
    flags: List[str]                   # Warning indicators
```

### CitationGraph (Proprietary)

```python
@dataclass
class CitationGraph:
    nodes: Set[str]
    edges: List[Tuple[str, str]]
    node_attributes: Dict              # Metadata storage
    edge_attributes: Dict              # Relationship data
    
    # Proprietary methods
    def get_degree(self, node_id: str) -> int
    def get_neighbors(self, node_id: str) -> List[str]
```

## Heuristic Rules

### Proprietary Heuristic Set

1. **Acceptance Rate Check** (Critical)
   - Detects unrealistic acceptance guarantees
   - Pattern matching on suspicious phrases
   - Weight: 0.30 impact

2. **Urgency Indicator Check** (Medium)
   - Counts deadline pressure signals
   - Threshold-based classification
   - Weight: 0.15 impact

3. **Website Quality Check** (High)
   - SSL verification
   - Page completeness
   - Structure depth
   - Weight: 0.20 impact

4. **Indexing Claims Check** (High)
   - Claim extraction
   - Verification status
   - Suspicion scoring
   - Weight: 0.25 impact

5. **Contact Legitimacy Check** (Medium)
   - Email domain analysis
   - Academic affiliation detection
   - Weight: 0.15 impact

6. **Fee Prominence Check** (Medium)
   - Payment emphasis detection
   - Financial risk assessment
   - Weight: 0.10 impact

7. **Publication Speed Check** (Low)
   - Speed claim detection
   - Realistic timeline verification
   - Weight: 0.10 impact

## Report Templates

### Proprietary Template Structure

```
Report Structure (Copyright-protected):
├── Header
│   ├── Title (styled)
│   ├── Subtitle
│   └── Timestamp
├── Executive Summary
│   ├── Venue Name
│   ├── Credibility Score
│   ├── Risk Level
│   └── Risk Statement
├── Credibility Analysis
│   ├── Component Scores
│   ├── Score Visualization
│   └── Breakdown Details
├── Risk Assessment
│   ├── Risk Flags
│   ├── Warning Indicators
│   └── Severity Classification
├── Detailed Findings
│   ├── Heuristic Results
│   ├── Pattern Detection
│   └── Evidence Collection
├── Recommendations
│   ├── Action Items
│   ├── Alternative Venues
│   └── Verification Steps
└── Footer
    ├── System Information
    └── Copyright Notice
```

## Performance Characteristics

### Time Complexity

- **CFP Analysis**: O(n) where n = document length
- **Website Analysis**: O(p) where p = page count
- **Citation Analysis**: O(c²) where c = citation count
- **Fingerprint Generation**: O(1) for hash generation
- **Report Rendering**: O(s) where s = section count

### Space Complexity

- **Venue Fingerprint**: O(1) - fixed structure
- **Assessment Data**: O(h + f) where h = heuristics, f = flags
- **Citation Graph**: O(n + e) where n = nodes, e = edges
- **Report Object**: O(s + c) where s = sections, c = content

## Security Considerations

### Input Validation

- File size limits (100MB)
- Format verification
- Malicious content detection
- Path traversal prevention

### Output Sanitization

- HTML escaping in reports
- SQL injection prevention (if DB added)
- XSS protection in web output
- Path sanitization for files

## Extension Points

While the core algorithms are proprietary, the system provides extension points:

1. **Custom Heuristics**: Add new rule-based checks
2. **Report Formats**: Implement new output formats
3. **Data Sources**: Integrate additional data providers
4. **Style Guides**: Add manuscript compliance rules

## Testing Strategy

### Unit Testing
- Individual algorithm verification
- Component isolation
- Edge case handling
- Input validation

### Integration Testing
- Module interaction
- Data flow verification
- Error propagation
- Output consistency

### Validation Testing
- Algorithm correctness
- Score reproducibility
- Report accuracy
- Performance benchmarks

## Maintenance Guidelines

### Code Organization
- One algorithm per file
- Clear documentation
- Type hints throughout
- Consistent naming

### Version Control
- Copyright headers in all files
- Change documentation
- Algorithm versioning
- Backward compatibility

---

**ARICCA-X Architecture**  
**Copyright © 2026. All Rights Reserved.**

This architecture document describes proprietary designs and implementations protected by copyright law.
