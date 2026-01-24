"""
Export Handler - Handles export to various file formats

Implements proprietary export algorithms.
Copyright (c) 2026. All rights reserved.
"""

import json
from enum import Enum
from typing import Dict, Any
from pathlib import Path


class ExportFormat(Enum):
    """Supported export formats"""
    TEXT = "txt"
    HTML = "html"
    JSON = "json"
    MARKDOWN = "md"
    PDF = "pdf"


class ExportHandler:
    """
    Handles exporting reports to various file formats.
    
    Implements proprietary export algorithms.
    """
    
    def __init__(self):
        """Initialize the export handler"""
        pass
    
    def export_json(self, report: Any) -> str:
        """
        Export report as JSON.
        
        Proprietary JSON serialization.
        """
        report_dict = self._report_to_dict(report)
        return json.dumps(report_dict, indent=2, default=str)
    
    def save_to_file(
        self,
        content: str,
        output_path: str,
        format: ExportFormat = ExportFormat.TEXT
    ) -> bool:
        """
        Save content to file.
        
        Args:
            content: Report content
            output_path: Output file path
            format: Export format
            
        Returns:
            Success boolean
        """
        try:
            # Ensure directory exists
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            
            # Write content
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return True
        except Exception as e:
            print(f"Error saving report: {e}")
            return False
    
    def _report_to_dict(self, report: Any) -> Dict:
        """Convert report object to dictionary"""
        if hasattr(report, '__dict__'):
            result = {}
            for key, value in report.__dict__.items():
                if hasattr(value, '__dict__'):
                    result[key] = self._report_to_dict(value)
                elif isinstance(value, list):
                    result[key] = [
                        self._report_to_dict(item) if hasattr(item, '__dict__') else item
                        for item in value
                    ]
                elif isinstance(value, dict):
                    result[key] = {
                        k: self._report_to_dict(v) if hasattr(v, '__dict__') else v
                        for k, v in value.items()
                    }
                else:
                    result[key] = value
            return result
        else:
            return report
