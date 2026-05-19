

from dataclasses import dataclass


@dataclass(frozen=True)
class RelationshipDef:
    name: str
    source_entity: str
    target_entity: str
    source_field: str
    target_field: str
    description: str = ""