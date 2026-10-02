"use client";
import { useEffect, useRef } from 'react';

export default function Home() {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Inject the raw JS logic into window scope so inline onclick handlers work
    const script = document.createElement('script');
    script.innerHTML = `
// ============================================================
// AUTHENTICATION LOGIC
// ============================================================
function toggleAuth(mode) {
    document.getElementById('login-box').style.display = mode === 'login' ? 'block' : 'none';
    document.getElementById('signup-box').style.display = mode === 'signup' ? 'block' : 'none';
}

window.handleLogin = function(e) {
    e.preventDefault();
    const email = document.getElementById('login-email').value;
    const pwd = document.getElementById('login-pwd').value;
    const err = document.getElementById('login-error');
    const badge = document.getElementById('role-badge');
    
    if(email === 'admin@aricca.com' && pwd === 'admin123') {
        err.style.display = 'none';
        document.getElementById('auth-container').style.display = 'none';
        document.getElementById('app-container').style.display = 'block';
        badge.style.display = 'inline-block';
        badge.innerText = 'ADMIN';
        badge.style.background = 'var(--accent-rose)';
    } else if(email === 'user@aricca.com' && pwd === 'user123') {
        err.style.display = 'none';
        document.getElementById('auth-container').style.display = 'none';
        document.getElementById('app-container').style.display = 'block';
        badge.style.display = 'inline-block';
        badge.innerText = 'USER';
        badge.style.background = 'var(--accent-blue)';
    } else {
        err.style.display = 'block';
    }
};

function logout() {
    document.getElementById('app-container').style.display = 'none';
    document.getElementById('auth-container').style.display = 'flex';
    document.getElementById('login-form').reset();
    document.getElementById('login-error').style.display = 'none';
}

// ============================================================
// ARICCA-X UI Engine — Client-side implementation of all
// patent-pending algorithms for demonstration purposes
// ============================================================

// Icon SVG Definition Helpers
const ICONS = {
    check: '<svg class="icon-sm icon-success" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>',
    x: '<svg class="icon-sm icon-error" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>',
    alert: '<svg class="icon-sm icon-warning" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>',
    info: '<svg class="icon-sm icon-info" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>'
};

// Tab Navigation
document.querySelectorAll('.nav-tab').forEach(tab => {
    tab.addEventListener('click', () => {
        document.querySelectorAll('.nav-tab').forEach(t => t.classList.remove('active'));
        document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
        tab.classList.add('active');
        document.getElementById('panel' + capitalize(tab.dataset.tab)).classList.add('active');
    });
});
function capitalize(s) { return s.charAt(0).toUpperCase() + s.slice(1); }

// ============================================================
// CLAIM 3: Grammatical Tense Analysis (GTA)
// ============================================================
function classifyClaimTense(text) {
    const lower = text.toLowerCase();
    const conditional = [
        /\b(?:may|might|could|would)\s+(?:be\s+)?(?:indexed|included|listed|submitted)/,
        /\b(?:possibly|potentially)\s+(?:indexed|included)/,
        /\bsubject\s+to\s+(?:indexing|inclusion|approval)/
    ];
    for (const p of conditional) if (p.test(lower)) return 'conditional';
    const future = [
        /\b(?:will|shall|going\s+to)\s+(?:be\s+)?(?:indexed|included|submitted|listed)/,
        /\b(?:planning|aiming|intending)\s+to\s+(?:submit|apply|index)/,
        /\bto\s+be\s+(?:indexed|submitted|included)/,
        /\bapplied?\s+for\s+(?:indexing|inclusion)/,
        /\bunder\s+(?:review|consideration|evaluation)\s+for/
    ];
    for (const p of future) if (p.test(lower)) return 'future';
    const past = [
        /\b(?:was|were|has\s+been|had\s+been)\s+(?:indexed|included|listed)/,
        /\bindexed\s+(?:in|by)\s+\w+\s+since\s+\d{4}/
    ];
    for (const p of past) if (p.test(lower)) return 'past';
    const present = [
        /\b(?:is|are)\s+(?:indexed|included|listed|covered|abstracted)/,
        /\bcurrently\s+(?:indexed|included|listed)/,
        /\bindexed\s+(?:in|by)\b/
    ];
    for (const p of present) if (p.test(lower)) return 'present';
    return 'unknown';
}

const TENSE_RISK = { past: -0.05, present: 0.0, future: 0.25, conditional: 0.30, unknown: 0.05 };
const TENSE_COLORS = { past: '#60a5fa', present: '#34d399', future: '#fb923c', conditional: '#f87171', unknown: '#94a3b8' };

function runTenseAnalysis() {
    const lines = document.getElementById('tenseInput').value.split('\n').filter(l => l.trim());
    const results = lines.map(line => ({ text: line.trim(), tense: classifyClaimTense(line), risk: 0 }));
    results.forEach(r => r.risk = TENSE_RISK[r.tense]);

    const counts = { past: 0, present: 0, future: 0, conditional: 0, unknown: 0 };
    results.forEach(r => counts[r.tense]++);

    let html = '';
    results.forEach(r => {
        html += \`<div style="display:flex;align-items:center;gap:10px;padding:10px;border-bottom:1px solid rgba(42,54,84,0.4);">
            <span class="tense-tag tense-\${r.tense}">\${r.tense}</span>
            <span style="flex:1;font-size:0.82rem;">\${escHtml(r.text)}</span>
            <span style="font-family:'JetBrains Mono';font-size:0.75rem;color:\${r.risk > 0 ? 'var(--accent-rose)' : r.risk < 0 ? 'var(--accent-emerald)' : 'var(--text-muted)'}">
                \${r.risk > 0 ? '+' : ''}\${r.risk.toFixed(2)}
            </span>
        </div>\`;
    });
    document.getElementById('tenseResults').innerHTML = html;

    // Distribution
    const total = results.length;
    let distHtml = '<div style="display:flex;gap:12px;flex-wrap:wrap;">';
    for (const [tense, count] of Object.entries(counts)) {
        const pct = total > 0 ? (count / total * 100).toFixed(0) : 0;
        distHtml += \`<div style="flex:1;min-width:80px;text-align:center;padding:12px;background:var(--bg-input);border-radius:var(--radius-sm);border:1px solid var(--border);">
            <div style="font-size:1.5rem;font-weight:800;color:\${TENSE_COLORS[tense]}">\${count}</div>
            <div style="font-size:0.7rem;color:var(--text-muted);text-transform:uppercase;">\${tense}</div>
            <div style="font-size:0.7rem;color:var(--text-muted);">\${pct}%</div>
        </div>\`;
    }
    distHtml += '</div>';
    const suspiciousCount = counts.future + counts.conditional;
    if (suspiciousCount > 0) {
        distHtml += \`<div class="flag-item flag-warning" style="margin-top:12px;">
            \${ICONS.alert}
            <div>
                <strong>\${suspiciousCount} claim\${suspiciousCount > 1 ? 's' : ''}</strong> utilize conditional or future tense paradigms.<br>
                This represents a robust grammatical indicator associated with deceptive venue indexing claims.
            </div>
        </div>\`;
    }
    document.getElementById('tenseDistribution').innerHTML = distHtml;
}

// ============================================================
// CFP ANALYSIS ENGINE
// ============================================================
function analyzeCFP(text) {
    const lower = text.toLowerCase();
    const urgencyPatterns = [/\b(hurry|urgent|limited|extended|last\s+chance|final\s+call)\b/gi,
        /\b(don't\s+miss|act\s+now|immediate|quick|fast\s+track)\b/gi,
        /\b(ends\s+soon|running\s+out|limited\s+time|submit\s+now)\b/gi];
    const suspiciousPatterns = [/\b(guaranteed\s+acceptance|100%\s+acceptance|no\s+rejection)\b/gi,
        /\b(pay\s+first|payment\s+required|fee\s+mandatory)\b/gi,
        /\b(all\s+papers\s+accepted|every\s+paper\s+published)\b/gi,
        /\b(easy\s+acceptance|quick\s+publication|fast\s+track\s+publication)\b/gi];
    let urgency = [], suspicious = [];
    urgencyPatterns.forEach(p => { let m; while ((m = p.exec(text)) !== null) urgency.push(m[0]); });
    suspiciousPatterns.forEach(p => { let m; while ((m = p.exec(text)) !== null) suspicious.push(m[0]); });
    urgency = [...new Set(urgency)]; suspicious = [...new Set(suspicious)];

    // Syntax score
    const sentences = text.split(/[.!?]+/).filter(s => s.trim());
    const avgLen = sentences.length > 0 ? sentences.reduce((s, x) => s + x.trim().split(/\s+/).length, 0) / sentences.length : 0;
    let lenScore = avgLen >= 5 && avgLen <= 40 ? 1.0 : 0.5;
    let capScore = sentences.length > 0 ? sentences.filter(s => s.trim()[0] && s.trim()[0] === s.trim()[0].toUpperCase()).length / sentences.length : 0;
    let syntaxScore = lenScore * 0.3 + capScore * 0.4 + 0.3;

    // Professionalism
    const posKw = ['peer-review', 'double-blind', 'committee', 'proceedings', 'indexing'];
    const negKw = ['cheap', 'easy', 'quick', 'guaranteed', 'no-rejection'];
    let posCount = posKw.reduce((s, k) => s + (lower.split(k).length - 1), 0);
    let negCount = negKw.reduce((s, k) => s + (lower.split(k).length - 1), 0);
    let profScore = (posCount + negCount) > 0 ? Math.max(0, Math.min(posCount / (posCount + negCount + 1) - negCount * 0.1, 1)) : 0.5;

    // Contact legitimacy
    let contactScore = 0.5;
    if (/(@[\w.-]+\.edu|@[\w.-]+\.ac\.[a-z]{2})/.test(text)) contactScore += 0.3;
    if (/@(gmail|yahoo|hotmail|outlook)\.com/.test(lower)) contactScore -= 0.2;
    contactScore = Math.max(0, Math.min(contactScore, 1));

    // Language quality
    let langQuality = 1.0;
    langQuality -= Math.min((text.match(/[!?]{2,}/g) || []).length / Math.max(text.length, 1) * 10, 0.3);
    const words = text.split(/\s+/);
    langQuality -= Math.min(words.filter(w => w.length > 2 && w === w.toUpperCase()).length / Math.max(words.length, 1) * 0.5, 0.3);
    langQuality = Math.max(0, langQuality);

    // Overall risk
    let risk = Math.min(1,
        (urgency.length / 10) * 0.20 +
        Math.min(suspicious.length * 0.15, 0.40) +
        (1 - syntaxScore) * 0.10 +
        (1 - profScore) * 0.15 +
        (1 - langQuality) * 0.10 +
        (1 - contactScore) * 0.15
    );

    return { urgency, suspicious, syntaxScore, profScore, contactScore, langQuality, risk };
}

// ============================================================
// CLAIM 1: Adaptive Decay Weighting
// ============================================================
const BASE_WEIGHTS = {
    cfp_risk: 0.25, website_credibility: 0.20, indexing_credibility: 0.20,
    contact_legitimacy: 0.15, organizational_structure: 0.10, publication_history: 0.10
};

function computeAdaptiveWeights(availability) {
    let avail = 0, absent = 0;
    for (const [k, v] of Object.entries(availability)) {
        if (v) avail += BASE_WEIGHTS[k]; else absent += BASE_WEIGHTS[k];
    }
    const eff = {};
    for (const [k, v] of Object.entries(availability)) {
        eff[k] = v && avail > 0 ? BASE_WEIGHTS[k] + (BASE_WEIGHTS[k] / avail) * absent : 0;
    }
    return eff;
}

// ============================================================
// CLAIM 2: Cross-Signal Anomaly Detection
// ============================================================
const CORR_PAIRS = [
    ['cfp_risk', 'website_credibility', 'quality_mismatch'],
    ['cfp_risk', 'contact_legitimacy', 'quality_mismatch'],
    ['website_credibility', 'indexing_credibility', 'claim_contradiction'],
    ['indexing_credibility', 'organizational_structure', 'claim_contradiction'],
    ['contact_legitimacy', 'organizational_structure', 'quality_mismatch']
];
const ANOMALY_THRESHOLD = 0.40;

function detectCrossSignalAnomalies(credScores, availability) {
    const anomalies = [];
    for (const [a, b, type] of CORR_PAIRS) {
        if (!availability[a] || !availability[b]) continue;
        const div = Math.abs(credScores[a] - credScores[b]);
        if (div > ANOMALY_THRESHOLD) {
            anomalies.push({ signalA: a, valA: credScores[a], signalB: b, valB: credScores[b],
                divergence: div, type, amplification: (div - ANOMALY_THRESHOLD) * 0.3 });
        }
    }
    return anomalies;
}

// ============================================================
// HEURISTIC EVALUATOR
// ============================================================
function evaluateHeuristics(cfp, website, hasFingerprint) {
    const results = [];
    // H1: Acceptance rate
    const accSusp = cfp.suspicious.some(s => /acceptance|guarantee/i.test(s));
    results.push({ name: 'Acceptance Rate Constraints', passed: !accSusp, importance: 'critical', impact: accSusp ? 0.3 : 0, evidence: accSusp ? 'Questionable acceptance assertions identified' : 'Within normal operational limits' });
    // H2: Urgency
    const exUrg = cfp.urgency.length > 3;
    results.push({ name: 'Urgency Threshold', passed: !exUrg, importance: 'medium', impact: exUrg ? 0.15 : 0, evidence: exUrg ? \`Metric exceeded: \${cfp.urgency.length} urgency indicators found\` : 'Below critical threshold' });
    // H3: Website
    const ssl = document.getElementById('toggleSSL').classList.contains('on');
    const contact = document.getElementById('toggleContact').classList.contains('on');
    const pages = parseInt(document.getElementById('venuePages').value) || 0;
    const webOk = ssl && contact && pages >= 5;
    const webEvidence = [];
    if (!ssl) webEvidence.push('SSL protocol missing'); if (!contact) webEvidence.push('Contact endpoint unavailable');
    if (pages < 5) webEvidence.push(\`Insufficient structure depth (\${pages} pages)\`);
    results.push({ name: 'Infrastructure Quality', passed: webOk, importance: 'high', impact: webOk ? 0 : 0.2, evidence: webOk ? 'Conforms to baseline requirements' : webEvidence.join(', ') });
    // H4: Indexing
    results.push({ name: 'Indexing Claim Verification', passed: !hasFingerprint, importance: 'high', impact: hasFingerprint ? 0.25 : 0, evidence: hasFingerprint ? 'Claims lack cryptographic verification' : 'No claims require verification' });
    // H5: Contact
    const noAcadEmail = /@(gmail|yahoo|hotmail|outlook)\.com/.test(document.getElementById('cfpText').value);
    results.push({ name: 'Contact Endpoint Validation', passed: !noAcadEmail, importance: 'medium', impact: noAcadEmail ? 0.15 : 0, evidence: noAcadEmail ? 'Non-institutional email provider used' : 'Verified institutional provider' });
    // H6: Fee prominence
    const feeSusp = cfp.suspicious.some(s => /fee|payment/i.test(s));
    results.push({ name: 'Economic Emphasis Check', passed: !feeSusp, importance: 'medium', impact: feeSusp ? 0.1 : 0, evidence: feeSusp ? 'Disproportionate financial focus' : 'Nominal financial phrasing' });
    // H7: Speed claims
    const speedClaims = ['fast publication', 'quick publication', 'rapid publication', 'fast track'].some(s => cfp.text && cfp.text.toLowerCase().includes(s));
    results.push({ name: 'Processing Speed Assurances', passed: !speedClaims, importance: 'low', impact: speedClaims ? 0.1 : 0, evidence: speedClaims ? 'Anomalous processing speed claims' : 'Standard processing timeframes implied' });
    return results;
}

// ============================================================
// FULL VENUE ANALYSIS PIPELINE (Claim 5: 6-phase)
// ============================================================
async function runVenueAnalysis() {
    const phases = document.querySelectorAll('.phase-step');
    phases.forEach(p => { p.classList.remove('complete', 'active'); });
    document.getElementById('pipelineEmpty').style.display = 'none';
    document.getElementById('resultCards').style.display = 'none';
    document.getElementById('adwCard').style.display = 'none';
    document.getElementById('csadCard').style.display = 'none';
    document.getElementById('heuristicsCard').style.display = 'none';
    document.getElementById('flagsRecsRow').style.display = 'none';

    const cfpText = document.getElementById('cfpText').value;
    const ssl = document.getElementById('toggleSSL').classList.contains('on');
    const contactPage = document.getElementById('toggleContact').classList.contains('on');
    const aboutPage = document.getElementById('toggleAbout').classList.contains('on');
    const pages = parseInt(document.getElementById('venuePages').value) || 0;
    const hasFingerprint = document.getElementById('toggleFingerprint').classList.contains('on');
    const url = document.getElementById('venueUrl').value;
    const hasSSLFromUrl = url.startsWith('https');

    // ---- PHASE 1: Component Scoring ----
    await animatePhase(0);
    const cfp = analyzeCFP(cfpText);
    cfp.text = cfpText;
    const webCred = (ssl ? 0.15 : 0) + (contactPage ? 0.15 : 0) + (aboutPage ? 0.10 : 0) +
        (pages >= 5 ? 0.10 : 0) + (pages >= 10 ? 0.05 : 0);
    const scores = {
        cfp_risk: cfp.risk,
        website_credibility: Math.min(webCred + 0.1, 1),
        indexing_credibility: hasFingerprint ? 0.35 : 0.5,
        contact_legitimacy: cfp.contactScore,
        organizational_structure: (aboutPage ? 0.3 : 0) + (pages > 5 ? 0.2 : 0) + 0.3,
        publication_history: 0.5
    };
    const availability = {
        cfp_risk: true, website_credibility: true,
        indexing_credibility: hasFingerprint,
        contact_legitimacy: true, organizational_structure: true,
        publication_history: false
    };
    const effWeights = computeAdaptiveWeights(availability);
    const dataCompleteness = Object.values(availability).filter(v => v).length / Object.keys(availability).length;
    const absentCount = Object.values(availability).filter(v => !v).length;

    await animatePhase(0, true);

    // ---- PHASE 2: Heuristic Evaluation ----
    await animatePhase(1);
    const heuristics = evaluateHeuristics(cfp, { ssl, contactPage, pages }, hasFingerprint);
    await animatePhase(1, true);

    // ---- PHASE 3: Credibility Calculation ----
    await animatePhase(2);
    const credScores = { ...scores, cfp_risk: 1 - scores.cfp_risk };
    const anomalies = detectCrossSignalAnomalies(credScores, availability);
    const anomalyAmp = anomalies.reduce((s, a) => s + a.amplification, 0);
    let totalRisk = 0;
    for (const [k, w] of Object.entries(effWeights)) {
        if (k === 'cfp_risk') totalRisk += scores[k] * w;
        else totalRisk += (1 - scores[k]) * w;
    }
    totalRisk += absentCount * 0.08 + anomalyAmp;
    totalRisk = Math.min(totalRisk, 1);
    // Heuristic credibility
    const impWeights = { critical: 0.25, high: 0.15, medium: 0.10, low: 0.05 };
    let heuristicCred = 1.0;
    heuristics.forEach(h => { if (!h.passed) heuristicCred -= (impWeights[h.importance] || 0.1); });
    heuristicCred = Math.max(0, heuristicCred);
    const componentCred = (1 - scores.cfp_risk) * 0.25 + scores.website_credibility * 0.20 +
        scores.indexing_credibility * 0.20 + scores.contact_legitimacy * 0.15 +
        scores.organizational_structure * 0.10 + scores.publication_history * 0.10;
    const finalCred = componentCred * 0.60 + heuristicCred * 0.40;
    await animatePhase(2, true);

    // ---- PHASE 4: Risk Classification ----
    await animatePhase(3);
    let riskLevel = totalRisk < 0.25 ? 'low' : totalRisk < 0.50 ? 'medium' : totalRisk < 0.75 ? 'high' : 'critical';
    await animatePhase(3, true);

    // ---- PHASE 5: Recommendations ----
    await animatePhase(4);
    const recs = [];
    if (scores.cfp_risk > 0.6) recs.push('CFP structure yields elevated risk index. Secondary verification of indexing assertions is advised.');
    if (scores.website_credibility < 0.4) recs.push('Infrastructure analysis results below standard parameters. Review SSL deployment and page structure.');
    if (scores.indexing_credibility < 0.5 && hasFingerprint) recs.push('Indexing metadata exhibits irregularities. Require cryptographic verification from standard academic databases.');
    if (totalRisk > 0.7) recs.push('CRITICAL CLASSIFICATION: High density of predatory markers identified. Recommendation: Seek alternative academic venue.');
    else if (totalRisk > 0.5) recs.push('ELEVATED RISK CLASSIFICATION: Proceed with independent validation of organizational credentials.');
    if (anomalies.length > 0) recs.push(\`Cross-signal dissonance detected (\${anomalies.length} instances). Contradictory modality outputs necessitate further investigation.\`);
    if (recs.length === 0) recs.push('Venue parameters conform to established baseline credibility metrics.');
    await animatePhase(4, true);

    // ---- PHASE 6: Flags ----
    await animatePhase(5);
    const flags = [];
    if (scores.cfp_risk > 0.8) flags.push({ text: 'CRITICAL: Structural analysis identifies severe predatory attributes in CFP', level: 'critical' });
    if (scores.website_credibility < 0.3) flags.push({ text: 'WARNING: Infrastructure evaluation falls below acceptable minimum thresholds', level: 'warning' });
    if (scores.contact_legitimacy < 0.4) flags.push({ text: 'WARNING: Initial contact endpoints fail legitimacy validation', level: 'warning' });
    heuristics.filter(h => !h.passed && h.importance === 'critical').forEach(h =>
        flags.push({ text: \`CRITICAL HEURISTIC FAILURE: \${h.name} — \${h.evidence}\`, level: 'critical' }));
    anomalies.forEach(a => flags.push({ text: \`ANOMALY DETECTED: \${formatKey(a.signalA)} and \${formatKey(a.signalB)} present contradictory data (Divergence: \${(a.divergence*100).toFixed(0)}%)\`, level: 'warning' }));
    await animatePhase(5, true);

    // ---- RENDER RESULTS ----
    renderResults(finalCred, totalRisk, riskLevel, scores, effWeights, availability, dataCompleteness, absentCount, anomalies, anomalyAmp, heuristics, flags, recs);
}

async function animatePhase(idx, complete = false) {
    const el = document.getElementById('phase' + (idx + 1));
    if (complete) { el.classList.remove('active'); el.classList.add('complete'); }
    else { el.classList.add('active'); }
    await sleep(250);
}
function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

function renderResults(cred, risk, riskLevel, scores, effWeights, availability, dataComp, absentCount, anomalies, anomalyAmp, heuristics, flags, recs) {
    // Score ring
    document.getElementById('resultCards').style.display = 'grid';
    const pct = cred;
    const ringColor = pct > 0.7 ? '#10b981' : pct > 0.5 ? '#f59e0b' : pct > 0.3 ? '#f97316' : '#ef4444';
    const ring = document.getElementById('credRing');
    ring.style.stroke = ringColor;
    ring.style.strokeDashoffset = 264 - (264 * pct);
    document.getElementById('credValue').textContent = (pct * 100).toFixed(0) + '%';
    document.getElementById('credValue').style.color = ringColor;
    document.getElementById('riskBadgeContainer').innerHTML = \`<span class="risk-badge risk-\${riskLevel}">\${riskLevel} risk</span>
        <div style="margin-top:8px;font-size:0.75rem;color:var(--text-muted);">Risk Coefficient: \${(risk*100).toFixed(1)}%</div>\`;

    // Score breakdown
    let breakdownHtml = '';
    const scoreNames = { cfp_risk: 'CFP Risk', website_credibility: 'Infrastructure', indexing_credibility: 'Indexing Verification',
        contact_legitimacy: 'Contact Validation', organizational_structure: 'Organization', publication_history: 'Historical Record' };
    for (const [k, v] of Object.entries(scores)) {
        const isRisk = k === 'cfp_risk';
        const display = isRisk ? v : v;
        const color = isRisk ? (v > 0.6 ? '#ef4444' : v > 0.3 ? '#f59e0b' : '#10b981') :
            (v > 0.6 ? '#10b981' : v > 0.3 ? '#f59e0b' : '#ef4444');
        breakdownHtml += \`<div class="stat-row">
            <span class="stat-label">\${scoreNames[k]}</span>
            <span style="display:flex;align-items:center;gap:8px;">
                <span style="width:80px;"><div class="metric-bar"><div class="metric-bar-fill" style="width:\${display*100}%;background:\${color}"></div></div></span>
                <span class="stat-value" style="color:\${color}">\${(display*100).toFixed(0)}%</span>
            </span>
        </div>\`;
    }
    document.getElementById('scoreBreakdown').innerHTML = breakdownHtml;

    // ADW Visualization
    document.getElementById('adwCard').style.display = 'block';
    let adwHtml = '';
    for (const [k, baseW] of Object.entries(BASE_WEIGHTS)) {
        const effW = effWeights[k] || 0;
        const avail = availability[k];
        adwHtml += \`<div class="weight-bar-container">
            <span class="weight-bar-label">\${scoreNames[k]} \${avail ? '' : '(absent)'}</span>
            <div class="weight-bar-track">
                <div class="weight-bar-base" style="width:\${baseW*500}%;background:var(--accent-blue);"></div>
                <div class="weight-bar-effective" style="width:\${effW*500}%;background:\${avail ? 'var(--accent-emerald)' : 'var(--border)'};opacity:0.7;"></div>
            </div>
            <span class="weight-bar-value">\${avail ? (effW*100).toFixed(1) + '%' : '—'}</span>
        </div>\`;
    }
    document.getElementById('adwBars').innerHTML = adwHtml;
    document.getElementById('dataCompleteness').textContent = (dataComp * 100).toFixed(0) + '%';
    document.getElementById('absencePenalty').textContent = '+' + (absentCount * 0.08 * 100).toFixed(1) + '% risk adjustment';

    // CSAD
    document.getElementById('csadCard').style.display = 'block';
    if (anomalies.length === 0) {
        document.getElementById('csadContent').innerHTML = \`<div style="padding:12px;display:flex;align-items:center;gap:8px;background:rgba(16,185,129,0.06);border:1px solid rgba(16,185,129,0.2);border-radius:var(--radius-sm);font-size:0.82rem;color:var(--accent-emerald);">
            \${ICONS.check}
            <span>Analysis confirmed: Cross-signal consistencies are within expected operational bounds.</span>
        </div>\`;
    } else {
        let csadHtml = \`<div style="margin-bottom:8px;font-size:0.78rem;color:var(--accent-orange);display:flex;align-items:center;gap:6px;">
            \${ICONS.alert}
            <span>\${anomalies.length} anomal\${anomalies.length > 1 ? 'ies' : 'y'} isolated — risk amplification coefficient: +\${(anomalyAmp*100).toFixed(1)}%</span>
        </div>\`;
        anomalies.forEach(a => {
            csadHtml += \`<div class="anomaly-card">
                <div class="anomaly-type">\${a.type.replace('_', ' ')}</div>
                <div class="anomaly-detail">
                    <strong>\${formatKey(a.signalA)}</strong> = \${(a.valA*100).toFixed(0)}% credibility vs 
                    <strong>\${formatKey(a.signalB)}</strong> = \${(a.valB*100).toFixed(0)}% credibility
                    <br>Measured divergence: <strong>\${(a.divergence*100).toFixed(0)}%</strong> (threshold limit: \${ANOMALY_THRESHOLD*100}%) → 
                    Calculated risk amplification: <strong>+\${(a.amplification*100).toFixed(1)}%</strong>
                </div>
            </div>\`;
        });
        document.getElementById('csadContent').innerHTML = csadHtml;
    }

    // Heuristics
    document.getElementById('heuristicsCard').style.display = 'block';
    let heurHtml = '';
    const impColors = { critical: 'var(--accent-rose)', high: 'var(--accent-orange)', medium: 'var(--accent-amber)', low: 'var(--text-muted)' };
    heuristics.forEach(h => {
        heurHtml += \`<div class="heuristic-row">
            <span class="heuristic-icon">\${h.passed ? ICONS.check : ICONS.x}</span>
            <span class="heuristic-name">\${h.name}</span>
            <span class="heuristic-importance" style="background:\${h.passed ? 'rgba(16,185,129,0.1);color:var(--accent-emerald)' : \`rgba(239,68,68,0.1);color:\${impColors[h.importance]}\`}">\${h.importance}</span>
            <span style="font-size:0.72rem;color:var(--text-muted);width:220px;text-align:right;">\${h.evidence}</span>
        </div>\`;
    });
    document.getElementById('heuristicsContent').innerHTML = heurHtml;

    // Flags & Recommendations
    document.getElementById('flagsRecsRow').style.display = 'grid';
    document.getElementById('flagsContent').innerHTML = flags.length > 0 ?
        flags.map(f => \`<div class="flag-item flag-\${f.level}">
            <span class="flag-icon">\${f.level === 'critical' ? ICONS.x : ICONS.alert}</span>
            <span>\${f.text}</span>
        </div>\`).join('') :
        \`<div style="font-size:0.82rem;color:var(--accent-emerald);display:flex;align-items:center;gap:6px;">\${ICONS.check}<span>System reports no operational flags</span></div>\`;
    
    document.getElementById('recsContent').innerHTML = recs.map(r =>
        \`<div class="flag-item flag-info">
            <span class="flag-icon">\${ICONS.info}</span>
            <span>\${r}</span>
        </div>\`).join('');
}

// ============================================================
// COMPLIANCE COMPILER
// ============================================================
function runCompliance() {
    const title = document.getElementById('msTitle').value;
    const style = document.getElementById('msStyle').value;
    const pages = parseInt(document.getElementById('msPages').value) || 0;
    const refs = parseInt(document.getElementById('msRefs').value) || 0;
    const hasAbstract = document.getElementById('toggleAbstract').classList.contains('on');
    const hasKeywords = document.getElementById('toggleKeywords').classList.contains('on');
    const hasDOI = document.getElementById('toggleDOI').classList.contains('on');

    const issues = [];
    const styleLimits = { IEEE: { minPages: 4, maxPages: 8, minRefs: 10 }, ACM: { minPages: 6, maxPages: 12, minRefs: 15 }, APA: { minPages: 8, maxPages: 25, minRefs: 20 } };
    const limits = styleLimits[style];

    if (pages < limits.minPages) issues.push({ severity: 'error', msg: \`Page parameter (\${pages}) falls below designated minimum (\${limits.minPages}) for \${style} standard\`, section: 'format' });
    if (pages > limits.maxPages) issues.push({ severity: 'error', msg: \`Page parameter (\${pages}) exceeds designated maximum (\${limits.maxPages}) for \${style} standard\`, section: 'format' });
    if (refs < limits.minRefs) issues.push({ severity: 'warning', msg: \`Reference count (\${refs}) insufficient for \${style} baseline recommendation (\${limits.minRefs})\`, section: 'references' });
    if (!hasAbstract) issues.push({ severity: 'error', msg: 'Abstract component missing — strict requirement across all parsing modules', section: 'structure' });
    if (!hasKeywords) issues.push({ severity: 'warning', msg: 'Keywords classification block missing', section: 'structure' });
    if (!hasDOI) issues.push({ severity: 'info', msg: 'Digital Object Identifiers (DOIs) absent — highly recommended for optimal indexing', section: 'references' });
    if (!title || title.length < 10) issues.push({ severity: 'warning', msg: 'Title string length falls below standard bounds', section: 'metadata' });

    const isCompliant = issues.filter(i => i.severity === 'error').length === 0;
    const sevColors = { error: 'var(--accent-rose)', warning: 'var(--accent-amber)', info: 'var(--accent-blue)' };

    document.getElementById('complianceEmpty').style.display = 'none';
    document.getElementById('complianceContent').style.display = 'block';

    let html = \`<div style="text-align:center;padding:1rem;margin-bottom:1rem;border-radius:var(--radius-sm);
        background:\${isCompliant ? 'rgba(16,185,129,0.06);border:1px solid rgba(16,185,129,0.2)' : 'rgba(239,68,68,0.06);border:1px solid rgba(239,68,68,0.2)'}">
        <div style="font-size:1.5rem;margin-bottom:4px;display:flex;justify-content:center;">\${isCompliant ? ICONS.check : ICONS.x}</div>
        <div style="font-weight:700;color:\${isCompliant ? 'var(--accent-emerald)' : 'var(--accent-rose)'}">
            \${isCompliant ? 'STATUS: COMPLIANT' : 'STATUS: NON-COMPLIANT'}
        </div>
        <div style="font-size:0.78rem;color:var(--text-muted);">\${style} Parse Tree · \${issues.length} diagnostic anomalies identified</div>
    </div>\`;

    if (issues.length > 0) {
        html += '<div class="section-title">Compiler Diagnostics output</div>';
        issues.forEach(i => {
            html += \`<div class="flag-item" style="border-left:3px solid \${sevColors[i.severity]};background:rgba(0,0,0,0.2);margin-bottom:6px;align-items:center;">
                <span style="font-weight:700;color:\${sevColors[i.severity]};text-transform:uppercase;font-size:0.7rem;width:70px;">[\${i.severity}]</span>
                <span style="font-size:0.82rem;flex:1;"> \${i.msg}</span>
                <span style="font-size:0.7rem;color:var(--text-muted);">\${i.section}</span>
            </div>\`;
        });
    }
    document.getElementById('complianceContent').innerHTML = html;
}

// ============================================================
// CITATION ANALYSIS
// ============================================================
function runCitationAnalysis() {
    const authors = document.getElementById('citAuthors').value.split(',').map(a => a.trim()).filter(Boolean);
    let refs;
    try { refs = JSON.parse(document.getElementById('citRefs').value); } catch (e) {
        alert('Data parsing failure: Invalid JSON format in references string.'); return;
    }
    const authorLastNames = new Set(authors.map(a => a.toLowerCase().split(/\s+/).pop()));
    let selfCites = 0;
    refs.forEach(r => {
        if ((r.authors || []).some(a => authorLastNames.has(a.toLowerCase().split(/\s+/).pop()))) selfCites++;
    });
    const selfRate = selfCites / Math.max(refs.length, 1);
    const venues = new Set(refs.map(r => (r.venue || '').toLowerCase()));
    const allAuthors = new Set();
    refs.forEach(r => (r.authors || []).forEach(a => allAuthors.add(a.toLowerCase())));
    const venueDiversity = Math.min(venues.size / Math.max(refs.length, 1), 1);
    const authorDiversity = Math.min(allAuthors.size / (refs.length * 2), 1);
    const diversity = venueDiversity * 0.6 + authorDiversity * 0.4;
    const years = refs.map(r => r.year).filter(Boolean);
    const currentYear = new Date().getFullYear();
    const recentCount = years.filter(y => y >= currentYear - 3).length;

    let risk = 0;
    if (selfRate > 0.3) risk += 0.3; else if (selfRate > 0.2) risk += 0.15;
    if (diversity < 0.3) risk += 0.15;
    if (recentCount === 0 && years.length > 0) risk += 0.1;
    risk = Math.min(risk, 1);

    document.getElementById('citationEmpty').style.display = 'none';
    document.getElementById('citationContent').style.display = 'block';

    const riskColor = risk > 0.5 ? '#ef4444' : risk > 0.25 ? '#f59e0b' : '#10b981';
    let html = \`<div class="grid-3" style="margin-bottom:1rem;">
        <div style="text-align:center;padding:1rem;background:var(--bg-input);border-radius:var(--radius-sm);border:1px solid var(--border);">
            <div style="font-size:2rem;font-weight:800;">\${refs.length}</div>
            <div style="font-size:0.72rem;color:var(--text-muted);">PROCESSED REFERENCES</div>
        </div>
        <div style="text-align:center;padding:1rem;background:var(--bg-input);border-radius:var(--radius-sm);border:1px solid var(--border);">
            <div style="font-size:2rem;font-weight:800;color:\${selfRate > 0.3 ? '#ef4444' : selfRate > 0.2 ? '#f59e0b' : '#10b981'}">\${(selfRate*100).toFixed(0)}%</div>
            <div style="font-size:0.72rem;color:var(--text-muted);">SELF-CITATION RATE</div>
        </div>
        <div style="text-align:center;padding:1rem;background:var(--bg-input);border-radius:var(--radius-sm);border:1px solid var(--border);">
            <div style="font-size:2rem;font-weight:800;color:\${riskColor}">\${(risk*100).toFixed(0)}%</div>
            <div style="font-size:0.72rem;color:var(--text-muted);">NETWORK RISK INDEX</div>
        </div>
    </div>\`;
    html += \`<div class="stat-row"><span class="stat-label">Identified self-citations</span><span class="stat-value">\${selfCites} / \${refs.length}</span></div>\`;
    html += \`<div class="stat-row"><span class="stat-label">Unique publishing venues</span><span class="stat-value">\${venues.size}</span></div>\`;
    html += \`<div class="stat-row"><span class="stat-label">Unique contributing authors</span><span class="stat-value">\${allAuthors.size}</span></div>\`;
    html += \`<div class="stat-row"><span class="stat-label">Calculated citation diversity</span><span class="stat-value">\${(diversity*100).toFixed(0)}%</span></div>\`;
    html += \`<div class="stat-row"><span class="stat-label">Recent literature (T-3 years)</span><span class="stat-value">\${recentCount}</span></div>\`;

    if (selfRate > 0.3) html += \`<div class="flag-item flag-warning" style="margin-top:12px;">\${ICONS.alert}<span>Self-citation algorithm detects rate (\${(selfRate*100).toFixed(0)}%) above acceptable baseline. Reference diversification required.</span></div>\`;
    if (diversity < 0.4) html += \`<div class="flag-item flag-warning" style="margin-top:8px;">\${ICONS.alert}<span>Network diversity index low. Broader literature foundation is recommended.</span></div>\`;
    if (recentCount === 0 && years.length > 0) html += \`<div class="flag-item flag-warning" style="margin-top:8px;">\${ICONS.alert}<span>Time-series analysis shows no recent integrations. Incorporate standard recent findings.</span></div>\`;

    document.getElementById('citationContent').innerHTML = html;
}

// ============================================================
// CLAIM 4: Temporal Fingerprint Evolution Tracking
// ============================================================
function runEvolutionAnalysis() {
    const t1 = {
        cfpRisk: parseFloat(document.getElementById('evo_t1_cfp').value),
        webDepth: parseFloat(document.getElementById('evo_t1_web').value),
        struct: parseFloat(document.getElementById('evo_t1_struct').value),
        indexers: document.getElementById('evo_t1_idx').value.split(',').map(s => s.trim()).filter(Boolean),
        organizers: document.getElementById('evo_t1_org').value.split(',').map(s => s.trim()).filter(Boolean)
    };
    const t2 = {
        cfpRisk: parseFloat(document.getElementById('evo_t2_cfp').value),
        webDepth: parseFloat(document.getElementById('evo_t2_web').value),
        struct: parseFloat(document.getElementById('evo_t2_struct').value),
        indexers: document.getElementById('evo_t2_idx').value.split(',').map(s => s.trim()).filter(Boolean),
        organizers: document.getElementById('evo_t2_org').value.split(',').map(s => s.trim()).filter(Boolean)
    };

    // Drift analysis
    const cfpDrift = Math.abs(t2.cfpRisk - t1.cfpRisk);
    const webDrift = (Math.abs(t2.webDepth - t1.webDepth) + Math.abs(t2.struct - t1.struct)) / 2;
    const prevIdx = new Set(t1.indexers.map(s => s.toLowerCase()));
    const currIdx = new Set(t2.indexers.map(s => s.toLowerCase()));
    const addedIdx = [...currIdx].filter(x => !prevIdx.has(x));
    const removedIdx = [...prevIdx].filter(x => !currIdx.has(x));
    const allIdx = new Set([...prevIdx, ...currIdx]);
    const idxDrift = allIdx.size > 0 ? (addedIdx.length + removedIdx.length) / allIdx.size : 0;
    const prevOrg = new Set(t1.organizers.map(s => s.toLowerCase()));
    const currOrg = new Set(t2.organizers.map(s => s.toLowerCase()));
    const orgUnion = new Set([...prevOrg, ...currOrg]);
    const orgIntersect = [...prevOrg].filter(x => currOrg.has(x));
    const orgOverlap = orgUnion.size > 0 ? orgIntersect.length / orgUnion.size : 0;
    const orgDrift = 1 - orgOverlap;

    const mutations = [];
    if (cfpDrift > 0.2) mutations.push({ dim: 'CFP Risk Vector', prev: t1.cfpRisk, curr: t2.cfpRisk, drift: cfpDrift, dir: t2.cfpRisk > t1.cfpRisk ? 'degraded' : 'stabilized' });
    if (webDrift > 0.15) mutations.push({ dim: 'Infrastructure Topology', prev: t1.webDepth, curr: t2.webDepth, drift: webDrift, dir: 'restructured' });
    if (addedIdx.length > 0) mutations.push({ dim: 'Indexing Meta-claims', added: addedIdx, removed: removedIdx, drift: idxDrift, dir: 'claims_expanded' });
    if (orgDrift > 0.5) mutations.push({ dim: 'Administrative Entities', overlap: orgOverlap, drift: orgDrift, dir: 'significant_turnover' });

    const aggregate = cfpDrift * 0.20 + webDrift * 0.15 + idxDrift * 0.30 + orgDrift * 0.15;
    const temporalAdj = aggregate > 0.3 ? Math.min(aggregate * 0.5, 0.25) : 0;

    // Render
    const driftColor = aggregate > 0.5 ? '#ef4444' : aggregate > 0.3 ? '#f59e0b' : '#10b981';
    let html = \`<div class="card">
        <div class="card-title">Temporal Drift Analysis Report <span class="claim-tag">Claim 4</span></div>
        <div class="grid-3" style="margin-bottom:1rem;">
            <div style="text-align:center;padding:1rem;background:var(--bg-input);border-radius:var(--radius-sm);border:1px solid var(--border);">
                <div style="font-size:2rem;font-weight:800;color:\${driftColor}">\${(aggregate*100).toFixed(0)}%</div>
                <div style="font-size:0.72rem;color:var(--text-muted);">AGGREGATE DRIFT VECTOR</div>
            </div>
            <div style="text-align:center;padding:1rem;background:var(--bg-input);border-radius:var(--radius-sm);border:1px solid var(--border);">
                <div style="font-size:2rem;font-weight:800;color:var(--accent-purple)">\${mutations.length}</div>
                <div style="font-size:0.72rem;color:var(--text-muted);">ISOLATED MUTATIONS</div>
            </div>
            <div style="text-align:center;padding:1rem;background:var(--bg-input);border-radius:var(--radius-sm);border:1px solid var(--border);">
                <div style="font-size:2rem;font-weight:800;color:\${temporalAdj > 0 ? 'var(--accent-rose)' : 'var(--accent-emerald)'}">\${temporalAdj > 0 ? '+' : ''}\${(temporalAdj*100).toFixed(1)}%</div>
                <div style="font-size:0.72rem;color:var(--text-muted);">RISK MODIFICATION FACTOR</div>
            </div>
        </div>\`;

    // Dimension bars
    const dims = [
        { name: 'CFP Risk Trajectory', value: cfpDrift, weight: 0.20 },
        { name: 'Infrastructure Deviation', value: webDrift, weight: 0.15 },
        { name: 'Indexing Modification', value: idxDrift, weight: 0.30 },
        { name: 'Administrative Drift', value: orgDrift, weight: 0.15 }
    ];
    dims.forEach(d => {
        const c = d.value > 0.5 ? '#ef4444' : d.value > 0.2 ? '#f59e0b' : '#10b981';
        html += \`<div class="stat-row">
            <span class="stat-label">\${d.name} (w=\${d.weight})</span>
            <span style="display:flex;align-items:center;gap:8px;">
                <span style="width:120px;"><div class="metric-bar"><div class="metric-bar-fill" style="width:\${d.value*100}%;background:\${c}"></div></div></span>
                <span class="stat-value" style="color:\${c}">\${(d.value*100).toFixed(0)}%</span>
            </span>
        </div>\`;
    });

    if (mutations.length > 0) {
        html += '<div class="section-title" style="margin-top:1rem;">Structural Mutations Documented</div>';
        mutations.forEach(m => {
            html += \`<div class="mutation-card">
                <div style="font-size:0.72rem;font-weight:700;color:var(--accent-purple);text-transform:uppercase;">\${m.dim} — Code: \${m.dir}</div>
                <div style="font-size:0.8rem;color:var(--text-secondary);margin-top:4px;">\`;
            if (m.added) html += \`Insertions: \${m.added.join(', ')}\${m.removed.length ? ' · Deletions: ' + m.removed.join(', ') : ''}\`;
            else if (m.overlap !== undefined) html += \`Organizational retention rate: \${(m.overlap*100).toFixed(0)}%\`;
            else html += \`Base: \${(m.prev*100).toFixed(0)}% → Current: \${(m.curr*100).toFixed(0)}%\`;
            html += \`<br>Computed drift parameter: \${(m.drift*100).toFixed(0)}%</div></div>\`;
        });
    } else {
        html += \`<div style="padding:12px;display:flex;align-items:center;gap:8px;background:rgba(16,185,129,0.06);border:1px solid rgba(16,185,129,0.2);border-radius:var(--radius-sm);margin-top:1rem;font-size:0.82rem;color:var(--accent-emerald);">
            \${ICONS.check}
            <span>Longitudinal analysis confirms baseline stability — no significant structural mutations isolated.</span>
        </div>\`;
    }
    html += '</div>';
    document.getElementById('evolutionResults').innerHTML = html;
}

// ============================================================
// NEW CORE ENGINES: LATENCY & GEO-TRIANGULATION
// ============================================================
function runLatencyAnalysis() {
    const sub = new Date(document.getElementById('lat_sub').value);
    const acc = new Date(document.getElementById('lat_acc').value);
    const stages = parseInt(document.getElementById('lat_stages').value);
    
    if (isNaN(sub) || isNaN(acc)) return;
    
    const diffTime = Math.abs(acc - sub);
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    
    // Deterministic rule: Standard peer review requires minimum 14 days per stage.
    const expectedMinDays = stages * 14;
    const latencyDivergence = diffDays - expectedMinDays;
    
    let html = '<div class="card"><div class="card-title">Latency Verification Output</div>';
    html += \`<div class="stat-row"><span class="stat-label">Actual Peer-Review Latency</span><span class="stat-value">\${diffDays} Days</span></div>\`;
    html += \`<div class="stat-row"><span class="stat-label">Minimum Expected Latency</span><span class="stat-value">\${expectedMinDays} Days</span></div>\`;
    
    if (latencyDivergence < 0) {
        html += \`<div class="flag-item flag-critical" style="margin-top:1rem;">
            \${ICONS.alert}
            <div>
                <strong>Temporal Impossibility Detected</strong><br>
                The claimed timeline (\${diffDays} days) is deterministically insufficient to complete \${stages} stage(s) of rigorous peer review. High probability of "Pay-to-Publish" immediate acceptance.
            </div>
        </div>\`;
    } else {
        html += \`<div class="flag-item flag-safe" style="margin-top:1rem;">
            \${ICONS.check}
            <div>
                <strong>Latency Validated</strong><br>
                The temporal delta conforms to standard academic publishing latency constraints.
            </div>
        </div>\`;
    }
    html += '</div>';
    document.getElementById('latencyResults').innerHTML = html;
}

function runGeoAnalysis() {
    const claim = document.getElementById('geo_claim').value;
    const ip = document.getElementById('geo_ip').value;
    const pay = document.getElementById('geo_pay').value;
    
    let dissonanceScore = 0;
    if (claim !== ip) dissonanceScore += 0.4;
    if (claim !== pay) dissonanceScore += 0.6;
    
    let html = '<div class="card"><div class="card-title">Geospatial Dissonance Vector</div>';
    
    const c = dissonanceScore > 0.5 ? '#ef4444' : dissonanceScore > 0 ? '#f59e0b' : '#10b981';
    html += \`<div class="stat-row">
        <span class="stat-label">Triangulation Divergence</span>
        <span style="display:flex;align-items:center;gap:8px;">
            <span style="width:120px;"><div class="metric-bar"><div class="metric-bar-fill" style="width:\${dissonanceScore*100}%;background:\${c}"></div></div></span>
            <span class="stat-value" style="color:\${c}">\${(dissonanceScore*100).toFixed(0)}%</span>
        </span>
    </div>\`;
    
    if (dissonanceScore > 0) {
        html += \`<div class="flag-item \${dissonanceScore > 0.5 ? 'flag-critical' : 'flag-warning'}" style="margin-top:1rem;">
            \${ICONS.alert}
            <div>
                <strong>Geospatial Fraud Indicator</strong><br>
                Structural divergence detected between claimed academic headquarters and actual digital/financial footprint. This shell-company structure is heavily utilized by deceptive publishing networks.
            </div>
        </div>\`;
    } else {
        html += \`<div class="flag-item flag-safe" style="margin-top:1rem;">
            \${ICONS.check}
            <div>
                <strong>Spatial Harmony</strong><br>
                All digital and financial vectors align with the claimed institutional headquarters.
            </div>
        </div>\`;
    }
    html += '</div>';
    document.getElementById('geoResults').innerHTML = html;
}

// ============================================================
// UTILITIES
// ============================================================
function formatKey(k) { return k.split('_').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' '); }
function escHtml(s) { const d = document.createElement('div'); d.textContent = s; return d.innerHTML; }
`;
    document.body.appendChild(script);
    
    // Simulate initial tab click to setup active state
    setTimeout(() => {
        if(window.document.getElementById('tabVenue')) {
            window.document.getElementById('tabVenue')?.click();
        }
    }, 100);

    return () => {
      if (document.body.contains(script)) {
          document.body.removeChild(script);
      }
    };
  }, []);

  return (
    <div ref={containerRef} dangerouslySetInnerHTML={{ __html: `

<div id="auth-container">
    <div class="auth-card" id="login-box">
        <div style="display:flex; justify-content:center; margin-bottom:1.5rem;">
            <div class="logo-icon" style="width:56px;height:56px;font-size:1.5rem;">AX</div>
        </div>
        <h2>ARICCA-X Secure Login</h2>
        <p>Role-Based System Access Verification</p>
        <div class="demo-box">
            <strong>Demo Credentials (Testing Only):</strong>
            Admin Role: <em>admin@aricca.com / admin123</em><br>
            User Role: <em>user@aricca.com / user123</em>
        </div>
        <form class="auth-form" id="login-form" onsubmit="window.handleLogin(event)">
            <input type="email" id="login-email" placeholder="Email Address" required>
            <input type="password" id="login-pwd" placeholder="Password" required>
            <button class="btn btn-primary" type="submit">Authenticate & Enter</button>
            <div id="login-error" style="color:var(--accent-rose); font-size:0.85rem; margin-top:12px; text-align:center; display:none; font-weight: 600;">Invalid credentials or role not recognized.</div>
        </form>
        <div class="auth-switch" onclick="toggleAuth('signup')">Need system access? <span>Request Account</span></div>
    </div>

    <div class="auth-card" id="signup-box" style="display: none;">
        <div style="display:flex; justify-content:center; margin-bottom:1.5rem;">
            <div class="logo-icon" style="width:56px;height:56px;font-size:1.5rem;">AX</div>
        </div>
        <h2>Request Access</h2>
        <p>ARICCA-X is currently in closed beta.</p>
        <form class="auth-form" id="signup-form">
            <input type="text" placeholder="Full Name" required>
            <input type="email" placeholder="Institutional Email" required>
            <input type="text" placeholder="Institution / Organization" required>
            <button class="btn btn-primary" type="button" onclick="alert('Signup requests are queued for manual administrative review in Demo Mode.')">Submit Request</button>
        </form>
        <div class="auth-switch" onclick="toggleAuth('login')">Already approved? <span>Login Here</span></div>
    </div>
</div>

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
    </nav>

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
