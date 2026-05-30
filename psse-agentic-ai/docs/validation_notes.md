# Validation Notes (Stage 7)

## 1. Topology-Aware Validation Semantics
As the complexity of deterministic templates grows, applying universal monolithic graph rules causes false positives (e.g., treating every topology as if it must be perfectly radial, or failing on hierarchical yards). The validation architecture uses a centralized canonical entry point (`validate_topology`) that dispatches to specific rules based on `topology_type`.

We explicitly avoid dynamic plugin registries, heuristic rule engines, and generic validation. The following explicit semantic checks are implemented:
- `validate_radial()`: connected, tree, single swing, no isolated buses.
- `validate_single_bus()`: connected, tree, single swing.
- `validate_double_bus()`: connected, tree, single swing.
- `validate_substation_feeder()`: connected, tree, single swing.
- `validate_transformer_substation()`: connected, tree, single swing.

*(Future updates can inject specific checks like `check_has_bus_coupler` into `validate_double_bus` without breaking other templates).*

## 2. Structural Requirements
- **Transformers vs Branches:** The `build_graph` module was expanded to include `transformers` as edges in the internal NetworkX graph. This ensures hierarchical trees (which use step-down transformers instead of AC branches) do not incorrectly trigger `GRAPH_DISCONNECTED` errors.
- **Swing Bus:** PSSE requires exactly one slack (swing) bus to converge. Our deterministic templates enforce exactly one swing bus (usually the POI or HV_MAIN) and mark subsequent yard/main buses as loads.

## 3. Scope Guardrails
No speculative electrical engineering constraints will be invented. Validation rules MUST be justified by:
1. PRD requirements
2. API.pdf behavior
3. Graph mathematical logic (connected, tree-like)
We do NOT support "non-radial subgraphs" or mesh-level heuristics, keeping the project safely inside the POC mandate.
