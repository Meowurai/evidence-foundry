
import csv
from pathlib import Path
from dataclasses import asdict
from typing import Any

from foundry.ontology.entity import EntityDef


def export_observed_record(record: Any, entity_def: EntityDef) -> dict[str, Any]:
    """
    Export only the fields that are allowed by the observed ontology.

    record:
        A runtime entity object, for example a Customer dataclass.

    entity_def:
        The observed EntityDef for that record type.
        This should alrady contain only observed variables.

    Returns:
        A dictionary that can later become a CSV row, JSON record, or evidence table row.
    """

    # Convert the dataclass obejct into a normal dictionary.
    #Customer(id="customer_1", product_fit=0.8, usage_score=0.6)
    # becomes:
    # {"id": "customer_1", "product_fit": 0.8, "usage_score": 0.6}
    data = asdict(record)

    # The observed ontology tells us which variable names are allowed
    # to leave the hidden world and become evidence.
    allowed_field_names = {
        variable.name
        for variable in entity_def.variables
    }

    # Keep only fields listed in the observed ontology.
    observed_data = {
        field_name: value
        for field_name, value in data.items()
        if field_name in allowed_field_names
    }

    return observed_data


def export_observed_records(records: list[Any], entity_def: EntityDef) -> list[dict[str, Any]]:
    """
    Export many runtime records using the same observed entity definition.
    """

    return [
        export_observed_record(record, entity_def)
        for record in records
    ]



def write_records_to_csv(
    records: list[dict[str, Any]],
    output_path: Path,
) -> None:
    """
    Write observed records to a CSV file.

    These records should already be filtered by the observed ontology.
    This function only handles writing them to disk.
    """

    if not records:
        raise ValueError("Cannot write CSV because records list is empty.")
    
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Use the keys from the first record as CSV columns.
    fieldnames = list(records[0].keys())

    with output_path.open("w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(records)