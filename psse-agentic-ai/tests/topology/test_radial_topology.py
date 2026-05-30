from app.topology.planner import build_radial

def test_build_radial():
    ir = build_radial(bus_count=5, voltage_kv=33.0)
    
    assert len(ir.buses) == 5
    assert len(ir.branches) == 4
    
    # Check bus numbering
    bus_numbers = [bus.bus_number for bus in ir.buses]
    assert bus_numbers == [33001, 33002, 33003, 33004, 33005]
    
    # Check bus types
    assert ir.buses[0].bus_type == "swing"
    for bus in ir.buses[1:]:
        assert bus.bus_type == "load"

    # Check branches connectivity
    for i in range(4):
        branch = ir.branches[i]
        assert branch.from_bus == bus_numbers[i]
        assert branch.to_bus == bus_numbers[i+1]
        assert branch.resistance_pu == 0.01
        assert branch.reactance_pu == 0.1
