import ast
from securepy.rules.base import BaseRule

class DangerousFunctionCheck(BaseRule, ast.NodeVisitor):
    id = "SEC-401"
    message = "Dangerous function usage detected."
    severity = "HIGH"
    # We remove the static remediation string from here
    remediation = "" 

    # MAP: Func Name -> (Severity, Warning Message, Specific Remediation)
    DANGEROUS_FUNCTIONS = {
        "eval": (
            "HIGH", 
            "Use of eval() allows arbitrary code execution.", 
            "Use `ast.literal_eval()` for safe evaluation of strings."
        ),
        "exec": (
            "HIGH", 
            "Use of exec() allows arbitrary code execution.", 
            "Refactor code to avoid dynamic execution."
        ),
        "pickle.loads": (
            "HIGH", 
            "Deserialization of untrusted data via pickle is insecure.", 
            "Use `json.loads()` or sign your data with HMAC."
        ),
        "yaml.load": (
            "HIGH", 
            "Unsafe YAML deserialization.", 
            "Use `yaml.safe_load()` instead."
        ),
        "hashlib.md5": (
            "MEDIUM", 
            "MD5 is a broken hash function.", 
            "Use `hashlib.sha256()` or `bcrypt` for passwords."
        ),
        "hashlib.sha1": (
            "MEDIUM", 
            "SHA1 is a broken hash function.", 
            "Use `hashlib.sha256()`."
        ),
        "subprocess.call": (
            "HIGH", 
            "subprocess.call is dangerous if shell=True.", 
            "Use `subprocess.run(..., shell=False)`."
        ),
        "base64.b64encode": (
            "LOW", 
            "Base64 is not encryption.", 
            "Do not use this to hide secrets. Use AES (cryptography lib)."
        ),
        "requests.get": (
            "MEDIUM", 
            "Potential SSRF risk.", 
            "Validate the 'url' parameter against an allowlist."
        )
    }

    def visit_Call(self, node: ast.Call):
        func_name = None

        if isinstance(node.func, ast.Name):
            func_name = node.func.id
        elif isinstance(node.func, ast.Attribute):
            if isinstance(node.func.value, ast.Name):
                 func_name = f"{node.func.value.id}.{node.func.attr}"

        if func_name and func_name in self.DANGEROUS_FUNCTIONS:
            # UNPACK TUPLE: Now we get severity, msg, AND remediation
            severity, msg, fix = self.DANGEROUS_FUNCTIONS[func_name]
            
            self.issues.append({
                "id": self.id,
                "line": node.lineno,
                "message": msg,
                "severity": severity,
                "remediation": fix  # <-- Pass the specific fix!
            })

        # Special Check for subprocess shell=True
        if func_name and "subprocess" in func_name:
            for keyword in node.keywords:
                if keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True:
                     self.add_issue(
                         node, 
                         "Shell injection risk detected.", 
                         "Set shell=False or use shlex.quote() on inputs."
                     )

        self.generic_visit(node)
    
    # Update helper to accept custom remediation
    def add_issue(self, node, msg, fix=None):
        self.issues.append({
            "id": self.id,
            "line": node.lineno,
            "message": msg,
            "severity": self.severity,
            "remediation": fix or "Check security documentation."
        })