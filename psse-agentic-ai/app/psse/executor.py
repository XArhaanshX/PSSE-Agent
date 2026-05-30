from pathlib import Path
from app.ir.topology_ir import TopologyIR
from app.validation.validator import validate_topology
from app.psse.execution_models import ExecutionReport, ExecutionArtifact

# Safe import for PSS/E
def get_psspy():
    import psspy
    return psspy

from app.psse.creators import (
    create_bus,
    create_branch,
    create_transformer,
    create_plant,
    create_machine,
    create_load
)

DEFAULT_FNSL_OPTIONS = [1, 0, 0, 1, 1, 0, 99, 0]

def execute_in_psse(ir: TopologyIR, output_dir: str = "outputs/runs/stage5", layout_config=None, output_filename: str = "case") -> ExecutionReport:
    """
    Deterministically execute the TopologyIR in PSSE.
    Execution order is strict to satisfy PSSE requirements.
    """
    from app.layout.engine import LayoutConfig
    layout_config = layout_config or LayoutConfig()
    
    report = ExecutionReport()
    
    # 1. Validation Guardrail
    validation = validate_topology(ir)
    if not validation.is_valid:
        report.execution_status = "validation_failed"
        report.errors.extend([iss.message for iss in validation.issues])
        return report

    try:
        psspy = get_psspy()
        
        # [STEP 1] Initializing PSSE session
        report.execution_steps.append("[STEP 1] Initializing PSSE session")
        # Ensure PSSE is actually initialized before APIs are called (Minimal fix for real PSSE)
        try:
            psspy.psseinit(12000)
        except Exception:
            pass
        # Ensure idempotent execution by starting a completely new case
        psspy.newcase_2([0, 1], 100.0, 60.0, "STAGE 4 EXECUTION", "DETERMINISTIC GRAPH")

        # [STEP 2] Creating buses
        report.execution_steps.append("[STEP 2] Creating buses")
        for bus in ir.buses:
            # Map semantic bus_type to IDE integer
            if bus.bus_type == "swing":
                ide = 3
            elif bus.bus_type == "generator":
                ide = 2
            else:
                ide = 1
                
            create_bus(bus.bus_number, bus.name, bus.base_kv, bus_type=ide)
            report.execution_steps.append(f"Created bus {bus.bus_number}")
            report.created_bus_count += 1

        # [STEP 3] Creating branches
        report.execution_steps.append("[STEP 3] Creating branches")
        for branch in ir.branches:
            create_branch(branch.from_bus, branch.to_bus)
            report.execution_steps.append(f"Created branch {branch.from_bus} -> {branch.to_bus}")
            report.created_branch_count += 1

        # [STEP 4] Creating transformers
        report.execution_steps.append("[STEP 4] Creating transformers")
        for transformer in ir.transformers:
            create_transformer(transformer.from_bus, transformer.to_bus, transformer.name)
            report.execution_steps.append(f"Created transformer {transformer.from_bus} -> {transformer.to_bus}")
            report.created_transformer_count += 1

        # [STEP 5] Creating plants
        report.execution_steps.append("[STEP 5] Creating plants")
        # Generators require a plant first
        for generator in ir.generators:
            create_plant(generator.bus_number)
            report.execution_steps.append(f"Created plant at bus {generator.bus_number}")

        # [STEP 6] Creating machines
        report.execution_steps.append("[STEP 6] Creating machines")
        for generator in ir.generators:
            create_machine(generator.bus_number, generator.p_mw)
            report.execution_steps.append(f"Created machine at bus {generator.bus_number}")
            report.created_generator_count += 1

        # [STEP 7] Creating loads
        report.execution_steps.append("[STEP 7] Creating loads")
        for load in ir.loads:
            create_load(load.bus_number, load.p_mw, load.q_mvar)
            report.execution_steps.append(f"Created load at bus {load.bus_number}")
            report.created_load_count += 1

        # [STEP 8] Running load flow
        report.execution_steps.append("[STEP 8] Running load flow")
        ierr = psspy.fnsl(DEFAULT_FNSL_OPTIONS)
        if ierr == 0:
            report.load_flow_converged = True
        else:
            report.load_flow_converged = False

        # Prepare output dir
        out_path = Path(output_dir)
        out_path.mkdir(parents=True, exist_ok=True)
        
        # [STEP 9] Saving SAV
        report.execution_steps.append("[STEP 9] Saving SAV")
        sav_file = str(out_path / f"{output_filename}.sav")
        psspy.save(sav_file)
        report.artifacts.append(ExecutionArtifact(artifact_type="sav", path=sav_file))

        # [STEP 10] Exporting RAW
        report.execution_steps.append("[STEP 10] Exporting RAW")
        raw_file = str(out_path / f"{output_filename}.raw")
        psspy.rawd_2(0, 1, [1, 0, 1, 0, 0, 0, 0], 0, raw_file)
        report.artifacts.append(ExecutionArtifact(artifact_type="raw", path=raw_file))

        # [STEP 11] Layout Coordinate Computation
        report.execution_steps.append("[STEP 11] Layout Coordinate Computation")
        from app.layout.engine import LayoutEngine
        layout_engine = LayoutEngine(config=layout_config)
        coords = layout_engine.compute_layout(ir)

        # [STEP 12] Diagram Materialization
        report.execution_steps.append("[STEP 12] Diagram Materialization")
        psspy.newdiagfile()
        
        bus_numbers = [b.bus_number for b in ir.buses]
        if bus_numbers:
            # Create a subsystem (bsys) containing all our buses
            # bsys(sid, use_tot, vrange, use_num, numlist, use_bus, buslist, use_area, arealist, use_zone, zonelist)
            psspy.bsys(1, 0, [0.0, 0.0], 0, [], len(bus_numbers), bus_numbers, 0, [], 0, [])
            
            # Place each bus using explicit coordinates
            for b_num, (x, y) in coords.items():
                psspy.growbus(b_num, float(x), float(y))
                
        sld_file = str(out_path / f"{output_filename}.sld")
        psspy.savediagfile(sld_file)
        report.artifacts.append(ExecutionArtifact(artifact_type="sld", path=sld_file))
        report.execution_steps.append("Diagram saved successfully")

        report.success = True
        report.execution_status = "success"

    except Exception as e:
        report.success = False
        report.execution_status = "execution_failed"
        report.errors.append(str(e))
        
    return report
