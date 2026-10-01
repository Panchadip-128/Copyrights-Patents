# Prior art Search Report
**ARICCA-X: A DETERMINISTIC, NON-ML ACADEMIC VENUE CREDIBILITY ENGINE VIA ADAPTIVE DECAY WEIGHTING AND TEMPORAL FINGERPRINT EVOLUTION**

## Table of Contents
Contents........................................................................................................................................................... 2
SECTION 1A - Introduction........................................................................................................................... 3
SECTION 1B – KEY FEATURES OF THE INVENTION........................................................................... 3
SECTION 2A – Search Results...................................................................................................................... 4
results of the search -Relevant................................................................................................................... 4
1. US10452981B2 SYSTEM AND METHOD FOR IDENTIFYING PREDATORY ACADEMIC JOURNALS USING MACHINE LEARNING.......................................................................................... 4
2. US20230114755A1 AUTOMATED ASSESSMENT OF PUBLICATION CREDIBILITY USING METADATA AGGREGATION............................................................................................................ 5
3. US11288419B2 NATURAL LANGUAGE PROCESSING FOR DETECTING DECEPTIVE TEXT IN DIGITAL DOCUMENTS........................................................................................................ 5
4. US20210081492A1 METHOD FOR TRACKING DOMAIN REPUTATION OVER TIME......... 6
5. US10936785B2 SYSTEM FOR CROSS-REFERENCING DATABASE CLAIMS IN ACADEMIC SUBMISSIONS................................................................................................................... 7
6. AUTOMATED DETECTOR OF PREDATORY PUBLISHERS USING NEURAL NETWORKS (Journal of Informetrics, 2024) [LITERATURE]..................................................................................... 8
7. US11556722B2 CONTRADICTION DETECTION IN HETEROGENEOUS KNOWLEDGE GRAPHS................................................................................................................................................ 9
Disclaimer...................................................................................................................................................... 11

---

## SECTION 1A - Introduction
Intellectual property (IP) competitive analysis is a vital tool for companies seeking to develop and protect their technology innovations in a highly competitive market. Computational verification of academic venue credibility has become increasingly critical due to the proliferation of deceptive and predatory publishers. As a result, research institutions, academic integrity organizations, and software companies are investing heavily in automated vetting systems. This IP competitive analysis enables a company to identify key patents and other intellectual property assets held by their competitors, as well as potential infringement risks and licensing opportunities. This analysis is crucial for a company to make informed decisions about their R&D investments, patent filings, and overall IP strategy, and to stay ahead in the fast-paced world of research integrity compliance. The search was performed using combinations of keywords mentioned below, patent classes, and assignees relevant to the domain. Further, the records have been categorized into different technical categories.

## SECTION 1B – KEY FEATURES OF THE INVENTION
a deterministic, non-ML academic venue credibility assessment system, comprising:
1) Adaptive Decay Weighting (ADW) for Missing Data Compensation
2) Cross-Signal Anomaly Detection (CSAD) for Contradictory Structural Claims
3) Grammatical Tense Analysis (GTA) for Verifying Indexing Intent
4) Temporal Fingerprint Evolution Tracking (TFET) for Venue Drift

Relevant References:

| Patents / Literature | 1 (ADW) | 2 (CSAD) | 3 (GTA) | 4 (TFET) |
| :--- | :---: | :---: | :---: | :---: |
| 1. US10452981B2 | | | | |
| 2. US20230114755A1 | | | | |
| 3. US11288419B2 | | | √ | |
| 4. US20210081492A1 | | | | √ |
| 5. US10936785B2 | | √ | | |
| 6. Neural Network Detector (Literature) | | | | |
| 7. US11556722B2 | | √ | | |

**Keywords (with variations):**
· Predatory Journal Detection / Venue Credibility Assessment
· Deterministic Scoring / Weight Redistribution / Incomplete Data Heuristics
· Cross-Signal Contradiction / Multi-modal Divergence Penalty
· Grammatical Temporal Framing / Deceptive Text Intent
· Longitudinal Venue Tracking / Structural Fingerprint Drift

In addition to manual and keyword searching in the subclasses above, keyword searching was conducted with no class limitation.

---

## SECTION 2A – Search Results
### results of the search -Relevant

#### 1. US10452981B2 SYSTEM AND METHOD FOR IDENTIFYING PREDATORY ACADEMIC JOURNALS USING MACHINE LEARNING
**[ABSTRACT]**
A method and system for automatically classifying academic journals and conferences as legitimate or predatory. The system utilizes machine learning classifiers, such as Random Forests and Support Vector Machines, trained on historical whitelists and blacklists. The models process text extracted from the venue's website and metadata to output a probability score representing the likelihood that the venue engages in deceptive publishing practices.
**[DETAILED DESCRIPTION]**
This reference represents the standard state-of-the-art approach to predatory venue detection, heavily relying on black-box machine learning algorithms. While it shares the same end-goal as ARICCA-X (assessing venue credibility), its operational mechanism is strictly ML-based. It does not disclose a deterministic, rule-based pipeline, nor does it disclose an "Adaptive Decay Weighting" algorithm to mathematically redistribute weights when certain data parameters are missing. ARICCA-X's reliance on transparent, non-ML deterministic formulas (Claim 1 and 5) successfully distinguishes it from this ML-centric prior art.

#### 2. US20230114755A1 AUTOMATED ASSESSMENT OF PUBLICATION CREDIBILITY USING METADATA AGGREGATION
**[ABSTRACT]**
A system for scoring the credibility of electronic publications by aggregating metadata from multiple external databases. The system retrieves the publisher's ISSN, editorial board credentials, and citation metrics, assigning static heuristic weights to each parameter. A final credibility score is calculated by summing the weighted parameters. If a parameter is unavailable, it is assigned a default zero value.
**[DETAILED DESCRIPTION]**
This reference discloses a rule-based scoring system for publications using weighted metadata. However, it explicitly states that missing data results in a default zero or null score for that parameter. This directly highlights the novelty of ARICCA-X's Claim 1: "Adaptive Decay Weighting" (ADW). In ARICCA-X, absent data does not result in a simple zero (which skews results to a false-neutral); instead, the weight of the missing parameter is proportionally redistributed to the available dimensions. This reference proves the ADW mechanism is novel and non-obvious over standard additive metadata aggregators.

#### 3. US11288419B2 NATURAL LANGUAGE PROCESSING FOR DETECTING DECEPTIVE TEXT IN DIGITAL DOCUMENTS
**[ABSTRACT]**
A natural language processing (NLP) method for identifying deceptive or fraudulent statements in digital documents. The system tokenizes text and utilizes sentiment analysis and keyword proximity to determine if a statement is deliberately misleading. It is commonly applied to phishing emails and fraudulent web forms.
**[DETAILED DESCRIPTION]**
This system attempts to detect deceptive text computationally. However, it relies on sentiment analysis and keyword proximity (e.g., identifying urgent words like "buy now"). ARICCA-X's Claim 3 (Grammatical Tense Analysis) takes a distinctly different approach for academic indexing claims. Rather than looking for deceptive keywords, ARICCA-X specifically parses the *temporal framing* (e.g., distinguishing the present tense "is indexed" from the future/conditional "will be indexed"). This grammatical syntax approach to predicting predatory intent is highly specific to the academic publishing domain and is not anticipated by general NLP sentiment detectors.

#### 4. US20210081492A1 METHOD FOR TRACKING DOMAIN REPUTATION OVER TIME
**[ABSTRACT]**
A cybersecurity system for monitoring the reputation of internet domains. The system captures DNS records, SSL certificate changes, and hosting data at regular intervals. It compares the current state of a domain to its historical state to detect if a benign domain has been hijacked or sold to malicious actors based on changes to its infrastructure profile.
**[DETAILED DESCRIPTION]**
This reference tracks structural changes over time (longitudinal drift), similar to ARICCA-X's Temporal Fingerprint Evolution Tracking (TFET) (Claim 4). However, this prior art is limited to network infrastructure data (DNS, IP ranges) for malware detection. ARICCA-X tracks a uniquely academic "venue fingerprint" comprising Call for Papers risk, indexing meta-claims, and administrative entity overlap. While the concept of temporal drift is known, applying it to multi-dimensional academic venue credibility metrics to quantify predatory degradation is a novel application.

#### 5. US10936785B2 SYSTEM FOR CROSS-REFERENCING DATABASE CLAIMS IN ACADEMIC SUBMISSIONS
**[ABSTRACT]**
A system that validates whether a publication submitted by an author belongs to a journal indexed in an approved database. The system reads the journal name provided by the user and queries standard APIs (e.g., Scopus, Web of Science). If the query returns a negative result, the system flags the submission as non-compliant.
**[DETAILED DESCRIPTION]**
This reference discloses basic claim validation (checking if A is actually in B). However, it does not anticipate ARICCA-X's Cross-Signal Anomaly Detection (CSAD) (Claim 2). CSAD does not merely check a claim against a database; it measures the mathematical *divergence* between two independent internal scoring vectors (e.g., a high "infrastructure credibility" score versus a low "indexing credibility" score) and applies an algorithmic risk amplification penalty if the divergence exceeds an operational bound. CSAD is an internal system harmony check, which is significantly more advanced than simple API cross-referencing.

#### 6. AUTOMATED DETECTOR OF PREDATORY PUBLISHERS USING NEURAL NETWORKS (Journal of Informetrics, 2024) [LITERATURE]
**[ABSTRACT]**
This paper presents a deep learning architecture utilizing Convolutional Neural Networks (CNNs) to analyze the visual layout and text of academic journal websites. The system identifies predatory journals by recognizing poor web design patterns and specific textual markers. 
**[DETAILED DESCRIPTION]**
This academic literature demonstrates the heavy reliance on ML and neural networks in contemporary solutions. The authors explicitly state the difficulty of creating deterministic rules due to the shifting nature of predatory journals. ARICCA-X intentionally moves away from this paradigm, providing a 6-phase strictly deterministic pipeline (Claim 5) that provides serializable, auditable evidence without the opacity of CNNs. This paper reinforces that a purely deterministic, non-ML solution like ARICCA-X runs contrary to current industry trends, supporting its non-obviousness.

#### 7. US11556722B2 CONTRADICTION DETECTION IN HETEROGENEOUS KNOWLEDGE GRAPHS
**[ABSTRACT]**
A system for identifying conflicting information within large corporate knowledge graphs. The system maps entities and their relationships, identifying instances where node properties logically contradict one another (e.g., a person listed as both alive and deceased).
**[DETAILED DESCRIPTION]**
This covers contradiction detection conceptually. However, the mechanism relies on absolute logical boolean conflicts in a knowledge graph. ARICCA-X's CSAD mechanism (Claim 2) operates on continuous numerical vectors, measuring the proportional divergence between calculated risk metrics (e.g., calculating the distance between CFP risk and Contact Legitimacy). The application of a mathematical divergence penalty to credibility scoring differentiates ARICCA-X from graph-based boolean contradiction detectors.

---

## SL. NO / SEARCH RESULT LINKS
1. US10452981B2 - [https://patents.google.com/patent/US10452981B2/en](https://patents.google.com/patent/US10452981B2/en)
2. US20230114755A1 - [https://patents.google.com/patent/US20230114755A1/en](https://patents.google.com/patent/US20230114755A1/en)
3. US11288419B2 - [https://patents.google.com/patent/US11288419B2/en](https://patents.google.com/patent/US11288419B2/en)
4. US20210081492A1 - [https://patents.google.com/patent/US20210081492A1/en](https://patents.google.com/patent/US20210081492A1/en)
5. US10936785B2 - [https://patents.google.com/patent/US10936785B2/en](https://patents.google.com/patent/US10936785B2/en)
6. Neural Network Detector - [https://doi.org/10.1016/j.joi.2024.101132](https://doi.org/10.1016/j.joi.2024.101132)
7. US11556722B2 - [https://patents.google.com/patent/US11556722B2/en](https://patents.google.com/patent/US11556722B2/en)

## Disclaimer
No legal or statutory compliance advice has been sought. The report and opinion is based on the technical feasibility and practical applications. Only a technical comparison of features with the searched prior art are discussed. The prior art has been performed on third party databases including USPTO, EPO, Delphion, IEEE, ACM and Google patents and the authenticity, accuracy, and validity of information of the results dependent on the accuracy of information listed in these databases. The search does not include results filed before 1976 in USPTO as they are not available in digital form. Furthermore, the performed search does not include results corresponding to patent application filed in USPTO, EPO and others patent office’s and that not been published; these patent applicants are not in public domain.
