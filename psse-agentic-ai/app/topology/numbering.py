from typing import List

def generate_radial_bus_numbers(count: int, voltage_kv: float) -> List[int]:
    """
    Generate a deterministic list of bus numbers for a radial topology.
    The numbering scheme uses the voltage_kv multiplied by 1000, plus an index.
    For example: 5 buses at 33kV -> [33001, 33002, 33003, 33004, 33005]
    """
    base_prefix = int(voltage_kv * 1000)
    return [base_prefix + i for i in range(1, count + 1)]

def generate_deterministic_bus_numbers(count: int, voltage_kv: float) -> List[int]:
    """
    Generate a deterministic list of bus numbers.
    Alias for generate_radial_bus_numbers to keep the domain generic for non-radial topologies.
    """
    return generate_radial_bus_numbers(count, voltage_kv)
