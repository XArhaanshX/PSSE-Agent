import networkx as nx
from app.ir.topology_ir import TopologyIR

def build_graph(ir: TopologyIR) -> nx.Graph:
    """
    Build a networkx Graph from the TopologyIR.
    Nodes represent buses and edges represent branches.
    Node and edge attributes map directly to their semantic IR fields.
    """
    G = nx.Graph()
    
    # Add nodes (buses)
    for bus in ir.buses:
        G.add_node(
            bus.bus_number,
            name=bus.name,
            base_kv=bus.base_kv,
            bus_type=bus.bus_type
        )
        
    # Add edges (branches)
    for branch in ir.branches:
        G.add_edge(
            branch.from_bus,
            branch.to_bus,
            resistance_pu=branch.resistance_pu,
            reactance_pu=branch.reactance_pu,
            circuit_id=branch.circuit_id,
            status=branch.status,
            edge_type="branch"
        )
        
    # Add edges (transformers)
    for transformer in ir.transformers:
        G.add_edge(
            transformer.from_bus,
            transformer.to_bus,
            resistance_pu=transformer.resistance_pu,
            reactance_pu=transformer.reactance_pu,
            circuit_id=transformer.circuit_id,
            status=transformer.status,
            edge_type="transformer"
        )
        
    return G
