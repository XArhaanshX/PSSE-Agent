import os
import sys
import argparse
from pathlib import Path

# MINIMAL FIX for Python 3.8+ DLL resolution in Windows for real PSSE36
os.environ["PATH"] = r"C:\Program Files\PTI\PSSE36\36.0\PSSBIN;" + os.environ.get("PATH", "")
sys.path.append(r"C:\Program Files\PTI\PSSE36\36.0\PSSPY311")
sys.path.append(r"C:\Program Files\PTI\PSSE36\36.0\PSSBIN")
try:
    os.add_dll_directory(r"C:\Program Files\PTI\PSSE36\36.0\PSSBIN")
except AttributeError:
    pass

from app.topology.planner import get_substation_feeder, get_transformer_substation
from app.validation.validator import validate_topology
from app.psse.executor import execute_in_psse
from app.layout.engine import LayoutConfig

def main():
    parser = argparse.ArgumentParser(description="Stage 7 Deterministic Hierarchical Topology Demo")
    parser.add_argument("--topology", type=str, choices=["substation_feeder", "transformer_substation"], default="substation_feeder")
    args = parser.parse_args()

    print("=" * 60)
    print(f"STAGE 7 - HIERARCHICAL TOPOLOGY DEMO: {args.topology.upper()}")
    print("=" * 60)

    # 1. Build deterministic topology
    print(f"\n[STEP 1] Building deterministic {args.topology} topology...")
    
    if args.topology == "substation_feeder":
        ir = get_substation_feeder(feeder_count=4, poi_voltage_kv=132.0, main_voltage_kv=33.0)
    elif args.topology == "transformer_substation":
        ir = get_transformer_substation(transformer_count=3, hv_kv=220.0, lv_kv=33.0)

    # 2. Validate
    print("\n[STEP 2] Validating topology...")
    report = validate_topology(ir)
    if not report.is_valid:
        print("Validation failed!")
        for issue in report.issues:
            print(f"- {issue.code}: {issue.message}")
        return
    print("Validation passed. Topology is structurally sound.")

    # 3. Configure Deterministic Layout
    print("\n[STEP 3] Configuring Deterministic Layout...")
    layout_config = LayoutConfig(
        x_spacing=3.0,
        y_spacing=3.0,
        orientation=args.topology
    )
    print(f"Layout mode: {layout_config.orientation}")
    print(f"Spacing: (x={layout_config.x_spacing}, y={layout_config.y_spacing})")

    # 4. Execute in REAL PSSE
    print("\n[STEP 4] Executing in REAL PSSE...")
    exec_report = execute_in_psse(ir, output_dir=f"outputs/runs/stage7_{args.topology}", layout_config=layout_config)
    
    print("\nExecution Report:")
    print(f"Status: {exec_report.execution_status}")
    if exec_report.errors:
        for err in exec_report.errors:
            print(f"ERROR: {err}")
    print(f"Buses created: {exec_report.created_bus_count}")
    print(f"Branches created: {exec_report.created_branch_count}")

    # 5. Verify Load Flow
    print("\n[STEP 5] Verifying load flow...")
    if exec_report.load_flow_converged:
        print("LOAD FLOW CONVERGED")
    else:
        print("LOAD FLOW FAILED")

    # 6. Verify Artifacts
    print("\n[STEP 6] Verifying generated artifacts...")
    for artifact in exec_report.artifacts:
        path = Path(artifact.path)
        if path.exists():
            size = path.stat().st_size
            print(f"[PASS] {artifact.artifact_type.upper()} file exists: {artifact.path} (Size: {size} bytes)")
        else:
            print(f"[FAIL] {artifact.artifact_type.upper()} file MISSING: {artifact.path}")

    sld_artifacts = [a for a in exec_report.artifacts if a.artifact_type == "sld"]
    if sld_artifacts and Path(sld_artifacts[0].path).exists() and Path(sld_artifacts[0].path).stat().st_size > 2600:
        print(f"\nSUCCESS: Deterministic SLD generated and hardened successfully for {args.topology}.")
    else:
        print("\nFAIL: SLD generation did not meet hardening standards.")

    print("\nDone.")

if __name__ == "__main__":
    main()
