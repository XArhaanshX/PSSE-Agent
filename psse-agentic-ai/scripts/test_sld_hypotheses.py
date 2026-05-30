import os
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.absolute()))

os.environ["PATH"] = r"C:\Program Files\PTI\PSSE36\36.0\PSSBIN;" + os.environ.get("PATH", "")

try:
    os.add_dll_directory(r"C:\Program Files\PTI\PSSE36\36.0\PSSBIN")
except AttributeError:
    pass
sys.path.append(r"C:\Program Files\PTI\PSSE36\36.0\PSSPY311")
sys.path.append(r"C:\Program Files\PTI\PSSE36\36.0\PSSBIN")

from app.topology.planner import build_radial
from app.psse.executor import execute_in_psse, get_psspy

def test_hypotheses():
    # Setup network
    ir = build_radial(bus_count=5, voltage_kv=33.0)
    # We will just use the executor since it handles initialization
    exec_report = execute_in_psse(ir, output_dir="outputs/runs/stage4_debug")
    psspy = get_psspy()
    
    out_dir = Path("outputs/runs/stage4_debug")
    out_dir.mkdir(parents=True, exist_ok=True)
    
    print("\n--- EXPERIMENT 4: seed growdiagram_2 with numlevels=-1 ---")
    try:
        psspy.newdiagfile()
        ierr4 = psspy.growdiagram_2(-1, 0, [], 0, 0, [0]*13)
        sld_path4 = out_dir / "exp4.sld"
        psspy.savediagfile(str(sld_path4.absolute()))
        print(f"numlevels -1 ierr: {ierr4}, size: {sld_path4.stat().st_size if sld_path4.exists() else 0}")
    except Exception as e:
        print(f"Exp 4 failed: {e}")

    print("\n--- EXPERIMENT 5: updatebuslocdiagfile ---")
    try:
        psspy.newdiagfile()
        psspy.growdiagram_2(1, 0, [], 0, 0, [0]*13)
        ierr5 = psspy.updatebuslocdiagfile()
        sld_path5 = out_dir / "exp5.sld"
        psspy.savediagfile(str(sld_path5.absolute()))
        print(f"updatebuslocdiagfile ierr: {ierr5}, size: {sld_path5.stat().st_size if sld_path5.exists() else 0}")
    except Exception as e:
        print(f"Exp 5 failed: {e}")
        
    print("\n--- EXPERIMENT 7: string itemlist for bus ---")
    try:
        psspy.newdiagfile()
        ierr7 = psspy.growdiagram_2(10, 1, ["33001"], 0, 0, [0]*13)
        sld_path7 = out_dir / "exp7.sld"
        psspy.savediagfile(str(sld_path7.absolute()))
        print(f"string list ierr: {ierr7}, size: {sld_path7.stat().st_size if sld_path7.exists() else 0}")
    except Exception as e:
        print(f"Exp 7 failed: {e}")

if __name__ == "__main__":
    test_hypotheses()
