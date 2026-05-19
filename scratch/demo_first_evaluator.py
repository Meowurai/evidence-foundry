from pathlib import Path

from foundry.reasoners.output import (
    Claim,
    Belief,
    ReasonerOutput,
    write_reasoner_output,
)

from foundry.evaluation.evaluator import (
    evaluate_reasoner_output,
    write_evaluation_result,
)

from foundry.evaluation.ground_truth import GroundTruth, write_ground_truth

ground_truth = GroundTruth(
    case_id="case_001_churn_pressure",
    root_cause="Low product fit increases frustration, which lowers usage and increases support tickets.",
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

write_ground_truth(
    ground_truth,
    Path("scratch/output/ground_truth.json"),
)

claim = Claim(
    text="Customer frustration appears to lower usage and increase support tickets.",
    supporting_evidence=[
        "Customer usage scores are lower for some customers.",
        "Support tickets are generated from frustrated customers.",
    ],
)

belief = Belief(
    claim=claim,
    confidence=0.75,
)

reasoner_output = ReasonerOutput(
    case_id="case_001_churn_pressure",
    reasoner_name="manual_baseline",
    beliefs=[
        belief,
    ],
)

write_reasoner_output(
    reasoner_output,
    Path("scratch/output/runs/manual_baseline/answer.json"),
)



evaluation = evaluate_reasoner_output(
    ground_truth=ground_truth,
    reasoner_output=reasoner_output,
)

write_evaluation_result(
    evaluation,
    Path("scratch/output/runs/manual_baseline/evaluation.json"),
)

print(evaluation)