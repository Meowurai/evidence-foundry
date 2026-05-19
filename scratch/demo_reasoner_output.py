from pathlib import Path

from foundry.reasoners.output import (
    Claim,
    Belief,
    ReasonerOutput,
    write_reasoner_output,
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