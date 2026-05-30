import os
import sys

os.environ["PATH"] = r"C:\Program Files\PTI\PSSE36\36.0\PSSBIN;" + os.environ.get("PATH", "")
sys.path.append(r"C:\Program Files\PTI\PSSE36\36.0\PSSPY311")
sys.path.append(r"C:\Program Files\PTI\PSSE36\36.0\PSSBIN")

try:
    os.add_dll_directory(r"C:\Program Files\PTI\PSSE36\36.0\PSSBIN")
except AttributeError:
    pass

import psspy
import sliderPy

def test_slider_psspy():
    psspy.psseinit(150000)
    psspy.newdiagfile()
    
    doc = sliderPy.GetActiveDocument()
    print("Active doc:", doc)
    
    diagram = doc.GetDiagram()
    print("Diagram:", diagram)
    
    print("Component types in diagram before:", len(diagram.GetComponents()))
    
    print("SymbolType:", dir(sliderPy.SymbolType))
    try:
        sym = diagram.CreateSymbol(sliderPy.SymbolType.Node)
        print("Created symbol:", sym)
        sym.SetMapString("33001")
        print("Symbol methods:", [m for m in dir(sym) if not m.startswith('_')])
    except Exception as e:
        print("Failed to create symbol:", e)

    # Save via psspy
    psspy.savediagfile("test_slider_psspy.sld")
    print("Saved test_slider_psspy.sld, size:", os.path.getsize("test_slider_psspy.sld"))

if __name__ == "__main__":
    test_slider_psspy()
