import json
from pathlib import Path
from app.ir.topology_ir import TopologyIR

def save_ir(ir: TopologyIR, filepath: str | Path) -> None:
    """Save a TopologyIR instance to a JSON file with full fidelity."""
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        f.write(ir.model_dump_json(indent=2))

def load_ir(filepath: str | Path) -> TopologyIR:
    """Load a TopologyIR instance from a JSON file."""
    path = Path(filepath)
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return TopologyIR.model_validate(data)
