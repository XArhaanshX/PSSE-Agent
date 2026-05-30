from app.topology.planner import build_radial
from app.validation.validator import validate_topology
from app.ir.component_models import Bus, Branch

def test_valid_topology():
    ir = build_radial(5, 33.0)
    report = validate_topology(ir)
    assert report.is_valid
    assert len(report.issues) == 0

def test_isolated_bus():
    ir = build_radial(5, 33.0)
    # Add an isolated bus
    ir.add_bus(Bus(bus_number=999, name="ISO", base_kv=33.0, bus_type="load"))
    
    report = validate_topology(ir)
    assert not report.is_valid
    
    # It will trigger ISOLATED_BUS and GRAPH_DISCONNECTED and NOT_RADIAL
    codes = [i.code for i in report.issues]
    assert "ISOLATED_BUS" in codes
    assert "GRAPH_DISCONNECTED" in codes
    assert "NOT_RADIAL" in codes

def test_not_radial_cycle():
    ir = build_radial(5, 33.0)
    # Add a branch connecting 33005 back to 33001 to create a cycle
    ir.add_branch(Branch(from_bus=33005, to_bus=33001, resistance_pu=0.1, reactance_pu=0.1))
    
    report = validate_topology(ir)
    assert not report.is_valid
    codes = [i.code for i in report.issues]
    assert "NOT_RADIAL" in codes
