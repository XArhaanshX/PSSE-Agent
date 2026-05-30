import os
import sys

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

def introspect():
    psspy.psseinit(150000)
    psspy.newdiagfile()
    doc = sliderPy.GetActiveDocument()
    diagram = doc.GetDiagram()
    
    print("=== DIAGRAM METHODS ===")
    for m in dir(diagram):
        if not m.startswith('__'):
            print(m)
            
    sym = diagram.CreateSymbol(sliderPy.SymbolType.Node)
    print("\n=== SYMBOL METHODS ===")
    for m in dir(sym):
        if not m.startswith('__'):
            print(m)

if __name__ == "__main__":
    introspect()
