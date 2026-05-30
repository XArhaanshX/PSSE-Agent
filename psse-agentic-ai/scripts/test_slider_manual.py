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

def build_test_diagram():
    psspy.psseinit(150000)
    
    # Needs a working case in memory to bind? Let's create a minimal case.
    psspy.newcase_2([0,1], 100.0, 60.0, "", "")
    psspy.bus_data_3(1, [1,1,1,1], [132.0,1.0,0.0,1.1,0.9,1.1,0.9], 'BUS_1')
    psspy.bus_data_3(2, [1,1,1,1], [132.0,1.0,0.0,1.1,0.9,1.1,0.9], 'BUS_2')

    psspy.newdiagfile()
    
    doc = sliderPy.GetActiveDocument()
    diagram = doc.GetDiagram()
    
    # Create Bus 1
    sym1 = diagram.CreateSymbol(sliderPy.SymbolType.Node)
    sym1.SetMapString("1")
    sym1.SetPosition(10.0, 10.0)
    
    # Create Bus 2
    sym2 = diagram.CreateSymbol(sliderPy.SymbolType.Node)
    sym2.SetMapString("2")
    sym2.SetPosition(20.0, 10.0)

    # Save via psspy
    out_file = os.path.abspath("test_slider_manual.sld")
    psspy.savediagfile(out_file)
    print(f"Saved {out_file}, size: {os.path.getsize(out_file)}")

if __name__ == "__main__":
    build_test_diagram()
