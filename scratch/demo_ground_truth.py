from pathlib import Path

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