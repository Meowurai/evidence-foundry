

from foundry.ontology.entity import EntityDef
from foundry.ontology.variable import Visbility
from foundry.ontology.world import WorldOntology

# TODO: data dictionary generation
# TODO: evidence exports 
# TODO: reasoner access rules
# TODO: safe metadata querying


def build_observed_ontology(world: WorldOntology) -> WorldOntology:
    """
    Create the ontology that the reasoner is allowed to see.

    The full Worldontology may contain both:
    - hidden variables
    - observed variables

    But the reasoner should only see observed variables.

    So this function creates a new WorldOntology where each entity
    keeps only variables marked as Visbility.OBSERVED.
    """

    observed_entities: dict[str, EntityDef] = {}

    for entity_name, entity_def in world.entities.items():
        # Keep only variables that are allowed to be observed.
        observed_variables = [
            variable
            for variable in entity_def.variables
            if variable.visibility == Visbility.OBSERVED
        ]

        # Create a new EntityDef with the same entity name, but only the observed variables.
        observed_entities[entity_name] = EntityDef(
            name=entity_def.name, 
            variables=observed_variables,
            description=entity_def.description,
        )

    # Return a new ontology.
    # This has the same relationships for now,
    # but only observed entity variables.
    return WorldOntology(
        name=f"{world.name}_observed",
        entities=observed_entities,
        relationships=world.relationships,
        description=f"Observed projection of {world.name}",
    )