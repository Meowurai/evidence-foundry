from foundry.ontology.world import WorldOntology


def build_data_dictionary_markdown(observed_world: WorldOntology) -> str:
    """
    Build a human-readable data dictionary from the observed ontology.

    This describes only what the reasoner is allowed to know:
    - observed entities
    - observed fields
    - relationships between observed entities
    """

    lines: list[str] = []

    lines.append("# Data Dictionary")
    lines.append("")
    lines.append(f"Ontology: {observed_world.name}")
    lines.append("")

    lines.append("## Entities")
    lines.append("")

    for entity_name, entity_def in observed_world.entities.items():
        lines.append(f"### {entity_name}")
        lines.append("")

        if entity_def.description:
            lines.append(entity_def.description)
            lines.append("")

        lines.append("| Field | Description |")
        lines.append("|---|---|")

        for variable in entity_def.variables:
            description = variable.description or ""
            lines.append(f"| {variable.name} | {description} |")

        lines.append("")

    if observed_world.relationships:
        lines.append("## Relationships")
        lines.append("")

        lines.append("| Relationship | From | To | Description |")
        lines.append("|---|---|---|---|")

        for relationship in observed_world.relationships:
            lines.append(
                "| "
                f"{relationship.name} | "
                f"{relationship.source_entity}.{relationship.source_field} | "
                f"{relationship.target_entity}.{relationship.target_field} | "
                f"{relationship.description or ''} |"
            )

        lines.append("")

    return "\n".join(lines)


def write_data_dictionary(
    observed_world: WorldOntology,
    output_path,
) -> None:
    """
    Write the observed ontology as a Markdown data dictionary.
    """

    output_path.parent.mkdir(parents=True, exist_ok=True)

    content = build_data_dictionary_markdown(observed_world)

    output_path.write_text(content)