"""PSSE session module."""
import sys

def check_psspy_import():
    if sys.version_info.major != 3 or sys.version_info.minor != 11:
        print("\nError: PSSE36 on this system requires Python 3.11.")
        print(f"You are running Python {sys.version_info.major}.{sys.version_info.minor}")
        print("Please run this script using Python 3.11.\n")
        sys.exit(1)

    import os
    # Auto-inject PSSE paths for Windows
    psspy_path = r"C:\Program Files\PTI\PSSE36\36.0\PSSPY311"
    pssbin_path = r"C:\Program Files\PTI\PSSE36\36.0\PSSBIN"
    
    if os.path.exists(psspy_path) and psspy_path not in sys.path:
        sys.path.insert(0, psspy_path)
    if os.path.exists(pssbin_path):
        os.environ['PATH'] = pssbin_path + ';' + os.environ.get('PATH', '')
        # Required for Python 3.8+ to load DLLs
        try:
            os.add_dll_directory(pssbin_path)
        except AttributeError:
            pass

    try:
        import psspy
        return psspy
    except ImportError as e:
        print(f"\nCould not import psspy. Error: {e}")
        print("\nPossible causes:")
        print("* PSSE36 not installed correctly")
        print("* PSSE environment not initialized\n")
        sys.exit(1)

def initialize_psse():
    psspy = check_psspy_import()
    ierr = psspy.psseinit(12000)
    if ierr != 0:
        raise Exception(f"psseinit failed with code {ierr}")

def create_case():
    psspy = check_psspy_import()
    ierr = psspy.newcase_2([0, 1], 100.0, 60.0, "", "")
    if ierr != 0:
        raise Exception(f"newcase_2 failed with code {ierr}")
