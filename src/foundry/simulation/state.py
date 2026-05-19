

from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any

from foundry.simulation.event import Event



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

    event_log: list[Event] = field(
        default_factory=list
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
    
    def add_event(self, event: Event) -> None:
        self.event_log.append(event)