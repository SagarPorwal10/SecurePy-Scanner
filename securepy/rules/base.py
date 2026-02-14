import ast
from abc import ABC, abstractmethod

class BaseRule(ABC):
    def __init__(self):
        self.issues = []

    @property
    @abstractmethod
    def id(self) -> str: pass

    @property
    @abstractmethod
    def message(self) -> str: pass

    @property
    @abstractmethod
    def severity(self) -> str: pass
    
    # NEW: Add this field for the "Fix" advice
    @property
    @abstractmethod
    def remediation(self) -> str: pass

    def add_issue(self, node: ast.AST, custom_msg: str = None):
        self.issues.append({
            "id": self.id,
            "line": getattr(node, 'lineno', 0),
            "message": custom_msg or self.message,
            "severity": self.severity,
            "remediation": self.remediation  # Pass the fix advice to the report
        })

    def reset(self):
        self.issues = []