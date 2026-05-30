# Diagram API Investigation Notes

This document contains empirical findings from interrogating the `psspy` namespace and `sliderPy` library for diagram and SLD generation capabilities.

## The Engineering Lesson
**"Experimental proof overrides theoretical assumptions."**
Theoretical analysis suggested that `sliderPy` was the appropriate interface for programmatic diagram modification. However, rigorous headless testing proved this false. Only empirical validation of native APIs revealed the working path.

## Discovered APIs

### 1. `newdiagfile` & `savediagfile`
1. **Signatures:** `psspy.newdiagfile()`, `psspy.savediagfile(filename)`
2. **Observed behavior:** Successfully initializes a new diagram canvas in memory and persists a proprietary binary `.sld` file to disk.
3. **Failure modes:** None observed in headless mode.
4. **Confidence level:** HIGH

### 2. `sliderPy.SldDiagram.CreateSymbol` (FAILED)
1. **Minimal experiment:** Invoked `CreateSymbol` to place bus nodes on the diagram canvas headlessly.
2. **Observed behavior:** Programmatic inspection showed `diagram_component_count == 0` after placement. The API failed to serialize the geometry, resulting in blank 2539-byte shell SLDs.
3. **Failure modes:** The C++ `CPyWrapperDiagram` swallows the objects in a pure headless process without throwing exceptions, but never commits them to the document.
4. **Conclusion:** DEPRECATED for headless MVP.

### 3. `growdiagram_2` (DEFERRED)
1. **Signature:** `psspy.growdiagram_2(numlevels, itemcount, itemlist, xposition, yposition, excludelist)`
2. **Observed behavior:** A bulk auto-router that relies heavily on GUI map-services (`mapservice.xml`). When executed in our headless mode, it produced non-visible/blank results.
3. **Conclusion:** DEFERRED. It remains a "Future Enhancement Candidate" for post-MVP layout-quality investigation (readability improvements and heuristic layout experimentation).

### 4. `growbus` (CANONICAL)
1. **Signature:** `psspy.growbus(busnumber, xposition, yposition)`
2. **Minimal experiment (Experiment 4.28A):** Loaded a solved `.sav` network case, initialized a new diagram, called `growbus` with explicit (x, y) coordinates for 5 buses, and saved.
3. **Observed behavior:** Successfully generated visible geometry. The binary `.sld` file jumped from a 2.5KB blank shell to 15KB, and internal logs printed "Grow Complete".
4. **Limitations:** Requires the electrical network case to exist in memory BEFORE calling. It strictly places buses at explicit coordinates.
5. **Confidence level:** HIGH

## Mandatory Conclusion: API Classification

Based strictly on experimental evidence, we classify the PSSE36 diagram capabilities as follows:

**Scenario A (MVP Deterministic Placement)**
- `psspy.newdiagfile()`
- `psspy.bsys()`
- `psspy.growbus()` / `psspy.growbuslevels()`
- `psspy.savediagfile()`

**Scenario B (Future Heuristic Enhancement)**
- `psspy.growdiagram_2()`

For the P4 MVP milestone (Basic SLD Generation), `growbus()` is established as the canonical deterministic placement primitive, fed by a decoupled layout coordinate computation engine.
