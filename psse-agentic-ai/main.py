import argparse
import sys
import os
import json
from pathlib import Path

# MINIMAL FIX for Python 3.8+ DLL resolution in Windows for real PSSE36
os.environ["PATH"] = r"C:\Program Files\PTI\PSSE36\36.0\PSSBIN;" + os.environ.get("PATH", "")
sys.path.append(r"C:\Program Files\PTI\PSSE36\36.0\PSSPY311")
sys.path.append(r"C:\Program Files\PTI\PSSE36\36.0\PSSBIN")
try:
    os.add_dll_directory(r"C:\Program Files\PTI\PSSE36\36.0\PSSBIN")
except AttributeError:
    pass  # Pre-3.8 or non-Windows

from app.ingestion.excel_parser import load_workbook
from app.ingestion.validator import IngestionValidator
from app.ingestion.normalizer import generate_topology_ir
from app.validation.validator import validate_topology
from app.psse.executor import execute_in_psse

def fail_loud(title: str, messages: list):
    print(f"\n{title}\n")
    for msg in messages:
        print(msg)
    sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Deterministic Excel Ingestion for PSSE Agentic AI")
    parser.add_argument("workbook", help="Path to the engineering workbook (.xlsx or .csv)")
    parser.add_argument("--output", help="Base name for output files (e.g. deoli_test1)", default="case")
    args = parser.parse_args()

    print("================================================")
    print("PSSE36 ENGINEERING AUTOMATION")
    print("================================================\n")

    # [1/6] Loading workbook
    print("[1/6] Loading workbook")
    try:
        rows = load_workbook(args.workbook)
        print("SUCCESS\n")
    except Exception as e:
        fail_loud("WORKBOOK LOAD FAILED", [str(e)])

    # [2/6] Workbook validation
    print("[2/6] Workbook validation")
    validator = IngestionValidator()
    is_valid, clean_rows = validator.validate(rows)
    
    if not is_valid:
        # validator.validate() already prints the structured error
        sys.exit(1)
    print("SUCCESS\n")
        
    # [3/6] TopologyIR generation
    print("[3/6] TopologyIR generation")
    try:
        ir = generate_topology_ir(clean_rows)
        print("SUCCESS\n")
    except Exception as e:
        fail_loud("TOPOLOGY IR GENERATION FAILED", [str(e)])
        
    # [4/6] Topology validation
    print("[4/6] Topology validation")
    topology_report = validate_topology(ir)
    if not topology_report.is_valid:
        errors = [issue.code for issue in topology_report.issues if issue.severity == "error"]
        fail_loud("TOPOLOGY VALIDATION FAILED", errors)
    print("SUCCESS\n")
    
    # [5/6] PSSE execution
    print("[5/6] PSSE execution")
    output_dir = "outputs/runs/latest"
    exec_report = execute_in_psse(ir, output_dir=output_dir, output_filename=args.output)
    
    if not exec_report.success:
        fail_loud("EXECUTION FAILED", exec_report.errors)
        
    if not exec_report.load_flow_converged:
        fail_loud("PSSE EXECUTION FAILED", [
            "Load flow did not converge.",
            "Artifacts may exist but electrical state is invalid."
        ])
    print("SUCCESS\n")
    
    # [6/6] Artifact reporting
    print("Load Flow:")
    print("CONVERGED\n")
    
    print("Artifacts Generated:")
    for artifact in exec_report.artifacts:
        # Ensure cross-platform clean paths
        clean_path = str(Path(artifact.path).as_posix())
        print(clean_path)
        
    print("\n# Execution Complete")

if __name__ == "__main__":
    main()
