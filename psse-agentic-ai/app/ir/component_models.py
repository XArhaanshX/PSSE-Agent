from pydantic import BaseModel, Field
from typing import Literal, Optional, Dict, Any

class Bus(BaseModel):
    """Semantic representation of a bus in the power system."""
    component_id: str = Field(alias="id")
    bus_number: int = Field(alias="from_bus")
    name: Optional[str] = ""
    base_kv: float
    bus_type: Literal["load", "generator", "swing"] = "load"
    status: bool = True
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)

class Branch(BaseModel):
    """Semantic representation of an AC branch."""
    component_id: str = Field(alias="id")
    from_bus: int
    to_bus: int
    resistance_pu: float = Field(alias="r_pu")
    reactance_pu: float = Field(alias="x_pu")
    circuit_id: str = "1"
    status: bool = True
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)

class Transformer(BaseModel):
    """Semantic representation of a 2-winding transformer."""
    component_id: str = Field(alias="id")
    from_bus: int
    to_bus: int
    resistance_pu: Optional[float] = Field(default=None, alias="r_pu")
    reactance_pu: Optional[float] = Field(default=None, alias="x_pu")
    base_mva: float = Field(alias="mva")
    name: Optional[str] = ""
    circuit_id: str = "1"
    vector_group: Optional[str] = None
    status: bool = True
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)

class Load(BaseModel):
    """Semantic representation of a load."""
    component_id: Optional[str] = Field(default=None, alias="id")
    bus_number: int = Field(alias="from_bus")
    p_mw: float
    q_mvar: Optional[float] = 0.0
    status: bool = True
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)

class Generator(BaseModel):
    """Semantic representation of a generator."""
    component_id: Optional[str] = Field(default=None, alias="id")
    bus_number: int = Field(alias="from_bus")
    p_mw: float = Field(default=0.0)
    base_mva: Optional[float] = Field(default=None, alias="mva")
    name: Optional[str] = ""
    status: bool = True
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)

class TopologyMetadata(BaseModel):
    """Metadata for the entire topology."""
    name: str = "Topology"
    description: str = ""
    version: str = "1.0"
    topology_type: Literal["radial", "single_bus", "double_bus", "substation_feeder", "transformer_substation"] = "radial"
