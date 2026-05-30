import os
import sys
import json
from pathlib import Path

# Fix PSSE Path for Python 3.8+ DLL loading
os.environ["PATH"] = r"C:\Program Files\PTI\PSSE36\36.0\PSSBIN;" + os.environ.get("PATH", "")
sys.path.append(r"C:\Program Files\PTI\PSSE36\36.0\PSSPY311")
sys.path.append(r"C:\Program Files\PTI\PSSE36\36.0\PSSBIN")
try:
    os.add_dll_directory(r"C:\Program Files\PTI\PSSE36\36.0\PSSBIN")
except AttributeError:
    pass

import psspy
import sliderPy

def introspect_diagram(diagram):
    output = {
        "diagram_component_count": 0,
        "bus_symbol_count": 0,
        "branch_symbol_count": 0,
        "coordinates": []
    }
    
    if not diagram:
        return output
        
    components = diagram.GetComponents()
    output["diagram_component_count"] = len(components)
    
    # Try layers as fallback
    if len(components) == 0:
        for layer in diagram.GetLayers():
            if hasattr(layer, "GetComponents"):
                l_comps = layer.GetComponents()
                if l_comps:
                    components.extend(l_comps)
                    output["diagram_component_count"] += len(l_comps)
    
    for c in components:
        try:
            if c.GetSymbolType() == sliderPy.SymbolType.Node:
                output["bus_symbol_count"] += 1
                pos = c.GetPosition()
                output["coordinates"].append({"type": "bus", "id": c.GetMapString(), "x": pos[0], "y": pos[1]})
            elif c.GetSymbolType() == sliderPy.SymbolType.Link:
                output["branch_symbol_count"] += 1
                output["coordinates"].append({"type": "branch", "id": c.GetMapString()})
        except Exception:
            pass
            
    return output

def run_experiment():
    print("==================================================")
    print("EXPERIMENT 2.2: sliderPy Proof-of-Life (CreateLayer + MapComponent)")
    print("==================================================")
    
    psspy.psseinit(150000)
    psspy.newcase_2([1, 1], 100.0, 60.0, "Proof of Life", "Test")
    psspy.bus_data_4(101, 0, [1, 1, 1, 1], [33.0, 1.0, 0.0, 1.1, 0.9, 1.1, 0.9], "BUS101")
    
    psspy.newdiagfile()
    
    doc = sliderPy.GetActiveDocument()
    diagram = doc.GetDiagram()
    
    # Check existing layers
    layers = diagram.GetLayers()
    if not layers:
        print("No layers found. Creating layer...")
        layer = diagram.CreateLayer()
        try:
            layer.SetName("Default")
        except:
            pass
        layer_name = layer.GetName() if hasattr(layer, 'GetName') else "Default"
    else:
        layer_name = layers[0].GetName()
    
    # Create ONE bus symbol
    sym = diagram.CreateSymbol(sliderPy.SymbolType.Node)
    
    # Map it using the diagram method instead of sym method
    try:
        diagram.MapComponent(sym.GetID(), "101")
    except Exception as e:
        print(f"diagram.MapComponent failed: {e}")
        sym.SetMapString("101")
        
    sym.SetPosition(50.0, 50.0)
    
    try:
        diagram.AssignComponentToLayer(sym, 0)
    except Exception as e:
        print(f"AssignComponentToLayer failed: {e}")
            
    try:
        sym.SetVisible(True)
        sym.Update()
        diagram.UpdateAllComponents()
        diagram.UpdateExtent()
    except Exception as e:
        print(f"Update failed: {e}")
    
    out_sld = Path("outputs/runs/stage4/exp2_proof.sld").absolute()
    psspy.savediagfile(str(out_sld))
    
    intro = introspect_diagram(diagram)
    print("\n[INTROSPECTION]")
    print(json.dumps(intro, indent=2))

if __name__ == "__main__":
    run_experiment()
