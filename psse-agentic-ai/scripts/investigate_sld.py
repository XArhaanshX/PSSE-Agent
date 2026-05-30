import os
import sys

# Minimal DLL fix
try:
    os.add_dll_directory(r"C:\Program Files\PTI\PSSE36\36.0\PSSBIN")
except AttributeError:
    pass

import psspy

def investigate():
    psspy.psseinit(12000)
    funcs = dir(psspy)
    
    # Hypothesis 1 & 4 keywords
    keywords = ['diag', 'view', 'zoom', 'fit', 'refresh', 'redraw', 'scale', 'center']
    
    found = set()
    for f in funcs:
        f_lower = f.lower()
        for k in keywords:
            if k in f_lower:
                found.add(f)
                
    print("Found Diagram / Viewport APIs in psspy:")
    for f in sorted(list(found)):
        print(f" - {f}")

if __name__ == "__main__":
    investigate()
