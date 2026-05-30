from typing import Dict, Tuple, Literal
from pydantic import BaseModel, Field
from app.ir.topology_ir import TopologyIR

class LayoutConfig(BaseModel):
    """Configuration for deterministic coordinate computation."""
    x_spacing: float = Field(default=2.0, description="Horizontal spacing multiplier")
    y_spacing: float = Field(default=2.0, description="Vertical spacing multiplier")
    orientation: Literal["horizontal", "vertical", "single_bus", "double_bus", "substation_feeder", "transformer_substation"] = Field(
        default="horizontal", 
        description="Layout direction or topology mode"
    )

class LayoutEngine:
    """
    Computes deterministic (X, Y) coordinates for TopologyIR components.
    Strictly mathematical, containing NO PSSE APIs.
    """
    def __init__(self, config: LayoutConfig = None):
        self.config = config or LayoutConfig()

    def compute_layout(self, ir: TopologyIR) -> Dict[int, Tuple[float, float]]:
        """
        Computes the layout for the given TopologyIR based on orientation.
        
        Returns:
            Dictionary mapping bus_number to (X, Y) coordinate tuples.
        """
        coordinates = {}
        
        # Sort buses by bus_number to ensure deterministic, predictable placement
        sorted_buses = sorted(ir.buses, key=lambda b: b.bus_number)
        
        x_pos = 0.0
        y_pos = 0.0
        
        if self.config.orientation in ["horizontal", "vertical"]:
            for bus in sorted_buses:
                coordinates[bus.bus_number] = (x_pos, y_pos)
                if self.config.orientation == "horizontal":
                    x_pos += self.config.x_spacing
                elif self.config.orientation == "vertical":
                    y_pos += self.config.y_spacing
                    
        elif self.config.orientation == "single_bus":
            # Main bus at (0,0), feeders spread horizontally below it
            main_bus_found = False
            feeder_idx = 0
            for bus in sorted_buses:
                if bus.bus_type == "swing" and not main_bus_found:
                    coordinates[bus.bus_number] = (0.0, 0.0)
                    main_bus_found = True
                else:
                    # Place feeder below main bus, spread horizontally
                    coordinates[bus.bus_number] = (feeder_idx * self.config.x_spacing, self.config.y_spacing)
                    feeder_idx += 1
                    
        elif self.config.orientation == "double_bus":
            # Main buses at top and bottom, feeders spread horizontally in the middle
            main_buses = [b for b in sorted_buses if "MAIN" in b.name]
            feeders = [b for b in sorted_buses if "MAIN" not in b.name]
            
            if len(main_buses) >= 1:
                coordinates[main_buses[0].bus_number] = (0.0, 0.0)
            if len(main_buses) >= 2:
                # Place second main bus below the feeders
                coordinates[main_buses[1].bus_number] = (0.0, 2 * self.config.y_spacing)
                
            feeder_idx = 0
            for bus in feeders:
                # Place feeders horizontally between the two main buses
                coordinates[bus.bus_number] = (feeder_idx * self.config.x_spacing, self.config.y_spacing)
                feeder_idx += 1
                
        elif self.config.orientation == "substation_feeder":
            # POI at depth 0, Yard at depth 1, Main at depth 2, Feeders at depth 3
            poi_bus = [b for b in sorted_buses if "POI" in b.name]
            yard_bus = [b for b in sorted_buses if "YARD" in b.name]
            main_bus = [b for b in sorted_buses if "MAIN" in b.name]
            feeders = [b for b in sorted_buses if "FDR" in b.name]
            
            if poi_bus: coordinates[poi_bus[0].bus_number] = (0.0, 0.0)
            if yard_bus: coordinates[yard_bus[0].bus_number] = (0.0, self.config.y_spacing)
            if main_bus: coordinates[main_bus[0].bus_number] = (0.0, 2 * self.config.y_spacing)
            
            feeder_idx = - (len(feeders) // 2) # Center feeders horizontally around x=0
            for bus in feeders:
                coordinates[bus.bus_number] = (feeder_idx * self.config.x_spacing, 3 * self.config.y_spacing)
                feeder_idx += 1
                
        elif self.config.orientation == "transformer_substation":
            # HV_MAIN at depth 0. LV_BUS at depth 1, LD_BUS at depth 2, grouped by branch
            hv_bus = [b for b in sorted_buses if "HV_MAIN" in b.name]
            lv_buses = [b for b in sorted_buses if "LV_" in b.name]
            ld_buses = [b for b in sorted_buses if "LD_" in b.name]
            
            if hv_bus: coordinates[hv_bus[0].bus_number] = (0.0, 0.0)
            
            branch_idx = - (len(lv_buses) // 2) # Center branches horizontally around x=0
            for lv_bus in sorted(lv_buses, key=lambda b: b.bus_number):
                x_coord = branch_idx * self.config.x_spacing * 2 # wider spacing for transformer chains
                coordinates[lv_bus.bus_number] = (x_coord, self.config.y_spacing)
                
                # Find associated load bus (assuming deterministic naming LD_xxx matching LV_yyy pattern isn't strict, we just zip them if sorted)
                branch_idx += 1
                
            # Assign load buses same X as their LV parent
            # Assuming LD_x corresponds to LV_y where they were created sequentially
            idx = - (len(ld_buses) // 2)
            for ld_bus in sorted(ld_buses, key=lambda b: b.bus_number):
                x_coord = idx * self.config.x_spacing * 2
                coordinates[ld_bus.bus_number] = (x_coord, 2 * self.config.y_spacing)
                idx += 1
            
        return coordinates
