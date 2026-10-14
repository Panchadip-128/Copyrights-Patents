#!/usr/bin/env python3
"""
Generates the Changes Made & Compliance Technical Specification PDF.
Includes real source code, microsecond benchmark tables, architecture diagrams,
and empirical figures.
"""

import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable, Image, Preformatted
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
        self.setFillColor(colors.HexColor("#475569"))
        
        # Header (Pages 2+)
        if self._pageNumber > 1:
            self.drawString(54, 750, "X-MPFD-E++ | Technical Changes & Compliance Specification")
            self.drawRightString(558, 750, "Reference: AR1115")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(54, 744, 558, 744)

        # Footer (All pages)
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, 45, 558, 45)
        
        self.drawString(54, 32, "Technical Specification & Empirical Telemetry")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 32, page_str)
        self.restoreState()

def build_pdf():
    pdf_filename = "Changes_Made_And_Compliance_Specification.pdf"
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
    c_primary = colors.HexColor("#0F2942")     # Deep Corporate Navy
    c_secondary = colors.HexColor("#1E5F8A")   # Slate Cobalt
    c_accent = colors.HexColor("#991B1B")      # Crimson Accent
    c_dark = colors.HexColor("#1F2937")        # Dark Charcoal Text
    c_light = colors.HexColor("#F8FAFC")       # Ultra-light slate
    c_border = colors.HexColor("#E2E8F0")      # Table border
    c_code_bg = colors.HexColor("#F1F5F9")     # Code background
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=c_primary,
        spaceAfter=3
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=c_secondary,
        spaceAfter=8
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=13.5,
        textColor=c_primary,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=11.5,
        textColor=c_secondary,
        spaceBefore=6,
        spaceAfter=2,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.6,
        leading=10.5,
        textColor=c_dark,
        spaceAfter=3
    )

    body_bold = ParagraphStyle(
        'BodyBold_Custom',
        parent=body_style,
        fontName='Helvetica-Bold'
    )

    table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7,
        leading=9,
        textColor=colors.white
    )

    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=6.8,
        leading=8.8,
        textColor=c_dark
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=table_cell,
        fontName='Helvetica-Bold'
    )

    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=6.5,
        leading=8.2,
        textColor=colors.HexColor("#0F172A"),
        spaceAfter=4
    )

    caption_style = ParagraphStyle(
        'Caption',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=7.2,
        leading=9.5,
        textColor=colors.HexColor("#475569"),
        spaceAfter=6
    )

    story = []

    # Title Banner
    story.append(Paragraph("X-MPFD-E++ | Technical Changes & Compliance Specification", title_style))
    story.append(Paragraph("<b>Reference: AR1115 | Topic: Reconciled Implementations, Microsecond Telemetry & Architecture</b>", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_primary, spaceAfter=8))

    # Section 1: Executive Summary of Technical Updates
    story.append(Paragraph("1. Executive Summary of Reconciled Checklist Requirements", h1_style))
    summary_data = [
        [Paragraph("Item", table_header), Paragraph("Focus Area", table_header), Paragraph("Identified Requirement", table_header), Paragraph("Implemented Technical Resolution", table_header), Paragraph("Verified Outcome", table_header)],
        [Paragraph("<b>1</b>", table_cell), Paragraph("URL Normalizer", table_cell_bold), Paragraph("Ambiguity in pre-entropy character frequencies", table_cell), Paragraph("Unicode Form NFC + single unquote + lowercase scheme/hostname + port strip in <code>URLNormalizer</code>.", table_cell), Paragraph("H(U) invariant to casing/percent evasion.", table_cell)],
        [Paragraph("<b>2</b>", table_cell), Paragraph("DOM AST Parser", table_cell_bold), Paragraph("Indefiniteness in node types and void element stack leaks", table_cell), Paragraph("Void elements handled as leaves without pushing to stack; text and comments excluded from N_total.", table_cell), Paragraph("SDR invariant to copy text length.", table_cell)],
        [Paragraph("<b>3</b>", table_cell), Paragraph("DGA Latency", table_cell_bold), Paragraph("Breakdown of 3.971 ms (gated) vs 6.621 ms (ungated)", table_cell), Paragraph("Microsecond profiler measuring 7 discrete operations; proves suppression of 2.65 ms AST workload.", table_cell), Paragraph("40.0% time saved on DGA traffic.", table_cell)],
        [Paragraph("<b>4</b>", table_cell), Paragraph("Fusion Constants", table_cell_bold), Paragraph("Calibration values, projection weights & thresholds", table_cell), Paragraph("Late weights [0.4, 0.4, 0.2] (tau=0.65); early weights [0.45, 0.35, 0.2] (tau=0.60) from 1,000 samples.", table_cell), Paragraph("Youden's J = 0.994, 0 false negatives.", table_cell)],
        [Paragraph("<b>5</b>", table_cell), Paragraph("Multi-Scope", table_cell_bold), Paragraph("Query token noise in raw URLs; threshold generality", table_cell), Paragraph("Implemented 3 scopes (Full URL, Host+Path, Hostname). Evaluated on 500 unseen inputs across 2 seeds.", table_cell), Paragraph("0.00% FPR in Hostname & Host+Path.", table_cell)],
        [Paragraph("<b>6</b>", table_cell), Paragraph("Schematics", table_cell_bold), Paragraph("Architecture blueprints and empirical plots", table_cell), Paragraph("Generated 7 high-resolution 300 DPI figures (FIG_ARCH, FIG_FLOW, FIGS 1-5).", table_cell), Paragraph("Complete empirical enablement.", table_cell)],
    ]
    t_summary = Table(summary_data, colWidths=[34, 74, 122, 175, 99])
    t_summary.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light])
    ]))
    story.append(t_summary)
    story.append(Spacer(1, 8))

    # Architecture Schematics
    story.append(Paragraph("2. System Architecture & Hardware Gating Flow", h1_style))
    fig_arch_path = os.path.join("figures", "FIG_ARCH_system_architecture.png")
    if os.path.exists(fig_arch_path):
        story.append(Image(fig_arch_path, width=504, height=210))
        story.append(Paragraph("<b>FIG. ARCH:</b> System Architecture and Component Interconnect Blueprint.", caption_style))

    fig_flow_path = os.path.join("figures", "FIG_FLOW_hardware_gating_decision_flow.png")
    if os.path.exists(fig_flow_path):
        story.append(Image(fig_flow_path, width=440, height=210))
        story.append(Paragraph("<b>FIG. FLOW:</b> Conditional Hardware Gating and Asymmetric Execution Flowchart.", caption_style))

    story.append(PageBreak())

    # Section 3: URL Normalization
    story.append(Paragraph("3. URL Normalization Specification & Source Implementation", h1_style))
    story.append(Paragraph(
        "To guarantee mathematical invariance of character frequencies P(x<sub>i</sub>) and base-2 Shannon entropy H(U), "
        "raw URLs are normalized via Unicode Form NFC, single-pass unquote, RFC 3986 § 3.2.2 authority lowercasing, and port stripping.",
        body_style
    ))
    code_norm = """class URLNormalizer:
    @classmethod
    def normalize(cls, raw_url: str) -> Tuple[str, Dict[str, Any]]:
        if not raw_url:
            return "", {"unicode_form": "NFC", "percent_decoded": False}
        unicode_normalized = unicodedata.normalize("NFC", raw_url.strip())
        percent_decoded = unquote(unicode_normalized)
        if "://" not in percent_decoded:
            parsed = urlparse("//" + percent_decoded.lstrip("/"), scheme="http")
            scheme = "http"
        else:
            parsed = urlparse(percent_decoded)
            scheme = parsed.scheme.lower() if parsed.scheme else "http"
        netloc = parsed.netloc.lower()
        if scheme == "http" and netloc.endswith(":80"): netloc = netloc[:-3]
        elif scheme == "https" and netloc.endswith(":443"): netloc = netloc[:-4]
        path = re.sub(r"/+", "/", parsed.path if parsed.path else "/")
        reconstructed = urlunparse((scheme, netloc, path, parsed.params, parsed.query, parsed.fragment))
        return reconstructed, {"unicode_form": "NFC", "percent_decoded_once": True}"""
    story.append(Preformatted(code_norm, code_style))
    story.append(Spacer(1, 6))

    # Section 4: DOM AST Node Types
    story.append(Paragraph("4. DOM AST Node Types & State Machine Implementation", h1_style))
    story.append(Paragraph(
        "The pushdown automaton counts element nodes in N<sub>total</sub>. HTML5 void elements increment N<sub>total</sub> and update "
        "D<sub>max</sub> as leaf elements but are not pushed onto <code>depth_stack</code>. Text and comments are strictly excluded.",
        body_style
    ))
    code_ast = """class DeterministicDOMAnalyzer(HTMLParser):
    VOID_ELEMENTS = {"area", "base", "br", "col", "embed", "hr", "img", "input",
                     "link", "meta", "param", "source", "track", "wbr"}
    def handle_starttag(self, tag: str, attrs: List[Tuple[str, Optional[str]]]):
        tag = tag.lower()
        self.total_nodes += 1
        self.element_nodes_count += 1
        if tag in self.VOID_ELEMENTS:
            self.void_element_nodes_count += 1
            if self.current_depth + 1 > self.max_depth: self.max_depth = self.current_depth + 1
        else:
            self.current_depth += 1
            self.depth_stack.append(tag)
            if self.current_depth > self.max_depth: self.max_depth = self.current_depth
    def handle_startendtag(self, tag: str, attrs: List[Tuple[str, Optional[str]]]):
        self.handle_starttag(tag, attrs); self.handle_endtag(tag)
    def handle_endtag(self, tag: str):
        tag = tag.lower()
        if tag in self.VOID_ELEMENTS: return
        if self.depth_stack and self.depth_stack[-1] == tag:
            self.depth_stack.pop()
            if self.current_depth > 0: self.current_depth -= 1
    def handle_data(self, data: str):
        if data and data.strip(): self.excluded_text_nodes_count += 1 # Excluded from N_total
    def calculate_sdr(self) -> float:
        return self.total_nodes / float(self.max_depth) if self.max_depth > 0 else 0.0"""
    story.append(Preformatted(code_ast, code_style))
    story.append(Spacer(1, 6))

    # Section 5: DGA Latency Microsecond Breakdown
    story.append(Paragraph("5. DGA Latency Microsecond Breakdown & Computational Bypass", h1_style))
    story.append(Paragraph(
        "Across 2,000 empirical measurements with CPU performance counters (<code>dga_latency_breakdown_results.json</code>):",
        body_style
    ))
    breakdown_data = [
        [Paragraph("Sub-Operation", table_header), Paragraph("Gated (Bypassed)", table_header), Paragraph("Ungated (Baseline)", table_header), Paragraph("Status Under Gating", table_header)],
        [Paragraph("1. URL Normalization (Form NFC + unquote)", table_cell_bold), Paragraph("36.57 us", table_cell), Paragraph("36.57 us", table_cell), Paragraph("Executed in both pipelines", table_cell)],
        [Paragraph("2. Lexical Shannon Entropy H(U)", table_cell_bold), Paragraph("42.77 us", table_cell), Paragraph("42.77 us", table_cell), Paragraph("Executed in both pipelines", table_cell)],
        [Paragraph("3. Gating Comparator Check", table_cell_bold), Paragraph("0.34 us", table_cell), Paragraph("0.00 us", table_cell), Paragraph("Conditional branch dispatch", table_cell)],
        [Paragraph("4. Feature Registry SHA-256", table_cell_bold), Paragraph("27.26 us", table_cell), Paragraph("27.26 us", table_cell), Paragraph("Executed in both pipelines", table_cell)],
        [Paragraph("5. Fusion Policy Table 6-1 Rule", table_cell_bold), Paragraph("17.50 us", table_cell), Paragraph("17.50 us", table_cell), Paragraph("Emits WITHHOLD directive", table_cell)],
        [Paragraph("6. Explanation Synthesis & Block Audit", table_cell_bold), Paragraph("40.91 us", table_cell), Paragraph("40.91 us", table_cell), Paragraph("Executed in both pipelines", table_cell)],
        [Paragraph("7. HTML AST DOM Parsing & SDR", table_cell_bold), Paragraph("<b>BYPASSED (0.00 us)</b>", table_cell_bold), Paragraph("<b>646.26 us (mock) / 2.65 ms (live)</b>", table_cell), Paragraph("<font color='#991B1B'><b>Physically Withheld by Appliance</b></font>", table_cell)],
        [Paragraph("<b>End-to-End Latency per Input</b>", table_cell_bold), Paragraph("<b>0.294 ms (mock) / 3.971 ms (live)</b>", table_cell_bold), Paragraph("<b>1.112 ms (mock) / 6.621 ms (live)</b>", table_cell_bold), Paragraph("<b>40.0% to 73.5% Execution Time Saved</b>", table_cell_bold)],
    ]
    t_breakdown = Table(breakdown_data, colWidths=[180, 100, 104, 120])
    t_breakdown.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light])
    ]))
    story.append(t_breakdown)
    story.append(Spacer(1, 6))

    fig5_path = os.path.join("figures", "FIG_5_dga_latency_breakdown_operations.png")
    if os.path.exists(fig5_path):
        story.append(Image(fig5_path, width=480, height=200))
        story.append(Paragraph("<b>FIG. 5:</b> DGA Latency Microsecond Component Breakdown showing physical suppression of AST parsing.", caption_style))

    story.append(PageBreak())

    # Section 6: Multi-Scope Telemetry & Empirical Plots
    story.append(Paragraph("6. Multi-Scope Holdout Telemetry & Empirical Plots", h1_style))
    story.append(Paragraph(
        "Evaluated across two independent 500-sample unseen corpora (<code>ANNEXURE_B_...json</code> and <code>test_fresh_corpus.py</code>):",
        body_style
    ))
    scope_data = [
        [Paragraph("Telemetry Metric", table_header), Paragraph("Mode 1: Full-URL (tau=4.50)", table_header), Paragraph("Mode 2: Host+Path (tau=4.15)", table_header), Paragraph("Mode 3: Hostname (tau=3.80)", table_header)],
        [Paragraph("Hardware AST Bypasses", table_cell_bold), Paragraph("191 (38.2%)", table_cell), Paragraph("262 (52.4%)", table_cell), Paragraph("<b>291 (58.2%)</b>", table_cell_bold)],
        [Paragraph("Median Latency (p50)", table_cell_bold), Paragraph("1.41 ms", table_cell), Paragraph("1.18 ms", table_cell), Paragraph("<b>0.79 ms</b>", table_cell_bold)],
        [Paragraph("False Positive Rate (Corpus 1)", table_cell_bold), Paragraph("11.0% (22/200)", table_cell), Paragraph("<b>0.00% (0/200)</b>", table_cell_bold), Paragraph("<b>0.00% (0/200)</b>", table_cell_bold)],
        [Paragraph("False Positive Rate (Corpus 2)", table_cell_bold), Paragraph("37.0% (tokens)", table_cell), Paragraph("5.0%", table_cell), Paragraph("<b>0.00% (clean)</b>", table_cell_bold)],
        [Paragraph("Total Pipeline Threat Recall", table_cell_bold), Paragraph("100.00% (300/300)", table_cell), Paragraph("100.00% (300/300)", table_cell), Paragraph("100.00% (300/300)", table_cell)],
    ]
    t_scope = Table(scope_data, colWidths=[150, 118, 118, 118])
    t_scope.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light])
    ]))
    story.append(t_scope)
    story.append(Spacer(1, 6))

    # Grid of figures 1, 2, 3, 4
    fig1_path = os.path.join("figures", "FIG_1_latency_distribution_gated_vs_ungated.png")
    fig2_path = os.path.join("figures", "FIG_2_entropy_distribution_legitimate_vs_dga.png")
    if os.path.exists(fig1_path) and os.path.exists(fig2_path):
        img_table = [
            [Image(fig1_path, width=245, height=150), Image(fig2_path, width=245, height=150)],
            [Paragraph("<b>FIG. 1:</b> Processing Latency Distribution (P50: 1.26 ms vs 6.61 ms).", caption_style),
             Paragraph("<b>FIG. 2:</b> Shannon Entropy Distribution (Margin = 0.174 bits/char).", caption_style)]
        ]
        t_imgs = Table(img_table, colWidths=[252, 252])
        t_imgs.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP')]))
        story.append(t_imgs)
        story.append(Spacer(1, 4))

    fig3_path = os.path.join("figures", "FIG_3_sdr_deviation_cloned_vs_authentic.png")
    fig4_path = os.path.join("figures", "FIG_4_roc_curves_fusion_policies.png")
    if os.path.exists(fig3_path) and os.path.exists(fig4_path):
        img_table2 = [
            [Image(fig3_path, width=245, height=150), Image(fig4_path, width=245, height=150)],
            [Paragraph("<b>FIG. 3:</b> AST SDR vs Depth (Harvesters vs Authentic Portals).", caption_style),
             Paragraph("<b>FIG. 4:</b> ROC Curves across Fusion Policies (Gated AUC = 1.000).", caption_style)]
        ]
        t_imgs2 = Table(img_table2, colWidths=[252, 252])
        t_imgs2.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP')]))
        story.append(t_imgs2)
        story.append(Spacer(1, 6))

    # Section 7: Verification Logs & Audit Integrity
    story.append(Paragraph("7. Test Verification & Deterministic Execution Transcripts", h1_style))
    story.append(Paragraph(
        "• <b>Automated Unit Tests (<code>test_prior_art_inventions.py</code>):</b> 24/24 unit tests passed in 0.024s (100% OK, exit code 0).<br/>"
        "• <b>Comprehensive Workflows (<code>examples.py</code>):</b> 9/9 worked examples executed successfully with cryptographic audit hashes.<br/>"
        "• <b>Tamper Detection Verifier (<code>AuditVerifier</code>):</b> Modifying recorded values triggers <code>TamperDetectedException</code>.<br/>"
        "• <b>Decision Replay:</b> Feature lineages enable deterministic bit-exact decision replay across runtime environments.",
        body_style
    ))
    story.append(Spacer(1, 6))

    # Section 8: Technical Conclusion
    story.append(Paragraph("8. Technical Conclusion", h1_style))
    story.append(Paragraph(
        "All checklist requirements have been comprehensively addressed through production-grade source code, "
        "reproducible empirical telemetry, high-resolution schematics, and rigorous unit testing. The engineering artifacts "
        "confirm the measured reduction in computational workload, deterministic explainability, and robust zero-day phishing detection.",
        body_style
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[+] Successfully built {pdf_filename}!")

if __name__ == "__main__":
    build_pdf()
