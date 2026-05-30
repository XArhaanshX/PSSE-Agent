"""PSSE creators module."""

from app.psse.error_handling import validate_ierr

def get_psspy():
    import psspy
    return psspy

def create_bus(bus_num: int, name: str, base_kv: float, bus_type: int = 1):
    psspy = get_psspy()
    name = name[:12] if name else ""
    ierr = psspy.bus_data_4(bus_num, 0, [bus_type, 1, 1, 1], [base_kv, 1.0, 0.0, 1.1, 0.9, 1.1, 0.9], name)
    validate_ierr(ierr, "bus_data_4", {"ibus": bus_num, "name": name, "baskv": base_kv, "bus_type": bus_type})

def create_branch(from_bus: int, to_bus: int):
    psspy = get_psspy()
    realar = [0.01, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0]
    ierr = psspy.branch_data_3(from_bus, to_bus, '1', [1, from_bus, 1, 0, 0, 0], realar, [0.0]*12, "")
    validate_ierr(ierr, "branch_data_3", {"ibus": from_bus, "jbus": to_bus})

def create_transformer(from_bus: int, to_bus: int, name: str = ""):
    psspy = get_psspy()
    name = name[:12] if name else ""
    # intgar: 16 elements. defaults mostly. (Status, Winding1Bus, Owner1, Owner2, Owner3, Owner4, ..., MeteredBus, ...)
    intgar = [1, from_bus, 1, 0, 0, 0, 33, 0, from_bus, 0, 0, 1, 0, 1, 1, 1]
    # realari: 21 elements. R=0.01, X=0.1
    realari = [0.01, 0.1, 100.0, 1.0, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 1.1, 0.9, 1.1, 0.9, 0.0, 0.0, 0.0]
    result = psspy.two_winding_data_6(from_bus, to_bus, '1', intgar, realari, [0.0]*12, name, "")
    # Python API sometimes returns (ierr, realaro) for this function
    ierr = result[0] if isinstance(result, tuple) else result
    validate_ierr(ierr, "two_winding_data_6", {"ibus": from_bus, "jbus": to_bus})

def create_load(bus_num: int, p_mw: float, q_mvar: float):
    psspy = get_psspy()
    intgar = [1, 1, 1, 1, 1, 0, 0]
    realar = [p_mw, q_mvar, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    ierr = psspy.load_data_6(bus_num, '1', intgar, realar, "")
    validate_ierr(ierr, "load_data_6", {"ibus": bus_num, "p_mw": p_mw, "q_mvar": q_mvar})

def create_plant(bus_num: int, v_pu: float = 1.0):
    psspy = get_psspy()
    ierr = psspy.plant_data_4(bus_num, 0, [0, 0], [v_pu, 100.0])
    validate_ierr(ierr, "plant_data_4", {"ibus": bus_num, "v_pu": v_pu})

def create_machine(bus_num: int, p_mw: float):
    psspy = get_psspy()
    intgar = [1, 1, 0, 0, 0, 0, 0]
    realar = [p_mw, 0.0, 9999.0, -9999.0, 9999.0, -9999.0, 100.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
    ierr = psspy.machine_data_4(bus_num, '1', intgar, realar, "")
    validate_ierr(ierr, "machine_data_4", {"ibus": bus_num, "p_mw": p_mw})
