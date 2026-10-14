"""
Architecture & Decision Flow Diagram Generator
Script: generate_architecture_diagrams.py
Project: X-MPFD-E++

Generates high-resolution 300 DPI system architecture and hardware control flow diagrams:
- figures/FIG_ARCH_system_architecture.png
- figures/FIG_FLOW_hardware_gating_decision_flow.png
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ArrowStyle

OUTPUT_DIR = "figures"
os.makedirs(OUTPUT_DIR, exist_ok=True)

plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'

def generate_system_architecture_diagram():
    print("[*] Generating System Architecture Diagram (FIG_ARCH)...")
    fig, ax = plt.subplots(figsize=(11, 7.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Background subtle styling
    ax.add_patch(patches.Rectangle((0, 0), 100, 100, facecolor='#F8FAFC', edgecolor='none'))

    # Helper function for styled boxes
    def draw_box(x, y, w, h, title, subtitle="", color='#1E3A8A', fill='#EFF6FF', edgecolor='#3B82F6'):
        box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.8,rounding_size=1.5",
                             facecolor=fill, edgecolor=edgecolor, linewidth=1.5)
        ax.add_patch(box)
        ax.text(x + w/2, y + h*0.65, title, ha='center', va='center', fontsize=9.5, fontweight='bold', color=color)
        if subtitle:
            ax.text(x + w/2, y + h*0.32, subtitle, ha='center', va='center', fontsize=7.5, color='#475569')

    # Layer 1: Ingestion & Normalization
    draw_box(4, 76, 26, 16, "Network Packet Ingestion", "Wire-speed Ethernet / TCP Streams", color='#0F172A', fill='#F1F5F9', edgecolor='#94A3B8')
    draw_box(37, 76, 26, 16, "Deterministic URL Normalizer", "Unicode Form NFC + Single unquote", color='#0F172A', fill='#F1F5F9', edgecolor='#94A3B8')
    draw_box(70, 76, 26, 16, "Lexical Shannon Entropy H(U)", "O(L) character frequency scan", color='#1E3A8A', fill='#EFF6FF', edgecolor='#3B82F6')

    # Layer 2: Gating Comparator
    draw_box(35, 48, 30, 18, "Hardware Gating Comparator", "Condition: H(U) > tau (4.50 / 4.15 / 3.80)", color='#991B1B', fill='#FEF2F2', edgecolor='#EF4444')

    # Layer 3: Branch Left (Bypassed) vs Branch Right (Downstream AST & Transport)
    draw_box(4, 20, 26, 20, "Hardware Directive:\nWITHHOLD_PARSER_AND_RENDERER", "O(L) early exit | Drop packet\nSaves 2.65 ms AST compute", color='#991B1B', fill='#FEE2E2', edgecolor='#DC2626')
    draw_box(37, 20, 26, 20, "Deterministic DOM AST Parser", "Tag-stack state machine\nCalculates SDR = N / D_max", color='#1E40AF', fill='#DBEAFE', edgecolor='#2563EB')
    draw_box(70, 20, 26, 20, "Transport & Form POST Analyzer", "TLS certificate verification\nTarget action endpoint check", color='#15803D', fill='#DCFCE7', edgecolor='#16A34A')

    # Layer 4: Feature Lineage & Fusion Core (Bottom)
    draw_box(20, 2, 60, 12, "Cryptographic Feature Registry & Fusion Core", "RFC 8785 Canonical JSON Serialization | Persistent SHA-256 Lineage DAG", color='#1E293B', fill='#F8FAFC', edgecolor='#64748B')

    # Connecting Arrows
    def draw_arrow(x1, y1, x2, y2, label=""):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", color='#334155', lw=1.8, shrinkA=4, shrinkB=4))
        if label:
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            ax.text(mx, my + 1.5, label, ha='center', va='bottom', fontsize=7.5, fontweight='bold', color='#1E293B')

    draw_arrow(30, 84, 37, 84)
    draw_arrow(63, 84, 70, 84)
    draw_arrow(83, 76, 55, 66)

    # From Gating Comparator to branches
    ax.annotate('', xy=(17, 40), xytext=(40, 48),
                arrowprops=dict(arrowstyle="->", color='#DC2626', lw=2.0))
    ax.text(26, 47, "YES: H(U) > tau\n(DGA Threat)", ha='center', fontsize=7.5, fontweight='bold', color='#B91C1C')

    ax.annotate('', xy=(50, 40), xytext=(50, 48),
                arrowprops=dict(arrowstyle="->", color='#2563EB', lw=2.0))
    ax.text(53, 44, "NO: Allocate Threads", ha='left', fontsize=7.5, fontweight='bold', color='#1D4ED8')

    draw_arrow(65, 48, 83, 40)

    # To Bottom Core
    draw_arrow(17, 20, 35, 14)
    draw_arrow(50, 20, 50, 14)
    draw_arrow(83, 20, 65, 14)

    plt.title("X-MPFD-E++ System Architecture & Component Interconnect Blueprint", fontsize=12, fontweight='bold', pad=15, color='#0F172A')
    plt.tight_layout()

    out_png = os.path.join(OUTPUT_DIR, "FIG_ARCH_system_architecture.png")
    plt.savefig(out_png, dpi=300)
    plt.close()
    print(f"    [+] Saved {out_png}")

def generate_decision_flowchart():
    print("[*] Generating Decision Flowchart (FIG_FLOW)...")
    fig, ax = plt.subplots(figsize=(10, 8), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    ax.add_patch(patches.Rectangle((0, 0), 100, 100, facecolor='#FFFFFF', edgecolor='none'))

    def draw_step(x, y, w, h, text, color='#0F172A', fill='#F8FAFC', border='#94A3B8'):
        box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.5,rounding_size=1.0",
                             facecolor=fill, edgecolor=border, linewidth=1.5)
        ax.add_patch(box)
        ax.text(x + w/2, y + h/2, text, ha='center', va='center', fontsize=8.5, fontweight='bold', color=color)

    def draw_diamond(x, y, w, h, text, color='#991B1B', fill='#FEF2F2', border='#DC2626'):
        poly = patches.Polygon([
            (x + w/2, y + h),
            (x + w, y + h/2),
            (x + w/2, y),
            (x, y + h/2)
        ], closed=True, facecolor=fill, edgecolor=border, linewidth=1.5)
        ax.add_patch(poly)
        ax.text(x + w/2, y + h/2, text, ha='center', va='center', fontsize=8, fontweight='bold', color=color)

    draw_step(30, 90, 40, 7, "Ingest Raw URL String U_raw", fill='#F1F5F9', border='#64748B')
    draw_step(25, 78, 50, 7, "URL Normalization (Form NFC + unquote + lowercase)", fill='#F1F5F9', border='#64748B')
    draw_step(25, 66, 50, 7, "Calculate Shannon Entropy H(U) = -SUM(p log2 p)", fill='#EFF6FF', border='#3B82F6')

    draw_diamond(30, 48, 40, 13, "H(U) > 4.50 ?\n(or Scope Threshold)", color='#991B1B', fill='#FEF2F2', border='#DC2626')

    # Left: Early Gated Exit
    draw_step(2, 32, 34, 11, "DECISION: PHISHING_DGA\nRisk = 0.99 (High)\nDirective: WITHHOLD_PARSER", color='#991B1B', fill='#FEE2E2', border='#DC2626')

    # Right: Downstream Structural AST
    draw_step(60, 49, 36, 11, "Allocate Parser Worker Threads\nExecute Deterministic HTML AST", color='#1E40AF', fill='#DBEAFE', border='#2563EB')
    draw_step(60, 32, 36, 11, "Calculate Structural Density\nSDR = N_total / D_max", color='#1E40AF', fill='#DBEAFE', border='#2563EB')

    draw_diamond(60, 15, 36, 12, "Delta SDR > 50% ?\n& TLS Invalid", color='#C2410C', fill='#FFF7ED', border='#EA580C')

    draw_step(15, 2, 32, 9, "DECISION: PHISHING_CLONE\nRisk = 0.95 | Directive: ISOLATE", color='#9A3412', fill='#FFEDD5', border='#EA580C')
    draw_step(60, 2, 36, 9, "DECISION: LEGITIMATE\nRisk = 0.05 | Directive: ALLOW_STREAM", color='#166534', fill='#DCFCE7', border='#16A34A')

    # Connectors
    ax.annotate('', xy=(50, 78), xytext=(50, 90), arrowprops=dict(arrowstyle="->", color='#334155', lw=1.5))
    ax.annotate('', xy=(50, 66), xytext=(50, 78), arrowprops=dict(arrowstyle="->", color='#334155', lw=1.5))
    ax.annotate('', xy=(50, 61), xytext=(50, 66), arrowprops=dict(arrowstyle="->", color='#334155', lw=1.5))

    # Diamond branches
    ax.annotate('', xy=(20, 43), xytext=(30, 54.5), arrowprops=dict(arrowstyle="->", color='#DC2626', lw=1.8))
    ax.text(22, 51, "YES (DGA)", fontsize=8, fontweight='bold', color='#B91C1C')

    ax.annotate('', xy=(60, 54.5), xytext=(70, 54.5), arrowprops=dict(arrowstyle="->", color='#2563EB', lw=1.8))
    ax.text(53, 56.5, "NO (Safe/Normal)", fontsize=7.5, fontweight='bold', color='#1D4ED8')

    ax.annotate('', xy=(78, 43), xytext=(78, 49), arrowprops=dict(arrowstyle="->", color='#2563EB', lw=1.5))
    ax.annotate('', xy=(78, 27), xytext=(78, 32), arrowprops=dict(arrowstyle="->", color='#2563EB', lw=1.5))

    ax.annotate('', xy=(31, 11), xytext=(60, 21), arrowprops=dict(arrowstyle="->", color='#EA580C', lw=1.8))
    ax.text(42, 18, "YES (Clone)", fontsize=7.5, fontweight='bold', color='#C2410C')

    ax.annotate('', xy=(78, 11), xytext=(78, 15), arrowprops=dict(arrowstyle="->", color='#16A34A', lw=1.8))
    ax.text(80, 13, "NO (Authentic)", fontsize=7.5, fontweight='bold', color='#15803D')

    plt.title("X-MPFD-E++ Conditional Hardware Gating & Execution Flowchart", fontsize=12, fontweight='bold', pad=15, color='#0F172A')
    plt.tight_layout()

    out_png = os.path.join(OUTPUT_DIR, "FIG_FLOW_hardware_gating_decision_flow.png")
    plt.savefig(out_png, dpi=300)
    plt.close()
    print(f"    [+] Saved {out_png}")

if __name__ == "__main__":
    generate_system_architecture_diagram()
    generate_decision_flowchart()
