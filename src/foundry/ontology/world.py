

from dataclasses import dataclass
from foundry.ontology.entity import EntityDef
from foundry.ontology.relationship import RelationshipDef


@dataclass(frozen=True)
class WorldOntology:
    name: str
    entities: dict[str, EntityDef]
    relationships: list[RelationshipDef]
    description: str = ""