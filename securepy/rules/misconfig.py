import ast
from securepy.rules.base import BaseRule

class SecurityMisconfigCheck(BaseRule, ast.NodeVisitor):
    id = "SEC-501"
    message = "Security Misconfiguration detected."
    severity = "LOW"
    remediation = "Ensure debug mode is disabled in production (debug=False)."

    def visit_Assign(self, node: ast.Assign):
        # Look for: app.debug = True or DEBUG = True
        for target in node.targets:
            # Check for "app.debug" (Attribute)
            if isinstance(target, ast.Attribute) and target.attr == 'debug':
                if isinstance(node.value, ast.Constant) and node.value.value is True:
                    self.add_issue(node, "Debug mode enabled (app.debug = True). Do not use in production.")
            
            # Check for global "DEBUG" variable (Name)
            elif isinstance(target, ast.Name) and target.id == 'DEBUG':
                if isinstance(node.value, ast.Constant) and node.value.value is True:
                    self.add_issue(node, "Global DEBUG flag set to True.")

        self.generic_visit(node)