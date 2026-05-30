from app.ir.component_models import Bus, Branch
from app.ir.topology_ir import TopologyIR
from app.validation.validation_models import ValidationReport
from app.validation.checks import (
    check_duplicate_bus_ids,
    check_duplicate_branches,
    check_branch_sanity,
    check_single_swing_bus
)
import networkx as nx

def test_check_duplicate_bus_ids():
    ir = TopologyIR()
    ir.add_bus(Bus(bus_number=1, name="B1", base_kv=33, bus_type="swing"))
    ir.add_bus(Bus(bus_number=1, name="B2", base_kv=33, bus_type="load"))
    
    report = ValidationReport()
    check_duplicate_bus_ids(ir, report)
    
    assert not report.is_valid
    assert len(report.issues) == 1
    assert report.issues[0].code == "DUPLICATE_BUS_ID"
    assert 1 in report.issues[0].context["duplicates"]

def test_check_duplicate_branches():
    ir = TopologyIR()
    # A->B and B->A should be caught as duplicates
    ir.add_branch(Branch(from_bus=1, to_bus=2, resistance_pu=0.1, reactance_pu=0.1))
    ir.add_branch(Branch(from_bus=2, to_bus=1, resistance_pu=0.1, reactance_pu=0.1))
    
    report = ValidationReport()
    check_duplicate_branches(ir, report)
    
    assert not report.is_valid
    assert len(report.issues) == 1
    assert report.issues[0].code == "DUPLICATE_BRANCH"
    assert (1, 2) in report.issues[0].context["duplicates"]

def test_check_branch_sanity():
    ir = TopologyIR()
    ir.add_branch(Branch(from_bus=1, to_bus=1, resistance_pu=0.1, reactance_pu=0.1))
    
    report = ValidationReport()
    check_branch_sanity(ir, report)
    
    assert not report.is_valid
    assert len(report.issues) == 1
    assert report.issues[0].code == "INVALID_BRANCH"

def test_check_single_swing_bus_multiple():
    G = nx.Graph()
    G.add_node(1, bus_type="swing")
    G.add_node(2, bus_type="swing")
    
    report = ValidationReport()
    check_single_swing_bus(G, report)
    
    assert not report.is_valid
    assert report.issues[0].code == "MULTIPLE_SWING_BUSES"

def test_check_single_swing_bus_none():
    G = nx.Graph()
    G.add_node(1, bus_type="load")
    
    report = ValidationReport()
    check_single_swing_bus(G, report)
    
    assert not report.is_valid
    assert report.issues[0].code == "NO_SWING_BUS"
