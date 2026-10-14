"""
Architecture & Decision Flow Diagram Generator
Script: generate_architecture_diagrams.py
Project: X-MPFD-E++

Generates publication-quality 300 DPI system architecture and hardware control flow diagrams:
- figures/FIG_ARCH_system_architecture.png (Without hardcoded 2.65 ms label)
- figures/FIG_FLOW_hardware_gating_decision_flow.png (Includes SUSPICIOUS branch for Delta SDR > 50% with valid TLS)
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

    # Layer 3: Branches (y = 18 to 38)
    # Notice: 2.65 ms label removed to avoid conflict with microsecond profiler file
    draw_box(4, 18, 34, 20, "Hardware Directive:\nWITHHOLD_PARSER_AND_RENDERER", "O(L) early exit | Drop packet\nSuppresses downstream AST parse", color='#991B1B', fill='#FEE2E2', edgecolor='#DC2626')
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
    print("[*] Generating Decision Flowchart (FIG_FLOW) with SUSPICIOUS branch...")
    fig, ax = plt.subplots(figsize=(12.5, 11), dpi=300)
    ax.set_xlim(0, 125)
    ax.set_ylim(0, 120)
    ax.axis('off')

    ax.add_patch(patches.Rectangle((0, 0), 125, 120, facecolor='#FFFFFF', edgecolor='none'))

    def draw_step(x, y, w, h, text, color='#0F172A', fill='#F8FAFC', border='#94A3B8'):
        box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.6,rounding_size=1.2",
                             facecolor=fill, edgecolor=border, linewidth=1.5)
        ax.add_patch(box)
        ax.text(x + w/2, y + h/2, text, ha='center', va='center', fontsize=8.2, fontweight='bold', color=color)

    def draw_diamond(cx, cy, w, h, text, color='#991B1B', fill='#FEF2F2', border='#DC2626'):
        poly = patches.Polygon([
            (cx, cy + h/2),
            (cx + w/2, cy),
            (cx, cy - h/2),
            (cx - w/2, cy)
        ], closed=True, facecolor=fill, edgecolor=border, linewidth=1.5)
        ax.add_patch(poly)
        ax.text(cx, cy, text, ha='center', va='center', fontsize=7.8, fontweight='bold', color=color)

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
    ax.plot([42, 19, 19], [62, 62, 44], color='#DC2626', lw=1.8)
    ax.annotate('', xy=(19, 44), xytext=(19, 46), arrowprops=dict(arrowstyle="->", color='#DC2626', lw=1.8))
    ax.text(30.5, 64.5, "YES: H(U) > tau\n(Zero-Day DGA)", ha='center', va='bottom', fontsize=8, fontweight='bold', color='#B91C1C',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#FFF5F5', edgecolor='#FEB2B2', alpha=0.9))

    # Left Result Box: centered at x=19, y=34, w=34, h=16
    draw_step(2, 26, 34, 16, "DECISION: PHISHING_DGA\nRisk = 0.99 (High Confidence)\nDirective: WITHHOLD_PARSER\n(Bypasses HTML AST Parsing)",
              color='#991B1B', fill='#FEE2E2', border='#DC2626')

    # -------------------------------------------------------------
    # Right Branch: Normal Downstream Pipeline (NO: H(U) <= tau)
    # Right diamond vertex is at (78, 62)
    # -------------------------------------------------------------
    ax.plot([78, 100, 100], [62, 62, 54], color='#2563EB', lw=1.8)
    ax.annotate('', xy=(100, 54), xytext=(100, 56), arrowprops=dict(arrowstyle="->", color='#2563EB', lw=1.8))
    ax.text(89, 64.5, "NO: H(U) <= tau\n(Allocate Threads)", ha='center', va='bottom', fontsize=8, fontweight='bold', color='#1D4ED8',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#EFF6FF', edgecolor='#BFDBFE', alpha=0.9))

    # Right Step 1: Allocate Worker Threads (center=(100, 49), w=40, h=8)
    draw_step(80, 45, 40, 8, "Allocate Parser Worker Threads\nExecute HTML AST State Machine", color='#1E40AF', fill='#DBEAFE', border='#2563EB')

    # Arrow down to Step 2
    ax.annotate('', xy=(100, 38), xytext=(100, 45), arrowprops=dict(arrowstyle="->", color='#2563EB', lw=1.6))

    # Right Step 2: Compute SDR (center=(100, 34), w=40, h=8)
    draw_step(80, 30, 40, 8, "Calculate Structural Density\nSDR = N_total / D_max", color='#1E40AF', fill='#DBEAFE', border='#2563EB')

    # Arrow down to Diamond 2
    ax.annotate('', xy=(100, 24), xytext=(100, 30), arrowprops=dict(arrowstyle="->", color='#2563EB', lw=1.6))

    # -------------------------------------------------------------
    # Diamond 2: Structural Density Anomaly Check (center at x=100, y=19, w=30, h=10)
    # -------------------------------------------------------------
    draw_diamond(100, 19, 30, 10, "Delta SDR > 50% ?\n(Anomalous DOM)", color='#C2410C', fill='#FFF7ED', border='#EA580C')

    # Diamond 2 Branch NO: Legitimate (Delta SDR <= 50%) -> straight down
    ax.annotate('', xy=(100, 8), xytext=(100, 14), arrowprops=dict(arrowstyle="->", color='#16A34A', lw=1.8))
    ax.text(108, 12, "NO (Safe)", ha='left', va='center', fontsize=7.5, fontweight='bold', color='#15803D')
    draw_step(84, 1, 32, 7, "DECISION: LEGITIMATE\nRisk = 0.05 | Directive: ALLOW_STREAM", color='#166534', fill='#DCFCE7', border='#16A34A')

    # Diamond 2 Branch YES: Elevated Delta SDR -> route left to Diamond 3 (TLS Check)
    ax.plot([85, 68], [19, 19], color='#EA580C', lw=1.8)
    ax.annotate('', xy=(68, 19), xytext=(70, 19), arrowprops=dict(arrowstyle="->", color='#EA580C', lw=1.8))
    ax.text(76.5, 21, "YES (Delta SDR > 50%)", ha='center', va='bottom', fontsize=7.2, fontweight='bold', color='#C2410C',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='#FFF7ED', edgecolor='#FDBA74'))

    # -------------------------------------------------------------
    # Diamond 3: Transport Layer Security Check (center at x=56, y=19, w=24, h=10)
    # -------------------------------------------------------------
    draw_diamond(56, 19, 24, 10, "TLS Valid ?\n(Certificate)", color='#1E40AF', fill='#EFF6FF', border='#3B82F6')

    # Diamond 3 Branch YES: Valid TLS with Delta SDR > 50% -> SUSPICIOUS (Risk = 0.70)
    ax.annotate('', xy=(56, 8), xytext=(56, 14), arrowprops=dict(arrowstyle="->", color='#CA8A04', lw=1.8))
    ax.text(64, 12, "YES: Valid TLS", ha='left', va='center', fontsize=7.2, fontweight='bold', color='#854D0E')
    draw_step(44, 1, 35, 7, "DECISION: SUSPICIOUS\nRisk = 0.70 | Directive: ALLOCATE_PARSER\n(Elevated SDR Anomaly with Valid TLS)",
              color='#854D0E', fill='#FEF9C3', border='#CA8A04')

    # Diamond 3 Branch NO: Invalid TLS with Delta SDR > 50% -> PHISHING_CLONE (Risk = 0.95)
    ax.plot([44, 20, 20], [19, 19, 8], color='#EA580C', lw=1.8)
    ax.annotate('', xy=(20, 8), xytext=(20, 10), arrowprops=dict(arrowstyle="->", color='#EA580C', lw=1.8))
    ax.text(32, 21, "NO: Invalid TLS", ha='center', va='bottom', fontsize=7.2, fontweight='bold', color='#C2410C',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='#FFF7ED', edgecolor='#FDBA74'))
    draw_step(4, 1, 35, 7, "DECISION: PHISHING_CLONE\nRisk = 0.95 | Directive: ISOLATE\n(Harvester: Shallow DOM + Invalid TLS)",
              color='#9A3412', fill='#FFEDD5', border='#EA580C')

    plt.title("X-MPFD-E++ Conditional Hardware Gating & Multi-Outcome Decision Flowchart", fontsize=12, fontweight='bold', pad=14, color='#0F172A')
    plt.tight_layout()

    out_png = os.path.join(OUTPUT_DIR, "FIG_FLOW_hardware_gating_decision_flow.png")
    plt.savefig(out_png, dpi=300)
    plt.close()
    print(f"    [+] Saved {out_png}")

if __name__ == "__main__":
    generate_system_architecture_diagram()
    generate_decision_flowchart()
