

from dataclasses import dataclass
from foundry.ontology.variable import VariableDef


@dataclass(frozen=True)
class EntityDef:
    name: str
    variables: list[VariableDef]
    description: str = ""