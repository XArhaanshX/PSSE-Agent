import networkx as nx
from typing import List
from app.ir.topology_ir import TopologyIR
from app.validation.validation_models import ValidationReport

def check_duplicate_bus_ids(ir: TopologyIR, report: ValidationReport) -> None:
    bus_ids = [bus.bus_number for bus in ir.buses]
    if len(bus_ids) != len(set(bus_ids)):
        # Find exactly which ones are duplicate
        seen = set()
        dupes = set()
        for b in bus_ids:
            if b in seen:
                dupes.add(b)
            seen.add(b)
        report.add_error(
            "DUPLICATE_BUS_ID",
            "Found duplicate bus IDs in the topology.",
            {"duplicates": list(dupes)}
        )

def check_duplicate_branches(ir: TopologyIR, report: ValidationReport) -> None:
    seen_edges = set()
    dupes = []
    for branch in ir.branches:
        # Canonicalize direction
        edge = tuple(sorted([branch.from_bus, branch.to_bus]))
        if edge in seen_edges:
            dupes.append(edge)
        seen_edges.add(edge)
        
    if dupes:
        report.add_error(
            "DUPLICATE_BRANCH",
            "Found duplicate branch connectivity.",
            {"duplicates": dupes}
        )

def check_branch_sanity(ir: TopologyIR, report: ValidationReport) -> None:
    invalid_branches = []
    for branch in ir.branches:
        if branch.from_bus == branch.to_bus:
            invalid_branches.append((branch.from_bus, branch.to_bus))
            
    if invalid_branches:
        report.add_error(
            "INVALID_BRANCH",
            "Found branch connecting a bus to itself (self-loop).",
            {"invalid_branches": invalid_branches}
        )

def check_connectedness(graph: nx.Graph, report: ValidationReport) -> None:
    if len(graph) > 0 and not nx.is_connected(graph):
        report.add_error("GRAPH_DISCONNECTED", "The topology graph is not fully connected.")

def check_no_isolated_buses(graph: nx.Graph, report: ValidationReport) -> None:
    isolated = [n for n, d in graph.degree() if d == 0]
    if isolated:
        report.add_error("ISOLATED_BUS", "Found isolated buses.", {"isolated_buses": isolated})

def check_single_swing_bus(graph: nx.Graph, report: ValidationReport) -> None:
    swing_buses = [n for n, attr in graph.nodes(data=True) if attr.get("bus_type") == "swing"]
    if len(swing_buses) == 0:
        report.add_error("NO_SWING_BUS", "Exactly one swing bus is required, but none were found.")
    elif len(swing_buses) > 1:
        report.add_error("MULTIPLE_SWING_BUSES", f"Expected exactly one swing bus, but found {len(swing_buses)}.", {"swing_buses": swing_buses})

def check_tree_structure(graph: nx.Graph, report: ValidationReport) -> None:
    if len(graph) > 0 and not nx.is_tree(graph):
        report.add_error("NOT_TREE", "The topology graph is not a mathematically valid tree.")

def validate_radial(graph: nx.Graph, report: ValidationReport) -> None:
    check_connectedness(graph, report)
    check_no_isolated_buses(graph, report)
    check_single_swing_bus(graph, report)
    check_tree_structure(graph, report)

def validate_single_bus(graph: nx.Graph, report: ValidationReport) -> None:
    check_connectedness(graph, report)
    check_no_isolated_buses(graph, report)
    check_single_swing_bus(graph, report)
    check_tree_structure(graph, report)
    
def validate_double_bus(graph: nx.Graph, report: ValidationReport) -> None:
    check_connectedness(graph, report)
    check_no_isolated_buses(graph, report)
    check_single_swing_bus(graph, report)
    check_tree_structure(graph, report)
    
def validate_substation_feeder(graph: nx.Graph, report: ValidationReport) -> None:
    check_connectedness(graph, report)
    check_no_isolated_buses(graph, report)
    check_single_swing_bus(graph, report)
    check_tree_structure(graph, report)
    
def validate_transformer_substation(graph: nx.Graph, report: ValidationReport) -> None:
    check_connectedness(graph, report)
    check_no_isolated_buses(graph, report)
    check_single_swing_bus(graph, report)
    check_tree_structure(graph, report)
