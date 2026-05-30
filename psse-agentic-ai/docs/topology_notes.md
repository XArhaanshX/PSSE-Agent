# Topology Expansion Notes (Stage 7)

## 1. Supported MVP Topologies
As strictly defined by the `PRD_PSSE36_AGENTIC_AI.pdf` POC scope bounds, only the following deterministic topologies are approved for MVP:
1. `radial`: A linear string of buses.
2. `single_bus`: One main bus (swing) with `N` feeders hanging off it.
3. `double_bus`: Two main buses connected by a bus tie, with feeders distributed between them.
4. `substation_feeder`: Hierarchical deterministic template representing `POI -> Yard -> Main Bus -> Feeders`.
5. `transformer_substation`: Hierarchical deterministic template representing `HV_BUS -> Transformers -> LV_BUS -> Loads`.

## 2. Hierarchical Topology Philosophy
Real substations have a natural hierarchy: voltage level → bus arrangement → bay → equipment chain. The SLD layout must reflect this hierarchy visually. By expanding our templates to include POI, Yards, and Transformer drops, we accurately model PSSE power flows without violating deterministic constraints.

## 3. Engineering Doctrine
The implementation follows the strict hierarchy: **PRD → API.pdf → experiment**.
- The PRD mandated boring, deterministic graph topologies (no stochastic builders).
- `app/topology/templates.py` builds explicit graphs without any PSSE dependencies.
- No `psspy` imports exist in the topology layer.

## 4. What Remains OUT OF SCOPE
- Arbitrary graph synthesis or generic graph CAD engines.
- Graph auto-discovery and topology inference.
- Dynamic graph construction or abstract topology registries.
- Stochastic layout engines (force-directed routing).
- Complex custom topologies like `ring_bus`, `breaker_and_half`, and `mesh`.
We are building EXPLICIT, DETERMINISTIC, and HARDCODED templates. No topology generalization is permitted.
