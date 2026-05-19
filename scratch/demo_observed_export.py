
from pathlib import Path
from dataclasses import dataclass

from foundry.evidence.export import (
    export_observed_records,
    write_records_to_csv
)
from foundry.ontology.entity import EntityDef
from foundry.ontology.variable import VariableDef, Visbility
from foundry.simulation.state import State

@dataclass
class Customer:
    id: str
    product_fit: float 
    frustration: float
    usage_score: float 
    churned: bool


observed_customer_def = EntityDef(
    name="Customer",
    variables=[
        VariableDef("id", Visbility.OBSERVED),
        VariableDef("usage_score", Visbility.OBSERVED),
        VariableDef("churned", Visbility.OBSERVED)
    ],
)

customers = [
    Customer("customer_1", 0.85, 0.2, 0.72, False),
    Customer("customer_2", 0.30, 0.8, 0.20, True),
]

state = State()

for customer in customers:
    state.add_record("Customer", customer)

customer_records = state.get_records("Customer")


observed_records = export_observed_records(customer_records, observed_customer_def)

write_records_to_csv(
    observed_records,
    Path("scratch/output/customers.csv")
)