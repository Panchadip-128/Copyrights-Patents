"use client";
import { useEffect } from 'react';

export default function PeerReviewForensics() {
  useEffect(() => {
    // ================================================================
    // CLAIM 9: REAL AI-Generated Review Detection via Deterministic
    //          Linguistic Fingerprinting
    // CLAIM 11: REAL Sentiment-Content Alignment Analysis
    // ================================================================

    (window as any).runReviewAnalysis = function() {
      const reviewText = (document.getElementById('reviewText') as HTMLTextAreaElement)?.value?.trim();
      const recommendation = (document.getElementById('reviewDecision') as HTMLSelectElement)?.value;
      const resultsDiv = document.getElementById('reviewResults');
      if (!resultsDiv || !reviewText) return;

      // ---- REAL FEATURE EXTRACTION ----

      // Tokenize sentences properly (handle abbreviations like "e.g.", "Fig.", "et al.")
      const cleanedText = reviewText.replace(/(?:e\.g\.|i\.e\.|et al\.|Fig\.|Eq\.|Dr\.|Prof\.|vs\.)/g, match => match.replace(/\./g, '@'));
      const sentences = cleanedText.split(/[.!?]+/).map((s: string) => s.trim().replace(/@/g, '.')).filter((s: string) => s.length > 5);
      const words = reviewText.split(/\s+/).filter((w: string) => w.length > 0);
      const wordCount = words.length;
      const sentenceCount = sentences.length;

      // (a)(i) Sentence Length Variance
      const sentLengths = sentences.map((s: string) => s.split(/\s+/).length);
      const avgSentLen = sentLengths.reduce((a: number, b: number) => a + b, 0) / (sentLengths.length || 1);
      const sentLenVariance = sentLengths.reduce((a: number, b: number) => a + Math.pow(b - avgSentLen, 2), 0) / (sentLengths.length || 1);
      const sentLenStdDev = Math.sqrt(sentLenVariance);
      const sentLenCV = sentLenStdDev / (avgSentLen || 1);  // Coefficient of Variation

      // (a)(ii) Hedging Phrase Frequency — comprehensive pattern list
      const hedgingPatterns = [
        'it seems', 'it appears', 'perhaps', 'possibly', 'might consider',
        'could be', 'may want', 'to some extent', 'somewhat', 'arguably',
        'it is possible', 'one might argue', 'it could be argued',
        'there may be', 'this might', 'this could', 'would suggest',
        'tends to', 'appears to', 'seems to', 'likely', 'unlikely',
        'roughly', 'approximately', 'in some cases', 'generally speaking'
      ];
      let hedgingCount = 0;
      const hedgingMatches: string[] = [];
      const lowerText = reviewText.toLowerCase();
      for (const pattern of hedgingPatterns) {
        const matches = lowerText.split(pattern).length - 1;
        if (matches > 0) {
          hedgingCount += matches;
          hedgingMatches.push(`"${pattern}" (×${matches})`);
        }
      }
      const hedgingDensity = (hedgingCount / (wordCount || 1)) * 100;

      // (a)(iii) Specific Criticism Ratio — references to concrete manuscript elements
      const specificPatterns = [
        /(?:equation|eq\.)\s*(?:\(?\d+\)?)/gi,
        /(?:table|tab\.)\s*\d+/gi,
        /(?:figure|fig\.)\s*\d+/gi,
        /(?:section|sec\.)\s*\d+/gi,
        /page\s*\d+/gi,
        /line\s*\d+/gi,
        /(?:theorem|lemma|proposition|corollary)\s*\d+/gi,
        /(?:algorithm|step)\s*\d+/gi,
        /(?:chapter)\s*\d+/gi,
        /(?:appendix)\s*[A-Z]/gi
      ];
      let specificCount = 0;
      const specificMatches: string[] = [];
      for (const pattern of specificPatterns) {
        const matches = reviewText.match(pattern) || [];
        specificCount += matches.length;
        specificMatches.push(...matches);
      }
      const specificityScore = specificCount / (sentenceCount || 1);

      // (a)(iv) Lexical Diversity — Type-Token Ratio
      const cleanWords = words.map((w: string) => w.toLowerCase().replace(/[^a-z'-]/g, '')).filter((w: string) => w.length > 2);
      const uniqueWords = new Set(cleanWords);
      const ttr = uniqueWords.size / (cleanWords.length || 1);

      // (a)(v) Formulaic Transition Frequency
      const formulaicPatterns = [
        'however', 'moreover', 'furthermore', 'additionally', 'in conclusion',
        'overall', 'in summary', 'to summarize', 'nevertheless', 'consequently',
        'therefore', 'thus', 'hence', 'accordingly', 'in addition',
        'on the other hand', 'in contrast', 'as a result', 'in particular',
        'more specifically', 'that being said', 'having said that'
      ];
      let formulaicCount = 0;
      const formulaicMatches: string[] = [];
      for (const pattern of formulaicPatterns) {
        const matches = lowerText.split(pattern).length - 1;
        if (matches > 0) {
          formulaicCount += matches;
          formulaicMatches.push(`"${pattern}" (×${matches})`);
        }
      }
      const formulaicDensity = (formulaicCount / (wordCount || 1)) * 1000;

      // ---- CLAIM 11: Sentiment-Decision Alignment ----
      const positiveWords = ['excellent', 'outstanding', 'strong', 'solid', 'compelling', 'novel', 'innovative', 'significant', 'important', 'valuable', 'interesting', 'well-written', 'thorough', 'rigorous', 'impressive', 'clear', 'elegant', 'insightful'];
      const negativeWords = ['weak', 'poor', 'lacking', 'insufficient', 'flawed', 'unclear', 'confusing', 'missing', 'inadequate', 'superficial', 'trivial', 'unconvincing', 'problematic', 'wrong', 'incorrect', 'erroneous', 'vague', 'incomplete', 'limited'];

      let posCount = 0, negCount = 0;
      const posMatches: string[] = [], negMatches: string[] = [];
      for (const w of positiveWords) {
        const count = lowerText.split(w).length - 1;
        if (count > 0) { posCount += count; posMatches.push(`"${w}" (×${count})`); }
      }
      for (const w of negativeWords) {
        const count = lowerText.split(w).length - 1;
        if (count > 0) { negCount += count; negMatches.push(`"${w}" (×${count})`); }
      }

      const sentimentTotal = posCount + negCount;
      const sentimentPolarity = sentimentTotal > 0 ? (posCount - negCount) / sentimentTotal : 0;
      // -1.0 = fully negative, +1.0 = fully positive

      const decisionMapping: Record<string, number> = { 'accept': 1, 'minor': 0.5, 'major': -0.5, 'reject': -1 };
      const decisionScore = decisionMapping[recommendation] || 0;
      const misalignment = Math.abs(sentimentPolarity - decisionScore);
      const misalignmentFlag = misalignment > 1.0;

      // ---- CLAIM 9(d): DETERMINISTIC DECISION TREE ----
      const flags: { text: string; severity: string }[] = [];
      let riskLevel = 'AUTHENTIC';
      let riskColor = '#10b981';

      // Rule 1: Low specificity + high hedging = HIGH risk
      if (specificityScore < 0.15 && hedgingDensity > 8.0) {
        riskLevel = 'LIKELY_GENERATED';
        riskColor = '#f43f5e';
        flags.push({ text: `Specificity (${specificityScore.toFixed(3)}) < 0.15 AND Hedging Density (${hedgingDensity.toFixed(2)}) > 8.0`, severity: 'critical' });
      }

      // Rule 2: Unnaturally uniform sentence lengths
      if (sentLenCV < 0.20) {
        if (riskLevel === 'AUTHENTIC') { riskLevel = 'SUSPICIOUS'; riskColor = '#f59e0b'; }
        flags.push({ text: `Sentence length CV (${sentLenCV.toFixed(3)}) < 0.20 — unnaturally uniform (LLMs produce consistent lengths)`, severity: 'high' });
      }

      // Rule 3: Excessive formulaic transitions
      if (formulaicDensity > 12.0) {
        if (riskLevel === 'AUTHENTIC') { riskLevel = 'SUSPICIOUS'; riskColor = '#f59e0b'; }
        flags.push({ text: `Formulaic transition density (${formulaicDensity.toFixed(2)}/1000w) > 12.0 — over-structured text`, severity: 'high' });
      }

      // Rule 4: Zero specific references
      if (specificCount === 0) {
        flags.push({ text: 'No specific manuscript references (equations, tables, figures, sections) detected', severity: 'medium' });
      }

      // Rule 5: Low lexical diversity
      if (ttr < 0.35) {
        flags.push({ text: `Lexical diversity TTR (${ttr.toFixed(3)}) < 0.35 — possible template or generated text`, severity: 'medium' });
      }

      // Rule 6: Sentiment misalignment (Claim 11)
      if (misalignmentFlag) {
        flags.push({ text: `Sentiment-Decision Misalignment: text polarity (${sentimentPolarity.toFixed(2)}) conflicts with recommendation "${recommendation}" (score ${decisionScore})`, severity: 'high' });
      }

      const severityColors: Record<string, string> = { critical: '#f43f5e', high: '#f59e0b', medium: '#eab308', low: '#10b981' };

      resultsDiv.innerHTML = `
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-top:1rem;">
          <div class="card" style="text-align:center;">
            <div class="card-title" style="justify-content:center;">Review Authenticity Classification <span class="claim-tag">Claim 9(f)</span></div>
            <div style="font-size:2.5rem;font-weight:900;color:${riskColor};margin:0.5rem 0;">${riskLevel}</div>
            <div style="font-size:0.8rem;color:var(--text-muted);">Deterministic Decision Tree Output</div>
          </div>
          <div class="card">
            <div class="card-title">Anomaly Flags (${flags.length})</div>
            ${flags.length > 0
              ? flags.map(f => `<div style="padding:6px 10px;margin-bottom:6px;background:rgba(${f.severity === 'critical' ? '244,63,94' : f.severity === 'high' ? '245,158,11' : '234,179,8'},0.08);border-left:3px solid ${severityColors[f.severity]};border-radius:4px;font-size:0.78rem;color:var(--text-secondary);"><span style="color:${severityColors[f.severity]};font-weight:700;text-transform:uppercase;font-size:0.65rem;">${f.severity}</span> ${f.text}</div>`).join('')
              : '<div style="color:#10b981;font-size:0.85rem;">No anomalies detected. Review appears authentically human-written.</div>'}
          </div>
        </div>

        <div class="card" style="margin-top:1rem;">
          <div class="card-title">Linguistic Feature Extraction <span class="claim-tag">Claim 9(a)</span></div>
          <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:1rem;">
            <div style="text-align:center;">
              <div style="font-size:0.68rem;color:var(--text-muted);text-transform:uppercase;margin-bottom:4px;">Specificity Score</div>
              <div style="font-size:1.3rem;font-weight:800;color:${specificityScore < 0.15 ? '#f43f5e' : '#10b981'};">${specificityScore.toFixed(3)}</div>
              <div style="font-size:0.6rem;color:var(--text-muted);">Threshold: 0.15</div>
              <div class="metric-bar" style="margin-top:6px;"><div class="metric-fill" style="width:${Math.min(specificityScore * 300, 100)}%;background:${specificityScore < 0.15 ? '#f43f5e' : '#10b981'};"></div></div>
            </div>
            <div style="text-align:center;">
              <div style="font-size:0.68rem;color:var(--text-muted);text-transform:uppercase;margin-bottom:4px;">Hedging Density</div>
              <div style="font-size:1.3rem;font-weight:800;color:${hedgingDensity > 8.0 ? '#f43f5e' : 'var(--text-primary)'};">${hedgingDensity.toFixed(2)}</div>
              <div style="font-size:0.6rem;color:var(--text-muted);">per 100 words (thresh: 8.0)</div>
              <div class="metric-bar" style="margin-top:6px;"><div class="metric-fill" style="width:${Math.min(hedgingDensity * 10, 100)}%;background:${hedgingDensity > 8.0 ? '#f43f5e' : 'var(--accent-blue)'};"></div></div>
            </div>
            <div style="text-align:center;">
              <div style="font-size:0.68rem;color:var(--text-muted);text-transform:uppercase;margin-bottom:4px;">Sentence CV</div>
              <div style="font-size:1.3rem;font-weight:800;color:${sentLenCV < 0.20 ? '#f43f5e' : 'var(--text-primary)'};">${sentLenCV.toFixed(3)}</div>
              <div style="font-size:0.6rem;color:var(--text-muted);">Threshold: 0.20</div>
              <div class="metric-bar" style="margin-top:6px;"><div class="metric-fill" style="width:${Math.min(sentLenCV * 200, 100)}%;background:${sentLenCV < 0.20 ? '#f43f5e' : 'var(--accent-blue)'};"></div></div>
            </div>
            <div style="text-align:center;">
              <div style="font-size:0.68rem;color:var(--text-muted);text-transform:uppercase;margin-bottom:4px;">Formulaic Density</div>
              <div style="font-size:1.3rem;font-weight:800;color:${formulaicDensity > 12.0 ? '#f43f5e' : 'var(--text-primary)'};">${formulaicDensity.toFixed(2)}</div>
              <div style="font-size:0.6rem;color:var(--text-muted);">per 1000w (thresh: 12.0)</div>
              <div class="metric-bar" style="margin-top:6px;"><div class="metric-fill" style="width:${Math.min(formulaicDensity * 5, 100)}%;background:${formulaicDensity > 12.0 ? '#f43f5e' : 'var(--accent-blue)'};"></div></div>
            </div>
            <div style="text-align:center;">
              <div style="font-size:0.68rem;color:var(--text-muted);text-transform:uppercase;margin-bottom:4px;">Lexical Diversity</div>
              <div style="font-size:1.3rem;font-weight:800;color:${ttr < 0.35 ? '#f59e0b' : 'var(--text-primary)'};">${ttr.toFixed(3)}</div>
              <div style="font-size:0.6rem;color:var(--text-muted);">TTR (thresh: 0.35)</div>
              <div class="metric-bar" style="margin-top:6px;"><div class="metric-fill" style="width:${ttr * 100}%;background:${ttr < 0.35 ? '#f59e0b' : 'var(--accent-blue)'};"></div></div>
            </div>
          </div>
        </div>

        <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-top:1rem;">
          <div class="card">
            <div class="card-title">Sentiment-Decision Alignment <span class="claim-tag">Claim 11</span></div>
            <div style="font-size:0.82rem;color:var(--text-secondary);line-height:1.8;">
              <strong>Positive signals:</strong> ${posCount} ${posMatches.length > 0 ? `(${posMatches.slice(0, 5).join(', ')})` : ''}<br>
              <strong>Negative signals:</strong> ${negCount} ${negMatches.length > 0 ? `(${negMatches.slice(0, 5).join(', ')})` : ''}<br>
              <strong>Sentiment Polarity:</strong> <span style="font-weight:700;">${sentimentPolarity.toFixed(3)}</span> (range: -1.0 to +1.0)<br>
              <strong>Recommendation:</strong> "${recommendation}" (score: ${decisionScore})<br>
              <strong>Misalignment:</strong> <span style="color:${misalignmentFlag ? '#f43f5e' : '#10b981'};font-weight:700;">${misalignment.toFixed(3)}</span> ${misalignmentFlag ? '— MISALIGNED' : '— Consistent'}
            </div>
          </div>
          <div class="card">
            <div class="card-title">Detected Pattern Evidence</div>
            <div style="font-size:0.78rem;color:var(--text-secondary);line-height:1.6;">
              <strong>Hedging phrases found:</strong> ${hedgingMatches.length > 0 ? hedgingMatches.join(', ') : 'None'}<br><br>
              <strong>Formulaic transitions:</strong> ${formulaicMatches.length > 0 ? formulaicMatches.join(', ') : 'None'}<br><br>
              <strong>Specific references:</strong> ${specificMatches.length > 0 ? specificMatches.join(', ') : 'None detected'}
            </div>
          </div>
        </div>

        <div class="card" style="margin-top:1rem;">
          <div class="card-title">Raw Statistics</div>
          <div style="font-size:0.82rem;color:var(--text-secondary);line-height:1.8;">
            Words: <strong>${wordCount}</strong> | Sentences: <strong>${sentenceCount}</strong> | Avg Sentence Length: <strong>${avgSentLen.toFixed(1)}</strong> | Std Dev: <strong>${sentLenStdDev.toFixed(2)}</strong> | Unique Words: <strong>${uniqueWords.size}</strong>/${cleanWords.length}
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
            <a href="/dashboard/researcher" class="module-link">Researcher Auditing</a>
            <a href="/dashboard/peer-review" class="module-link active">Peer-Review Forensics</a>
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
        <h1>Module C: Peer-Review Forensics Engine</h1>
        <p>Deterministic detection of AI-generated reviews via linguistic fingerprinting and sentiment-decision alignment analysis. All features are computed from actual input text — no simulations.</p>
        <div class="innovation-chips">
            <span class="innovation-chip chip-adw">Claim 9: Deterministic Linguistic Fingerprinting</span>
            <span class="innovation-chip chip-csad">Claim 10: Reviewer Cartel Detection</span>
            <span class="innovation-chip chip-gta">Claim 11: Sentiment-Decision Alignment</span>
        </div>
    </div>

    <div class="card" style="margin-top:1.5rem;">
        <div class="card-title">Peer Review Input</div>
        <div class="input-group">
            <label>Paste the complete peer review text</label>
            <textarea id="reviewText" style="min-height:200px;" placeholder="Paste the full peer review text here...">This paper presents an interesting approach to the problem. The methodology seems sound and the results appear promising. However, the authors might consider expanding their discussion section. Additionally, it would be helpful to include more recent references. Furthermore, the experimental setup could be described in more detail. Overall, this is a solid contribution to the field. Nevertheless, some minor revisions would strengthen the manuscript. In summary, I recommend acceptance with minor revisions. The paper could potentially have a significant impact on future research directions.</textarea>
        </div>
        <div class="input-group">
            <label>Reviewer's Recommendation</label>
            <select id="reviewDecision">
                <option value="accept">Accept</option>
                <option value="minor" selected>Minor Revisions</option>
                <option value="major">Major Revisions</option>
                <option value="reject">Reject</option>
            </select>
        </div>
        <button class="btn btn-primary" onclick="window.runReviewAnalysis()">Analyze Review Authenticity (Claims 9 + 11)</button>
    </div>

    <div id="reviewResults"></div>
</div>
    `}} />
  );
}
