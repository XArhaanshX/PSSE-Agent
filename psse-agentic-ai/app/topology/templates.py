from app.ir.topology_ir import TopologyIR
from app.ir.component_models import Bus, Branch
from app.topology.numbering import generate_radial_bus_numbers, generate_deterministic_bus_numbers

def build_radial_topology(bus_count: int, voltage_kv: float) -> TopologyIR:
    """
    Build a deterministic radial topology containing only buses and branches.
    First bus is swing, remaining are loads.
    """
    ir = TopologyIR()
    ir.metadata.topology_type = "radial"
    bus_numbers = generate_radial_bus_numbers(bus_count, voltage_kv)
    
    # Create buses
    for i, bnum in enumerate(bus_numbers):
        bus_type = "swing" if i == 0 else "load"
        bus = Bus(
            bus_number=bnum,
            name=f"BUS_{bnum}",
            base_kv=voltage_kv,
            bus_type=bus_type
        )
        ir.add_bus(bus)
        
    # Create branches
    for i in range(bus_count - 1):
        from_bus = bus_numbers[i]
        to_bus = bus_numbers[i + 1]
        branch = Branch(
            from_bus=from_bus,
            to_bus=to_bus,
            resistance_pu=0.01,
            reactance_pu=0.1,
            circuit_id="1",
            status=True
        )
        ir.add_branch(branch)
        
    return ir

def build_single_bus_topology(feeder_count: int, voltage_kv: float) -> TopologyIR:
    """
    Build a deterministic single bus topology.
    One main bus (Swing), and N feeder buses (Load) connected to it.
    """
    ir = TopologyIR()
    ir.metadata.topology_type = "single_bus"
    # Main bus is 0, feeders are 1 to feeder_count
    bus_numbers = generate_deterministic_bus_numbers(feeder_count + 1, voltage_kv)
    
    main_bus = bus_numbers[0]
    ir.add_bus(Bus(bus_number=main_bus, name=f"MAIN_{main_bus}", base_kv=voltage_kv, bus_type="swing"))
    
    for i in range(1, feeder_count + 1):
        f_bus = bus_numbers[i]
        ir.add_bus(Bus(bus_number=f_bus, name=f"FDR_{f_bus}", base_kv=voltage_kv, bus_type="load"))
        
        ir.add_branch(Branch(
            from_bus=main_bus,
            to_bus=f_bus,
            resistance_pu=0.01,
            reactance_pu=0.1,
            circuit_id="1",
            status=True
        ))
        
    return ir

def build_double_bus_topology(feeder_count: int, voltage_kv: float) -> TopologyIR:
    """
    Build a deterministic double bus topology.
    Two main buses connected by a bus coupler, with feeders split between them.
    """
    ir = TopologyIR()
    ir.metadata.topology_type = "double_bus"
    # Main buses are 0 and 1, feeders are 2 to feeder_count + 1
    bus_numbers = generate_deterministic_bus_numbers(feeder_count + 2, voltage_kv)
    
    main_bus_1 = bus_numbers[0]
    main_bus_2 = bus_numbers[1]
    
    ir.add_bus(Bus(bus_number=main_bus_1, name=f"MAIN1_{main_bus_1}", base_kv=voltage_kv, bus_type="swing"))
    ir.add_bus(Bus(bus_number=main_bus_2, name=f"MAIN2_{main_bus_2}", base_kv=voltage_kv, bus_type="load"))
    
    # Bus coupler (low impedance tie)
    ir.add_branch(Branch(
        from_bus=main_bus_1,
        to_bus=main_bus_2,
        resistance_pu=0.001,
        reactance_pu=0.01,
        circuit_id="1",
        status=True
    ))
    
    for i in range(2, feeder_count + 2):
        f_bus = bus_numbers[i]
        ir.add_bus(Bus(bus_number=f_bus, name=f"FDR_{f_bus}", base_kv=voltage_kv, bus_type="load"))
        
        # Connect even index to MAIN1, odd to MAIN2
        parent_bus = main_bus_1 if i % 2 == 0 else main_bus_2
        
        ir.add_branch(Branch(
            from_bus=parent_bus,
            to_bus=f_bus,
            resistance_pu=0.01,
            reactance_pu=0.1,
            circuit_id="1",
            status=True
        ))
        
    return ir

def build_substation_feeder(feeder_count: int, poi_voltage_kv: float, main_voltage_kv: float) -> TopologyIR:
    """
    Build a deterministic substation feeder topology.
    POI -> Yard -> Main Bus -> Feeders
    """
    ir = TopologyIR()
    ir.metadata.topology_type = "substation_feeder"
    
    # 0 = POI, 1 = Yard, 2 = Main Bus, 3.. = Feeders
    bus_numbers = generate_deterministic_bus_numbers(feeder_count + 3, main_voltage_kv)
    
    poi_bus = bus_numbers[0]
    yard_bus = bus_numbers[1]
    main_bus = bus_numbers[2]
    
    # POI is the swing bus
    ir.add_bus(Bus(bus_number=poi_bus, name="POI", base_kv=poi_voltage_kv, bus_type="swing"))
    # Yard is just a node (load type in PSSE with 0 load)
    ir.add_bus(Bus(bus_number=yard_bus, name="YARD", base_kv=poi_voltage_kv, bus_type="load"))
    # Main bus is load type
    ir.add_bus(Bus(bus_number=main_bus, name="MAIN", base_kv=main_voltage_kv, bus_type="load"))
    
    # POI -> Yard branch
    ir.add_branch(Branch(from_bus=poi_bus, to_bus=yard_bus, resistance_pu=0.01, reactance_pu=0.1))
    
    # Yard -> Main Bus transformer (assumed step-down)
    from app.ir.component_models import Transformer
    ir.add_transformer(Transformer(
        from_bus=yard_bus, 
        to_bus=main_bus, 
        resistance_pu=0.005, 
        reactance_pu=0.05, 
        base_mva=100.0, 
        name="TR1"
    ))
    
    # Main -> Feeders
    for i in range(3, feeder_count + 3):
        f_bus = bus_numbers[i]
        ir.add_bus(Bus(bus_number=f_bus, name=f"FDR_{f_bus}", base_kv=main_voltage_kv, bus_type="load"))
        ir.add_branch(Branch(from_bus=main_bus, to_bus=f_bus, resistance_pu=0.01, reactance_pu=0.1))
        
    return ir

def build_transformer_substation(transformer_count: int, hv_kv: float, lv_kv: float) -> TopologyIR:
    """
    Build a deterministic transformer substation topology.
    HV_BUS -> Transformers -> LV_BUSes -> Loads
    """
    ir = TopologyIR()
    ir.metadata.topology_type = "transformer_substation"
    
    bus_numbers = generate_deterministic_bus_numbers(transformer_count * 2 + 1, hv_kv)
    
    hv_bus = bus_numbers[0]
    ir.add_bus(Bus(bus_number=hv_bus, name="HV_MAIN", base_kv=hv_kv, bus_type="swing"))
    
    from app.ir.component_models import Transformer, Load
    for i in range(1, transformer_count + 1):
        lv_bus = bus_numbers[i]
        load_bus = bus_numbers[i + transformer_count]
        
        # LV Bus
        ir.add_bus(Bus(bus_number=lv_bus, name=f"LV_{lv_bus}", base_kv=lv_kv, bus_type="load"))
        # Transformer HV -> LV
        ir.add_transformer(Transformer(
            from_bus=hv_bus,
            to_bus=lv_bus,
            resistance_pu=0.005,
            reactance_pu=0.05,
            base_mva=100.0,
            name=f"TR_{i}"
        ))
        
        # Load Bus
        ir.add_bus(Bus(bus_number=load_bus, name=f"LD_{load_bus}", base_kv=lv_kv, bus_type="load"))
        # Branch LV -> Load
        ir.add_branch(Branch(from_bus=lv_bus, to_bus=load_bus, resistance_pu=0.01, reactance_pu=0.1))
        # Actual Load
        ir.add_load(Load(bus_number=load_bus, p_mw=10.0, q_mvar=2.0))
        
    return ir
