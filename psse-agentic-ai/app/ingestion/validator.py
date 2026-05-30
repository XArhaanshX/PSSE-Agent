import json
from typing import List, Dict, Any, Tuple

class ValidationError:
    def __init__(self, component_type: str, component_id: str, field: str, reason: str):
        self.component_type = component_type
        self.component_id = component_id
        self.field = field
        self.reason = reason

    def __str__(self):
        return f"[{self.component_type.capitalize()} {self.component_id}] {self.reason}: {self.field}"
        
    def to_dict(self):
        return {
            "component_type": self.component_type,
            "component_id": self.component_id,
            "field": self.field,
            "reason": self.reason
        }

class IngestionValidator:
    def __init__(self):
        self.errors: List[ValidationError] = []
        self.bus_ids = set()
        self.component_ids = set()

    def add_error(self, row: Dict[str, Any], field: str, reason: str):
        c_type = row.get("component_type", "Unknown")
        c_id = row.get("component_id", "Unknown")
        # Fallbacks if component_id is not provided but from_bus is
        if c_id == "Unknown" and row.get("from_bus") is not None:
            c_id = f"Bus_{row.get('from_bus')}"
        self.errors.append(ValidationError(c_type, c_id, field, reason))

    def validate(self, rows: List[Dict[str, Any]]) -> Tuple[bool, List[Dict[str, Any]]]:
        """
        Executes the 6-step deterministic validation pipeline.
        Returns (is_valid, rows).
        """
        self.errors.clear()
        self.bus_ids.clear()
        self.component_ids.clear()

        # STEP 1: Schema Validation (Global required columns)
        for row in rows:
            for field in ["component_type", "component_id", "status"]:
                if field not in row:
                    self.add_error(row, field, "Missing required global column in schema")
            
            if row.get("component_type") is None:
                self.add_error(row, "component_type", "Value cannot be null")

        if self.errors:
            self._report_failures()
            return False, rows

        # STEP 2: Discovery Pass (Order-Independent)
        for row in rows:
            c_type = str(row.get("component_type", "")).lower()
            c_id = str(row.get("component_id", ""))
            
            if c_id:
                if c_id in self.component_ids:
                    self.add_error(row, "component_id", "Duplicate component ID")
                self.component_ids.add(c_id)
                
            if c_type == "bus":
                bus_id = row.get("from_bus")
                if bus_id is not None:
                    if bus_id in self.bus_ids:
                        self.add_error(row, "from_bus", "Duplicate bus definition")
                    self.bus_ids.add(bus_id)

        # STEP 3 & 5: Component-Specific Validation & Row-Level Sanity
        for row in rows:
            c_type = str(row.get("component_type", "")).lower()
            
            # Conditionally required fields
            required_fields = []
            if c_type == "bus":
                required_fields = ["from_bus", "base_kv"]
            elif c_type == "branch":
                required_fields = ["from_bus", "to_bus", "r_pu", "x_pu"]
            elif c_type == "transformer":
                required_fields = ["from_bus", "to_bus", "mva"]
            elif c_type == "load":
                required_fields = ["from_bus", "p_mw"]
            elif c_type == "generator":
                required_fields = ["from_bus", "mva"]
            else:
                self.add_error(row, "component_type", f"Invalid component_type: {c_type}")
                continue
                
            for field in required_fields:
                if row.get(field) is None:
                    self.add_error(row, field, "Missing required field")

            # Row-level Sanity: Negative electrical values
            for field in ["base_kv", "mva", "x_pu"]:
                val = row.get(field)
                if val is not None and isinstance(val, (int, float)) and val < 0:
                    self.add_error(row, field, f"Invalid value (must be >= 0): {val}")
                    
            # Row-level Sanity: Status normalization sanity
            status = row.get("status")
            if status is not None and status not in [1, 0, 1.0, 0.0, True, False, "1", "0"]:
                self.add_error(row, "status", f"Invalid status value (must be 1/0): {status}")

        # STEP 4: Reference Integrity Validation (Order-Independent)
        for row in rows:
            c_type = str(row.get("component_type", "")).lower()
            if c_type != "bus":
                for ref_field in ["from_bus", "to_bus"]:
                    ref_val = row.get(ref_field)
                    if ref_val is not None:
                        if ref_val not in self.bus_ids:
                            self.add_error(row, ref_field, f"Unknown bus reference ({ref_val})")

        # STEP 6: Human-Readable Validation Reporting
        if self.errors:
            self._report_failures()
            return False, rows
            
        # STEP 7: Return Validated Rows
        return True, rows

    def _report_failures(self):
        print("\n========================================")
        print("VALIDATION FAILED")
        print("========================================\n")
        
        for err in self.errors:
            print(f"[{err.component_type.capitalize()} {err.component_id}]")
            print(f"{err.reason}:")
            print(f"{err.field}\n")
            
        report = {
            "status": "failed",
            "errors": [err.to_dict() for err in self.errors]
        }
        
        with open("validation_report.json", "w", encoding="utf-8") as f:
            json.dump(report, f, indent=4)
        
        print("Detailed error report written to validation_report.json")
