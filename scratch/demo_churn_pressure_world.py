from datetime import date, timedelta
from pathlib import Path
from random import Random

from foundry.evaluation.evaluator import (
    evaluate_reasoner_output,
    write_evaluation_result,
)
from foundry.evaluation.ground_truth import write_ground_truth
from foundry.evidence.export import (
    export_observed_records,
    write_records_to_csv,
)
from foundry.ontology.projection import build_observed_ontology
from foundry.reasoners.output import (
    Belief,
    Claim,
    ReasonerOutput,
    write_reasoner_output,
)
from foundry.simulation.clock import Clock
from foundry.simulation.context import Context
from foundry.simulation.engine import Engine
from foundry.simulation.state import State
from foundry.worlds.churn_pressure import (
    build_ground_truth,
    build_systems,
    build_world_ontology,
)

from foundry.reasoners.naive_churn import run_naive_churn_reasoner

from foundry.evidence.events import export_events


OUTPUT_DIR = Path("scratch/output/case_001_churn_pressure")


def main() -> None:
    # 1. Build the full hidden world ontology.
    # This contains both hidden and observed variables.
    world = build_world_ontology()

    # 2. Build the observed ontology.
    # This filters out hidden variables so only observable fields remain.
    observed_world = build_observed_ontology(world)

    # 3. Create runtime context.
    # The clock controls simulation time.
    # The seeded random generator makes the run reproducible.
    context = Context(
        clock=Clock(
            start_date=date(2026, 1, 1),
            ticks=10,
            delta=timedelta(days=1),
        ),
        rng=Random(42),
    )

    # 4. Create empty simulation state.
    # Systems will add and update records here.
    state = State()

    # 5. Build and run the simulation engine.
    # The world systems create customers, update frustration,
    # update usage, and generate support tickets.
    engine = Engine(
        systems=build_systems(),
    )

    engine.run(context, state)

    # 6. Export observed evidence files.
    # We loop over the observed ontology, not the full world ontology.
    # This means hidden fields like product_fit and frustration are excluded.
    for entity_name, entity_def in observed_world.entities.items():
        records = state.get_records(entity_name)

        # Some entity types may have no records in a given run.
        if not records:
            continue

        observed_records = export_observed_records(
            records=records,
            entity_def=entity_def,
        )

        write_records_to_csv(
            records=observed_records,
            output_path=OUTPUT_DIR / "observed" / f"{entity_name}.csv",
        )


    event_records = export_events(state.event_log)

    if event_records:
        write_records_to_csv(
            records=event_records,
            output_path=OUTPUT_DIR / "observed" / "events.csv"
        )

    # 7. Export hidden ground truth.
    # The reasoner should not see this during investigation.
    ground_truth = build_ground_truth()

    write_ground_truth(
        ground_truth=ground_truth,
        output_path=OUTPUT_DIR / "ground_truth" / "ground_truth.json",
    )

    # 8. Create a manual baseline reasoner output.
    # This is not a real reasoner yet.
    # It only proves that the output/evaluation contract works.
    claim = Claim(
        text="Customer frustration lowers product usage.",
        supporting_evidence=[
            "Observed customer usage scores vary after the simulation.",
            "Support tickets appear for some customers.",
        ],
    )

    belief = Belief(
        claim=claim,
        confidence=0.75,
    )

    reasoner_output = run_naive_churn_reasoner(
    case_id="case_001_churn_pressure",
    observed_dir=OUTPUT_DIR / "observed",
)

    write_reasoner_output(
        output=reasoner_output,
        output_path=OUTPUT_DIR / "runs" / "naive_churn" / "answer.json",
    )

    # 9. Evaluate reasoner output against ground truth.
    evaluation = evaluate_reasoner_output(
        ground_truth=ground_truth,
        reasoner_output=reasoner_output,
    )

    write_evaluation_result(
        result=evaluation,
        output_path=OUTPUT_DIR / "runs" / "naive_churn" / "evaluation.json",
    )

    # 10. Print a tiny summary so you know it worked.
    print("Simulation complete.")
    print(f"Output written to: {OUTPUT_DIR}")
    print(f"Customers: {len(state.get_records('Customer'))}")
    print(f"Support tickets: {len(state.get_records('SupportTicket'))}")
    print(f"Evaluation score: {evaluation.score}")


if __name__ == "__main__":
    main()