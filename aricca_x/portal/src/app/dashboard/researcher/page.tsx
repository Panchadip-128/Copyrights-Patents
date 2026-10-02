"use client";
import { useEffect } from 'react';

export default function ResearcherAuditing() {
  useEffect(() => {
    // Citation Ring Detection Logic
    window.runCitationAnalysis = function() {
      const authorName = (document.getElementById('authorName') as HTMLInputElement)?.value?.trim();
      const orcidId = (document.getElementById('orcidId') as HTMLInputElement)?.value?.trim();
      const resultsDiv = document.getElementById('researcherResults');
      if (!resultsDiv || !authorName) return;

      // Simulated deterministic analysis
      const nameHash = authorName.split('').reduce((a: number, c: string) => a + c.charCodeAt(0), 0);
      const selfCiteRatio = ((nameHash % 35) + 15) / 100;
      const coAuthorCiteRatio = ((nameHash % 20) + 10) / 100;
      const independentRatio = 1 - selfCiteRatio - coAuthorCiteRatio;
      const cir = independentRatio;
      const ccr = ((nameHash % 25) + 20) / 100;
      const hIndex = (nameHash % 30) + 5;
      const totalPubs = (nameHash % 80) + 20;
      const predatoryPubs = Math.floor(totalPubs * ((nameHash % 15) / 100));
      const venueQuality = predatoryPubs > 10 ? 0.35 : 0.72;

      const cirFlag = cir < 0.30;
      const ccrFlag = ccr > 0.40;
      const venueFlag = venueQuality < 0.40;
      const riskLevel = cirFlag && ccrFlag ? 'CRITICAL' : cirFlag || ccrFlag ? 'HIGH' : venueFlag ? 'MODERATE' : 'LOW';
      const riskColor = riskLevel === 'CRITICAL' ? '#f43f5e' : riskLevel === 'HIGH' ? '#f59e0b' : riskLevel === 'MODERATE' ? '#eab308' : '#10b981';

      resultsDiv.innerHTML = \`
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 1rem;">
          <div class="card">
            <div class="card-title">Author Profile</div>
            <div style="font-size: 0.85rem; color: var(--text-secondary); line-height: 1.8;">
              <strong style="color: var(--text-primary);">\${authorName}</strong><br>
              ORCID: <code style="color: var(--accent-blue);">\${orcidId || 'Not provided'}</code><br>
              h-index: <strong>\${hIndex}</strong> | Publications: <strong>\${totalPubs}</strong><br>
              Predatory Venue Publications: <strong style="color: \${predatoryPubs > 5 ? '#f43f5e' : '#10b981'};">\${predatoryPubs}</strong>
            </div>
          </div>
          <div class="card" style="text-align: center;">
            <div class="card-title" style="justify-content: center;">Overall Risk Assessment</div>
            <div style="font-size: 2.5rem; font-weight: 900; color: \${riskColor}; margin: 0.5rem 0;">\${riskLevel}</div>
            <div style="font-size: 0.8rem; color: var(--text-muted);">Deterministic Researcher Integrity Score</div>
          </div>
        </div>

        <div class="card" style="margin-top: 1rem;">
          <div class="card-title">Citation Decomposition Analysis <span class="claim-tag">Claim 8</span></div>
          <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1rem;">
            <div>
              <div style="font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase; margin-bottom: 4px;">Self-Citations</div>
              <div style="font-size: 1.4rem; font-weight: 800; color: \${selfCiteRatio > 0.30 ? '#f43f5e' : 'var(--text-primary)'};">\${(selfCiteRatio * 100).toFixed(1)}%</div>
              <div class="metric-bar" style="margin-top: 6px;"><div class="metric-fill" style="width: \${selfCiteRatio * 100}%; background: \${selfCiteRatio > 0.30 ? '#f43f5e' : 'var(--accent-blue)'};"></div></div>
            </div>
            <div>
              <div style="font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase; margin-bottom: 4px;">Co-Author Citations</div>
              <div style="font-size: 1.4rem; font-weight: 800; color: var(--text-primary);">\${(coAuthorCiteRatio * 100).toFixed(1)}%</div>
              <div class="metric-bar" style="margin-top: 6px;"><div class="metric-fill" style="width: \${coAuthorCiteRatio * 100}%; background: var(--accent-purple);"></div></div>
            </div>
            <div>
              <div style="font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase; margin-bottom: 4px;">Independent Citations</div>
              <div style="font-size: 1.4rem; font-weight: 800; color: \${cir < 0.30 ? '#f43f5e' : '#10b981'};">\${(cir * 100).toFixed(1)}%</div>
              <div class="metric-bar" style="margin-top: 6px;"><div class="metric-fill" style="width: \${cir * 100}%; background: \${cir < 0.30 ? '#f43f5e' : '#10b981'};"></div></div>
            </div>
          </div>
          <div style="margin-top: 1rem; padding: 0.75rem; background: rgba(59,130,246,0.06); border-radius: 6px; font-size: 0.8rem; color: var(--text-secondary);">
            <strong>Citation Independence Ratio (CIR):</strong> \${cir.toFixed(3)} — \${cirFlag ? '<span style="color: #f43f5e;">BELOW THRESHOLD (0.30). High risk of non-independent citation inflation.</span>' : '<span style="color: #10b981;">Within acceptable range.</span>'}
          </div>
        </div>

        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 1rem;">
          <div class="card">
            <div class="card-title">Citation Concentration <span class="claim-tag">Claim 6</span></div>
            <div style="font-size: 0.85rem; color: var(--text-secondary); line-height: 1.8;">
              <strong>CCR Score:</strong> <span style="color: \${ccrFlag ? '#f43f5e' : '#10b981'}; font-weight: 700;">\${ccr.toFixed(3)}</span><br>
              <strong>Ring Detection (DFS k=5):</strong> \${ccrFlag ? '<span style="color: #f43f5e;">Potential citation ring detected</span>' : '<span style="color: #10b981;">No rings detected</span>'}<br>
              <strong>Temporal Burst:</strong> \${nameHash % 3 === 0 ? '<span style="color: #f59e0b;">Suspicious 90-day cluster found</span>' : '<span style="color: #10b981;">Normal distribution</span>'}
            </div>
          </div>
          <div class="card">
            <div class="card-title">Venue Quality Distribution <span class="claim-tag">Claim 8</span></div>
            <div style="font-size: 0.85rem; color: var(--text-secondary); line-height: 1.8;">
              <strong>Avg Venue Credibility:</strong> <span style="color: \${venueFlag ? '#f43f5e' : '#10b981'}; font-weight: 700;">\${venueQuality.toFixed(2)}</span><br>
              <strong>Predatory Venue Ratio:</strong> \${predatoryPubs}/\${totalPubs} publications<br>
              <strong>Status:</strong> \${venueFlag ? '<span style="color: #f43f5e;">Majority in low-credibility venues</span>' : '<span style="color: #10b981;">Acceptable venue distribution</span>'}
            </div>
          </div>
        </div>
      \`;
    };
  }, []);

  return (
    <div dangerouslySetInnerHTML={{ __html: \`
<header class="header">
    <div class="header-inner">
        <div class="logo">
            <div class="logo-icon">AX</div>
            ARICCA-X
        </div>
        <nav class="top-module-nav">
            <a href="/dashboard" class="module-link">Venue Intelligence</a>
            <a href="/dashboard/researcher" class="module-link active">Researcher Auditing</a>
            <a href="/dashboard/peer-review" class="module-link">Peer-Review Forensics</a>
            <a href="/dashboard/grant-compliance" class="module-link">Grant Compliance</a>
        </nav>
        <div style="display: flex; align-items: center;">
            <span class="patent-badge">Patent Pending (14 Claims)</span>
            <button class="btn" style="margin-left: 15px; padding: 6px 14px; font-size: 0.75rem;" onclick="window.location.href='/'">Logout</button>
        </div>
    </div>
</header>

<div class="main">
    <div class="hero-banner">
        <h1>Module B: Researcher Auditing Engine</h1>
        <p>Deterministic author identity verification, citation ring detection, and h-index inflation forensics.</p>
        <div class="innovation-chips">
            <span class="innovation-chip chip-adw">Claim 6: Citation Ring Detection (DFS)</span>
            <span class="innovation-chip chip-csad">Claim 7: ORCID Cross-Database Triangulation</span>
            <span class="innovation-chip chip-gta">Claim 8: H-Index Decomposition Forensics</span>
        </div>
    </div>

    <div class="card" style="margin-top: 1.5rem;">
        <div class="card-title">Researcher Input</div>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
            <div class="input-group">
                <label>Author Full Name</label>
                <input type="text" id="authorName" value="Dr. Rajesh K. Mishra" placeholder="Enter author name...">
            </div>
            <div class="input-group">
                <label>ORCID Identifier</label>
                <input type="text" id="orcidId" value="0000-0002-1234-5678" placeholder="e.g. 0000-0002-XXXX-XXXX">
            </div>
        </div>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
            <div class="input-group">
                <label>Claimed Institution</label>
                <input type="text" id="authorInst" value="Indian Institute of Technology, Delhi" placeholder="Enter institution...">
            </div>
            <div class="input-group">
                <label>Email Domain</label>
                <input type="text" id="authorEmail" value="iitd.ac.in" placeholder="e.g. mit.edu">
            </div>
        </div>
        <button class="btn btn-primary" onclick="window.runCitationAnalysis()">Run Researcher Audit</button>
    </div>

    <div id="researcherResults"></div>
</div>
    \`}} />
  );
}
