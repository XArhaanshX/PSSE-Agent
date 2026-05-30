import os
import pytest
from pathlib import Path

from app.topology.planner import build_radial
from app.psse.executor import execute_in_psse
from app.layout.engine import LayoutConfig

# Require PSSE environment for these tests
pytestmark = pytest.mark.skipif(
    not os.path.exists(r"C:\Program Files\PTI\PSSE36\36.0\PSSBIN"),
    reason="PSSE36 installation not found."
)

@pytest.fixture
def executed_report(tmp_path):
    ir = build_radial(bus_count=5, voltage_kv=33.0)
    config = LayoutConfig(orientation="horizontal")
    
    # ensure DLLs can be loaded
    import sys
    sys.path.append(r"C:\Program Files\PTI\PSSE36\36.0\PSSPY311")
    sys.path.append(r"C:\Program Files\PTI\PSSE36\36.0\PSSBIN")
    os.environ["PATH"] = r"C:\Program Files\PTI\PSSE36\36.0\PSSBIN;" + os.environ.get("PATH", "")
    try:
        os.add_dll_directory(r"C:\Program Files\PTI\PSSE36\36.0\PSSBIN")
    except AttributeError:
        pass
        
    report = execute_in_psse(ir, output_dir=str(tmp_path), layout_config=config)
    return report

def test_sld_artifact_exists(executed_report):
    """TEST 4 - SLD Artifact Exists: After execution, .sld exists."""
    assert executed_report.success, "Execution should be successful"
    
    sld_artifacts = [a for a in executed_report.artifacts if a.artifact_type == "sld"]
    assert len(sld_artifacts) == 1, "There should be exactly one SLD artifact"
    
    sld_path = Path(sld_artifacts[0].path)
    assert sld_path.exists(), f"SLD file should exist at {sld_path}"

def test_non_blank_sld(executed_report):
    """TEST 5 - Non-Blank SLD: Validate generated .sld size > blank-shell threshold."""
    sld_artifacts = [a for a in executed_report.artifacts if a.artifact_type == "sld"]
    sld_path = Path(sld_artifacts[0].path)
    
    # Empirically determined threshold for blank shell is ~2539 bytes.
    # We assert > 3000 bytes to be safe that real geometry was added.
    size = sld_path.stat().st_size
    assert size > 3000, f"SLD file size ({size} bytes) is too small, indicates a blank shell."

def test_execution_report_integrity(executed_report):
    """TEST 6 - ExecutionReport Integrity: Ensure ExecutionArtifact(type='sld') is properly tracked."""
    artifact_types = [a.artifact_type for a in executed_report.artifacts]
    assert "sld" in artifact_types, "SLD artifact should be tracked in the execution report."
    assert "sav" in artifact_types, "SAV artifact should be tracked."
    assert "raw" in artifact_types, "RAW artifact should be tracked."
