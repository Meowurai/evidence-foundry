

from dataclasses import dataclass

from foundry.evidence.export import export_observed_records
from foundry.ontology.entity import EntityDef
from foundry.ontology.variable import VariableDef, Visbility



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

print(export_observed_records(customers, observed_customer_def))