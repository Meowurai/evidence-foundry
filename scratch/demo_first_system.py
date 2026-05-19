from dataclasses import dataclass
from datetime import date, timedelta
from random import Random
from pathlib import Path

from foundry.simulation.clock import Clock
from foundry.simulation.context import Context
from foundry.simulation.state import State
from foundry.simulation.system import System
from foundry.simulation.engine import Engine

from foundry.ontology.entity import EntityDef
from foundry.ontology.relationship import RelationshipDef
from foundry.ontology.variable import VariableDef, Visbility
from foundry.ontology.world import WorldOntology
from foundry.ontology.projection import build_observed_ontology

from foundry.evidence.export import export_observed_records, write_records_to_csv


@dataclass
class Customer:
    id: str
    product_fit: float
    frustration: float
    usage_score: float
    churned: bool


customer_def = EntityDef(
    name="Customer",
    variables=[
        VariableDef("id", Visbility.OBSERVED),
        VariableDef("product_fit", Visbility.HIDDEN),
        VariableDef("frustration", Visbility.HIDDEN),
        VariableDef("usage_score", Visbility.OBSERVED),
        VariableDef("churned", Visbility.OBSERVED),
    ],
)

@dataclass
class SupportTicket:
    id: str
    customer_id: str
    created_tick: int
    severity: str
    category: str


support_ticket_def = EntityDef(
    name="SupportTicket",
    variables=[
        VariableDef("id", Visbility.OBSERVED),
        VariableDef("customer_id", Visbility.OBSERVED),
        VariableDef("created_tick", Visbility.OBSERVED),
        VariableDef("severity", Visbility.OBSERVED),
        VariableDef("category", Visbility.OBSERVED),
    ],
)

ticket_customer_relationship = RelationshipDef(
    name="support_ticket_belongs_to_customer",
    source_entity="SupportTicket",
    target_entity="Customer",
    source_field="customer_id",
    target_field="id"
)

world = WorldOntology(
    name="churn_pressure_world",
    entities={
        "Customer": customer_def,
        "SupportTicket": support_ticket_def,
    },
    relationships=[
        ticket_customer_relationship,
    ],
)


class CustomerCreationSystem(System):
    """
    Creates a few customers on the first tick only.
    """

    def step(self, context: Context, state: State, tick: int) -> None:
        if tick != 0:
            return

        for i in range(5):
            customer = Customer(
                id=f"customer_{i + 1}",
                product_fit=context.rng.random(),
                frustration=0.0,
                usage_score=0.0,
                churned=False,
            )

            state.add_record("Customer", customer)


class UsageSystem(System):
    """
    Updates customer usage each tick.

    In this tiny world:
    - higher product_fit increases usage
    - higher frustration lowers usage
    - randomness adds noise
    """

    def step(self, context: Context, state: State, tick: int) -> None:
        customers = state.get_records("Customer")

        for customer in customers:
            noise = context.rng.uniform(-0.1, 0.1)

            usage_score = (
                customer.product_fit
                - customer.frustration
                + noise 
            )

            # Keep usage between 0 and 1
            customer.usage_score = max(0.0, min(1.0, usage_score))

class FrustrationSystem(System):
    """
    Updates hidden customer frustration each tick.

    In this tiny world:
    - low product_fit slowly increases frustration
    - some random noise makes customers vary
    """

    def step(self, context: Context, state: State, tick: int) -> None:
        customers = state.get_records("Customer")

        for customer in customers:
            pressure = 1.0 - customer.product_fit
            noise = context.rng.uniform(-0.03, 0.03)

            customer.frustration += (pressure * 0.05) + noise

            # Keep frustration between 0 and 1.
            customer.frustration = max(0.0, min(1.0, customer.frustration))



class SupportTicketSystem(System):
    """
    Creates observable support tickets.

    In this tiny world:
    - higher frustration increases the chance of a ticket
    - tickets become observed evidence
    """

    def step(self, context: Context, state: State, tick: int) -> None:
        customers = state.get_records("Customer")

        for customer in customers:
            ticket_probability = customer.frustration * 0.25

            if context.rng.random() < ticket_probability:
                ticket = SupportTicket(
                    id=f"ticket_{tick}_{customer.id}",
                    customer_id=customer.id,
                    created_tick=tick,
                    severity="high" if customer.frustration > 0.7 else "medium",
                    category="product_issue",
                )

                state.add_record("SupportTicket", ticket)


clock = Clock(
    start_date=date(2026, 1, 1),
    ticks=10,
    delta=timedelta(days=1),
)

context = Context(
    clock=clock,
    rng=Random(42),
)

state = State()


engine = Engine(
    systems=[
        CustomerCreationSystem(),
        FrustrationSystem(),
        UsageSystem(),
        SupportTicketSystem()
    ]
)

engine.run(context, state)

observed_world = build_observed_ontology(world)

for entity_name, entity_def in observed_world.entities.items():
    records = state.get_records(entity_name)
    observed_records = export_observed_records(records, entity_def)

    write_records_to_csv(
        observed_records,
        Path(f"scratch/output/{entity_name}.csv"),
    )