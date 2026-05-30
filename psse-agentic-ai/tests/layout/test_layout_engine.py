import pytest
from app.topology.planner import build_radial
from app.layout.engine import LayoutEngine, LayoutConfig

def test_deterministic_coordinates():
    """TEST 1 - Deterministic Coordinates: Same IR should produce identical coordinates."""
    ir = build_radial(bus_count=5, voltage_kv=33.0)
    config = LayoutConfig(x_spacing=2.0, y_spacing=2.0, orientation="horizontal")
    engine1 = LayoutEngine(config)
    engine2 = LayoutEngine(config)
    
    coords1 = engine1.compute_layout(ir)
    coords2 = engine2.compute_layout(ir)
    
    assert coords1 == coords2, "Coordinates should be identical across runs"

def test_horizontal_layout_correctness():
    """TEST 2 - Horizontal Layout Correctness: x strictly increases, y constant."""
    ir = build_radial(bus_count=5, voltage_kv=33.0)
    config = LayoutConfig(x_spacing=2.0, y_spacing=2.0, orientation="horizontal")
    engine = LayoutEngine(config)
    
    coords = engine.compute_layout(ir)
    
    buses = sorted(ir.buses, key=lambda b: b.bus_number)
    
    prev_x = -1.0
    for bus in buses:
        x, y = coords[bus.bus_number]
        assert y == 0.0, "Y coordinate must be constant in horizontal layout"
        assert x > prev_x, "X coordinate must strictly increase in horizontal layout"
        prev_x = x

def test_vertical_layout_correctness():
    """TEST 3 - Vertical Layout Correctness: y strictly increases, x constant."""
    ir = build_radial(bus_count=5, voltage_kv=33.0)
    config = LayoutConfig(x_spacing=2.0, y_spacing=2.0, orientation="vertical")
    engine = LayoutEngine(config)
    
    coords = engine.compute_layout(ir)
    
    buses = sorted(ir.buses, key=lambda b: b.bus_number)
    
    prev_y = -1.0
    for bus in buses:
        x, y = coords[bus.bus_number]
        assert x == 0.0, "X coordinate must be constant in vertical layout"
        assert y > prev_y, "Y coordinate must strictly increase in vertical layout"
        prev_y = y

from app.topology.planner import build_single_bus, build_double_bus

def test_single_bus_layout():
    ir = build_single_bus(feeder_count=3, voltage_kv=33.0)
    config = LayoutConfig(x_spacing=2.0, y_spacing=3.0, orientation="single_bus")
    engine = LayoutEngine(config)
    coords = engine.compute_layout(ir)
    
    swing = [b for b in ir.buses if b.bus_type == "swing"][0]
    feeders = [b for b in ir.buses if b.bus_type == "load"]
    
    assert coords[swing.bus_number] == (0.0, 0.0)
    
    x_pos = 0.0
    for f in sorted(feeders, key=lambda b: b.bus_number):
        assert coords[f.bus_number] == (x_pos, 3.0)
        x_pos += 2.0

def test_double_bus_layout():
    ir = build_double_bus(feeder_count=4, voltage_kv=132.0)
    config = LayoutConfig(x_spacing=2.0, y_spacing=3.0, orientation="double_bus")
    engine = LayoutEngine(config)
    coords = engine.compute_layout(ir)
    
    mains = [b for b in ir.buses if "MAIN" in b.name]
    feeders = [b for b in ir.buses if b.bus_type == "load" and "FDR" in b.name]
    
    m1, m2 = sorted(mains, key=lambda b: b.bus_number)
    
    assert coords[m1.bus_number] == (0.0, 0.0)
    assert coords[m2.bus_number] == (0.0, 6.0)
    
    x_pos = 0.0
    for f in sorted(feeders, key=lambda b: b.bus_number):
        assert coords[f.bus_number] == (x_pos, 3.0)
        x_pos += 2.0
