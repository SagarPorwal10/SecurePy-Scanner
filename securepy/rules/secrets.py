import ast
from securepy.rules.base import BaseRule

class HardcodedSecretCheck(BaseRule, ast.NodeVisitor):
    id = "SEC-201"
    message = "Hardcoded secret detected in source code."
    severity = "HIGH"
    
    # --- NEW LINE ADDED HERE ---
    remediation = "Do not hardcode secrets. Use environment variables (os.getenv) or a secret manager (e.g., AWS Secrets Manager, HashiCorp Vault)."

    SUSPICIOUS_NAMES = {"api_key", "secret", "password", "token", "auth"}

    def visit_Assign(self, node: ast.Assign):
        for target in node.targets:
            if isinstance(target, ast.Name):
                var_name = target.id.lower()
                
                if any(s in var_name for s in self.SUSPICIOUS_NAMES):
                    if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                        secret_value = node.value.value
                        if len(secret_value) > 8 and "example" not in secret_value:
                             self.add_issue(
                                 node, 
                                 f"Possible hardcoded secret in variable '{target.id}'."
                             )

        self.generic_visit(node)