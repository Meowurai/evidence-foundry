import csv
from pathlib import Path

from foundry.reasoners.output import (
    Belief,
    Claim,
    ReasonerOutput,
)


def read_csv(path: Path) -> list[dict[str, str]]:
    """
    Read a CSV evidence file into a list of dictionaries.

    Each row becomes one dict.
    CSV values are strings by default.
    """

    with path.open() as file:
        reader = csv.DictReader(file)
        return list(reader)


def run_naive_churn_reasoner(
    case_id: str,
    observed_dir: Path,
) -> ReasonerOutput:
    """
    Very simple baseline reasoner.

    This reasoner only looks at observed evidence.

    It does not know:
    - product_fit
    - frustration
    - the true causal chain

    It only sees:
    - customer usage scores
    - support tickets
    """

    customers = read_csv(observed_dir / "Customer.csv")
    support_tickets = read_csv(observed_dir / "SupportTicket.csv")

    low_usage_customers = [
        customer
        for customer in customers
        if float(customer["usage_score"]) < 0.4
    ]

    has_support_tickets = len(support_tickets) > 0
    has_low_usage = len(low_usage_customers) > 0

    beliefs: list[Belief] = []

    if has_low_usage:
        beliefs.append(
            Belief(
                claim=Claim(
                    text="Customer frustration lowers product usage.",
                    supporting_evidence=[
                        f"{len(low_usage_customers)} customers have usage_score below 0.4."
                    ],
                ),
                confidence=0.55,
            )
        )

    if has_support_tickets:
        beliefs.append(
            Belief(
                claim=Claim(
                    text="Customer frustration increases support ticket probability.",
                    supporting_evidence=[
                        f"{len(support_tickets)} support tickets were observed."
                    ],
                ),
                confidence=0.55,
            )
        )

    if has_low_usage and has_support_tickets:
        beliefs.append(
            Belief(
                claim=Claim(
                    text="Low product fit increases customer frustration.",
                    supporting_evidence=[
                        "Low usage and support tickets appear together in the observed evidence."
                    ],
                ),
                confidence=0.35,
            )
        )

    return ReasonerOutput(
        case_id=case_id,
        reasoner_name="naive_churn",
        beliefs=beliefs,
    )