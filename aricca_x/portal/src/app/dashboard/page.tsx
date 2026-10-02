"use client";
import { useEffect, useRef } from 'react';

export default function Dashboard() {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!document.querySelector('script[src="/aricca_logic.js"]')) {
        const script = document.createElement('script');
        script.src = '/aricca_logic.js';
        document.body.appendChild(script);
    }
    setTimeout(() => {
        if(window.document.getElementById('tabVenue')) {
            window.document.getElementById('tabVenue')?.click();
        }
        const appContainer = document.getElementById('app-container');
        if (appContainer) appContainer.style.display = 'block';
    }, 200);
  }, []);

  return (
    <div ref={containerRef} dangerouslySetInnerHTML={{ __html: `
<div id="app-container">
<header class="header">
    <div class="header-inner">
        <div class="logo">
            <div class="logo-icon">AX</div>
            ARICCA-X
            <span id="role-badge" class="admin-badge"></span>
        </div>
        <div style="display: flex; align-items: center;">
            <span class="patent-badge">Patent Pending (5 Claims)</span>
            <button class="btn" style="margin-left: 15px; padding: 6px 14px; font-size: 0.75rem;" onclick="logout()">Logout</button>
        </div>
    </div>
</header>

<div class="main">
    <div class="hero-banner">
        <h1>Automated Research Integrity, Credibility & Compliance Analyzer</h1>
        <p>Deterministic, non-ML venue credibility assessment system integrating adaptive weight redistribution and multi-dimensional analysis.</p>
        <div class="innovation-chips">
            <span class="innovation-chip chip-adw">Claim 1: Adaptive Decay Weighting</span>
            <span class="innovation-chip chip-csad">Claim 2: Cross-Signal Anomaly Detection</span>
            <span class="innovation-chip chip-gta">Claim 3: Grammatical Tense Analysis</span>
            <span class="innovation-chip chip-tfet">Claim 4: Temporal Fingerprint Evolution</span>
            <span class="innovation-chip chip-pipeline">Claim 5: Deterministic Pipeline</span>
        </div>
    </div>

    <nav class="nav-tabs" id="navTabs">
        <button class="nav-tab active" data-tab="venue" id="tabVenue">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
            Venue Analysis
        </button>
        <button class="nav-tab" data-tab="tense" id="tabTense">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" /></svg>
            Tense Analysis
        </button>
        <button class="nav-tab" data-tab="compliance" id="tabCompliance">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
            Compliance
        </button>
        <button class="nav-tab" data-tab="citation" id="tabCitation">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" /></svg>
            Citations
        </button>
        <button class="nav-tab" data-tab="evolution" id="tabEvolution">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" /></svg>
            Evolution
        </button>
        <button class="nav-tab" data-tab="latency" id="tabLatency">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
            Latency (PRLV)
        </button>
        <button class="nav-tab" data-tab="geo" id="tabGeo">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064" /></svg>
            Geo-Triangulation
        </button>
        <button class="nav-tab" data-tab="ml" id="tabML" style="border: 1px dashed var(--accent-rose);">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="var(--accent-rose)"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" /></svg>
            <span style="color: var(--accent-rose);">ML Sandbox</span>
        </button>
    </nav>

    <!-- =============== PANEL: ML VERIFICATION =============== -->
    <div class="panel" id="panelML">
        <div class="card" style="margin-top:1.5rem; text-align: center;">
            <div class="card-title" style="justify-content:center; color: var(--accent-rose);">
                <svg class="icon-md" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
                Experimental Machine Learning Module
            </div>
            <p style="color: var(--text-muted); font-size: 0.9rem; max-width: 600px; margin: 1rem auto;">
                Warning: This Deep Learning classification module is currently sandboxed. To preserve 35 U.S.C. § 101 patent eligibility, ARICCA-X relies on its core Deterministic Pipeline (Claims 1-5). ML features are strictly utilized for off-chain heuristic verification and are undergoing empirical validation before UI integration.
            </p>
            <div style="background: rgba(244,63,94,0.08); border: 1px solid rgba(244,63,94,0.3); border-radius: 8px; padding: 1.5rem; margin: 2rem auto; max-width: 500px;">
                <h3 style="color: var(--text-primary); margin-bottom: 0.5rem;">Verification Status: <span style="color: var(--accent-amber);">IN PROGRESS</span></h3>
                <p style="font-size: 0.8rem; color: var(--text-secondary); margin-bottom: 1.5rem;">
                    Local testing of the DL models is being conducted via standalone Python validation scripts. UI integration will occur post-validation.
                </p>
                <button class="btn btn-secondary" style="border-color: var(--accent-rose); color: var(--accent-rose);" onclick="alert('ML Model is currently running in an isolated environment. Check the ml_verification.py validation script.')">
                    <svg class="icon-sm" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path></svg>
                    View DL Engine Status
                </button>
            </div>
        </div>
    </div>

    <!-- =============== PANEL: VENUE ANALYSIS =============== -->
    <div class="panel active" id="panelVenue">
        <div class="grid-23" style="margin-top:1.5rem">
            <!-- Input Column -->
            <div>
                <div class="card">
                    <div class="card-title">Venue Input Data</div>
                    <div class="input-group">
                        <label>Venue Name</label>
                        <input type="text" id="venueName" value="International Conference on Intelligent Computing 2026" placeholder="Enter venue name...">
                    </div>
                    <div class="input-group">
                        <label>Call for Papers Text</label>
                        <textarea id="cfpText" placeholder="Paste CFP text here...">ICICT 2026 - CALL FOR PAPERS

Submit your papers NOW! Extended deadline: January 30, 2026.
Last chance to submit! Don't miss this opportunity!

All papers will be reviewed. Fast track publication guaranteed.
Papers will be indexed in Scopus and may be included in Web of Science.
Conference proceedings published quickly.

Topics include: AI, Machine Learning, IoT, Data Science

Registration fee: \$500 USD (early bird: \$350)
Contact: icict2026@gmail.com
Payment required before acceptance notification.</textarea>
                    </div>
                    <div class="grid-2">
                        <div class="input-group">
                            <label>Website URL</label>
                            <input type="text" id="venueUrl" value="http://icict2026-conf.com" placeholder="https://...">
                        </div>
                        <div class="input-group">
                            <label>Website Pages</label>
                            <input type="number" id="venuePages" value="3" min="0" max="50">
                        </div>
                    </div>
                    <div class="grid-2">
                        <div class="toggle-row">
                            <div class="toggle" id="toggleSSL" onclick="this.classList.toggle('on')"></div>
                            <span class="toggle-label">Has SSL/HTTPS</span>
                        </div>
                        <div class="toggle-row">
                            <div class="toggle on" id="toggleContact" onclick="this.classList.toggle('on')"></div>
                            <span class="toggle-label">Has Contact Page</span>
                        </div>
                    </div>
                    <div class="grid-2">
                        <div class="toggle-row">
                            <div class="toggle" id="toggleAbout" onclick="this.classList.toggle('on')"></div>
                            <span class="toggle-label">Has About Page</span>
                        </div>
                        <div class="toggle-row">
                            <div class="toggle" id="toggleFingerprint" onclick="this.classList.toggle('on')"></div>
                            <span class="toggle-label">Include Fingerprint Data</span>
                        </div>
                    </div>
                    <button class="btn btn-primary" onclick="runVenueAnalysis()" style="width:100%;margin-top:0.5rem;justify-content:center;">
                        Execute Full Analysis Pipeline
                    </button>
                </div>
            </div>

            <!-- Results Column -->
            <div id="venueResults">
                <div class="card">
                    <div class="card-title">Pipeline Status <span class="claim-tag">Claim 5</span></div>
                    <div class="pipeline-phases" id="pipelinePhases">
                        <div class="phase-step" id="phase1"><span class="phase-num">1</span>Components</div>
                        <div class="phase-step" id="phase2"><span class="phase-num">2</span>Heuristics</div>
                        <div class="phase-step" id="phase3"><span class="phase-num">3</span>Credibility</div>
                        <div class="phase-step" id="phase4"><span class="phase-num">4</span>Risk Level</div>
                        <div class="phase-step" id="phase5"><span class="phase-num">5</span>Recommendations</div>
                        <div class="phase-step" id="phase6"><span class="phase-num">6</span>Flags</div>
                    </div>
                    <div class="empty-state" id="pipelineEmpty">Execute analysis to view the deterministic pipeline sequence.</div>
                </div>

                <div class="grid-2" id="resultCards" style="display:none">
                    <div class="card" style="text-align:center;">
                        <div class="card-title" style="justify-content:center;">Credibility Score</div>
                        <div class="score-ring">
                            <svg viewBox="0 0 100 100">
                                <circle class="score-ring-bg" cx="50" cy="50" r="42"/>
                                <circle class="score-ring-fill" id="credRing" cx="50" cy="50" r="42"
                                    stroke-dasharray="264" stroke-dashoffset="264"/>
                            </svg>
                            <div class="score-ring-label">
                                <span class="score-ring-value" id="credValue">--</span>
                                <span class="score-ring-unit">Score</span>
                            </div>
                        </div>
                        <div style="margin-top:12px;" id="riskBadgeContainer"></div>
                    </div>
                    <div class="card">
                        <div class="card-title">Score Breakdown</div>
                        <div id="scoreBreakdown"></div>
                    </div>
                </div>

                <!-- ADW Visualization -->
                <div class="card" id="adwCard" style="display:none">
                    <div class="card-title">Adaptive Decay Weighting <span class="claim-tag">Claim 1</span></div>
                    <p style="font-size:0.78rem;color:var(--text-muted);margin-bottom:12px;">
                        Blue = base weight · Green = effective weight after redistribution. Absent data sources have their weights proportionally redistributed to available sources to prevent false-neutral outputs.
                    </p>
                    <div id="adwBars"></div>
                    <div class="stat-row" style="margin-top:8px">
                        <span class="stat-label">Data Completeness</span>
                        <span class="stat-value" id="dataCompleteness">--</span>
                    </div>
                    <div class="stat-row">
                        <span class="stat-label">Absence Penalty Applied</span>
                        <span class="stat-value" id="absencePenalty">--</span>
                    </div>
                </div>

                <!-- CSAD Visualization -->
                <div class="card" id="csadCard" style="display:none">
                    <div class="card-title">Cross-Signal Anomaly Detection <span class="claim-tag">Claim 2</span></div>
                    <div id="csadContent"></div>
                </div>

                <!-- Heuristics -->
                <div class="card" id="heuristicsCard" style="display:none">
                    <div class="card-title">Heuristic Evaluation Results</div>
                    <div id="heuristicsContent"></div>
                </div>

                <!-- Flags & Recommendations -->
                <div class="grid-2" id="flagsRecsRow" style="display:none">
                    <div class="card">
                        <div class="card-title">System Flags</div>
                        <div id="flagsContent"></div>
                    </div>
                    <div class="card">
                        <div class="card-title">Recommendations</div>
                        <div id="recsContent"></div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- =============== PANEL: TENSE ANALYSIS =============== -->
    <div class="panel" id="panelTense">
        <div class="grid-23" style="margin-top:1.5rem">
            <div>
                <div class="card">
                    <div class="card-title">Indexing Claim Tense Analysis <span class="claim-tag">Claim 3</span></div>
                    <p style="font-size:0.8rem;color:var(--text-secondary);margin-bottom:1rem;">
                        Enter indexing claim phrases to analyze their grammatical tense. 
                        Prior art systems detect <em>whether</em> an indexer is mentioned — ARICCA-X analyzes 
                        the <strong>temporal framing</strong> to detect deceptive claims computationally.
                    </p>
                    <div class="input-group">
                        <label>Indexing Claims (one per line)</label>
                        <textarea id="tenseInput" style="min-height:200px">This journal is indexed in Scopus since 2018
Papers will be submitted to Scopus for indexing
The conference may be indexed in Web of Science
All papers are currently listed in IEEE Xplore
The proceedings could be included in DBLP
We have applied for Scopus indexing
Under review for inclusion in Web of Science
Has been indexed in PubMed for five years
Fast-track indexing guaranteed in all databases
Indexed by Google Scholar and Crossref</textarea>
                    </div>
                    <button class="btn btn-primary" onclick="runTenseAnalysis()" style="width:100%;justify-content:center;">
                        Analyze Claim Tenses
                    </button>
                </div>
            </div>
            <div>
                <div class="card">
                    <div class="card-title">Grammatical Tense Classification</div>
                    <div id="tenseResults">
                        <div class="empty-state">Submit claims to view tense classification results.</div>
                    </div>
                </div>
                <div class="card">
                    <div class="card-title">Tense Risk Distribution</div>
                    <div id="tenseDistribution">
                        <div class="empty-state">Distribution statistics will render upon analysis completion.</div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- =============== PANEL: COMPLIANCE =============== -->
    <div class="panel" id="panelCompliance">
        <div class="grid-23" style="margin-top:1.5rem">
            <div>
                <div class="card">
                    <div class="card-title">Manuscript Compliance Compiler</div>
                    <div class="input-group">
                        <label>Manuscript Title</label>
                        <input type="text" id="msTitle" value="A Novel Approach to Deep Learning for IoT">
                    </div>
                    <div class="input-group">
                        <label>Style Guide</label>
                        <select id="msStyle">
                            <option value="IEEE">IEEE</option>
                            <option value="ACM">ACM</option>
                            <option value="APA">APA</option>
                        </select>
                    </div>
                    <div class="grid-2">
                        <div class="input-group">
                            <label>Page Count</label>
                            <input type="number" id="msPages" value="6" min="1" max="100">
                        </div>
                        <div class="input-group">
                            <label>Reference Count</label>
                            <input type="number" id="msRefs" value="12" min="0" max="200">
                        </div>
                    </div>
                    <div class="toggle-row">
                        <div class="toggle on" id="toggleAbstract" onclick="this.classList.toggle('on')"></div>
                        <span class="toggle-label">Has Abstract</span>
                    </div>
                    <div class="toggle-row">
                        <div class="toggle on" id="toggleKeywords" onclick="this.classList.toggle('on')"></div>
                        <span class="toggle-label">Has Keywords</span>
                    </div>
                    <div class="toggle-row">
                        <div class="toggle" id="toggleDOI" onclick="this.classList.toggle('on')"></div>
                        <span class="toggle-label">Has DOI Citations</span>
                    </div>
                    <button class="btn btn-primary" onclick="runCompliance()" style="width:100%;margin-top:0.5rem;justify-content:center;">
                        Compile Manuscript
                    </button>
                </div>
            </div>
            <div>
                <div class="card" id="complianceResults">
                    <div class="card-title">Compilation Diagnostic Report</div>
                    <div class="empty-state" id="complianceEmpty">Configure parameters and compile manuscript to generate diagnostic output.</div>
                    <div id="complianceContent" style="display:none"></div>
                </div>
            </div>
        </div>
    </div>

    <!-- =============== PANEL: CITATION =============== -->
    <div class="panel" id="panelCitation">
        <div class="grid-23" style="margin-top:1.5rem">
            <div>
                <div class="card">
                    <div class="card-title">Citation Graph Analyzer</div>
                    <div class="input-group">
                        <label>Author Names (comma-separated)</label>
                        <input type="text" id="citAuthors" value="Smith, Johnson">
                    </div>
                    <div class="input-group">
                        <label>References (JSON array)</label>
                        <textarea id="citRefs" style="min-height:180px">[
  {"authors": ["Smith"], "year": 2024, "venue": "Journal A", "title": "Self-cite paper 1"},
  {"authors": ["Smith"], "year": 2023, "venue": "Journal A", "title": "Self-cite paper 2"},
  {"authors": ["Jones"], "year": 2022, "venue": "Conference B", "title": "External paper"},
  {"authors": ["Brown", "Davis"], "year": 2021, "venue": "Journal A", "title": "Co-authored"},
  {"authors": ["Wilson"], "year": 2024, "venue": "Journal C", "title": "Recent work"},
  {"authors": ["Smith", "Lee"], "year": 2020, "venue": "Journal A", "title": "Another self-cite"},
  {"authors": ["Taylor"], "year": 2019, "venue": "Conference D", "title": "Old reference"}
]</textarea>
                    </div>
                    <button class="btn btn-primary" onclick="runCitationAnalysis()" style="width:100%;justify-content:center;">
                        Analyze Citations
                    </button>
                </div>
            </div>
            <div>
                <div class="card" id="citationResults">
                    <div class="card-title">Citation Analysis Results</div>
                    <div class="empty-state" id="citationEmpty">Enter references array and click analyze.</div>
                    <div id="citationContent" style="display:none"></div>
                </div>
            </div>
        </div>
    </div>

    <!-- =============== PANEL: EVOLUTION =============== -->
    <div class="panel" id="panelEvolution">
        <div style="margin-top:1.5rem">
            <div class="card">
                <div class="card-title">Temporal Fingerprint Evolution Tracking <span class="claim-tag">Claim 4</span></div>
                <p style="font-size:0.8rem;color:var(--text-secondary);margin-bottom:1rem;">
                    Compare two venue fingerprints acquired at different intervals to quantify longitudinal drift.
                    This methodology replaces static single-point analysis with continuous behavioral evolution tracking.
                </p>
                <div class="grid-2">
                    <div>
                        <div class="section-title">Previous Fingerprint (T1)</div>
                        <div class="grid-2">
                            <div class="input-group">
                                <label>CFP Risk Score</label>
                                <input type="number" id="evo_t1_cfp" value="0.25" min="0" max="1" step="0.05">
                            </div>
                            <div class="input-group">
                                <label>Website Depth</label>
                                <input type="number" id="evo_t1_web" value="0.70" min="0" max="1" step="0.05">
                            </div>
                        </div>
                        <div class="input-group">
                            <label>Structural Completeness</label>
                            <input type="number" id="evo_t1_struct" value="0.65" min="0" max="1" step="0.05">
                        </div>
                        <div class="input-group">
                            <label>Claimed Indexers (comma-separated)</label>
                            <input type="text" id="evo_t1_idx" value="Scopus, IEEE Xplore">
                        </div>
                        <div class="input-group">
                            <label>Organizers (comma-separated)</label>
                            <input type="text" id="evo_t1_org" value="Dr. Smith, Dr. Jones, Dr. Brown">
                        </div>
                    </div>
                    <div>
                        <div class="section-title">Current Fingerprint (T2)</div>
                        <div class="grid-2">
                            <div class="input-group">
                                <label>CFP Risk Score</label>
                                <input type="number" id="evo_t2_cfp" value="0.65" min="0" max="1" step="0.05">
                            </div>
                            <div class="input-group">
                                <label>Website Depth</label>
                                <input type="number" id="evo_t2_web" value="0.30" min="0" max="1" step="0.05">
                            </div>
                        </div>
                        <div class="input-group">
                            <label>Structural Completeness</label>
                            <input type="number" id="evo_t2_struct" value="0.40" min="0" max="1" step="0.05">
                        </div>
                        <div class="input-group">
                            <label>Claimed Indexers (comma-separated)</label>
                            <input type="text" id="evo_t2_idx" value="Scopus, IEEE Xplore, Web of Science, PubMed">
                        </div>
                        <div class="input-group">
                            <label>Organizers (comma-separated)</label>
                            <input type="text" id="evo_t2_org" value="Dr. Wilson, Dr. Lee">
                        </div>
                    </div>
                </div>
                <button class="btn btn-primary" onclick="runEvolutionAnalysis()" style="width:100%;justify-content:center;margin-top:0.5rem;">
                    Compare Fingerprints & Detect Drift
                </button>
            </div>
            <div id="evolutionResults">
                <div class="card">
                    <div class="empty-state">Configure temporal fingerprint snapshots to execute comparison.</div>
                </div>
            </div>
        </div>
    </div>

    <!-- =============== PANEL: LATENCY VERIFIER =============== -->
    <div class="panel" id="panelLatency">
        <div class="grid-2" style="margin-top:1.5rem">
            <div>
                <div class="card">
                    <div class="card-title">
                        Peer-Review Latency Verifier (PRLV)
                        <span class="claim-tag">Core Engine</span>
                    </div>
                    <div class="input-group">
                        <label>Claimed Submission Date</label>
                        <input type="date" id="lat_sub" value="2026-09-01">
                    </div>
                    <div class="input-group">
                        <label>Claimed Acceptance Date</label>
                        <input type="date" id="lat_acc" value="2026-09-12">
                    </div>
                    <div class="input-group">
                        <label>Claimed Review Stages (e.g., Double-Blind, Revisions)</label>
                        <input type="number" id="lat_stages" value="2" min="1" max="5">
                    </div>
                    <button class="btn btn-primary" onclick="runLatencyAnalysis()" style="width:100%;justify-content:center;">Verify Temporal Logic</button>
                </div>
            </div>
            <div id="latencyResults">
                <div class="card"><div class="empty-state">Input temporal metadata to verify review logic.</div></div>
            </div>
        </div>
    </div>

    <!-- =============== PANEL: GEO-TRIANGULATION =============== -->
    <div class="panel" id="panelGeo">
        <div class="grid-2" style="margin-top:1.5rem">
            <div>
                <div class="card">
                    <div class="card-title">
                        Geospatial Triangulation
                        <span class="claim-tag">Core Engine</span>
                    </div>
                    <div class="input-group">
                        <label>Claimed HQ Location</label>
                        <select id="geo_claim" style="width:100%; padding:10px; background:var(--bg-input); border:1px solid var(--border); color:white; border-radius:var(--radius-sm);">
                            <option value="UK">London, United Kingdom</option>
                            <option value="US">New York, USA</option>
                            <option value="CH">Zurich, Switzerland</option>
                        </select>
                    </div>
                    <div class="input-group">
                        <label>Actual Server/IP Location</label>
                        <select id="geo_ip" style="width:100%; padding:10px; background:var(--bg-input); border:1px solid var(--border); color:white; border-radius:var(--radius-sm);">
                            <option value="UK">London, United Kingdom</option>
                            <option value="IN" selected>Mumbai, India</option>
                            <option value="NG">Lagos, Nigeria</option>
                        </select>
                    </div>
                    <div class="input-group">
                        <label>Payment Gateway Registration</label>
                        <select id="geo_pay" style="width:100%; padding:10px; background:var(--bg-input); border:1px solid var(--border); color:white; border-radius:var(--radius-sm);">
                            <option value="UK">London, United Kingdom</option>
                            <option value="IN" selected>Mumbai, India</option>
                            <option value="CY">Nicosia, Cyprus (Offshore)</option>
                        </select>
                    </div>
                    <button class="btn btn-primary" onclick="runGeoAnalysis()" style="width:100%;justify-content:center;margin-top:1rem;">Calculate Spatial Dissonance</button>
                </div>
            </div>
            <div id="geoResults">
                <div class="card"><div class="empty-state">Select spatial nodes to compute dissonance.</div></div>
            </div>
        </div>
    </div>
</div>

<footer class="footer">
    ARICCA-X v1.0.0 — Patent Pending — © 2026 Panchadip B & Somyajeet A. All Rights Reserved.
</footer>

` }} />
  );
}

    `}} />
  );
}
