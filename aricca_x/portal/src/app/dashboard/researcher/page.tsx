"use client";
import { useEffect } from 'react';

export default function ResearcherAuditing() {
  useEffect(() => {
    // ================================================================
    // CLAIM 6: REAL Citation Ring Detection via Bounded DFS
    // CLAIM 8: REAL H-Index Decomposition via Self-Citation Analysis
    // ================================================================

    // Build a real directed graph and run actual bounded DFS
    class CitationGraph {
      adjacency: Map<string, Set<string>>;
      edgeWeights: Map<string, number>;

      constructor() {
        this.adjacency = new Map();
        this.edgeWeights = new Map();
      }

      addEdge(from: string, to: string, count: number = 1) {
        if (!this.adjacency.has(from)) this.adjacency.set(from, new Set());
        if (!this.adjacency.has(to)) this.adjacency.set(to, new Set());
        this.adjacency.get(from)!.add(to);
        this.edgeWeights.set(`${from}->${to}`, count);
      }

      // Claim 6(b): Bounded DFS with max depth k to detect reciprocal paths
      findReciprocralPaths(source: string, target: string, maxDepth: number): string[][] {
        const paths: string[][] = [];
        const visited = new Set<string>();

        const dfs = (current: string, path: string[], depth: number) => {
          if (depth > maxDepth) return;
          if (current === target && path.length > 1) {
            paths.push([...path]);
            return;
          }
          visited.add(current);
          const neighbors = this.adjacency.get(current) || new Set();
          for (const neighbor of neighbors) {
            if (!visited.has(neighbor) || (neighbor === target && path.length > 1)) {
              dfs(neighbor, [...path, neighbor], depth + 1);
            }
          }
          visited.delete(current);
        };

        dfs(source, [source], 0);
        return paths;
      }

      // Claim 6(c): Compute Citation Concentration Ratio
      computeCCR(author: string): { ccr: number; maxCiter: string; maxCount: number; totalIncoming: number } {
        let maxCiter = '';
        let maxCount = 0;
        let totalIncoming = 0;

        for (const [edge, count] of this.edgeWeights.entries()) {
          const [from, to] = edge.split('->');
          if (to === author) {
            totalIncoming += count;
            if (count > maxCount) {
              maxCount = count;
              maxCiter = from;
            }
          }
        }

        return {
          ccr: totalIncoming > 0 ? maxCount / totalIncoming : 0,
          maxCiter,
          maxCount,
          totalIncoming
        };
      }

      // Claim 6(d): Detect temporal citation bursts
      detectTemporalBurst(citations: { from: string; date: string }[]): { hasBurst: boolean; clusterSize: number; windowDays: number } {
        if (citations.length < 3) return { hasBurst: false, clusterSize: 0, windowDays: 0 };

        const timestamps = citations.map(c => new Date(c.date).getTime()).sort((a, b) => a - b);
        const WINDOW_MS = 90 * 24 * 60 * 60 * 1000; // 90 days in ms

        let maxCluster = 0;
        for (let i = 0; i < timestamps.length; i++) {
          let count = 0;
          for (let j = i; j < timestamps.length; j++) {
            if (timestamps[j] - timestamps[i] <= WINDOW_MS) count++;
            else break;
          }
          maxCluster = Math.max(maxCluster, count);
        }

        const burstRatio = maxCluster / citations.length;
        return {
          hasBurst: burstRatio > 0.60,
          clusterSize: maxCluster,
          windowDays: 90
        };
      }

      // Detect all rings passing through a given author
      detectRings(author: string, maxDepth: number = 5): { rings: string[][]; ringCount: number } {
        const rings: string[][] = [];
        const neighbors = this.adjacency.get(author) || new Set();

        for (const neighbor of neighbors) {
          const returnPaths = this.findReciprocralPaths(neighbor, author, maxDepth - 1);
          for (const path of returnPaths) {
            rings.push([author, ...path]);
          }
        }

        return { rings, ringCount: rings.length };
      }
    }

    // Claim 8: H-Index Decomposition
    function computeHIndexDecomposition(publications: { citations: number; selfCites: number; coAuthorCites: number; sameInstCites: number }[]) {
      // Sort by total citations descending
      const sorted = [...publications].sort((a, b) => b.citations - a.citations);

      // Compute standard h-index
      let hIndex = 0;
      for (let i = 0; i < sorted.length; i++) {
        if (sorted[i].citations >= i + 1) hIndex = i + 1;
        else break;
      }

      // Decompose citation sources
      let totalCitations = 0, totalSelf = 0, totalCoAuthor = 0, totalSameInst = 0, totalIndependent = 0;
      for (const pub of publications) {
        totalCitations += pub.citations;
        totalSelf += pub.selfCites;
        totalCoAuthor += pub.coAuthorCites;
        totalSameInst += pub.sameInstCites;
        totalIndependent += pub.citations - pub.selfCites - pub.coAuthorCites - pub.sameInstCites;
      }

      // Claim 8(b): Citation Independence Ratio
      const cir = totalCitations > 0 ? totalIndependent / totalCitations : 0;

      // Compute h-index WITHOUT self-citations
      const sortedWithout = [...publications].map(p => ({
        ...p,
        citations: p.citations - p.selfCites
      })).sort((a, b) => b.citations - a.citations);

      let hIndexWithout = 0;
      for (let i = 0; i < sortedWithout.length; i++) {
        if (sortedWithout[i].citations >= i + 1) hIndexWithout = i + 1;
        else break;
      }

      return {
        hIndex,
        hIndexWithoutSelf: hIndexWithout,
        hIndexInflation: hIndex - hIndexWithout,
        totalCitations,
        totalSelf,
        totalCoAuthor,
        totalSameInst,
        totalIndependent,
        cir,
        selfRatio: totalCitations > 0 ? totalSelf / totalCitations : 0,
        coAuthorRatio: totalCitations > 0 ? totalCoAuthor / totalCitations : 0,
        sameInstRatio: totalCitations > 0 ? totalSameInst / totalCitations : 0,
        independentRatio: cir,
        publicationCount: publications.length
      };
    }

    // Expose to window for onclick handlers
    (window as any).runCitationAnalysis = function() {
      const citationTextarea = document.getElementById('citationEdges') as HTMLTextAreaElement;
      const pubTextarea = document.getElementById('publicationData') as HTMLTextAreaElement;
      const targetAuthor = (document.getElementById('targetAuthor') as HTMLInputElement)?.value?.trim();
      const resultsDiv = document.getElementById('researcherResults');
      if (!resultsDiv || !targetAuthor) return;

      // Parse citation edges: "AuthorA -> AuthorB : count"
      const graph = new CitationGraph();
      const citationDates: { from: string; date: string }[] = [];
      const edgeLines = citationTextarea.value.trim().split('\n').filter((l: string) => l.trim());

      for (const line of edgeLines) {
        const match = line.match(/^(.+?)\s*->\s*(.+?)(?:\s*:\s*(\d+))?(?:\s*@\s*(.+))?$/);
        if (match) {
          const from = match[1].trim();
          const to = match[2].trim();
          const count = parseInt(match[3] || '1');
          const date = match[4]?.trim() || '2025-06-01';
          graph.addEdge(from, to, count);
          if (to === targetAuthor) {
            for (let i = 0; i < count; i++) {
              citationDates.push({ from, date });
            }
          }
        }
      }

      // Parse publication data: "Title | totalCites | selfCites | coAuthorCites | sameInstCites"
      const publications: { title: string; citations: number; selfCites: number; coAuthorCites: number; sameInstCites: number }[] = [];
      const pubLines = pubTextarea.value.trim().split('\n').filter((l: string) => l.trim());

      for (const line of pubLines) {
        const parts = line.split('|').map((p: string) => p.trim());
        if (parts.length >= 5) {
          publications.push({
            title: parts[0],
            citations: parseInt(parts[1]) || 0,
            selfCites: parseInt(parts[2]) || 0,
            coAuthorCites: parseInt(parts[3]) || 0,
            sameInstCites: parseInt(parts[4]) || 0
          });
        }
      }

      // Run Claim 6: Ring detection
      const ringResult = graph.detectRings(targetAuthor, 5);
      const ccrResult = graph.computeCCR(targetAuthor);
      const burstResult = graph.detectTemporalBurst(citationDates);

      // Run Claim 8: H-Index Decomposition
      const decomp = computeHIndexDecomposition(publications);

      // Claim 6(e): Aggregate using simple weighted scoring (mirrors ADW from Claim 1)
      const ccrFlag = ccrResult.ccr > 0.40;
      const ringFlag = ringResult.ringCount > 0;
      const burstFlag = burstResult.hasBurst;
      const cirFlag = decomp.cir < 0.30;

      // Weighted risk aggregation
      const ringScore = ringFlag ? 0.35 : 0;
      const ccrScore = ccrFlag ? 0.25 : 0;
      const burstScore = burstFlag ? 0.20 : 0;
      const cirScore = cirFlag ? 0.20 : 0;
      const totalRisk = ringScore + ccrScore + burstScore + cirScore;

      const riskLevel = totalRisk >= 0.55 ? 'CRITICAL' : totalRisk >= 0.35 ? 'HIGH' : totalRisk >= 0.20 ? 'MODERATE' : 'LOW';
      const riskColor = riskLevel === 'CRITICAL' ? '#f43f5e' : riskLevel === 'HIGH' ? '#f59e0b' : riskLevel === 'MODERATE' ? '#eab308' : '#10b981';

      const ringsHtml = ringResult.rings.length > 0
        ? ringResult.rings.map((r: string[], i: number) => `<div style="padding:6px 10px;margin-bottom:4px;background:rgba(244,63,94,0.08);border-left:3px solid #f43f5e;border-radius:4px;font-size:0.8rem;color:var(--text-secondary);">Ring ${i + 1} (size ${r.length}): ${r.join(' → ')}</div>`).join('')
        : '<div style="color:#10b981;font-size:0.85rem;">No citation rings detected via bounded DFS (k=5).</div>';

      resultsDiv.innerHTML = `
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-top:1rem;">
          <div class="card" style="text-align:center;">
            <div class="card-title" style="justify-content:center;">Cartel Risk Classification <span class="claim-tag">Claim 6(f)</span></div>
            <div style="font-size:2.5rem;font-weight:900;color:${riskColor};margin:0.5rem 0;">${riskLevel}</div>
            <div style="font-size:0.8rem;color:var(--text-muted);">Composite Risk Score: ${totalRisk.toFixed(3)}</div>
          </div>
          <div class="card">
            <div class="card-title">Risk Score Breakdown</div>
            <div style="font-size:0.82rem;color:var(--text-secondary);line-height:2;">
              Ring Detection (0.35): <strong style="color:${ringFlag ? '#f43f5e' : '#10b981'};">${ringScore.toFixed(2)}</strong> — ${ringResult.ringCount} ring(s) found<br>
              CCR Analysis (0.25): <strong style="color:${ccrFlag ? '#f43f5e' : '#10b981'};">${ccrScore.toFixed(2)}</strong> — CCR = ${ccrResult.ccr.toFixed(3)}${ccrFlag ? ' (> 0.40 threshold)' : ''}<br>
              Temporal Burst (0.20): <strong style="color:${burstFlag ? '#f43f5e' : '#10b981'};">${burstScore.toFixed(2)}</strong> — ${burstResult.clusterSize}/${citationDates.length} in 90-day window<br>
              CIR Analysis (0.20): <strong style="color:${cirFlag ? '#f43f5e' : '#10b981'};">${cirScore.toFixed(2)}</strong> — CIR = ${decomp.cir.toFixed(3)}${cirFlag ? ' (< 0.30 threshold)' : ''}
            </div>
          </div>
        </div>

        <div class="card" style="margin-top:1rem;">
          <div class="card-title">Citation Ring Detection — Bounded DFS (k=5) <span class="claim-tag">Claim 6(b)</span></div>
          <div style="padding:0.75rem;background:rgba(59,130,246,0.06);border-radius:6px;font-size:0.82rem;color:var(--text-secondary);margin-bottom:0.75rem;">
            <strong>Algorithm:</strong> For target author "<strong>${targetAuthor}</strong>", performed bounded depth-first search with max traversal depth k=5 across ${graph.adjacency.size} vertices and ${graph.edgeWeights.size} edges.
          </div>
          ${ringsHtml}
        </div>

        <div class="card" style="margin-top:1rem;">
          <div class="card-title">Citation Concentration Ratio (CCR) <span class="claim-tag">Claim 6(c)</span></div>
          <div style="font-size:0.85rem;color:var(--text-secondary);line-height:1.8;">
            <strong>CCR(${targetAuthor}):</strong> <span style="color:${ccrFlag ? '#f43f5e' : '#10b981'};font-weight:700;">${ccrResult.ccr.toFixed(4)}</span>
            = max_citing_count(${ccrResult.maxCount}) / total_incoming(${ccrResult.totalIncoming})<br>
            <strong>Most-Citing Author:</strong> ${ccrResult.maxCiter || 'N/A'} (${ccrResult.maxCount} citations)<br>
            <strong>Threshold:</strong> ${ccrFlag ? '<span style="color:#f43f5e;">EXCEEDED (> 0.40)</span>' : '<span style="color:#10b981;">Within acceptable range (≤ 0.40)</span>'}
          </div>
        </div>

        <div class="card" style="margin-top:1rem;">
          <div class="card-title">H-Index Decomposition <span class="claim-tag">Claim 8</span></div>
          <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:1rem;margin-bottom:1rem;">
            <div style="text-align:center;">
              <div style="font-size:0.7rem;color:var(--text-muted);text-transform:uppercase;margin-bottom:4px;">Self-Citations</div>
              <div style="font-size:1.4rem;font-weight:800;color:${decomp.selfRatio > 0.30 ? '#f43f5e' : 'var(--text-primary)'};">${(decomp.selfRatio * 100).toFixed(1)}%</div>
              <div style="font-size:0.7rem;color:var(--text-muted);">${decomp.totalSelf} of ${decomp.totalCitations}</div>
              <div class="metric-bar" style="margin-top:6px;"><div class="metric-fill" style="width:${decomp.selfRatio * 100}%;background:${decomp.selfRatio > 0.30 ? '#f43f5e' : 'var(--accent-blue)'};"></div></div>
            </div>
            <div style="text-align:center;">
              <div style="font-size:0.7rem;color:var(--text-muted);text-transform:uppercase;margin-bottom:4px;">Co-Author Cites</div>
              <div style="font-size:1.4rem;font-weight:800;color:var(--text-primary);">${(decomp.coAuthorRatio * 100).toFixed(1)}%</div>
              <div style="font-size:0.7rem;color:var(--text-muted);">${decomp.totalCoAuthor} of ${decomp.totalCitations}</div>
              <div class="metric-bar" style="margin-top:6px;"><div class="metric-fill" style="width:${decomp.coAuthorRatio * 100}%;background:var(--accent-purple);"></div></div>
            </div>
            <div style="text-align:center;">
              <div style="font-size:0.7rem;color:var(--text-muted);text-transform:uppercase;margin-bottom:4px;">Same-Institution</div>
              <div style="font-size:1.4rem;font-weight:800;color:var(--text-primary);">${(decomp.sameInstRatio * 100).toFixed(1)}%</div>
              <div style="font-size:0.7rem;color:var(--text-muted);">${decomp.totalSameInst} of ${decomp.totalCitations}</div>
              <div class="metric-bar" style="margin-top:6px;"><div class="metric-fill" style="width:${decomp.sameInstRatio * 100}%;background:var(--accent-cyan);"></div></div>
            </div>
            <div style="text-align:center;">
              <div style="font-size:0.7rem;color:var(--text-muted);text-transform:uppercase;margin-bottom:4px;">Independent</div>
              <div style="font-size:1.4rem;font-weight:800;color:${decomp.cir < 0.30 ? '#f43f5e' : '#10b981'};">${(decomp.independentRatio * 100).toFixed(1)}%</div>
              <div style="font-size:0.7rem;color:var(--text-muted);">${decomp.totalIndependent} of ${decomp.totalCitations}</div>
              <div class="metric-bar" style="margin-top:6px;"><div class="metric-fill" style="width:${decomp.independentRatio * 100}%;background:${decomp.cir < 0.30 ? '#f43f5e' : '#10b981'};"></div></div>
            </div>
          </div>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;">
            <div style="padding:0.75rem;background:rgba(59,130,246,0.06);border-radius:6px;font-size:0.82rem;color:var(--text-secondary);">
              <strong>Standard h-index:</strong> ${decomp.hIndex}<br>
              <strong>h-index without self-cites:</strong> ${decomp.hIndexWithoutSelf}<br>
              <strong>Inflation due to self-citation:</strong> <span style="color:${decomp.hIndexInflation > 3 ? '#f43f5e' : '#10b981'};font-weight:700;">${decomp.hIndexInflation}</span>
            </div>
            <div style="padding:0.75rem;background:rgba(59,130,246,0.06);border-radius:6px;font-size:0.82rem;color:var(--text-secondary);">
              <strong>Citation Independence Ratio (CIR):</strong> <span style="color:${decomp.cir < 0.30 ? '#f43f5e' : '#10b981'};font-weight:700;">${decomp.cir.toFixed(4)}</span><br>
              <strong>Formula:</strong> independent(${decomp.totalIndependent}) / total(${decomp.totalCitations})<br>
              <strong>Threshold:</strong> ${decomp.cir < 0.30 ? '<span style="color:#f43f5e;">BELOW 0.30 — HIGH RISK</span>' : '<span style="color:#10b981;">Acceptable (≥ 0.30)</span>'}
            </div>
          </div>
        </div>
      `;
    };
  }, []);

  return (
    <div dangerouslySetInnerHTML={{ __html: `
<header class="header">
    <div class="header-inner">
        <div class="logo"><div class="logo-icon">AX</div> ARICCA-X</div>
        <nav class="top-module-nav">
            <a href="/dashboard" class="module-link">Venue Intelligence</a>
            <a href="/dashboard/researcher" class="module-link active">Researcher Auditing</a>
            <a href="/dashboard/peer-review" class="module-link">Peer-Review Forensics</a>
            <a href="/dashboard/grant-compliance" class="module-link">Grant Compliance</a>
        </nav>
        <div style="display:flex;align-items:center;">
            <span class="patent-badge">Patent Pending (14 Claims)</span>
            <button class="btn" style="margin-left:15px;padding:6px 14px;font-size:0.75rem;" onclick="window.location.href='/'">Logout</button>
        </div>
    </div>
</header>

<div class="main">
    <div class="hero-banner">
        <h1>Module B: Researcher Auditing Engine</h1>
        <p>Deterministic citation ring detection via bounded DFS, citation concentration ratio analysis, and h-index inflation forensics via self-citation decomposition.</p>
        <div class="innovation-chips">
            <span class="innovation-chip chip-adw">Claim 6: Bounded DFS Ring Detection</span>
            <span class="innovation-chip chip-csad">Claim 7: ORCID Cross-Database Triangulation</span>
            <span class="innovation-chip chip-gta">Claim 8: H-Index Self-Citation Decomposition</span>
        </div>
    </div>

    <div class="card" style="margin-top:1.5rem;">
        <div class="card-title">Target Author</div>
        <div class="input-group">
            <label>Author Name (must match exactly as used in citation edges below)</label>
            <input type="text" id="targetAuthor" value="AuthorA" placeholder="e.g. AuthorA">
        </div>
    </div>

    <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-top:1rem;">
        <div class="card">
            <div class="card-title">Citation Edge Data <span class="claim-tag">Claim 6 Input</span></div>
            <div style="font-size:0.75rem;color:var(--text-muted);margin-bottom:8px;">
                Format: <code>FromAuthor -> ToAuthor : count @ date</code> (one per line)
            </div>
            <textarea id="citationEdges" style="min-height:220px;font-family:'JetBrains Mono',monospace;font-size:0.78rem;">AuthorA -> AuthorB : 8 @ 2025-03-15
AuthorB -> AuthorA : 12 @ 2025-04-02
AuthorB -> AuthorC : 3 @ 2025-05-10
AuthorC -> AuthorA : 6 @ 2025-04-20
AuthorD -> AuthorA : 2 @ 2024-11-01
AuthorA -> AuthorC : 5 @ 2025-06-01
AuthorC -> AuthorB : 4 @ 2025-03-28
AuthorE -> AuthorA : 1 @ 2024-08-15
AuthorA -> AuthorD : 2 @ 2025-01-10
AuthorD -> AuthorB : 3 @ 2025-02-20
AuthorB -> AuthorD : 2 @ 2025-07-01</textarea>
        </div>

        <div class="card">
            <div class="card-title">Publication Data <span class="claim-tag">Claim 8 Input</span></div>
            <div style="font-size:0.75rem;color:var(--text-muted);margin-bottom:8px;">
                Format: <code>Title | totalCites | selfCites | coAuthorCites | sameInstCites</code>
            </div>
            <textarea id="publicationData" style="min-height:220px;font-family:'JetBrains Mono',monospace;font-size:0.78rem;">Adaptive Weighting for Venue Assessment | 45 | 12 | 8 | 5
Cross-Signal Anomaly Detection Methods | 32 | 9 | 6 | 4
Temporal Fingerprinting in Research | 28 | 7 | 5 | 3
NLP-Based Tense Classification System | 19 | 8 | 4 | 2
Citation Graph Analysis Techniques | 15 | 6 | 3 | 1
Deep Learning for Text Classification | 12 | 4 | 2 | 1
Web Structure Mining for Credibility | 8 | 3 | 2 | 1
Deterministic Pipeline Architecture | 5 | 2 | 1 | 0</textarea>
        </div>
    </div>

    <div style="margin-top:1rem;">
        <button class="btn btn-primary" onclick="window.runCitationAnalysis()">Execute Researcher Audit (Claims 6 + 8)</button>
    </div>

    <div id="researcherResults"></div>
</div>
    `}} />
  );
}
