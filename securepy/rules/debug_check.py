import ast
from securepy.rules.base import BaseRule

class DebugModeCheck(BaseRule, ast.NodeVisitor):
    id = "SEC-101"
    message = "Debug mode enabled in production code."
    severity = "MEDIUM"

    def visit_Assign(self, node: ast.Assign):
        """
        This function runs automatically whenever the scanner finds an assignment 
        (e.g., x = 1, DEBUG = True).
        """
        # We are looking for assignments to a variable named 'DEBUG'
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == "DEBUG":
                # Now check if the value being assigned is 'True'
                if isinstance(node.value, ast.Constant) and node.value.value is True:
                    self.add_issue(node, "Global variable 'DEBUG' is set to True.")
        
        # Continue generic traversal
        self.generic_visit(node)