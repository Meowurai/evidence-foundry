

from dataclasses import dataclass, asdict
import json
from pathlib import Path 


@dataclass
class GroundTruth:
    """
    Hidden answer key for one simulated case.

    The reasoner should not see this during investigation.
    It is used later for evaluation.
    """

    case_id: str
    root_cause: str
    causal_chain: list[str]
    expected_claims: list[str]



def write_ground_truth(ground_truth: GroundTruth, output_path: Path) -> None:
    """
    Write ground truth to JSON.
    """

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w") as file:
        json.dump(asdict(ground_truth), file, indent=2)