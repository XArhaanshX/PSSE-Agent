from app.ir.topology_ir import TopologyIR
from app.validation.validation_models import ValidationReport
from app.topology.graph_builder import build_graph

from app.validation.checks import (
    check_duplicate_bus_ids,
    check_duplicate_branches,
    check_branch_sanity,
    validate_radial,
    validate_single_bus,
    validate_double_bus,
    validate_substation_feeder,
    validate_transformer_substation
)

def validate_topology(ir: TopologyIR) -> ValidationReport:
    """
    Validate a topology deterministically via static dispatch by topology_type.
    Execution order is strict: IR-level checks must run BEFORE graph-level checks.
    """
    report = ValidationReport()
    
    # Universal IR-level checks
    check_duplicate_bus_ids(ir, report)
    check_duplicate_branches(ir, report)
    check_branch_sanity(ir, report)
    
    # Universal graph build
    graph = build_graph(ir)
    
    # Dispatch to topology-specific validation semantics
    topo_type = ir.metadata.topology_type
    
    if topo_type == "radial":
        validate_radial(graph, report)
    elif topo_type == "single_bus":
        validate_single_bus(graph, report)
    elif topo_type == "double_bus":
        validate_double_bus(graph, report)
    elif topo_type == "substation_feeder":
        validate_substation_feeder(graph, report)
    elif topo_type == "transformer_substation":
        validate_transformer_substation(graph, report)
    else:
        report.add_error("UNKNOWN_TOPOLOGY", f"Validation rules for '{topo_type}' are not defined.")
        
    return report
