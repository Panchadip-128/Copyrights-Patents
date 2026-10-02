
class ReportGenerator:
    def generate_text_report(self, result):
        report = []
        report.append("==================================================")
        report.append(f"DECISION: {result.decision}")
        report.append(f"RISK SCORE: {result.risk_score:.2%}")
        report.append(f"CONFIDENCE: {result.confidence}")
        report.append("==================================================")
        report.append("MATHEMATICAL EXPLANATION:")
        report.append(result.explanation)
        report.append("--------------------------------------------------")
        report.append("FEATURE PROVENANCE:")
        for f in result.features:
            report.append(f"- {f.name}: {f.value:.2f} [Source: {f.provenance.source_modality}]")
        return chr(10).join(report)
        
    def generate_json_report(self, result):
        return "{}"
        
    def generate_html_report(self, result):
        return "<html></html>"
