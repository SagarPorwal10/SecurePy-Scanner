import ast
import os

class ScannerEngine:
    def __init__(self, rules):
        """
        Initialize the engine with a list of rule instances.
        """
        self.rules = rules

    def scan_file(self, filepath):
        """
        Reads a file, parses it, and runs all rules against it.
        Returns a list of issues found in that file.
        """
        results = []
        
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            
            # 1. Parse the code into an AST
            tree = ast.parse(content)
            
            # 2. Run every rule against the tree
            for rule in self.rules:
                rule.reset() # Clear previous results
                rule.visit(tree) # This triggers the visit_* methods in the rule
                
                # Collect findings
                results.extend(rule.issues)
                
        except SyntaxError:
            print(f"[ERROR] Could not parse {filepath}. Invalid Python syntax.")
        except Exception as e:
            print(f"[ERROR] Failed to scan {filepath}: {str(e)}")

        return results