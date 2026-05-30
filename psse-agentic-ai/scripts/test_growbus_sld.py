import os
import sys
import json
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
try:
    import sliderPy
except ImportError:
    sliderPy = None

def introspect_diagram(diagram):
    """Programmatic Diagram Introspection"""
    output = {
        "diagram_component_count": 0,
        "bus_symbol_count": 0,
        "coordinates": []
    }
    
    if not diagram or sliderPy is None:
        return output
        
    components = diagram.GetComponents()
    
    # Fallback to layers if components empty
    if len(components) == 0:
        for layer in diagram.GetLayers():
            if hasattr(layer, "GetComponents"):
                l_comps = layer.GetComponents()
                if l_comps:
                    components.extend(l_comps)
                    
    output["diagram_component_count"] = len(components)
    
    for c in components:
        try:
            if c.GetSymbolType() == sliderPy.SymbolType.Node:
                output["bus_symbol_count"] += 1
                pos = c.GetPosition()
                output["coordinates"].append({"id": c.GetMapString(), "x": pos[0], "y": pos[1]})
        except Exception:
            pass
            
    return output

def run_experiment():
    print("==================================================")
    print("EXPERIMENT 4.28A — growbus() Proof of Visible Geometry")
    print("==================================================")
    
    psspy.psseinit(150000)
    
    # 1. Load EXISTING VALID CASE
    sav_path = Path("outputs/runs/stage4/stage4_case.sav").absolute()
    print(f"Loading case: {sav_path}")
    ierr_case = psspy.case(str(sav_path))
    
    # 2. Create fresh diagram
    ierr_newdiag = psspy.newdiagfile()
    print("Created fresh diagram")
    
    # 3. Place buses using growbus()
    buses = [33001, 33002, 33003, 33004, 33005]
    coordinates = []
    
    # Bsys to define subsystem containing these buses
    ierr_bsys = psspy.bsys(1, 0, [0.0, 0.0], 0, [], len(buses), buses, 0, [], 0, [])
    
    x_pos = 0.0
    growbus_ierrs = []
    for bus_num in buses:
        y_pos = 0.0
        ierr_grow = psspy.growbus(bus_num, x_pos, y_pos)
        growbus_ierrs.append(ierr_grow)
        coordinates.append((bus_num, x_pos, y_pos))
        x_pos += 2.0
    
    # 4. Save Diagram
    out_sld = Path("outputs/runs/stage4/growbus_test.sld").absolute()
    ierr_save = psspy.savediagfile(str(out_sld))
    print("Saved diagram")
    
    # 5. Programmatic Verification
    if sliderPy is not None:
        try:
            doc = sliderPy.GetActiveDocument()
            diagram = doc.GetDiagram()
            intro = introspect_diagram(diagram)
        except Exception as e:
            intro = {"error": f"Introspection failed: {e}"}
    else:
        intro = {"error": "sliderPy unavailable for introspection."}
        
    print("\n[IERVALS]")
    print(f"case: {ierr_case}")
    print(f"newdiagfile: {ierr_newdiag}")
    print(f"bsys: {ierr_bsys}")
    print(f"growbus: {growbus_ierrs}")
    print(f"savediagfile: {ierr_save}")
    
    print("\n[INTROSPECTION]")
    print(json.dumps(intro, indent=2))
    
    print("\n[OUTCOMES]")
    print(f"SLD created: {out_sld.exists()}")
    print(f"SLD file size: {out_sld.stat().st_size if out_sld.exists() else 0} bytes")
    
    print("\n[HUMAN CONFIRMATION CHECKLIST]")
    print("1. Open PSSE normally")
    print(f"2. Open generated .sav: {sav_path}")
    print(f"3. Open SLD: {out_sld}")
    print("4. Check: Are buses visible? Are bus labels visible? Is radial chain visible?")

if __name__ == "__main__":
    run_experiment()
