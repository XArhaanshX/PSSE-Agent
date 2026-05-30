from typing import List, Dict, Any
from app.ir.component_models import Bus, Branch, Transformer, Load, Generator
from app.ir.topology_ir import TopologyIR

def normalize_status(val: Any) -> bool:
    """Deterministically normalize status to boolean."""
    if val is None:
        return True # Default to in-service
    val_str = str(val).strip().lower()
    if val_str in ['1', '1.0', 'true']:
        return True
    if val_str in ['0', '0.0', 'false']:
        return False
    return True

def normalize_bus_type(val: Any) -> str:
    """Deterministically normalize bus type mapping without implicit inference."""
    if val is None:
        return "load" # Safe deterministic default
        
    val_str = str(val).strip().lower()
    if val_str in ["swing", "generator", "load"]:
        return val_str
        
    return "load"

def generate_topology_ir(rows: List[Dict[str, Any]]) -> TopologyIR:
    """Map deterministic, validated dictionaries into the TopologyIR Pydantic models."""
    ir = TopologyIR()
    
    for row in rows:
        c_type = str(row.get("component_type", "")).lower()
        c_id = str(row.get("component_id", ""))
        status = normalize_status(row.get("status"))
        
        if c_type == "bus":
            ir.add_bus(Bus(
                id=c_id,
                from_bus=int(row["from_bus"]),
                name=row.get("notes", ""),
                base_kv=float(row["base_kv"]),
                bus_type=normalize_bus_type(row.get("bus_type")),
                status=status
            ))
            
        elif c_type == "branch":
            ir.add_branch(Branch(
                id=c_id,
                from_bus=int(row["from_bus"]),
                to_bus=int(row["to_bus"]),
                r_pu=float(row["r_pu"]),
                x_pu=float(row["x_pu"]),
                status=status
            ))
            
        elif c_type == "transformer":
            ir.add_transformer(Transformer(
                id=c_id,
                from_bus=int(row["from_bus"]),
                to_bus=int(row["to_bus"]),
                mva=float(row["mva"]),
                r_pu=float(row["r_pu"]) if row.get("r_pu") is not None else None,
                x_pu=float(row["x_pu"]) if row.get("x_pu") is not None else None,
                vector_group=row.get("vector_group"),
                status=status
            ))
            
        elif c_type == "load":
            ir.add_load(Load(
                id=c_id if c_id else None,
                from_bus=int(row["from_bus"]),
                p_mw=float(row["p_mw"]),
                q_mvar=float(row["q_mvar"]) if row.get("q_mvar") is not None else 0.0,
                status=status
            ))
            
        elif c_type == "generator":
            ir.add_generator(Generator(
                id=c_id if c_id else None,
                from_bus=int(row["from_bus"]),
                mva=float(row["mva"]),
                p_mw=float(row["p_mw"]) if row.get("p_mw") is not None else 0.0,
                status=status
            ))
            
    # Add metadata
    ir.metadata.topology_type = "radial"  # Default type for now, as it's order-independent graph
    ir.metadata.description = "Ingested via deterministic Excel adapter"
    
    return ir
