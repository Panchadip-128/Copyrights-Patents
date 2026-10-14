"""
Architecture & Decision Flow Diagram Generator
Script: generate_architecture_diagrams.py
Project: X-MPFD-E++

Generates publication-quality 300 DPI system architecture and hardware control flow diagrams
with generous spacing, orthogonal non-overlapping routing, and zero label collisions:
- figures/FIG_ARCH_system_architecture.png
- figures/FIG_FLOW_hardware_gating_decision_flow.png
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch

OUTPUT_DIR = "figures"
os.makedirs(OUTPUT_DIR, exist_ok=True)

plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'

def generate_system_architecture_diagram():
    print("[*] Generating System Architecture Diagram (FIG_ARCH)...")
    fig, ax = plt.subplots(figsize=(12, 8.5), dpi=300)
    ax.set_xlim(0, 120)
    ax.set_ylim(0, 100)
    ax.axis('off')

    ax.add_patch(patches.Rectangle((0, 0), 120, 100, facecolor='#F8FAFC', edgecolor='none'))

    def draw_box(x, y, w, h, title, subtitle="", color='#1E3A8A', fill='#EFF6FF', edgecolor='#3B82F6'):
        box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.8,rounding_size=1.5",
                             facecolor=fill, edgecolor=edgecolor, linewidth=1.5)
        ax.add_patch(box)
        if subtitle:
            ax.text(x + w/2, y + h*0.62, title, ha='center', va='center', fontsize=9, fontweight='bold', color=color)
            ax.text(x + w/2, y + h*0.28, subtitle, ha='center', va='center', fontsize=7.2, color='#475569')
        else:
            ax.text(x + w/2, y + h*0.5, title, ha='center', va='center', fontsize=9, fontweight='bold', color=color)

    # Layer 1: Ingestion & Normalization (Top row, y = 78 to 94)
    draw_box(4, 78, 34, 15, "Network Packet Ingestion", "Wire-speed Ethernet / TCP Streams", color='#0F172A', fill='#F1F5F9', edgecolor='#94A3B8')
    draw_box(43, 78, 34, 15, "Deterministic URL Normalizer", "Unicode Form NFC + Single unquote", color='#0F172A', fill='#F1F5F9', edgecolor='#94A3B8')
    draw_box(82, 78, 34, 15, "Lexical Shannon Entropy H(U)", "O(L) character frequency scan", color='#1E3A8A', fill='#EFF6FF', edgecolor='#3B82F6')

    # Layer 2: Gating Comparator (Center, y = 50 to 66)
    draw_box(43, 50, 34, 16, "Hardware Gating Comparator", "Condition: H(U) > tau (4.50 / 4.15 / 3.80)", color='#991B1B', fill='#FEF2F2', edgecolor='#EF4444')

    # Layer 3: Branches (y = 20 to 38)
    draw_box(4, 18, 34, 20, "Hardware Directive:\nWITHHOLD_PARSER_AND_RENDERER", "O(L) early exit | Drop packet\nSaves 2.65 ms AST compute", color='#991B1B', fill='#FEE2E2', edgecolor='#DC2626')
    draw_box(43, 18, 34, 20, "Deterministic DOM AST Parser", "Tag-stack state machine\nCalculates SDR = N / D_max", color='#1E40AF', fill='#DBEAFE', edgecolor='#2563EB')
    draw_box(82, 18, 34, 20, "Transport & Form POST Analyzer", "TLS certificate verification\nTarget action endpoint check", color='#15803D', fill='#DCFCE7', edgecolor='#16A34A')

    # Layer 4: Feature Lineage & Fusion Core (Bottom, y = 2 to 11)
    draw_box(15, 2, 90, 10, "Cryptographic Feature Registry & Deterministic Fusion Core", "RFC 8785 Canonical JSON Serialization | Persistent SHA-256 Lineage DAG", color='#1E293B', fill='#F8FAFC', edgecolor='#64748B')

    # Connectors
    def draw_arrow(x1, y1, x2, y2, label="", label_pos=(0, 0), color='#334155'):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", color=color, lw=1.8, shrinkA=3, shrinkB=3))
        if label:
            lx = (x1 + x2) / 2 + label_pos[0]
            ly = (y1 + y2) / 2 + label_pos[1]
            ax.text(lx, ly, label, ha='center', va='center', fontsize=7.5, fontweight='bold', color=color)

    # Top row connections
    draw_arrow(38, 85.5, 43, 85.5)
    draw_arrow(77, 85.5, 82, 85.5)

    # Top right down to center comparator
    ax.annotate('', xy=(60, 66), xytext=(99, 78),
                arrowprops=dict(arrowstyle="->", color='#3B82F6', lw=1.8, shrinkA=3, shrinkB=3))
    ax.text(82, 70, "Entropy H(U)", ha='center', fontsize=7.5, fontweight='bold', color='#1E3A8A')

    # From Gating Comparator to Left Branch (WITHHOLD)
    ax.annotate('', xy=(21, 38), xytext=(43, 56),
                arrowprops=dict(arrowstyle="->", color='#DC2626', lw=2.0, shrinkA=3, shrinkB=3))
    ax.text(28, 51, "YES: H(U) > tau\n(DGA Threat)", ha='center', fontsize=8, fontweight='bold', color='#B91C1C')

    # From Gating Comparator to Middle Branch (ALLOCATE AST)
    draw_arrow(60, 50, 60, 38, label="NO: Allocate", label_pos=(7, 0), color='#1D4ED8')

    # From Gating Comparator to Right Branch (Transport)
    ax.annotate('', xy=(99, 38), xytext=(77, 56),
                arrowprops=dict(arrowstyle="->", color='#16A34A', lw=1.8, shrinkA=3, shrinkB=3))
    ax.text(93, 51, "Evaluate TLS", ha='center', fontsize=7.5, fontweight='bold', color='#15803D')

    # From Layer 3 to Layer 4
    draw_arrow(21, 18, 35, 12, color='#991B1B')
    draw_arrow(60, 18, 60, 12, color='#1E40AF')
    draw_arrow(99, 18, 85, 12, color='#15803D')

    plt.title("X-MPFD-E++ System Architecture & Component Interconnect Blueprint", fontsize=12, fontweight='bold', pad=14, color='#0F172A')
    plt.tight_layout()

    out_png = os.path.join(OUTPUT_DIR, "FIG_ARCH_system_architecture.png")
    plt.savefig(out_png, dpi=300)
    plt.close()
    print(f"    [+] Saved {out_png}")

def generate_decision_flowchart():
    print("[*] Generating Decision Flowchart (FIG_FLOW)...")
    # Generous dimensions so all boxes, labels, and orthogonal arrows have complete clearance
    fig, ax = plt.subplots(figsize=(12, 11), dpi=300)
    ax.set_xlim(0, 120)
    ax.set_ylim(0, 120)
    ax.axis('off')

    ax.add_patch(patches.Rectangle((0, 0), 120, 120, facecolor='#FFFFFF', edgecolor='none'))

    def draw_step(x, y, w, h, text, color='#0F172A', fill='#F8FAFC', border='#94A3B8'):
        box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.6,rounding_size=1.2",
                             facecolor=fill, edgecolor=border, linewidth=1.5)
        ax.add_patch(box)
        ax.text(x + w/2, y + h/2, text, ha='center', va='center', fontsize=8.5, fontweight='bold', color=color)

    def draw_diamond(cx, cy, w, h, text, color='#991B1B', fill='#FEF2F2', border='#DC2626'):
        poly = patches.Polygon([
            (cx, cy + h/2),
            (cx + w/2, cy),
            (cx, cy - h/2),
            (cx - w/2, cy)
        ], closed=True, facecolor=fill, edgecolor=border, linewidth=1.5)
        ax.add_patch(poly)
        ax.text(cx, cy, text, ha='center', va='center', fontsize=8, fontweight='bold', color=color)

    # -------------------------------------------------------------
    # Main Spine (Center at x = 60)
    # -------------------------------------------------------------
    # Step 1: Ingest Raw URL (y = 104 to 112)
    draw_step(35, 104, 50, 8, "Ingest Raw URL String U_raw", fill='#F1F5F9', border='#64748B')

    # Step 2: URL Normalization (y = 90 to 98)
    draw_step(27, 90, 66, 8, "URL Normalization (Form NFC + single unquote + lowercase host)", fill='#F1F5F9', border='#64748B')

    # Step 3: Shannon Entropy Calculation (y = 76 to 84)
    draw_step(27, 76, 66, 8, "Calculate Shannon Entropy H(U) = -SUM(p log2 p) [Linear O(L)]", fill='#EFF6FF', border='#3B82F6')

    # Diamond 1: Gating Comparator (center at x=60, y=62, w=36, h=12)
    draw_diamond(60, 62, 36, 12, "H(U) > tau ?\n(Gating Threshold)", color='#991B1B', fill='#FEF2F2', border='#DC2626')

    # Connectors for main top spine
    ax.annotate('', xy=(60, 98), xytext=(60, 104), arrowprops=dict(arrowstyle="->", color='#334155', lw=1.6))
    ax.annotate('', xy=(60, 84), xytext=(60, 90), arrowprops=dict(arrowstyle="->", color='#334155', lw=1.6))
    ax.annotate('', xy=(60, 68), xytext=(60, 76), arrowprops=dict(arrowstyle="->", color='#334155', lw=1.6))

    # -------------------------------------------------------------
    # Left Branch: Early Exit for DGAs (YES: H(U) > tau)
    # Left diamond vertex is at (42, 62)
    # -------------------------------------------------------------
    # Orthogonal arrow: Left to x=22, then down to y=44
    ax.plot([42, 22, 22], [62, 62, 44], color='#DC2626', lw=1.8)
    ax.annotate('', xy=(22, 44), xytext=(22, 46), arrowprops=dict(arrowstyle="->", color='#DC2626', lw=1.8))
    # Label placed cleanly above horizontal path with clear background
    ax.text(32, 64.5, "YES: H(U) > tau\n(Zero-Day DGA)", ha='center', va='bottom', fontsize=8, fontweight='bold', color='#B91C1C',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#FFF5F5', edgecolor='#FEB2B2', alpha=0.9))

    # Left Result Box: centered at x=22, y=34, w=34, h=16
    draw_step(5, 26, 34, 16, "DECISION: PHISHING_DGA\nRisk = 0.99 (High Confidence)\nDirective: WITHHOLD_PARSER\n(Bypasses HTML AST Parsing)",
              color='#991B1B', fill='#FEE2E2', border='#DC2626')

    # -------------------------------------------------------------
    # Right Branch: Normal Downstream Pipeline (NO: H(U) <= tau)
    # Right diamond vertex is at (78, 62)
    # -------------------------------------------------------------
    # Orthogonal arrow: Right to x=96, then down to y=54
    ax.plot([78, 96, 96], [62, 62, 54], color='#2563EB', lw=1.8)
    ax.annotate('', xy=(96, 54), xytext=(96, 56), arrowprops=dict(arrowstyle="->", color='#2563EB', lw=1.8))
    # Label placed cleanly above horizontal path with clear background
    ax.text(87, 64.5, "NO: H(U) <= tau\n(Allocate Threads)", ha='center', va='bottom', fontsize=8, fontweight='bold', color='#1D4ED8',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#EFF6FF', edgecolor='#BFDBFE', alpha=0.9))

    # Right Step 1: Allocate Worker Threads (y = 44 to 52, center=(96, 48), w=38, h=8)
    draw_step(77, 44, 38, 8, "Allocate Parser Worker Threads\nExecute HTML AST State Machine", color='#1E40AF', fill='#DBEAFE', border='#2563EB')

    # Arrow down to Step 2
    ax.annotate('', xy=(96, 36), xytext=(96, 44), arrowprops=dict(arrowstyle="->", color='#2563EB', lw=1.6))

    # Right Step 2: Compute SDR (y = 28 to 36, center=(96, 32), w=38, h=8)
    draw_step(77, 28, 38, 8, "Calculate Structural Density\nSDR = N_total / D_max", color='#1E40AF', fill='#DBEAFE', border='#2563EB')

    # Arrow down to Diamond 2
    ax.annotate('', xy=(96, 21), xytext=(96, 28), arrowprops=dict(arrowstyle="->", color='#2563EB', lw=1.6))

    # Diamond 2: Cloned Harvester Check (center at x=96, y=15, w=32, h=10)
    # Top: (96, 20), Bottom: (96, 10), Left: (80, 15), Right: (112, 15)
    draw_diamond(96, 15, 32, 10, "Delta SDR > 50% ?\n& TLS Invalid", color='#C2410C', fill='#FFF7ED', border='#EA580C')

    # Diamond 2 Left Branch: Phishing Clone (from (80, 15) to left x=58, down to y=8)
    ax.plot([80, 58, 58], [15, 15, 8], color='#EA580C', lw=1.8)
    ax.annotate('', xy=(58, 8), xytext=(58, 10), arrowprops=dict(arrowstyle="->", color='#EA580C', lw=1.8))
    ax.text(69, 17, "YES (Clone)", ha='center', va='bottom', fontsize=7.5, fontweight='bold', color='#C2410C',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='#FFF7ED', edgecolor='#FDBA74'))

    draw_step(43, 1, 30, 7, "DECISION: PHISHING_CLONE\nRisk = 0.95 | Directive: ISOLATE", color='#9A3412', fill='#FFEDD5', border='#EA580C')

    # Diamond 2 Bottom Branch: Legitimate (from (96, 10) down to y=8)
    ax.annotate('', xy=(96, 8), xytext=(96, 10), arrowprops=dict(arrowstyle="->", color='#16A34A', lw=1.8))
    ax.text(105, 9, "NO (Safe)", ha='left', va='center', fontsize=7.5, fontweight='bold', color='#15803D')

    draw_step(81, 1, 30, 7, "DECISION: LEGITIMATE\nRisk = 0.05 | Directive: ALLOW_STREAM", color='#166534', fill='#DCFCE7', border='#16A34A')

    plt.title("X-MPFD-E++ Conditional Hardware Gating & Execution Flowchart", fontsize=12, fontweight='bold', pad=14, color='#0F172A')
    plt.tight_layout()

    out_png = os.path.join(OUTPUT_DIR, "FIG_FLOW_hardware_gating_decision_flow.png")
    plt.savefig(out_png, dpi=300)
    plt.close()
    print(f"    [+] Saved {out_png}")

if __name__ == "__main__":
    generate_system_architecture_diagram()
    generate_decision_flowchart()
