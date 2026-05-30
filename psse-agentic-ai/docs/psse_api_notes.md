# PSSE API Investigation Notes

This document contains empirical findings from P0 capability experiments. It strictly documents tested realities, quirks, and required array structures for the `psspy` API to serve as a foundation for future Intermediate Representation (IR) design.

## 1. `bus_data_4`
1. **Working signature:** `ierr = psspy.bus_data_4(ibus, intgar, realar, name)`
2. **Minimal working example:** `psspy.bus_data_4(101, 0, [1, 1, 1, 1], [33.0, 1.0, 0.0, 1.1, 0.9, 1.1, 0.9], "BUS_101")`
3. **Required positional arrays:** `intgar` (4 elements), `realar` (7 elements). 
4. **Exact parameter pattern used:** `intgar=[IDE, 1, 1, 1]` (IDE=1 for load, 2 for generator, 3 for swing). `realar=[BASKV, 1.0, 0.0, 1.1, 0.9, 1.1, 0.9]`.
5. **Observed quirks:** Modifying the bus type (IDE) via `intgar[0]` is critical if you intend to later add a generator.
6. **Return code behavior:** `0` on success. `>0` on fatal error (e.g. invalid arguments).
7. **Failing result(s):** Passing incorrect array sizes results in immediate Python argument exceptions rather than PSSE `ierr` values.
8. **Human-readable failure interpretation:** "Invalid parameter type or missing required positional list length."
9. **Confidence level:** HIGH
10. **Recommendation for future IR assumptions:** The IR must explicitly capture the bus type (Load, Generator, Swing) so the Executor can correctly populate `intgar[0]`.

## 2. `branch_data_3`
1. **Working signature:** `ierr = psspy.branch_data_3(ibus, jbus, ckt, intgar, realar, ratings, name)`
2. **Minimal working example:** `psspy.branch_data_3(101, 102, '1', [1, 101, 1, 0, 0, 0], [0.01, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0], [0.0]*12, "")`
3. **Required positional arrays:** `intgar` (6 elements), `realar` (12 elements), `ratings` (12 elements).
4. **Exact parameter pattern used:** Hardcoded defaults padding the R and X values in `realar[0]` and `realar[1]`.
5. **Observed quirks:** The `ckt` identifier must be passed as a string (e.g., `'1'`), not an integer.
6. **Return code behavior:** `0` on success. `1` if bus is not found.
7. **Failing result(s):** `ierr = 1`
8. **Human-readable failure interpretation:** "FATAL: Bus 999 not found" — Occurs when the `to_bus` or `from_bus` has not been initialized via `bus_data_4`.
9. **Confidence level:** HIGH
10. **Recommendation for future IR assumptions:** The Topology planner must guarantee that buses exist prior to generating branch edges in the IR sequence.

## 3. `two_winding_data_6`
1. **Working signature:** `result = psspy.two_winding_data_6(ibus, jbus, ckt, intgar, realari, ratings, namear, vgrpar)`
2. **Minimal working example:** `psspy.two_winding_data_6(101, 102, '1', [1, 101, 101, 0, 0, 0, 33, 0, 101, 0, 0, 1, 0, 1, 1, 1], [0.01, 0.1, 100.0, 1.0, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 1.1, 0.9, 1.1, 0.9, 0.0, 0.0, 0.0], [0.0]*12, "TX_1", "")`
3. **Required positional arrays:** `intgar` (16 elements), `realari` (21 elements), `ratings` (12 elements).
4. **Exact parameter pattern used:** Full array padding. `R1-2` and `X1-2` map to `realari[0]` and `realari[1]`.
5. **Observed quirks:** In Python, this wrapper returns a tuple `(ierr, realaro)` instead of just `ierr`. We must extract `ierr = result[0]` to perform failure validation correctly.
6. **Return code behavior:** `0` on success.
7. **Failing result(s):** Tuple indexing errors if `ierr` is naively assumed to be an integer return.
8. **Human-readable failure interpretation:** Requires extracting `[0]` to process the integer return code.
9. **Confidence level:** HIGH
10. **Recommendation for future IR assumptions:** The IR must encode transformer Resistance (R), Reactance (X), and Winding Base MVA properties directly, as these are mandatory elements of the 21-element `realari` array.

## 4. `load_data_6`
1. **Working signature:** `ierr = psspy.load_data_6(ibus, id, intgar, realar, name)`
2. **Minimal working example:** `psspy.load_data_6(102, '1', [1, 1, 1, 1, 1, 0, 0], [5.0, 2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], "")`
3. **Required positional arrays:** `intgar` (7 elements), `realar` (8 elements).
4. **Exact parameter pattern used:** Active power (P) and Reactive power (Q) placed at `realar[0]` and `realar[1]`.
5. **Observed quirks:** Unlike older versions, `load_data_6` requires the 8-element real array.
6. **Return code behavior:** `0` on success.
7. **Failing result(s):** Failing to pre-create the bus results in `ierr=1`.
8. **Human-readable failure interpretation:** "Bus not found."
9. **Confidence level:** HIGH
10. **Recommendation for future IR assumptions:** The IR must map Load constraints clearly into P and Q elements, differentiating them from current or admittance load properties within the array.

## 5. `plant_data_4` and `machine_data_4`
1. **Working signature:** 
   - `ierr = psspy.plant_data_4(ibus, inode, intgar, realar)`
   - `ierr = psspy.machine_data_4(ibus, id, intgar, realar, name)`
2. **Minimal working example:** 
   - `psspy.plant_data_4(101, 0, [0, 0], [1.0, 100.0])`
   - `psspy.machine_data_4(101, '1', [1, 1, 0, 0, 0, 0, 0], [15.0, 0.0, 9999.0, -9999.0, 9999.0, -9999.0, 100.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0], "")`
3. **Required positional arrays:** Machine requires `intgar` (7) and `realar` (17). Plant requires `intgar` (2) and `realar` (2).
4. **Exact parameter pattern used:** P_mw is passed as `realar[0]` to the machine data call.
5. **Observed quirks:** `machine_data_4` will fatally fail if `plant_data_4` has not been called on the bus first. Setting `IDE=2` on the bus is necessary but not sufficient; the plant data object must explicitly exist. Additionally, `plant_data_4` will return `ierr=-1` (warning) if `IREG` and `INODE` are improperly configured; using `[0, 0]` cleanly regulates the host bus.
6. **Return code behavior:** `0` on success, `-1` on warning, `3` on fatal error (No plant data).
7. **Failing result(s):** `ierr = 3` (when skipping `plant_data_4`), `ierr = -1` (when using `[0, 1]` in plant).
8. **Human-readable failure interpretation:** "FATAL: No plant data at this bus" — the user must explicitly construct the plant before creating a generator.
9. **Confidence level:** HIGH
10. **Recommendation for future IR assumptions:** The IR to PSSE Executor mapping *must* inject a `create_plant` event into the sequence immediately before executing a `create_machine` event for any generator node.

## 6. `save`, `rawd_2`, `fnsl`, `fdns`
1. **Working signatures:** 
   - `psspy.save(filename)`
   - `psspy.rawd_2(0, 1, [1,1,1,0,0,0,0], 0, filename)`
   - `psspy.fnsl([1,0,0,1,1,0,0,0])`
2. **Minimal working example:** Used extensively in the frozen Stage 0 baseline.
3. **Required positional arrays:** `rawd_2` requires a 7-element intgar for export toggles. `fnsl` requires an 8-element intgar array for solver toggles.
4. **Exact parameter pattern used:** Defaults mapping to flat start and standard Newton-Raphson iteration.
5. **Observed quirks:** None that cause instability. Output printing to stdout cannot easily be suppressed natively.
6. **Return code behavior:** `0` on success.
7. **Failing result(s):** `fnsl` will gracefully fail (diverge) without throwing an `ierr` if the system matrix is singular (e.g., no swing bus).
8. **Human-readable failure interpretation:** Power flow failure requires inspecting the iteration console output rather than just the `ierr` code.
9. **Confidence level:** HIGH
10. **Recommendation for future IR assumptions:** The IR validation phase must ensure that exactly one bus is designated as a swing bus (IDE=3) to prevent `fnsl` from blowing up matrix calculations.
