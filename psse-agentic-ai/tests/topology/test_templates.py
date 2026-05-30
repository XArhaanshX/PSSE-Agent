from app.topology.templates import build_single_bus_topology, build_double_bus_topology

def test_single_bus_topology():
    feeder_count = 3
    voltage = 33.0
    ir = build_single_bus_topology(feeder_count, voltage)
    
    assert len(ir.buses) == feeder_count + 1
    assert len(ir.branches) == feeder_count
    
    swing_buses = [b for b in ir.buses if b.bus_type == "swing"]
    assert len(swing_buses) == 1
    assert swing_buses[0].bus_number == int(voltage * 1000) + 1

def test_double_bus_topology():
    feeder_count = 4
    voltage = 132.0
    ir = build_double_bus_topology(feeder_count, voltage)
    
    assert len(ir.buses) == feeder_count + 2
    # 4 feeders + 1 bus tie
    assert len(ir.branches) == feeder_count + 1
    
    # 1 swing, rest load (since we changed MAIN2 to load)
    swing_buses = [b for b in ir.buses if b.bus_type == "swing"]
    assert len(swing_buses) == 1
