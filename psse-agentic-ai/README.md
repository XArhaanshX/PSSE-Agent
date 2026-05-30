# PSSE36 Agentic AI

Project overview: Natural language-driven electrical CAD automation for PSSE36.

## Current Stage: Stage 0 (Environment + PSSE Feasibility Proof)
This phase is exclusively a feasibility proof that Python can reliably control PSSE36.

**Strict Scope Boundary**:
- No AI/NLP features
- No IR/Topology Planner
- No Diagram layout engine
- Hardcoded deterministic execution only.

## Execution Instructions
Ensure PSSE36 is installed and environment variables (`PATH`, `PYTHONPATH`) are configured correctly so `psspy` can be imported.
Run the feasibility test:
```bash
python main.py
```

## Expected Outputs
The script will output readable execution logs and generate the following artifacts in `outputs/runs/stage0/`:
- `test.sav`
- `test.raw`
