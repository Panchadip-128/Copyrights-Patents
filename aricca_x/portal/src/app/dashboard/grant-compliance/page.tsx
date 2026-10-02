"use client";
import { useEffect } from 'react';

export default function GrantCompliance() {
  useEffect(() => {
    window.runGrantCompliance = function() {
      const grantId = (document.getElementById('grantId') as HTMLInputElement)?.value?.trim();
      const funder = (document.getElementById('funderSelect') as HTMLSelectElement)?.value;
      const resultsDiv = document.getElementById('grantResults');
      if (!resultsDiv || !grantId) return;

      // Simulated publication list for grant
      const publications = [
        { title: 'Deep Learning for Venue Classification', venue: 'IEEE TPAMI', oa: 'Gold OA', license: 'CC-BY', deposited: true, compliant: true },
        { title: 'Adaptive Weighting in Multi-Signal Systems', venue: 'ACM Computing Surveys', oa: 'Hybrid', license: 'CC-BY-NC', deposited: true, compliant: funder !== 'plans' },
        { title: 'Temporal Fingerprinting for Research Integrity', venue: 'Springer LNCS', oa: 'Green OA', license: 'Publisher', deposited: false, compliant: false },
        { title: 'Cross-Signal Anomaly Detection Methods', venue: 'Elsevier Pattern Recognition', oa: 'Closed', license: 'Publisher', deposited: false, compliant: false },
        { title: 'NLP-Based Tense Classification', venue: 'AAAI 2026 Proceedings', oa: 'Gold OA', license: 'CC-BY', deposited: true, compliant: true },
      ];

      const compliantCount = publications.filter(p => p.compliant).length;
      const nonCompliantCount = publications.length - compliantCount;
      const complianceRate = ((compliantCount / publications.length) * 100).toFixed(1);

      const funderNames: Record<string, string> = { 'nih': 'NIH Public Access Policy', 'nsf': 'NSF Public Access Plan', 'plans': 'Plan S (cOAlition S)', 'ukri': 'UKRI Open Access Policy' };
      const funderRules: Record<string, string> = {
        'nih': 'Accepted manuscripts must be deposited in PubMed Central within 12 months.',
        'nsf': 'Peer-reviewed publications must be deposited in an approved repository.',
        'plans': 'All publications must be immediate Gold OA with CC-BY license. No embargo periods allowed.',
        'ukri': 'Research articles must be OA immediately. CC-BY license required for research articles.'
      };

      const overallStatus = compliantCount === publications.length ? 'COMPLIANT' : nonCompliantCount > 2 ? 'NON_COMPLIANT' : 'PARTIALLY_COMPLIANT';
      const statusColor = overallStatus === 'COMPLIANT' ? '#10b981' : overallStatus === 'NON_COMPLIANT' ? '#f43f5e' : '#f59e0b';

      const pubRows = publications.map((p, i) => \`
        <tr style="border-bottom: 1px solid var(--border);">
          <td style="padding: 10px; font-size: 0.8rem; color: var(--text-primary); font-weight: 600;">\${p.title}</td>
          <td style="padding: 10px; font-size: 0.8rem; color: var(--text-secondary);">\${p.venue}</td>
          <td style="padding: 10px; font-size: 0.8rem; color: var(--text-secondary);">\${p.oa}</td>
          <td style="padding: 10px; font-size: 0.8rem; color: var(--text-secondary);">\${p.license}</td>
          <td style="padding: 10px; font-size: 0.8rem; color: \${p.deposited ? '#10b981' : '#f43f5e'};">\${p.deposited ? 'Yes' : 'No'}</td>
          <td style="padding: 10px; text-align: center;">
            <span style="padding: 3px 10px; border-radius: 12px; font-size: 0.7rem; font-weight: 700; background: \${p.compliant ? 'rgba(16,185,129,0.15)' : 'rgba(244,63,94,0.15)'}; color: \${p.compliant ? '#10b981' : '#f43f5e'};">\${p.compliant ? 'COMPLIANT' : 'NON-COMPLIANT'}</span>
          </td>
        </tr>
      \`).join('');

      const remediations = publications.filter(p => !p.compliant).map(p => {
        if (!p.deposited) return \`<strong>\${p.title}</strong>: Deposit accepted manuscript in institutional repository within 12 months.\`;
        if (p.license !== 'CC-BY') return \`<strong>\${p.title}</strong>: Negotiate CC-BY license with publisher or publish version of record under compliant license.\`;
        return \`<strong>\${p.title}</strong>: Convert to Gold OA or deposit Green OA version.\`;
      });

      resultsDiv.innerHTML = \`
        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1rem; margin-top: 1rem;">
          <div class="card" style="text-align: center;">
            <div class="card-title" style="justify-content: center;">Grant Compliance Status</div>
            <div style="font-size: 2rem; font-weight: 900; color: \${statusColor}; margin: 0.5rem 0;">\${overallStatus}</div>
            <div style="font-size: 0.8rem; color: var(--text-muted);">Under \${funderNames[funder] || funder}</div>
          </div>
          <div class="card" style="text-align: center;">
            <div class="card-title" style="justify-content: center;">Compliance Rate</div>
            <div style="font-size: 2.5rem; font-weight: 900; color: \${statusColor}; margin: 0.5rem 0;">\${complianceRate}%</div>
            <div style="font-size: 0.8rem; color: var(--text-muted);">\${compliantCount}/\${publications.length} publications compliant</div>
          </div>
          <div class="card" style="text-align: center;">
            <div class="card-title" style="justify-content: center;">Actions Required</div>
            <div style="font-size: 2.5rem; font-weight: 900; color: \${nonCompliantCount > 0 ? '#f59e0b' : '#10b981'}; margin: 0.5rem 0;">\${nonCompliantCount}</div>
            <div style="font-size: 0.8rem; color: var(--text-muted);">Publications need remediation</div>
          </div>
        </div>

        <div class="card" style="margin-top: 1rem;">
          <div class="card-title">Per-Publication Compliance Audit <span class="claim-tag">Claim 12</span></div>
          <div style="overflow-x: auto;">
            <table style="width: 100%; border-collapse: collapse;">
              <thead>
                <tr style="border-bottom: 2px solid var(--border);">
                  <th style="padding: 10px; text-align: left; font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase;">Publication</th>
                  <th style="padding: 10px; text-align: left; font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase;">Venue</th>
                  <th style="padding: 10px; text-align: left; font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase;">OA Type</th>
                  <th style="padding: 10px; text-align: left; font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase;">License</th>
                  <th style="padding: 10px; text-align: left; font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase;">Deposited</th>
                  <th style="padding: 10px; text-align: center; font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase;">Status</th>
                </tr>
              </thead>
              <tbody>\${pubRows}</tbody>
            </table>
          </div>
        </div>

        \${remediations.length > 0 ? \`
        <div class="card" style="margin-top: 1rem;">
          <div class="card-title" style="color: var(--accent-amber);">Remediation Recommendations <span class="claim-tag">Claim 12</span></div>
          \${remediations.map((r, i) => \`<div style="padding: 8px 12px; margin-bottom: 8px; background: rgba(245,158,11,0.06); border-left: 3px solid var(--accent-amber); border-radius: 4px; font-size: 0.82rem; color: var(--text-secondary); line-height: 1.6;">\${i + 1}. \${r}</div>\`).join('')}
        </div>\` : ''}

        <div class="card" style="margin-top: 1rem;">
          <div class="card-title">Applicable Mandate Rules</div>
          <div style="padding: 0.75rem; background: rgba(59,130,246,0.06); border-radius: 6px; font-size: 0.85rem; color: var(--text-secondary); line-height: 1.6;">
            <strong style="color: var(--accent-blue);">\${funderNames[funder] || funder}:</strong> \${funderRules[funder] || 'No specific rules loaded.'}
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
            <a href="/dashboard/researcher" class="module-link">Researcher Auditing</a>
            <a href="/dashboard/peer-review" class="module-link">Peer-Review Forensics</a>
            <a href="/dashboard/grant-compliance" class="module-link active">Grant Compliance</a>
        </nav>
        <div style="display: flex; align-items: center;">
            <span class="patent-badge">Patent Pending (14 Claims)</span>
            <button class="btn" style="margin-left: 15px; padding: 6px 14px; font-size: 0.75rem;" onclick="window.location.href='/'">Logout</button>
        </div>
    </div>
</header>

<div class="main">
    <div class="hero-banner">
        <h1>Module D: Grant Compliance Engine</h1>
        <p>Deterministic funding agency mandate verification for Plan S, NIH, NSF, and UKRI policies.</p>
        <div class="innovation-chips">
            <span class="innovation-chip chip-adw">Claim 12: Mandate Compliance Verification</span>
            <span class="innovation-chip chip-csad">Claim 13: Grant Attribution Mining</span>
        </div>
    </div>

    <div class="card" style="margin-top: 1.5rem;">
        <div class="card-title">Grant Compliance Input</div>
        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1rem;">
            <div class="input-group">
                <label>Grant Identifier</label>
                <input type="text" id="grantId" value="NSF-2024-IIS-1234567" placeholder="e.g. NSF-2024-IIS-XXXXXXX">
            </div>
            <div class="input-group">
                <label>Funding Agency</label>
                <select id="funderSelect">
                    <option value="nsf">NSF (National Science Foundation)</option>
                    <option value="nih">NIH (National Institutes of Health)</option>
                    <option value="plans">Plan S (cOAlition S)</option>
                    <option value="ukri">UKRI (UK Research & Innovation)</option>
                </select>
            </div>
            <div class="input-group">
                <label>Grant Period</label>
                <input type="text" id="grantPeriod" value="2024-2027" placeholder="e.g. 2024-2027">
            </div>
        </div>
        <button class="btn btn-primary" onclick="window.runGrantCompliance()">Run Compliance Audit</button>
    </div>

    <div id="grantResults"></div>
</div>
    \`}} />
  );
}
