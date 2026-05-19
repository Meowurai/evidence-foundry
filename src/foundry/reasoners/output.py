

from dataclasses import dataclass, asdict
import json
from pathlib import Path


@dataclass
class Claim:
    """
    An explicit statement made by a reasoner.

    A claim may be correct, incorrect, partially correct,
    or unsupported by evidence.
    """

    text: str
    supporting_evidence: list[str]


@dataclass
class Belief:
    """
    A confidence-weighted stance toward a claim.

    The claim is the statement.
    The belief is how strongly the reasoner currently trust it.
    """

    claim: Claim
    confidence: float 


@dataclass
class ReasonerOutput:
    """
    The full output from one reasoner run.
    """

    case_id: str
    reasoner_name: str 
    beliefs: list[Belief]


def write_reasoner_output(output: ReasonerOutput, output_path: Path) -> None:
    """
    Write reasoner output to JSON.
    """

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w") as file:
        json.dump(asdict(output), file, indent=2)

