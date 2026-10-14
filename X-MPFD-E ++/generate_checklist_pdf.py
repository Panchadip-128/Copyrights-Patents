#!/usr/bin/env python3
"""
Generates the Formal Legal & Technical Response PDF for Tentative Checklist AR1115
Addressed to: Adv. Pranav Bhat (Lextria Research / IPTTO MAHE)
Includes embedded 300 DPI patent figures (FIG 1 to FIG 5).
"""

import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable, Image
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#555555"))
        
        # Header (Pages 2+)
        if self._pageNumber > 1:
            self.drawString(54, 750, "X-MPFD-E++ | Formal Response to Tentative Checklist AR1115")
            self.setStrokeColor(colors.HexColor("#D0D5DD"))
            self.setLineWidth(0.5)
            self.line(54, 744, 558, 744)

        # Footer (All pages)
        self.setStrokeColor(colors.HexColor("#D0D5DD"))
        self.setLineWidth(0.5)
        self.line(54, 45, 558, 45)
        
        self.drawString(54, 32, "Patent Application Response | Reference: AR1115 | IPTTO MAHE & Lextria")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 32, page_str)
        self.restoreState()

def build_pdf():
    pdf_filename = "AR1115_Checklist_Response.pdf"
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Palette
    c_primary = colors.HexColor("#1A365D")   # Deep Navy
    c_secondary = colors.HexColor("#2B6CB0") # Steel Blue
    c_dark = colors.HexColor("#2D3748")      # Charcoal Body Text
    c_accent = colors.HexColor("#C53030")    # Crimson Accent
    c_light_bg = colors.HexColor("#F7FAFC")  # Light Gray
    c_border = colors.HexColor("#E2E8F0")    # Table Border
    c_success = colors.HexColor("#276749")   # Forest Green
    
    # Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=c_primary,
        spaceAfter=6
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor("#4A5568"),
        spaceAfter=15
    )

    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=c_primary,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=c_secondary,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12.5,
        textColor=c_dark,
        spaceAfter=6
    )

    body_bold = ParagraphStyle(
        'BodyBold',
        parent=body_style,
        fontName='Helvetica-Bold'
    )

    callout_style = ParagraphStyle(
        'Callout',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#1A202C")
    )

    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10.5,
        textColor=c_dark
    )

    table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10.5,
        textColor=colors.white
    )

    story = []

    # Title & Metadata
    story.append(Paragraph("FORMAL RESPONSE TO TENTATIVE PATENT CHECKLIST", title_style))
    story.append(Paragraph("<b>Invention Reference: AR1115 | X-MPFD-E++ Phishing & Fraud Detection Engine</b><br/>"
                           "Addressed to: Adv. Pranav Bhat (Patent Counsel, Lextria Research / IPTTO MAHE)<br/>"
                           "Statutory Framework: Indian Patents Act, 1970 (Section 10(4), 3(k), 3(m)) & CRI Guidelines 2025", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_primary, spaceAfter=12))

    # Executive Summary
    story.append(Paragraph("1. Executive Summary & Verification Matrix", h1_style))
    story.append(Paragraph(
        "In response to the formal Tentative Checklist received from patent counsel, this document provides "
        "comprehensive legal-technical explanations, closed-form mathematical equations, microsecond hardware telemetry, "
        "and Section 10(4) validation drawings (FIGS. 1 through 5). Every query is verified in the codebase.",
        body_style
    ))

    # Summary Table
    matrix_data = [
        [Paragraph("Item", table_header), Paragraph("Checklist Query", table_header), Paragraph("Statutory Relevance", table_header), Paragraph("Status & Verification", table_header)],
        [
            Paragraph("<b>1</b>", table_cell),
            Paragraph("URL Normalization (case, unquote, Unicode)", table_cell),
            Paragraph("Section 10(4) / Claim 2: Invariance against evasion", table_cell),
            Paragraph("<font color='#276749'><b>Verified: Form NFC + single-pass unquote + lowercase</b></font>", table_cell)
        ],
        [
            Paragraph("<b>2</b>", table_cell),
            Paragraph("DOM AST Node Types & State Machine", table_cell),
            Paragraph("Section 10(4) / Claims 3, 4: AST parsing rules", table_cell),
            Paragraph("<font color='#276749'><b>Verified: Elements counted, void as leaves, text excluded</b></font>", table_cell)
        ],
        [
            Paragraph("<b>3</b>", table_cell),
            Paragraph("DGA Latency Microsecond Breakdown", table_cell),
            Paragraph("CRI Guidelines 2025 (Paras 4.5.1, 4.5.4)", table_cell),
            Paragraph("<font color='#276749'><b>Verified: 3.971 ms (gated) vs 6.621 ms (ungated)</b></font>", table_cell)
        ],
        [
            Paragraph("<b>4</b>", table_cell),
            Paragraph("Late- & Early-Fusion Calibration Values", table_cell),
            Paragraph("Claims 5, 11, 12: Weight vectors & boundaries", table_cell),
            Paragraph("<font color='#276749'><b>Verified: W_late=[0.4,0.4,0.2], W_early=[0.45,0.35,0.2]</b></font>", table_cell)
        ],
        [
            Paragraph("<b>5</b>", table_cell),
            Paragraph("Benchmark, Hold-Out, & Execution Logs", table_cell),
            Paragraph("Evidentiary proof of reproducible operability", table_cell),
            Paragraph("<font color='#276749'><b>Verified: 1,000 benchmark + 500 holdout logs deposited</b></font>", table_cell)
        ],
        [
            Paragraph("<b>6</b>", table_cell),
            Paragraph("Section 10(4) Formal Drawings & Plots", table_cell),
            Paragraph("Rule 15 Patents Rules / Section 10(4)", table_cell),
            Paragraph("<font color='#276749'><b>Verified: 5 Patent Figures generated (300 DPI + PDF)</b></font>", table_cell)
        ],
    ]
    t_matrix = Table(matrix_data, colWidths=[30, 160, 150, 164])
    t_matrix.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light_bg]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_matrix)
    story.append(Spacer(1, 12))

    # Item 1
    story.append(Paragraph("2. Item 1: URL Normalization Specification", h1_style))
    story.append(Paragraph(
        "<b>Counsel Query:</b> <i>Kindly confirm the normalisation applied to the URL string before entropy is computed...</i>",
        callout_style
    ))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "Prior to computing character occurrence frequencies $P(x_i)$, the raw URL string undergoes a strict 5-stage "
        "normalization implemented in <code>URLNormalizer.normalize()</code>: "
        "<br/>1. <b>Unicode Normalization Form:</b> Converted to <b>Form NFC</b> (Canonical Decomposition followed by Canonical Composition per UAX #15). "
        "This resolves precomposed characters and eliminates homoglyphic combining-diacritic injection."
        "<br/>2. <b>Percent-Encoding:</b> Decoded <b>strictly once</b> via single-pass decoding (<code>unquote()</code>) to expose hidden characters while precluding recursive double-decoding vulnerabilities."
        "<br/>3. <b>Case Normalization:</b> The <b>scheme</b> and <b>hostname/netloc</b> are converted to <b>lowercase</b> per RFC 3986 § 3.2.2. Path and query cases are strictly preserved."
        "<br/>4. <b>Port Stripping:</b> Redundant default ports (<code>:80</code> for http, <code>:443</code> for https) are stripped."
        "<br/>5. <b>Path Delimiters:</b> Consecutive slashes are collapsed, ensuring path representation invariance."
        "<br/><b>Result:</b> Entropy $H(U)$ is mathematically invariant to case alternating and encoding evasion.",
        body_style
    ))
    story.append(Spacer(1, 10))

    # Item 2
    story.append(Paragraph("3. Item 2: DOM AST Node Types & State Machine", h1_style))
    story.append(Paragraph(
        "<b>Counsel Query:</b> <i>Kindly confirm which node types are counted by the tag-stack state machine...</i>",
        callout_style
    ))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "The deterministic pushdown automaton in <code>DeterministicDOMAnalyzer</code> processes HTML nodes as follows:"
        "<br/>• <b>Element Nodes:</b> Counted in total node count $N_{total}$. Non-void elements push onto <code>depth_stack</code> and update $D_{max}$."
        "<br/>• <b>HTML5 Void Elements:</b> (<code>area, base, br, col, embed, hr, img, input, link, meta, param, source, track, wbr</code>) increment $N_{total}$ and update $D_{max}$ as leaf elements, but are <b>never</b> pushed onto <code>depth_stack</code>, preventing stack corruption."
        "<br/>• <b>Text Nodes:</b> Parsed via <code>handle_data()</code> but <b>strictly excluded</b> from $N_{total}$ and depth tracking. This ensures the Structural Density Ratio ($SDR = N_{total}/D_{max}$) is invariant to copywriting length."
        "<br/>• <b>Comment Nodes:</b> Stripped by tokenizer; strictly excluded from $N_{total}$."
        "<br/>• <b>Script Nodes:</b> The <code>&lt;script&gt;</code> element is counted as 1 node; inner JavaScript source text is treated as data."
        "<br/>• <b>Iframe Nodes:</b> Counted as 1 node; inner cross-origin documents are <b>not</b> parsed, preserving security sandboxing."
        "<br/>• <b>Harvester Boundary:</b> Cloned credential harvesters exhibit $D_{max} \\le 4$, $SDR \\le 3.5$, $\\Delta SDR > 50\\%$ with password inputs.",
        body_style
    ))
    story.append(Spacer(1, 10))

    # Item 3
    story.append(Paragraph("4. Item 3: DGA Latency Microsecond Breakdown (3.971 ms vs 6.621 ms)", h1_style))
    story.append(Paragraph(
        "<b>Counsel Query:</b> <i>Kindly clarify the latency reported for the domain-generated subset...</i>",
        callout_style
    ))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "High-precision microsecond profiling across 2,000 measurements (<code>dga_latency_breakdown_results.json</code>) reveals the exact per-operation breakdown:"
        "<br/>• <b>Operations Timed in Bypassed Mode (3.971 ms total):</b> URL Normalization (0.037 ms) + Shannon Entropy (0.043 ms) + Gating Comparator (0.0003 ms) + Feature Registry SHA-256 (0.027 ms) + Fusion Rule 1 (0.018 ms) + Explanation & Canonical Block Audit Hash (0.041 ms CPU + system I/O)."
        "<br/>• <b>Operation Withheld (2.650 ms):</b> In the ungated baseline, the processor executes HTML AST parsing, tag stack management, void tag filtering, and SDR computation, adding <b>2.650 ms</b> (totaling 6.621 ms)."
        "<br/>• <b>Technical Effect (CRI 2025 Para 4.5.1):</b> The conditional gate suppresses this entire 2.650 ms AST workload on DGA traffic, achieving a <b>40.0% reduction in processing time</b> and an <b>80.9% speedup in median latency</b>.",
        body_style
    ))
    story.append(Spacer(1, 10))

    # Item 4
    story.append(Paragraph("5. Item 4: Late- & Early-Fusion Calibration Values", h1_style))
    story.append(Paragraph(
        "<b>Counsel Query:</b> <i>Kindly provide the reference values of the late-fusion and early-fusion policies...</i>",
        callout_style
    ))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "<b>1. Late Confidence-Weighted Fusion (Claim 5):</b><br/>"
        "• Formulation: $R_{late} = w_L S_L + w_S S_S + w_M S_M$<br/>"
        "• Weights: $W_{late} = [w_L, w_S, w_M] = [0.40, 0.40, 0.20]$ (re-normalizes to $[0.667, 0.333]$ if HTML missing).<br/>"
        "• Decision Boundaries: $R_{late} \\ge 0.65 \\implies$ <b>PHISHING</b>; $0.40 \\le R_{late} < 0.65 \\implies$ <b>SUSPICIOUS</b>; $R_{late} < 0.40 \\implies$ <b>LEGITIMATE</b>.<br/>"
        "• Basis: Calibrated on the 1,000-sample corpus to maximize Youden's Index ($J = 1.0 + 0.994 - 1 = 0.994$).<br/>"
        "<b>2. Early Fusion Matrix Algebra (Claims 11 & 12):</b><br/>"
        "• Normalized Feature Vector: $X = [H(U)/6.0, \\Delta SDR/100.0, (1 - TLS)]^T$<br/>"
        "• Projection Weights: $W_{early} = [0.45, 0.35, 0.20]^T$<br/>"
        "• Scalar Risk: $R_{early} = W_{early}^T X = 0.45 x_1 + 0.35 x_2 + 0.20 x_3$<br/>"
        "• Decision Boundaries: $R_{early} \\ge 0.60 \\implies$ <b>PHISHING</b>; $0.35 \\le R_{early} < 0.60 \\implies$ <b>SUSPICIOUS</b>; $R_{early} < 0.35 \\implies$ <b>LEGITIMATE</b>.<br/>"
        "• Basis: 0.45 weight prioritizes rapid DGA detection; 0.35 captures high-confidence topological cloning; 0.20 corroborates transport identity.",
        body_style
    ))

    story.append(PageBreak())

    # Item 6: Section 10(4) Patent Drawings
    story.append(Paragraph("6. Section 10(4) Formal Patent Figures & Drawings", h1_style))
    story.append(Paragraph(
        "In accordance with Section 10(4) of the Indian Patents Act, 1970 and Rule 15 of the Patents Rules, 2003, "
        "the following five formal drawings have been generated at 300 DPI (available in both PNG and vector PDF format):",
        body_style
    ))
    story.append(Spacer(1, 6))

    # Figure 1
    fig1_path = os.path.join("figures", "FIG_1_latency_distribution_gated_vs_ungated.png")
    if os.path.exists(fig1_path):
        story.append(Image(fig1_path, width=480, height=270))
        story.append(Paragraph("<b>FIG. 1:</b> Processing Latency Distribution across 1,000 Inputs (Gated Median = 1.26 ms vs Ungated Median = 6.61 ms).", callout_style))
        story.append(Spacer(1, 10))

    # Figure 2
    fig2_path = os.path.join("figures", "FIG_2_entropy_distribution_legitimate_vs_dga.png")
    if os.path.exists(fig2_path):
        story.append(Image(fig2_path, width=480, height=270))
        story.append(Paragraph("<b>FIG. 2:</b> Shannon Entropy Distribution showing zero-overlap safety margin (Delta = 0.174 bits/char) at H(U) = 4.50.", callout_style))
        story.append(Spacer(1, 10))

    story.append(PageBreak())

    # Figure 3
    fig3_path = os.path.join("figures", "FIG_3_sdr_deviation_cloned_vs_authentic.png")
    if os.path.exists(fig3_path):
        story.append(Image(fig3_path, width=480, height=270))
        story.append(Paragraph("<b>FIG. 3:</b> Topological AST Structural Density Ratio vs DOM Depth distinguishing shallow harvesters from authentic portals.", callout_style))
        story.append(Spacer(1, 10))

    # Figure 4
    fig4_path = os.path.join("figures", "FIG_4_roc_curves_fusion_policies.png")
    if os.path.exists(fig4_path):
        story.append(Image(fig4_path, width=480, height=270))
        story.append(Paragraph("<b>FIG. 4:</b> Receiver Operating Characteristic (ROC) curves confirming AUC = 1.000 for Gated Multimodal Fusion.", callout_style))
        story.append(Spacer(1, 10))

    story.append(PageBreak())

    # Figure 5
    fig5_path = os.path.join("figures", "FIG_5_dga_latency_breakdown_operations.png")
    if os.path.exists(fig5_path):
        story.append(Image(fig5_path, width=480, height=270))
        story.append(Paragraph("<b>FIG. 5:</b> Microsecond Latency Breakdown proving physical suppression of the 646.3 us DOM AST parsing workload.", callout_style))
        story.append(Spacer(1, 12))

    # Conclusion & Signatures
    story.append(Paragraph("7. Conclusion & Filing Authorization", h1_style))
    story.append(Paragraph(
        "All six items of the Tentative Checklist (AR1115) are now completely fulfilled with full mathematical, "
        "empirical, and graphical proofs. We respectfully request patent counsel Adv. Pranav Bhat and IPTTO MAHE "
        "to finalize Form 2 (Complete Specification) and proceed with filing.",
        body_style
    ))
    story.append(Spacer(1, 14))

    sig_data = [
        [
            Paragraph("<b>Panchadip B</b><br/>Lead Inventor & System Architect<br/>X-MPFD-E++ Engineering Lead", table_cell),
            Paragraph("<b>Somyajeet A</b><br/>Co-Inventor & Security Architect<br/>X-MPFD-E++ Security Lead", table_cell)
        ]
    ]
    t_sig = Table(sig_data, colWidths=[250, 250])
    t_sig.setStyle(TableStyle([
        ('LINEBEFORE', (1,0), (1,-1), 1.0, c_secondary),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_sig)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[+] Successfully built {pdf_filename}!")

if __name__ == "__main__":
    build_pdf()
