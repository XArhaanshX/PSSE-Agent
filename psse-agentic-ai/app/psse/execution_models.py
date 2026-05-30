from pydantic import BaseModel, Field
from typing import Literal, List

class ExecutionArtifact(BaseModel):
    artifact_type: Literal["sav", "raw", "log", "sld"]
    path: str

class ExecutionReport(BaseModel):
    success: bool = False
    execution_status: Literal["success", "validation_failed", "execution_failed"] = "execution_failed"
    load_flow_converged: bool = False
    
    created_bus_count: int = 0
    created_branch_count: int = 0
    created_transformer_count: int = 0
    created_generator_count: int = 0
    created_load_count: int = 0
    
    artifacts: List[ExecutionArtifact] = Field(default_factory=list)
    errors: List[str] = Field(default_factory=list)
    execution_steps: List[str] = Field(default_factory=list)
