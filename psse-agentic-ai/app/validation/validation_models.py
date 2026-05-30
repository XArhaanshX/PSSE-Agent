from pydantic import BaseModel, Field
from typing import Literal, List, Dict, Any

class ValidationIssue(BaseModel):
    severity: Literal["error", "warning"]
    code: str
    message: str
    context: Dict[str, Any] = Field(default_factory=dict)

class ValidationReport(BaseModel):
    is_valid: bool = True
    issues: List[ValidationIssue] = Field(default_factory=list)

    def add_error(self, code: str, message: str, context: Dict[str, Any] = None) -> None:
        self.issues.append(
            ValidationIssue(
                severity="error",
                code=code,
                message=message,
                context=context or {}
            )
        )
        self.is_valid = False

    def add_warning(self, code: str, message: str, context: Dict[str, Any] = None) -> None:
        self.issues.append(
            ValidationIssue(
                severity="warning",
                code=code,
                message=message,
                context=context or {}
            )
        )
