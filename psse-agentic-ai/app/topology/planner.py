from app.ir.topology_ir import TopologyIR
from app.topology.templates import (
    build_radial_topology, 
    build_single_bus_topology, 
    build_double_bus_topology,
    build_substation_feeder,
    build_transformer_substation
)

def build_radial(bus_count: int, voltage_kv: float) -> TopologyIR:
    """
    Minimal deterministic entrypoint for building a radial topology.
    """
    return build_radial_topology(bus_count, voltage_kv)

def build_single_bus(feeder_count: int, voltage_kv: float) -> TopologyIR:
    """
    Minimal deterministic entrypoint for building a single bus topology.
    """
    return build_single_bus_topology(feeder_count, voltage_kv)

def build_double_bus(feeder_count: int, voltage_kv: float) -> TopologyIR:
    """
    Minimal deterministic entrypoint for building a double bus topology.
    """
    return build_double_bus_topology(feeder_count, voltage_kv)

def get_substation_feeder(feeder_count: int, poi_voltage_kv: float, main_voltage_kv: float) -> TopologyIR:
    """
    Minimal deterministic entrypoint for building a substation feeder topology.
    """
    return build_substation_feeder(feeder_count, poi_voltage_kv, main_voltage_kv)

def get_transformer_substation(transformer_count: int, hv_kv: float, lv_kv: float) -> TopologyIR:
    """
    Minimal deterministic entrypoint for building a transformer substation topology.
    """
    return build_transformer_substation(transformer_count, hv_kv, lv_kv)
