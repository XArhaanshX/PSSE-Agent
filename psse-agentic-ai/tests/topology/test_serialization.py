import tempfile
from pathlib import Path
from app.topology.planner import build_radial
from app.ir.serializers import save_ir, load_ir

def test_serialization_roundtrip():
    ir = build_radial(bus_count=5, voltage_kv=33.0)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = Path(tmpdir) / "example_ir.json"
        
        # Save
        save_ir(ir, filepath)
        assert filepath.exists()
        
        # Load
        loaded_ir = load_ir(filepath)
        
        # Mandatory roundtrip equality verification
        assert ir.model_dump() == loaded_ir.model_dump()
