from pydantic import BaseModel, Field
from typing import List, Optional

from app.ir.component_models import Bus, Branch, Transformer, Load, Generator, TopologyMetadata

class TopologyIR(BaseModel):
    """
    The deterministic Intermediate Representation of the power system topology.
    This acts as the bridge between planning and the executor.
    """
    metadata: TopologyMetadata = Field(default_factory=TopologyMetadata)
    buses: List[Bus] = Field(default_factory=list)
    branches: List[Branch] = Field(default_factory=list)
    transformers: List[Transformer] = Field(default_factory=list)
    loads: List[Load] = Field(default_factory=list)
    generators: List[Generator] = Field(default_factory=list)

    def add_bus(self, bus: Bus) -> None:
        self.buses.append(bus)

    def add_branch(self, branch: Branch) -> None:
        self.branches.append(branch)

    def add_transformer(self, transformer: Transformer) -> None:
        self.transformers.append(transformer)

    def add_load(self, load: Load) -> None:
        self.loads.append(load)

    def add_generator(self, generator: Generator) -> None:
        self.generators.append(generator)
