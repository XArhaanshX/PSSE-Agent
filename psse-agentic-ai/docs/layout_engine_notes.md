# Layout Engine Notes (Stage 7)

## 1. Core Philosophy
The Layout Engine acts as a pure mathematical translation layer: `TopologyIR → (X, Y) Coordinates`. It is strictly decoupled from PSSE diagram logic, importing zero `psspy` modules.

## 2. Coordinate Philosophy
For hierarchical substations, we apply deterministic depth-based placement:
- **Depth → Y Axis:** Vertical spacing correlates directly to logical topology depth (e.g., POI at `y=0`, Yard at `y=1`, Main at `y=2`, Feeders at `y=3`).
- **Siblings → X Axis:** Horizontal spacing separates peer components (e.g., feeders, transformer chains). Components are center-aligned around `x=0`.

This approach ensures "ugly but deterministic" coordinate math without relying on stochastic graph routing or complex UI layout packages.

## 3. Supported Layout Modes
For the Stage 5-7 MVPs, the Layout Engine strictly supports explicit deterministic modes:
- **`horizontal`:** Places buses left-to-right along a constant Y axis (e.g., `(0, 0), (2, 0), (4, 0)`).
- **`vertical`:** Places buses top-to-bottom along a constant X axis (e.g., `(0, 0), (0, 2), (0, 4)`).
- **`single_bus`:** Places one main bus at `(0,0)`, and aligns N feeder buses in a horizontal row below it `(X, Y)`.
- **`double_bus`:** Places two main buses at `(0,0)` and `(0, 2Y)`, placing the feeder buses horizontally in the space between them.
- **`substation_feeder`:** Maps `POI -> YARD -> MAIN` vertically, and spreads feeders horizontally at depth 3.
- **`transformer_substation`:** Maps `HV_MAIN` at depth 0, and groups `LV_BUS` and `LOAD_BUS` vertically within isolated transformer branches spaced horizontally.

## 4. Transformer-Aware Placement
Transformers act as edges connecting vertical depths. Visual coherence requires placing the connected buses (`HV_BUS` and `LV_BUS`) vertically in line so that the `growbus()` logic drops a straight transformer branch between them. Optimization of aesthetics is explicitly out of scope for the POC.
