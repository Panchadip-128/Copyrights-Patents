#!/usr/bin/env python3
"""
X-MPFD-E++ Command-Line Interface

Explainable Multimodal Phishing & Fraud Detection and Reasoning Engine
Copyright © 2026. All Rights Reserved.
"""

import argparse
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from x_mpfd_e_plus import PhishingDetector, FusionPolicy, FusionStrategy
from x_mpfd_e_plus.report_generator import ReportGenerator


def main():
    parser = argparse.ArgumentParser(
        description='X-MPFD-E++: Explainable Multimodal Phishing & Fraud Detection',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Analyze URL command
    analyze_parser = subparsers.add_parser('analyze-url', help='Analyze URL for phishing')
    analyze_parser.add_argument('url', help='URL to analyze')
    analyze_parser.add_argument('--html', help='Path to HTML file')
    analyze_parser.add_argument('--screenshot', help='Path to screenshot image')
    analyze_parser.add_argument('--output', '-o', help='Output report file')
    analyze_parser.add_argument('--format', '-f', choices=['text', 'json', 'html'], 
                               default='text', help='Output format')
    analyze_parser.add_argument('--fusion-policy', choices=['early', 'late', 'weighted', 'gated', 'consensus'],
                               default='weighted', help='Fusion policy to use')
    
    # Batch analyze command
    batch_parser = subparsers.add_parser('batch-analyze', help='Analyze multiple URLs')
    batch_parser.add_argument('input_file', help='File containing URLs (one per line)')
    batch_parser.add_argument('--output', '-o', help='Output file', default='batch_results.json')
    
    # Demo command
    demo_parser = subparsers.add_parser('demo', help='Run demonstration')
    
    # Version command
    parser.add_argument('--version', action='version', version='X-MPFD-E++ v1.0.0')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 0
    
    if args.command == 'analyze-url':
        return analyze_url_command(args)
    elif args.command == 'batch-analyze':
        return batch_analyze_command(args)
    elif args.command == 'demo':
        return demo_command()
    
    return 0


def analyze_url_command(args):
    """Analyze single URL"""
    print(f"Analyzing: {args.url}")
    print()
    
    # Load optional inputs
    html = None
    screenshot = None
    
    if args.html:
        with open(args.html, 'r', encoding='utf-8') as f:
            html = f.read()
        print(f"✓ Loaded HTML from {args.html}")
    
    if args.screenshot:
        with open(args.screenshot, 'rb') as f:
            screenshot = f.read()
        print(f"✓ Loaded screenshot from {args.screenshot}")
    
    # Get fusion policy
    policy_map = {
        'early': 'early_fusion',
        'late': 'late_fusion',
        'weighted': 'confidence_weighted',
        'gated': 'gated_fusion',
        'consensus': 'consensus_fusion'
    }
    
    # Initialize detector
    detector = PhishingDetector()
    policy = detector.fusion_engine.get_policy(policy_map[args.fusion_policy])
    detector.fusion_engine.set_policy(policy)
    
    print(f"✓ Using fusion policy: {args.fusion_policy}")
    print()
    
    # Perform detection
    result = detector.analyze_url(args.url, html, screenshot)
    
    # Generate report
    generator = ReportGenerator()
    
    if args.format == 'text':
        report = generator.generate_text_report(result)
        print(report)
    elif args.format == 'json':
        report = generator.generate_json_report(result)
        print(report)
    elif args.format == 'html':
        report = generator.generate_html_report(result)
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"✓ HTML report saved to {args.output}")
        else:
            print(report)
    
    # Save report if output specified
    if args.output and args.format != 'html':
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"\n✓ Report saved to {args.output}")
    
    return 0


def batch_analyze_command(args):
    """Batch analyze URLs"""
    import json
    
    print(f"Loading URLs from {args.input_file}...")
    
    with open(args.input_file, 'r') as f:
        urls = [line.strip() for line in f if line.strip()]
    
    print(f"✓ Loaded {len(urls)} URLs")
    print()
    
    # Initialize detector
    detector = PhishingDetector()
    
    results = []
    for i, url in enumerate(urls, 1):
        print(f"[{i}/{len(urls)}] Analyzing {url}...")
        try:
            result = detector.analyze_url(url)
            results.append({
                'url': url,
                'decision': result.decision,
                'risk_score': result.risk_score,
                'confidence': result.confidence
            })
            print(f"  → {result.decision} ({result.risk_score:.0%})")
        except Exception as e:
            results.append({'url': url, 'error': str(e)})
            print(f"  → ERROR: {e}")
    
    # Save results
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    
    print()
    print(f"✓ Results saved to {args.output}")
    
    return 0


def demo_command():
    """Run demonstration"""
    print("="*80)
    print("X-MPFD-E++ DEMONSTRATION")
    print("Explainable Multimodal Phishing & Fraud Detection and Reasoning Engine")
    print("="*80)
    print()
    
    # Demo URLs
    demo_urls = [
        ("https://paypal.com", "Legitimate financial service"),
        ("https://paypa1-secure-login.tk", "Suspicious phishing attempt"),
        ("https://192.168.1.1/login", "IP-based URL (suspicious)"),
    ]
    
    detector = PhishingDetector()
    generator = ReportGenerator()
    
    for url, description in demo_urls:
        print(f"\nAnalyzing: {url}")
        print(f"Description: {description}")
        print("-" * 80)
        
        result = detector.analyze_url(url)
        report = generator.generate_text_report(result)
        print(report)
        print()
    
    print("="*80)
    print("Demo completed successfully!")
    print("="*80)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
