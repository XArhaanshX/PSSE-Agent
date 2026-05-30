import os
import sys
from pathlib import Path

# MINIMAL FIX for Python 3.8+ DLL resolution in Windows for real PSSE36
os.environ["PATH"] = r"C:\Program Files\PTI\PSSE36\36.0\PSSBIN;" + os.environ.get("PATH", "")
sys.path.append(r"C:\Program Files\PTI\PSSE36\36.0\PSSPY311")
sys.path.append(r"C:\Program Files\PTI\PSSE36\36.0\PSSBIN")
try:
    os.add_dll_directory(r"C:\Program Files\PTI\PSSE36\36.0\PSSBIN")
except AttributeError:
    pass  # Pre-3.8 or non-Windows

from app.topology.planner import build_radial
from app.validation.validator import validate_topology
from app.psse.executor import execute_in_psse, get_psspy

def main():
    print("=" * 50)
    print("STAGE 4.25 - REAL PSSE INTEGRATION VALIDATION DEMO")
    print("=" * 50)

    # 1. Build deterministic topology
    print("\n[STEP 1] Building deterministic radial topology...")
    ir = build_radial(bus_count=5, voltage_kv=33.0)

    # 2. Validate
    print("\n[STEP 2] Validating topology...")
    report = validate_topology(ir)
    if not report.is_valid:
        print("Validation failed!")
        for issue in report.issues:
            print(f"- {issue.code}: {issue.message}")
        return
    print("Validation passed. Topology is structurally sound.")

    # 3. Execute in REAL PSSE
    print("\n[STEP 3] Executing in REAL PSSE...")
    exec_report = execute_in_psse(ir, output_dir="outputs/runs/stage4")
    
    print("\nExecution Report:")
    print(f"Status: {exec_report.execution_status}")
    if exec_report.errors:
        for err in exec_report.errors:
            print(f"ERROR: {err}")
    print(f"Buses created: {exec_report.created_bus_count}")
    print(f"Branches created: {exec_report.created_branch_count}")
    print(f"Transformers created: {exec_report.created_transformer_count}")
    print(f"Generators created: {exec_report.created_generator_count}")
    print(f"Loads created: {exec_report.created_load_count}")

    # 4. Verify Files
    print("\n[STEP 4] Verifying generated artifacts...")
    all_exist = True
    for artifact in exec_report.artifacts:
        if Path(artifact.path).exists():
            print(f"[PASS] {artifact.artifact_type.upper()} file exists: {artifact.path}")
        else:
            print(f"[FAIL] {artifact.artifact_type.upper()} file MISSING: {artifact.path}")
            all_exist = False

    if all_exist:
        print("PASS: All artifacts generated successfully.")
    else:
        print("FAIL: Artifact generation failed.")

    # 5. Verify Load Flow
    print("\n[STEP 5] Verifying load flow...")
    if exec_report.load_flow_converged:
        print("LOAD FLOW CONVERGED")
    else:
        print("LOAD FLOW FAILED")

    # 6. Verify SLD Artifact
    print("\n[STEP 6] Verifying SLD Materialization...")
    sld_artifacts = [a for a in exec_report.artifacts if a.artifact_type == "sld"]
    if sld_artifacts:
        sld_path = Path(sld_artifacts[0].path)
        if sld_path.exists():
            size = sld_path.stat().st_size
            print("SLD GENERATED")
            print(f"[PASS] Diagram saved to: {sld_path} (Size: {size} bytes)")
        else:
            print("SLD FAILED (File not found after execution)")
    else:
        print("SLD FAILED (No SLD artifact in execution report)")

    print("\nDone.")

if __name__ == "__main__":
    main()
