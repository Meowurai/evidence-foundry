

from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any



@dataclass
class State:
    """
    Holds the actual runtime records for one simulation run.

    The ontology describes what entity types exist.
    The state holds the actual entity instances created during a run.
    """

    entity_data: dict[str, list[Any]] = field(
        default_factory=lambda: defaultdict(list)
    )

    def add_record(self, entity_name: str, record: Any) -> None:
        """
        Store one runtime entity record under its entity name.

        Example:
            state.add_record("Customer", customer)
        """
        self.entity_data[entity_name].append(record)

    def get_records(self, entity_name: str) -> list[Any]:
        """
        Return all records for one entity type.
        """
        return self.entity_data[entity_name]