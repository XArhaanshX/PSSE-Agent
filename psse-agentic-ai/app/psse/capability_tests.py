import os
from app.psse.session import check_psspy_import, create_case, initialize_psse
from app.psse.creators import create_bus, create_branch, create_transformer, create_load, create_plant, create_machine
from app.psse.error_handling import validate_ierr

OUTPUT_DIR = "outputs/runs/stage0"

def _ensure_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def _save_case(name: str):
    psspy = check_psspy_import()
    sav_path = os.path.join(OUTPUT_DIR, f"{name}.sav")
    raw_path = os.path.join(OUTPUT_DIR, f"{name}.raw")
    
    ierr = psspy.save(sav_path)
    validate_ierr(ierr, "save", {"sfile": sav_path})
    
    ierr = psspy.rawd_2(0, 1, [1, 1, 1, 0, 0, 0, 0], 0, raw_path)
    validate_ierr(ierr, "rawd_2", {"ofile": raw_path})
    
    print(f"[{name}] Case saved to {sav_path} and {raw_path}")

def test_transformer_case():
    print("Running transformer capability test...")
    _ensure_dir()
    initialize_psse()
    create_case()
    
    create_bus(101, "BUS_101", 33.0)
    create_bus(102, "BUS_102", 11.0)
    create_transformer(101, 102, "TX_1")
    
    _save_case("transformer_test")

def test_load_case():
    print("Running load capability test...")
    _ensure_dir()
    initialize_psse()
    create_case()
    
    create_bus(102, "BUS_102", 11.0)
    create_load(102, 5.0, 2.0)
    
    _save_case("load_test")

def test_machine_case():
    print("Running machine capability test...")
    _ensure_dir()
    initialize_psse()
    create_case()
    
    create_bus(101, "BUS_101", 33.0, bus_type=2)
    create_plant(101)
    create_machine(101, 15.0)
    
    _save_case("machine_test")

def test_error_handling_case():
    print("Running error handling capability test...")
    _ensure_dir()
    initialize_psse()
    create_case()
    
    # Intentionally trigger an error by creating a branch to a non-existent bus
    create_bus(101, "BUS_101", 33.0)
    try:
        create_branch(101, 999) # 999 doesn't exist
    except Exception as e:
        print(f"Exception successfully caught: {e}")
        return
        
    raise RuntimeError("Error handling failed to raise an exception!")
