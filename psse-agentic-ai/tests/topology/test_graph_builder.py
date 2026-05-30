from app.topology.planner import build_radial
from app.topology.graph_builder import build_graph

def test_build_graph():
    ir = build_radial(bus_count=5, voltage_kv=33.0)
    G = build_graph(ir)
    
    assert G.number_of_nodes() == 5
    assert G.number_of_edges() == 4
    
    # Check node metadata
    for bus in ir.buses:
        node_data = G.nodes[bus.bus_number]
        assert node_data["name"] == bus.name
        assert node_data["base_kv"] == bus.base_kv
        assert node_data["bus_type"] == bus.bus_type

    # Check edge metadata
    for branch in ir.branches:
        edge_data = G.edges[branch.from_bus, branch.to_bus]
        assert edge_data["resistance_pu"] == branch.resistance_pu
        assert edge_data["reactance_pu"] == branch.reactance_pu
        assert edge_data["circuit_id"] == branch.circuit_id
        assert edge_data["status"] == branch.status
