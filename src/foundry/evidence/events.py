

from typing import Any 

from foundry.simulation.event import Event


def export_events(events: list[Event]) -> list[dict[str, Any]]:
    """
    Convert simulation events into flat evidence records.

    For now, payload fields are expanded into the same row.
    """

    rows: list[dict[str, Any]] = []

    for event in events:
        row = {
            "event_type": event.event_type,
            "tick": event.tick
        }

        row.update(event.payload)

    return rows