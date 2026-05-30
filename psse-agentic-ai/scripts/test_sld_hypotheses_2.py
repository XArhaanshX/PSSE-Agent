import os
import sys
from pathlib import Path

# Setup PSSE paths
os.environ["PATH"] = r"C:\Program Files\PTI\PSSE36\36.0\PSSBIN;" + os.environ.get("PATH", "")
sys.path.append(r"C:\Program Files\PTI\PSSE36\36.0\PSSPY311")
sys.path.append(r"C:\Program Files\PTI\PSSE36\36.0\PSSBIN")
try:
    os.add_dll_directory(r"C:\Program Files\PTI\PSSE36\36.0\PSSBIN")
except AttributeError:
    pass

import psspy
import sliderPy

def init_case():
    psspy.psseinit(150000)
    psspy.newcase_2([1, 1], 100.0, 60.0, "Test Case", "Test")
    psspy.bus_data_4(101, 0, [1, 1, 1, 1], [33.0, 1.0, 0.0, 1.1, 0.9, 1.1, 0.9], "BUS1")
    psspy.bus_data_4(102, 0, [1, 1, 1, 1], [33.0, 1.0, 0.0, 1.1, 0.9, 1.1, 0.9], "BUS2")
    psspy.branch_data_3(101, 102, '1', [1,1,1,0,0,0], [0.01, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0], [0.0]*12, "")
    psspy.fnsl([0,0,0,1,1,1,-1,0])

def run_experiment_2a():
    print("\n--- EXPERIMENT 2A: Baseline growdiagram_2 ---")
    init_case()
    ierr1 = psspy.newdiagfile()
    print(f"newdiagfile() -> ierr={ierr1}")
    ierr2 = psspy.growdiagram_2(-1, 0, [], 10.0, 10.0, [0]*13)
    print(f"growdiagram_2() -> ierr={ierr2}")
    ierr3 = psspy.savediagfile("exp2a.sld")
    print(f"savediagfile() -> ierr={ierr3}")
    print(f"File size exp2a.sld: {os.path.getsize('exp2a.sld') if os.path.exists('exp2a.sld') else 'MISSING'}")

def run_experiment_2b():
    print("\n--- EXPERIMENT 2B: refreshdiagfile after growdiagram_2 ---")
    init_case()
    ierr1 = psspy.newdiagfile()
    print(f"newdiagfile() -> ierr={ierr1}")
    ierr2 = psspy.growdiagram_2(-1, 0, [], 10.0, 10.0, [0]*13)
    print(f"growdiagram_2() -> ierr={ierr2}")
    ierr3 = psspy.refreshdiagfile()
    print(f"refreshdiagfile() -> ierr={ierr3}")
    ierr4 = psspy.savediagfile("exp2b.sld")
    print(f"savediagfile() -> ierr={ierr4}")
    print(f"File size exp2b.sld: {os.path.getsize('exp2b.sld') if os.path.exists('exp2b.sld') else 'MISSING'}")

def run_experiment_4a():
    print("\n--- EXPERIMENT 4A: sliderPy single bus visibility ---")
    init_case()
    ierr1 = psspy.newdiagfile()
    print(f"newdiagfile() -> ierr={ierr1}")
    
    doc = sliderPy.GetActiveDocument()
    diagram = doc.GetDiagram()
    
    sym = diagram.CreateSymbol(sliderPy.SymbolType.Node)
    sym.SetMapString("101")
    sym.SetPosition(50.0, 50.0)
    
    # Try updating the symbol
    try: sym.Update()
    except Exception as e: print(f"sym.Update() failed: {e}")
    
    # Try updating the document/diagram
    try: diagram.UpdateAllComponents()
    except Exception as e: print(f"diagram.UpdateAllComponents() failed: {e}")
    
    # Try refresh
    psspy.refreshdiagfile()
    
    psspy.savediagfile("exp4a.sld")
    
    # Introspection
    components = diagram.GetComponents()
    print(f"Components in sliderPy Diagram: {len(components)}")
    for i, c in enumerate(components):
        print(f"  [{i}] MapString: {c.GetMapString()}, Pos: {c.GetPosition()}")
        
    print(f"File size exp4a.sld: {os.path.getsize('exp4a.sld') if os.path.exists('exp4a.sld') else 'MISSING'}")

if __name__ == "__main__":
    run_experiment_2a()
    run_experiment_2b()
    run_experiment_4a()
