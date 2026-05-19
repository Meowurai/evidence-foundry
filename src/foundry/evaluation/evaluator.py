

from dataclasses import dataclass, asdict
import json 
from pathlib import Path

from foundry.evaluation.ground_truth import GroundTruth
from foundry.reasoners.output import ReasonerOutput


@dataclass
class EvaluationResult:
    """
    Result of evaluating one reasoner output against ground truth.

    This is intentionally simple for now.
    """

    case_id: str
    reasoner_name: str
    matched_expected_claims: int
    total_expected_claims: int
    score: float 

def evaluate_reasoner_output(
        ground_truth: GroundTruth,
        reasoner_output: ReasonerOutput
) -> EvaluationResult:
    """
    Compare reasoner claims against expected ground truth claims.

    This first evaluator uses simple exact text matching.

    Later, this can become semantic matching, rubic scoring,
    evidence scoring, calibration scoring, and causal-chain scoring.
    """

    reasoner_claim_texts = {
        belief.claim.text
        for belief in reasoner_output.beliefs
    }

    matched = 0

    for expected_claim in ground_truth.expected_claims:
        if expected_claim in reasoner_claim_texts:
            matched += 1

    total = len(ground_truth.expected_claims)
    score = matched / total if total > 0 else 0.0

    return EvaluationResult(
        case_id=ground_truth.case_id,
        reasoner_name=reasoner_output.reasoner_name,
        matched_expected_claims=matched,
        total_expected_claims=total,
        score=score
    )


def write_evaluation_result(
    result: EvaluationResult,
    output_path: Path,
) -> None:
    """
    Write evaluation result to JSON.
    """

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w") as file:
        json.dump(asdict(result), file, indent=2)