import tempfile
import pytest
from pathlib import Path
import sys
from unittest.mock import MagicMock, patch

# Mock psspy safely
class PsspyMock(MagicMock):
    def __call__(self, *args, **kwargs):
        return 0
    def two_winding_data_6(self, *args, **kwargs):
        return (0, [])

@pytest.fixture(autouse=True)
def mock_psspy_env():
    mock_psspy = PsspyMock()
    for attr in ['bus_data_4', 'branch_data_3', 'load_data_6', 'plant_data_4', 'machine_data_4', 'fnsl', 'newcase_2', 'save', 'rawd_2', 'newdiagfile', 'bsys', 'growbus', 'savediagfile']:
        setattr(mock_psspy, attr, MagicMock(return_value=0))
    
    with patch.dict('sys.modules', {'psspy': mock_psspy}):
        yield mock_psspy

from app.psse.executor import execute_in_psse
from app.topology.planner import build_radial
from app.ir.component_models import Generator

@pytest.fixture
def mock_output_dir():
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir

def test_valid_radial_execution(mock_output_dir):
    ir = build_radial(bus_count=5, voltage_kv=33.0)
    report = execute_in_psse(ir, output_dir=mock_output_dir)
    
    assert report.success
    assert report.execution_status == "success"
    
    assert report.created_bus_count == 5
    assert report.created_branch_count == 4
    
    # We expect a .sav, .raw, and .sld
    assert len(report.artifacts) == 3
    artifact_types = [a.artifact_type for a in report.artifacts]
    assert "sav" in artifact_types
    assert "raw" in artifact_types
    assert "sld" in artifact_types
    
    # Load flow converges in this simple mock case because PSSE runs it
    # We just assert it ran and boolean exists
    assert isinstance(report.load_flow_converged, bool)

def test_invalid_topology_blocking(mock_output_dir):
    ir = build_radial(bus_count=5, voltage_kv=33.0)
    # Add a duplicate branch to make it invalid
    from app.ir.component_models import Branch
    ir.add_branch(Branch(from_bus=33001, to_bus=33002, resistance_pu=0.01, reactance_pu=0.1))
    
    report = execute_in_psse(ir, output_dir=mock_output_dir)
    
    assert not report.success
    assert report.execution_status == "validation_failed"
    assert report.created_bus_count == 0  # Execution stopped
    assert len(report.execution_steps) == 0

def test_functional_idempotency(mock_output_dir):
    ir = build_radial(bus_count=5, voltage_kv=33.0)
    
    report1 = execute_in_psse(ir, output_dir=mock_output_dir)
    report2 = execute_in_psse(ir, output_dir=mock_output_dir)
    
    assert report1.success
    assert report2.success
    assert report1.execution_status == report2.execution_status
    assert report1.created_bus_count == report2.created_bus_count
    assert report1.load_flow_converged == report2.load_flow_converged
    
    # Ensure no contamination
    assert report2.created_bus_count == 5

def test_generator_path(mock_output_dir):
    ir = build_radial(bus_count=3, voltage_kv=33.0)
    # Manually change bus 33003 to generator and add machine
    ir.buses[-1].bus_type = "generator"
    ir.add_generator(Generator(bus_number=33003, p_mw=10.0, name="GEN1"))
    
    report = execute_in_psse(ir, output_dir=mock_output_dir)
    
    assert report.success
    assert report.created_generator_count == 1
    # Check steps for plant -> machine order
    steps_str = "\n".join(report.execution_steps)
    assert "[STEP 5] Creating plants" in steps_str
    assert "Created plant at bus 33003" in steps_str
    assert "[STEP 6] Creating machines" in steps_str
    assert "Created machine at bus 33003" in steps_str
