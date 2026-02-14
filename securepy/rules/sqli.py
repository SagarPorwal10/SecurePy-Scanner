import ast
from securepy.rules.base import BaseRule

class SQLInjectionCheck(BaseRule, ast.NodeVisitor):
    id = "SEC-301"
    # CHANGED: 'name' -> 'message'
    message = "Potential SQL Injection detected." 
    severity = "CRITICAL"
    # In SQLInjectionCheck class:
    remediation = "Use parameterized queries (e.g., 'SELECT * FROM users WHERE id = %s', (user_id,)). Do NOT use string concatenation or f-strings for SQL queries."

    def visit_Call(self, node: ast.Call):
        is_execute = False
        # Check if it's a method call like cursor.execute()
        if isinstance(node.func, ast.Attribute) and node.func.attr == 'execute':
            is_execute = True
        
        if is_execute and node.args:
            first_arg = node.args[0]
            
            if isinstance(first_arg, ast.BinOp):
                self.add_issue(
                    node,
                    "SQL query construction using binary operation (+) detected. Use parameterized queries."
                )
            
            elif isinstance(first_arg, ast.JoinedStr):
                self.add_issue(
                    node,
                    "SQL query construction using f-string detected. Use parameterized queries."
                )

        self.generic_visit(node)