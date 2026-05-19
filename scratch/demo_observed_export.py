

from dataclasses import dataclass

from foundry.evidence.export import export_observed_record
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

customer = Customer(
    id="customer_1",
    product_fit=0.85,
    frustration=0.2,
    usage_score=0.72,
    churned=False
)

print(export_observed_record(customer, observed_customer_def))