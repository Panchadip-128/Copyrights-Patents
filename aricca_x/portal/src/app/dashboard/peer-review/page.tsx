"use client";
import { useEffect } from 'react';

export default function PeerReviewForensics() {
  useEffect(() => {
    window.runReviewAnalysis = function() {
      const reviewText = (document.getElementById('reviewText') as HTMLTextAreaElement)?.value?.trim();
      const resultsDiv = document.getElementById('reviewResults');
      if (!resultsDiv || !reviewText) return;

      // Deterministic linguistic feature extraction
      const sentences = reviewText.split(/[.!?]+/).filter((s: string) => s.trim().length > 0);
      const words = reviewText.split(/\s+/);
      const wordCount = words.length;
      const sentenceCount = sentences.length;

      // Sentence length variance
      const sentLengths = sentences.map((s: string) => s.trim().split(/\s+/).length);
      const avgSentLen = sentLengths.reduce((a: number, b: number) => a + b, 0) / sentLengths.length;
      const sentLenVariance = sentLengths.reduce((a: number, b: number) => a + Math.pow(b - avgSentLen, 2), 0) / sentLengths.length;
      const sentLenCV = Math.sqrt(sentLenVariance) / (avgSentLen || 1);

      // Hedging phrases
      const hedgingPatterns = ['it seems', 'perhaps', 'might consider', 'could be', 'may want', 'it appears', 'possibly', 'somewhat', 'to some extent', 'arguably'];
      const hedgingCount = hedgingPatterns.reduce((count: number, p: string) => count + (reviewText.toLowerCase().split(p).length - 1), 0);
      const hedgingDensity = (hedgingCount / wordCount) * 100;

      // Specificity score
      const specificPatterns = /(?:equation|table|figure|fig\.|section|page|line|theorem|lemma|algorithm|step)\s*\d+/gi;
      const specificMatches = reviewText.match(specificPatterns) || [];
      const specificityScore = specificMatches.length / (sentenceCount || 1);

      // Formulaic transitions
      const formulaicPatterns = ['however', 'moreover', 'furthermore', 'additionally', 'in conclusion', 'overall', 'in summary', 'to summarize', 'nevertheless', 'consequently'];
      const formulaicCount = formulaicPatterns.reduce((count: number, p: string) => count + (reviewText.toLowerCase().split(p).length - 1), 0);
      const formulaicDensity = (formulaicCount / wordCount) * 1000;

      // Lexical diversity
      const uniqueWords = new Set(words.map((w: string) => w.toLowerCase().replace(/[^a-z]/g, '')).filter((w: string) => w.length > 2));
      const ttr = uniqueWords.size / (wordCount || 1);

      // Deterministic decision tree
      let riskLevel = 'AUTHENTIC';
      let riskColor = '#10b981';
      const flags: string[] = [];

      if (specificityScore < 0.15 && hedgingDensity > 8.0) {
        riskLevel = 'LIKELY_GENERATED';
        riskColor = '#f43f5e';
        flags.push('Low specificity + high hedging density');
      } else if (sentLenCV < 0.20) {
        riskLevel = 'SUSPICIOUS';
        riskColor = '#f59e0b';
        flags.push('Unnaturally uniform sentence lengths (CV < 0.20)');
      } else if (formulaicDensity > 12.0) {
        riskLevel = 'SUSPICIOUS';
        riskColor = '#f59e0b';
        flags.push('Excessive formulaic transitions');
      }

      if (specificityScore < 0.10) flags.push('No specific manuscript references detected');
      if (hedgingDensity > 5.0 && riskLevel === 'AUTHENTIC') flags.push('Elevated hedging language');
      if (ttr < 0.35) flags.push('Low lexical diversity (possible template text)');

      resultsDiv.innerHTML = \`
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 1rem;">
          <div class="card" style="text-align: center;">
            <div class="card-title" style="justify-content: center;">Review Authenticity Classification <span class="claim-tag">Claim 9</span></div>
            <div style="font-size: 2.5rem; font-weight: 900; color: \${riskColor}; margin: 0.5rem 0;">\${riskLevel}</div>
            <div style="font-size: 0.8rem; color: var(--text-muted);">Deterministic Linguistic Fingerprint</div>
          </div>
          <div class="card">
            <div class="card-title">Flags Detected</div>
            \${flags.length > 0 ? flags.map(f => \`<div style="padding: 6px 10px; margin-bottom: 6px; background: rgba(244,63,94,0.08); border-left: 3px solid #f43f5e; border-radius: 4px; font-size: 0.8rem; color: var(--text-secondary);">\${f}</div>\`).join('') : '<div style="color: #10b981; font-size: 0.85rem;">No anomalies detected. Review appears authentic.</div>'}
          </div>
        </div>

        <div class="card" style="margin-top: 1rem;">
          <div class="card-title">Linguistic Feature Extraction</div>
          <div style="display: grid; grid-template-columns: repeat(5, 1fr); gap: 1rem;">
            <div style="text-align: center;">
              <div style="font-size: 0.7rem; color: var(--text-muted); text-transform: uppercase; margin-bottom: 4px;">Specificity</div>
              <div style="font-size: 1.3rem; font-weight: 800; color: \${specificityScore < 0.15 ? '#f43f5e' : '#10b981'};">\${specificityScore.toFixed(3)}</div>
              <div style="font-size: 0.65rem; color: var(--text-muted);">Threshold: 0.15</div>
            </div>
            <div style="text-align: center;">
              <div style="font-size: 0.7rem; color: var(--text-muted); text-transform: uppercase; margin-bottom: 4px;">Hedging Density</div>
              <div style="font-size: 1.3rem; font-weight: 800; color: \${hedgingDensity > 8.0 ? '#f43f5e' : 'var(--text-primary)'};">\${hedgingDensity.toFixed(2)}</div>
              <div style="font-size: 0.65rem; color: var(--text-muted);">per 100 words</div>
            </div>
            <div style="text-align: center;">
              <div style="font-size: 0.7rem; color: var(--text-muted); text-transform: uppercase; margin-bottom: 4px;">Sentence CV</div>
              <div style="font-size: 1.3rem; font-weight: 800; color: \${sentLenCV < 0.20 ? '#f43f5e' : 'var(--text-primary)'};">\${sentLenCV.toFixed(3)}</div>
              <div style="font-size: 0.65rem; color: var(--text-muted);">Threshold: 0.20</div>
            </div>
            <div style="text-align: center;">
              <div style="font-size: 0.7rem; color: var(--text-muted); text-transform: uppercase; margin-bottom: 4px;">Formulaic Density</div>
              <div style="font-size: 1.3rem; font-weight: 800; color: \${formulaicDensity > 12.0 ? '#f43f5e' : 'var(--text-primary)'};">\${formulaicDensity.toFixed(2)}</div>
              <div style="font-size: 0.65rem; color: var(--text-muted);">per 1000 words</div>
            </div>
            <div style="text-align: center;">
              <div style="font-size: 0.7rem; color: var(--text-muted); text-transform: uppercase; margin-bottom: 4px;">Lexical Diversity</div>
              <div style="font-size: 1.3rem; font-weight: 800; color: \${ttr < 0.35 ? '#f59e0b' : 'var(--text-primary)'};">\${ttr.toFixed(3)}</div>
              <div style="font-size: 0.65rem; color: var(--text-muted);">Type-Token Ratio</div>
            </div>
          </div>
        </div>

        <div class="card" style="margin-top: 1rem;">
          <div class="card-title">Text Statistics</div>
          <div style="font-size: 0.85rem; color: var(--text-secondary); line-height: 1.8;">
            Words: <strong>\${wordCount}</strong> | Sentences: <strong>\${sentenceCount}</strong> | Avg Sentence Length: <strong>\${avgSentLen.toFixed(1)}</strong> words | Unique Words: <strong>\${uniqueWords.size}</strong> | Specific References: <strong>\${specificMatches.length}</strong>
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
            <a href="/dashboard/peer-review" class="module-link active">Peer-Review Forensics</a>
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
        <h1>Module C: Peer-Review Forensics Engine</h1>
        <p>Deterministic detection of AI-generated reviews, reviewer cartels, and sentiment-decision misalignment.</p>
        <div class="innovation-chips">
            <span class="innovation-chip chip-adw">Claim 9: AI-Generated Review Detection</span>
            <span class="innovation-chip chip-csad">Claim 10: Reviewer Cartel Detection</span>
            <span class="innovation-chip chip-gta">Claim 11: Sentiment-Content Alignment</span>
        </div>
    </div>

    <div class="card" style="margin-top: 1.5rem;">
        <div class="card-title">Peer Review Text Input</div>
        <div class="input-group">
            <label>Paste Review Text for Forensic Analysis</label>
            <textarea id="reviewText" style="min-height: 180px;" placeholder="Paste the full peer review text here...">This paper presents an interesting approach to the problem. The methodology seems sound and the results appear promising. However, the authors might consider expanding their discussion section. Additionally, it would be helpful to include more recent references. Furthermore, the experimental setup could be described in more detail. Overall, this is a solid contribution to the field. Nevertheless, some minor revisions would strengthen the manuscript. In summary, I recommend acceptance with minor revisions. The paper could potentially have a significant impact on future research directions.</textarea>
        </div>
        <button class="btn btn-primary" onclick="window.runReviewAnalysis()">Analyze Review Authenticity</button>
    </div>

    <div id="reviewResults"></div>
</div>
    \`}} />
  );
}
