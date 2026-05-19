

from dataclasses import dataclass

from foundry.evaluation.ground_truth import GroundTruth
from foundry.ontology.entity import EntityDef
from foundry.ontology.relationship import RelationshipDef
from foundry.ontology.variable import VariableDef, Visbility
from foundry.ontology.world import WorldOntology
from foundry.simulation.context import Context
from foundry.simulation.state import State
from foundry.simulation.system import System


@dataclass
class Customer:
    id: str
    product_fit: float 
    frustration: float
    usage_score: float 
    churned: bool

@dataclass
class SupportTicket:
    id: str
    customer_id: str
    created_tick: int
    severity: str
    category: str


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


def build_world_ontology() -> WorldOntology:
    customer_def = EntityDef(
        name="Customer",
        variables=[
            VariableDef("id", Visbility.OBSERVED, "Unique customer identifier."),
            VariableDef("product_fit", Visbility.HIDDEN, "How well the product fits the customer."),
            VariableDef("frustration", Visbility.HIDDEN, "Internal customer frustration level."),
            VariableDef("usage_score", Visbility.OBSERVED, "Observed customer product usage score."),
            VariableDef("churned", Visbility.OBSERVED, "Whether the customer has churned."),
        ],
        description="A customer using the product.",
    )

    support_ticket_def = EntityDef(
        name="SupportTicket",
        variables=[
            VariableDef("id", Visbility.OBSERVED, "Unique support ticket identifier."),
            VariableDef("customer_id", Visbility.OBSERVED, "Customer this ticket belongs to."),
            VariableDef("created_tick", Visbility.OBSERVED, "Simulation tick when the ticket was created."),
            VariableDef("severity", Visbility.OBSERVED, "Ticket severity."),
            VariableDef("category", Visbility.OBSERVED, "Ticket category."),
        ],
        description="An observable support ticket created by a customer.",
    )

    ticket_customer_relationship = RelationshipDef(
        name="support_ticket_belongs_to_customer",
        source_entity="SupportTicket",
        target_entity="Customer",
        source_field="customer_id",
        target_field="id",
        description="Each support ticket belongs to one customer.",
    )

    return WorldOntology(
        name="churn_pressure_world",
        entities={
            "Customer": customer_def,
            "SupportTicket": support_ticket_def,
        },
        relationships=[
            ticket_customer_relationship,
        ],
        description="A tiny churn pressure world where low product fit increases frustration, lowering usage and increasing support tickets.",
    )


def build_ground_truth() -> GroundTruth:
    return GroundTruth(
        case_id="case_001_churn_pressure",
        root_cause=(
            "Low product fit increases hidden customer frustration. "
            "Higher frustration lowers observed usage and increases support ticket probability."
        ),
        causal_chain=[
            "low_product_fit",
            "increased_frustration",
            "lower_usage_score",
            "more_support_tickets",
        ],
        expected_claims=[
            "Low product fit increases customer frustration.",
            "Customer frustration lowers product usage.",
            "Customer frustration increases support ticket probability.",
        ],
    )


def build_systems() -> list[System]:
    return [
        CustomerCreationSystem(),
        FrustrationSystem(),
        UsageSystem(),
        SupportTicketSystem(),
    ]