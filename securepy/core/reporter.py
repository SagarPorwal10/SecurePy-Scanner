import json
import sys
from datetime import datetime

class Reporter:
    @staticmethod
    def print_console(issues):
        """
        Prints a colorful, human-readable report to the terminal.
        """
        if not issues:
            print("\n[+] Audit Passed: No obvious vulnerabilities found.")
            return

        print(f"\n[!] Audit Failed: {len(issues)} vulnerabilities found.")
        print("=" * 60)
        
        for issue in issues:
            # Color coding: Red for High/Critical, Yellow for Medium
            color = "\033[91m" if issue['severity'] in ['HIGH', 'CRITICAL'] else "\033[93m"
            reset = "\033[0m"
            
            print(f"{color}[{issue['severity']}] {issue['id']}: {issue['message']}{reset}")
            print(f"    Line: {issue['line']}")
            print("-" * 60)

    @staticmethod
    def save_json(issues, filename="report.json"):
        """
        Saves the scan results as a structured JSON file for CI/CD tools.
        """
        report = {
            "timestamp": datetime.now().isoformat(),
            "scan_summary": {
                "total_issues": len(issues),
                "high_severity": sum(1 for i in issues if i['severity'] == 'HIGH'),
                "medium_severity": sum(1 for i in issues if i['severity'] == 'MEDIUM')
            },
            "issues": issues
        }
        
        try:
            with open(filename, "w") as f:
                json.dump(report, f, indent=4)
            print(f"\n[+] JSON report successfully saved to: {filename}")
        except Exception as e:
            print(f"\n[ERROR] Failed to save JSON report: {e}")