import os
import sys

# Setup paths for PSSE36
os.environ["PATH"] = r"C:\Program Files\PTI\PSSE36\36.0\PSSBIN;" + os.environ.get("PATH", "")
sys.path.append(r"C:\Program Files\PTI\PSSE36\36.0\PSSPY311")
sys.path.append(r"C:\Program Files\PTI\PSSE36\36.0\PSSBIN")

try:
    os.add_dll_directory(r"C:\Program Files\PTI\PSSE36\36.0\PSSBIN")
except AttributeError:
    pass

import psspy
import sliderPy

def test_sliderpy():
    psspy.psseinit(150000)
    
    # Try to get active document
    try:
        doc = sliderPy.GetActiveDocument()
        print("Active doc:", doc)
    except Exception as e:
        print("Failed to get active doc:", e)

    # Try to load slider document
    try:
        doc = sliderPy.SldDocument()
        print("Created SldDocument:", doc)
    except Exception as e:
        print("Failed to create SldDocument:", e)

if __name__ == "__main__":
    test_sliderpy()
