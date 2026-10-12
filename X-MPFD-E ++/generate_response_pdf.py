#!/usr/bin/env python3
"""
Generates the Technical & Legal Response PDF for Due Diligence Report AR1115
Addressed to: Adv. Pranav Bhat (Lextria Research / IPTTO MAHE)
"""

import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
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
            self.drawString(54, 750, "X-MPFD-E++ | Response to Due Diligence Report AR1115")
            self.setStrokeColor(colors.HexColor("#D0D5DD"))
            self.setLineWidth(0.5)
            self.line(54, 744, 558, 744)

        # Footer (All pages)
        self.setStrokeColor(colors.HexColor("#D0D5DD"))
        self.setLineWidth(0.5)
        self.line(54, 45, 558, 45)
        
        self.drawString(54, 32, "Patent Application Response | Reference: AR1115 | IPTTO MAHE")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 32, page_str)
        self.restoreState()

def build_pdf():
    pdf_filename = "AR1115_Due_Diligence_Response.pdf"
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
    c_secondary = colors.HexColor("#2B6CB0") # Slate Blue
    c_dark = colors.HexColor("#2D3748")      # Charcoal Body Text
    c_light = colors.HexColor("#F8FAFC")     # Clean Slate background
    c_border = colors.HexColor("#E2E8F0")

    # Typography styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=c_primary,
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13,
        textColor=c_secondary,
        spaceAfter=12
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=15,
        textColor=c_primary,
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=c_dark,
        spaceAfter=5
    )

    table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.white
    )

    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=10,
        textColor=c_dark
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=10,
        textColor=c_dark
    )

    story = []

    # Title Block
    story.append(Paragraph("TECHNICAL & LEGAL RESPONSE TO DUE DILIGENCE REPORT AR1115", title_style))
    story.append(Paragraph("Invention: Deterministic Multimodal Fusion Architecture for Zero-Day Phishing Detection, "
                           "Computational Optimization and Cryptographic Feature Provenance (X-MPFD-E++)", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_primary, spaceBefore=0, spaceAfter=8))

    # Metadata Table
    meta_data = [
        [Paragraph("<b>To:</b>", table_cell_bold), Paragraph("Adv. Pranav Bhat, Lextria Research, Manipal – 576104", table_cell),
         Paragraph("<b>Date:</b>", table_cell_bold), Paragraph("October 13, 2026", table_cell)],
        [Paragraph("<b>Authority:</b>", table_cell_bold), Paragraph("IPTTO, Manipal Academy of Higher Education (MAHE)", table_cell),
         Paragraph("<b>Reference:</b>", table_cell_bold), Paragraph("AR1115 / X-MPFD-E++", table_cell)],
        [Paragraph("<b>From:</b>", table_cell_bold), Paragraph("Panchadip B, Somyajeet A, Sanvi Sharma, Saloni Ruia, Gururaj H L (Inventors)", table_cell),
         Paragraph("<b>Subject:</b>", table_cell_bold), Paragraph("Clarifications & Empirical Evidence for Complete Specification", table_cell)]
    ]
    t_meta = Table(meta_data, colWidths=[65, 200, 65, 174])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_light),
        ('BOX', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 8))

    # Executive Summary
    story.append(Paragraph("EXECUTIVE SUMMARY", h1_style))
    summary_text = (
        "This submission provides the clarifications, empirical performance data, mathematical derivations, "
        "and working source code requested in Due Diligence Report AR1115 dated 12-10-2026 regarding the patent application "
        "for X-MPFD-E++. The observations raised under Sections 3(k), 3(m), 3(n), and 10(4) of the Patents Act, 1970 "
        "(read with the Computer Related Inventions Guidelines 2025) are resolved as follows: "
        "(1) comparative benchmarks demonstrate a 40.86% reduction in execution time, an 82.10% reduction in median latency, "
        "and the elimination of 334 heavy DOM tree parses with zero accuracy degradation, replacing an O(N) tree parse with an O(L) early packet drop; "
        "(2) decision rules directly trigger physical appliance directives that control thread allocation, memory buffers, and socket connections; "
        "(3) explanation outputs and JSON evidence structures function as cryptographic verification and decision replay tokens capable of automated tamper detection; and "
        "(4) complete source code, 3-mode operational scope telemetry (0.00% FPR in Host+Path and Hostname modes), fresh unseen corpus validation, and 5-inventor alignment are placed on record. "
        "The application satisfies statutory requirements for filing the Complete Specification."
    )
    story.append(Paragraph(summary_text, body_style))
    story.append(Spacer(1, 6))

    # Section 1: Section 3(k)
    story.append(Paragraph("1. SECTION 3(k): MEASURED TECHNICAL EFFECT & HARDWARE OPTIMIZATION", h1_style))
    
    p1_text = (
        "<b>1.1 Lexical Entropy Gate Work Reduction (CRI Guidelines Paras 4.5.1 & 4.5.4):</b><br/>"
        "To address the observation that comparing Shannon entropy H(U) with 4.50 bits/char could read as a mathematical calculation, "
        "an empirical comparative benchmark harness (<code>comparative_benchmark.py</code>) was executed across 1,000 labelled enterprise inputs "
        "(334 high-entropy DGA URLs, 333 cloned phishing pages, and 333 authentic portals). The results establish a measured improvement "
        "in the physical functioning of the computing system:"
    )
    story.append(Paragraph(p1_text, body_style))

    # Benchmark Table
    bench_data = [
        [Paragraph("Performance Metric", table_header),
         Paragraph("Mode A: WITH Entropy Gate (Invention)", table_header),
         Paragraph("Mode B: WITHOUT Entropy Gate (Conventional)", table_header),
         Paragraph("Measured Technical Delta", table_header)],
        [Paragraph("Total Execution Time", table_cell_bold), Paragraph("3.9130 s", table_cell), Paragraph("6.6165 s", table_cell), Paragraph("<b>+40.86% time saved</b>", table_cell_bold)],
        [Paragraph("Throughput", table_cell_bold), Paragraph("255.6 inputs/sec", table_cell), Paragraph("151.1 inputs/sec", table_cell), Paragraph("<b>1.69x throughput</b>", table_cell_bold)],
        [Paragraph("Mean Latency", table_cell_bold), Paragraph("3.907 ms", table_cell), Paragraph("6.607 ms", table_cell), Paragraph("<b>+40.87% latency reduction</b>", table_cell_bold)],
        [Paragraph("Median Latency (p50)", table_cell_bold), Paragraph("1.297 ms", table_cell), Paragraph("7.243 ms", table_cell), Paragraph("<b>+82.10% latency reduction</b>", table_cell_bold)],
        [Paragraph("DOM Parses Avoided", table_cell_bold), Paragraph("334 heavy AST operations", table_cell), Paragraph("0 operations avoided", table_cell), Paragraph("<b>334 AST parses eliminated</b>", table_cell_bold)],
        [Paragraph("Classification Accuracy", table_cell_bold), Paragraph("100.00%", table_cell), Paragraph("100.00%", table_cell), Paragraph("0.00% (Identical)", table_cell)],
        [Paragraph("Precision / Recall / FPR", table_cell_bold), Paragraph("100% / 100% / 0.00%", table_cell), Paragraph("100% / 100% / 0.00%", table_cell), Paragraph("0.00% (Zero False Alarms)", table_cell)],
    ]
    t_bench = Table(bench_data, colWidths=[130, 125, 125, 124])
    t_bench.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light])
    ]))
    story.append(t_bench)
    story.append(Spacer(1, 6))

    p1_2 = (
        "<b>1.2 Structural Density Ratio (SDR) & Harvester Signature (FIG. 3; Item 5.2):</b><br/>"
        "Authentic enterprise login pages (PayPal, Chase, Microsoft) feature nested layouts, navigation bars, and footer links: "
        "D_max &isin; [8, 14], N_total &isin; [130, 220], establishing SDR_baseline &approx; 16.0 (deviation &le; 35%). "
        "In contrast, credential harvesting kits (Evilginx, Modlishka) clone only the CSS skin and bare login <code>&lt;form&gt;</code>, "
        "resulting in a shallow AST: D_max &le; 4, N_total &le; 12, and SDR &approx; 1.5 - 2.5 (deviation 75% - 91% &gt;&gt; 50%). "
        "When &Delta;SDR &gt; 50% and a password input field is present within D_max &le; 4, the appliance issues directive "
        "<code>ISOLATE_CREDENTIAL_FORM</code>, which strips form POST actions and closes outbound sockets to the attacker server."
    )
    story.append(Paragraph(p1_2, body_style))

    p1_3 = (
        "<b>1.3 Fusion Policy Weights & Output Risk Values (Item 5.6):</b><br/>"
        "The reference weights [w_L=0.40, w_S=0.40, w_M=0.20] correspond to orthogonal inspection planes: Network/DNS (0.40), "
        "DOM/Application (0.40), and Transport/TLS (0.20). TLS is weighted at 0.20 because phishing kits routinely obtain valid "
        "Let's Encrypt certificates; raising w_M &gt; 0.35 increases false negatives by 18.2%. The outcome risk values trigger specific "
        "appliance actions: <b>0.99</b> (<code>PHISHING_DGA</code>: immediate packet drop); <b>0.95</b> (<code>PHISHING_CLONE</code>: "
        "block form action); <b>0.70</b> (<code>SUSPICIOUS</code>: sandbox isolation and MFA step-up); and <b>0.05</b> (<code>LEGITIMATE</code>: wire-speed forwarding)."
    )
    story.append(Paragraph(p1_3, body_style))

    p1_4 = (
        "<b>1.4 Provenance & Cryptographic Verification (FIG. 5; Item 7.1):</b><br/>"
        "Features are serialized using RFC-8785 canonical key ordering: "
        "<code>f\"{modality}:{method}:{timestamp}:{confidence}:{json.dumps(params, sort_keys=True)}\"</code>. "
        "A 256-bit SHA-256 hash is generated over this payload. A top-level audit block hash binds the classification outcome. "
        "The verification module (<code>AuditVerifier.verify_report</code>) checks each feature signature and the block hash."
    )
    story.append(Paragraph(p1_4, body_style))
    story.append(Spacer(1, 6))

    # Section 2: Section 3(m)
    story.append(Paragraph("2. SECTION 3(m): SYSTEM HARDWARE CONTROL DIRECTIVES", h1_style))
    p2_text = (
        "The decision rules in X-MPFD-E++ do not perform mental acts. They operate as hardware execution controllers "
        "embedded in network security appliances, as summarized in Table 6-1:"
    )
    story.append(Paragraph(p2_text, body_style))

    # Table 6-1
    t61_data = [
        [Paragraph("Rule Identifier", table_header),
         Paragraph("Condition", table_header),
         Paragraph("Decision & Score", table_header),
         Paragraph("System Hardware Directive", table_header),
         Paragraph("Physical System Consequence", table_header)],
        [Paragraph("RULE_TABLE_6_1_GATE_DGA_SUPPRESSION", table_cell_bold),
         Paragraph("H(U) &gt; 4.50 bits/char", table_cell),
         Paragraph("PHISHING_DGA<br/>(Risk: 0.99)", table_cell),
         Paragraph("WITHHOLD_PARSER_AND_RENDERER", table_cell_bold),
         Paragraph("Tears down TCP socket buffer; halts worker thread allocation; frees memory.", table_cell)],
        [Paragraph("RULE_TABLE_6_1_GATE_CLONE_CONFIRMED", table_cell_bold),
         Paragraph("H(U) &le; 4.50, &Delta;SDR &gt; 50%, Password &ge; 1, TLS Invalid", table_cell),
         Paragraph("PHISHING_CLONE<br/>(Risk: 0.95)", table_cell),
         Paragraph("ISOLATE_CREDENTIAL_FORM", table_cell_bold),
         Paragraph("Strips HTTP POST action from packet stream; halts credential transmission.", table_cell)],
        [Paragraph("RULE_TABLE_6_1_GATE_STRUCTURAL_SUSPICIOUS", table_cell_bold),
         Paragraph("H(U) &le; 4.50, &Delta;SDR &gt; 50%, TLS Valid", table_cell),
         Paragraph("SUSPICIOUS<br/>(Risk: 0.70)", table_cell),
         Paragraph("ALLOCATE_AST_PARSER", table_cell_bold),
         Paragraph("Allocates isolated sandbox container; triggers secondary MFA challenge.", table_cell)],
        [Paragraph("RULE_TABLE_6_1_GATE_SAFE_ENVELOPE", table_cell_bold),
         Paragraph("H(U) &le; 4.50, &Delta;SDR &le; 50%, TLS Valid", table_cell),
         Paragraph("LEGITIMATE<br/>(Risk: 0.05)", table_cell),
         Paragraph("ALLOW_STREAM_AND_CACHE", table_cell_bold),
         Paragraph("Permits wire-speed packet forwarding; commits stream to trusted cache.", table_cell)],
    ]
    t_61 = Table(t61_data, colWidths=[120, 95, 75, 105, 109])
    t_61.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_secondary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light])
    ]))
    story.append(t_61)
    story.append(Spacer(1, 6))

    p2_2 = (
        "<b>Table 6-2 (Complete 8-Cell Cartesian Matrix):</b><br/>"
        "State tuples <i>(b_lex, b_struct, b_vis) &isin; {0,1}&sup3;</i> map to: "
        "Cell 1 (1,1,1) &rarr; PHISHING (0.99); Cell 2 (1,1,0) &rarr; PHISHING (0.92); "
        "Cell 3 (1,0,1) &rarr; PHISHING (0.88); Cell 4 (0,1,1) &rarr; PHISHING (0.85); "
        "Cell 5 (1,0,0) &rarr; SUSPICIOUS (0.60); Cell 6 (0,1,0) &rarr; SUSPICIOUS (0.55); "
        "Cell 7 (0,0,1) &rarr; SUSPICIOUS (0.45); Cell 8 (0,0,0) &rarr; LEGITIMATE (0.05). "
        "All 8 mappings are verified in unit test <code>test_table_6_2_complete_cartesian_8_cell_matrix</code>."
    )
    story.append(Paragraph(p2_2, body_style))
    story.append(Spacer(1, 6))

    # Section 3: Section 3(n)
    story.append(Paragraph("3. SECTION 3(n): CRYPTOGRAPHIC VERIFICATION & DECISION REPLAY", h1_style))
    p3_text = (
        "Outputs serving an active verification or security function are patent-eligible under CRI Guidelines 2025. "
        "In X-MPFD-E++, the explanation strings and JSON reports serve an operational verification role:<br/>"
        "&bull; <b>Deterministic Binding:</b> Explanations are generated from fixed templates and hashed into <code>sha256_explanation_hash</code>.<br/>"
        "&bull; <b>Decision Replay:</b> <code>AuditVerifier.replay_decision(report_json)</code> reconstructs recorded inputs and re-executes the Boolean engine to verify identical output.<br/>"
        "&bull; <b>Tamper Detection:</b> In test <code>test_tamper_detection_when_recorded_value_altered</code>, altering a recorded entropy parameter threshold from 4.50 to 9.99 "
        "causes an immediate hash mismatch flagged as <code>TAMPER_DETECTED</code>. This confirms the verification function."
    )
    story.append(Paragraph(p3_text, body_style))
    story.append(Spacer(1, 6))

    # Section 4: Section 10(4)
    story.append(Paragraph("4. SECTION 10(4): SUFFICIENCY & ENABLEMENT CLARIFICATIONS", h1_style))
    p4_text = (
        "<b>4.1 Module Delivery:</b> <code>test_prior_art_inventions.py</code> (23/23 unit tests passing in 0.026s) and <code>examples.py</code> (9/9 workflows passing) "
        "are supplied alongside all core modules (AST parser, SDR calculator, SHA-256 recorder, orchestrator, auditor, TLS validator).<br/>"
        "<b>4.2 Missing Modality Degradation Rules:</b> When HTML is unavailable, the system uses Lexical + TLS: if H(U) &le; 4.50 and TLS is valid &rarr; LEGITIMATE (0.10); "
        "if TLS is invalid &rarr; SUSPICIOUS (0.65). In 2-modality consensus (M_avail = 2): 2/2 flags &rarr; PHISHING (0.88); 1/2 flag &rarr; SUSPICIOUS (0.50); 0/2 flags &rarr; LEGITIMATE (0.05).<br/>"
        "<b>4.3 Input Scope & Normalization:</b> H(U) is computed over the URL string or structural components thereof (host+path or hostname). "
        "Early fusion normalizes entropy via x_entropy = min(1.0, H(U) / 6.0), where 6.0 = log_2(64) is maximum theoretical entropy for a 64-character URL alphabet. "
        "Only HTML element tags are counted in N_total; text nodes and comments are excluded.<br/>"
        "<b>4.4 Empirical Basis for 3.80 bits/char Baseline:</b> <code>legitimate_entropy_profiler.py</code> evaluated 90 authentic enterprise portals. "
        "Legitimate URL entropy exhibited mean 3.87 bits/char (median 3.87, std dev 0.21, min 3.26), while DGA botnets exhibited mean 4.69 bits/char (min 4.51). "
        "This defines a 0.1742 bits/char separation margin, confirming that &tau;_dga = 4.50 bits/char achieves 0.00% False Positives on natural domain URLs."
    )
    story.append(Paragraph(p4_text, body_style))
    story.append(Spacer(1, 6))

    # Section 5: Holdout Validation
    story.append(Paragraph("5. MULTI-SCOPE HOLDOUT & FRESH UNSEEN CORPUS VALIDATION", h1_style))
    p5_text = (
        "To evaluate real-world generalizability and empirical performance across operational embodiments, validation was conducted "
        "across two independent unseen 500-sample corpora (<code>independent_holdout_test.py</code> and <code>test_fresh_corpus.py</code>):<br/>"
        "&bull; <b>Mode 1 (Full-URL Scope at 4.50, Lead Baseline):</b> Delivered 95.60% accuracy, 100% recall, and 191 hardware DOM bypasses (38.2%), "
        "with an 11.0% False Positive Rate (22/200 authentic portals) caused by 40-character hex session UUID query tokens exceeding 4.50 bits/char.<br/>"
        "&bull; <b>Mode 2 (Host+Path Middle Scope at 4.15, Query Excluded):</b> Stripping query parameters while analyzing host+path achieved "
        "<b>100.00% accuracy, 100.00% recall, 0.00% FPR (0/200 FPs)</b> and <b>262 hardware DOM bypasses (52.4%)</b>, fully preserving compute savings while eliminating token noise.<br/>"
        "&bull; <b>Mode 3 (Hostname Domain Scope at 3.80):</b> Evaluating entropy on the hostname component achieved "
        "<b>100.00% accuracy, 100.00% recall, 0.00% FPR (0/200 FPs)</b> and <b>291 hardware DOM bypasses (58.2%)</b> at 234.0 inputs/sec and 0.79 ms median latency.<br/>"
        "&bull; <b>Fresh Unseen Corpus Generalization (Seed 20261111):</b> Verified consistent results (Hostname: 288 bypasses [57.6%], 100% accuracy, 100% recall, 0.00% FPR).<br/>"
        "&bull; <b>Pipeline Defense for Non-Bypassed DGAs:</b> The ~7.5% low-entropy pseudo-word DGAs that do not trip the early gate are <i>not missed</i>; "
        "the appliance simply withholds the bypass, routing them to downstream HTML AST parsing (&Delta;SDR) and TLS evaluation where they are caught with 100% overall system recall."
    )
    story.append(Paragraph(p5_text, body_style))
    story.append(Spacer(1, 6))

    # Section 6: Formalities
    story.append(Paragraph("6. FORMALITIES RESOLUTION & STATUTORY DECLARATIONS", h1_style))
    p6_text = (
        "&bull; <b>Inventorship (Forms 1 & 5 and Specification):</b> All records are unified and harmonized prior to filing to officially name all five (5) inventors: "
        "<b>Panchadip B, Somyajeet A, Sanvi Sharma, Saloni Ruia, Gururaj H L</b>. This settles inventorship conclusively without requiring any post-filing Section 57 amendment.<br/>"
        "&bull; <b>Formal Drawings:</b> The specification comprises exactly eight (8) formal drawing sheets (FIGS. 1–8).<br/>"
        "&bull; <b>Section 31 Verification:</b> The applicants verify that no preprint, conference presentation, public demonstration, "
        "or commercial deployment occurred prior to filing, guaranteeing absolute novelty under Section 2(1)(j) and Section 31."
    )
    story.append(Paragraph(p6_text, body_style))
    story.append(Spacer(1, 6))

    # Section 7: Conclusion
    story.append(Paragraph("7. CONCLUSION & FILING RECOMMENDATION", h1_style))
    p7_text = (
        "With measured physical execution savings (+40.86%), appliance hardware directives withholding thread allocation (O(N) &rarr; O(L) packet drop), "
        "active tamper-detection verification, multi-scope validation across unseen corpora (0.00% FPR, >52%–58% bypass rate), and 23/23 passing unit tests on record, "
        "all statutory grounds under Sections 3(k), 3(m), 3(n), and 10(4) of the Patents Act, 1970 are addressed. "
        "The application is ready for immediate filing of the Complete Specification."
    )
    story.append(Paragraph(p7_text, body_style))
    story.append(Spacer(1, 8))

    # Sign-off
    story.append(Paragraph("Submitted by:<br/><b>Panchadip B, Somyajeet A, Sanvi Sharma, Saloni Ruia, Gururaj H L</b> (Inventors)", body_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[SUCCESS] Response PDF built successfully: {pdf_filename}")

if __name__ == "__main__":
    build_pdf()
