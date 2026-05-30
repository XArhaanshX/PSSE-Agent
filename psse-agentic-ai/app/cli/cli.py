"""CLI entrypoint."""
from app.psse.executor import run_stage0

def run():
    print("PSSE36 Agentic AI")
    print("Running Stage 0 feasibility test...\n")
    run_stage0()

if __name__ == "__main__":
    run()
