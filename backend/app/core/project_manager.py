from pathlib import Path
import json

import cadquery as cq

from app.schema.project import Project
from app.geometry.dispatcher import build_component
from app.core.component_registry import registry


class ProjectManager:

    def __init__(self):

        self.project = None
        self.assembly = None
        self.project_path = None
        self.generated_components = {}

    # --------------------------------------------------
    # Load Project
    # --------------------------------------------------

    def load_project(self, filepath):

        filepath = Path(filepath)

        with open(filepath, "r") as f:
            data = json.load(f)

        self.project = Project(**data)
        self.project_path = filepath

        return self.project

    # --------------------------------------------------
    # Save Project
    # --------------------------------------------------

    def save_project(self, filepath):

        if self.project is None:
            raise ValueError("No project loaded")

        filepath = Path(filepath)

        with open(filepath, "w") as f:

            json.dump(
                self.project.model_dump(),
                f,
                indent=2
            )

    # --------------------------------------------------
    # Rebuild Entire Project
    # --------------------------------------------------

    def rebuild_project(self):

        if self.project is None:
            raise ValueError("No project loaded")

        self.generated_components = {}

        assembly = cq.Assembly()

        for component in self.project.components:

            solids = build_component(component)

            self.generated_components[
                component.id
            ] = solids

            for i, solid in enumerate(solids):

                assembly.add(
                    solid,
                    name=f"{component.id}_{i}"
                )

        self.assembly = assembly

        return assembly

    # --------------------------------------------------
    # Rebuild Single Component
    # --------------------------------------------------

    def rebuild_component(self, component_id):

        if self.project is None:
            raise ValueError("No project loaded")

        target_component = None

        for component in self.project.components:

            if component.id == component_id:
                target_component = component
                break

        if target_component is None:
            raise ValueError(
                f"Component not found: {component_id}"
            )

        solids = build_component(target_component)

        self.generated_components[
            component_id
        ] = solids

        return solids

    # --------------------------------------------------
    # Update Component Data
    # --------------------------------------------------

    def update_component(
        self,
        component_id,
        new_data
    ):

        if self.project is None:
            raise ValueError("No project loaded")

        for component in self.project.components:

            if component.id == component_id:
#replace with schema validation later - ok, updated.
#                component.data.update(new_data)
                schema_class = registry.get_schema(
                    component.type
                )

                merged_data = {
                    **component.data,
                    **new_data
                }

                validated = schema_class(
                    id=component.id,
                    type=component.type,
                    **merged_data
                )

                component.data = validated.model_dump(
                    exclude={"id", "type"}
                )

                return component

        raise ValueError(
            f"Component not found: {component_id}"
        )

    # --------------------------------------------------
    # Export STEP
    # --------------------------------------------------

    def export_step(self, output_filepath):

        if self.assembly is None:
            raise ValueError(
                "No assembly generated"
            )

        output_filepath = Path(output_filepath)

        self.assembly.save(str(output_filepath))

        return output_filepath
        
# preview pipeline and export pipeline must eventually diverge.
        
        
    # Get component Data to prevent repeated loops later    
    def get_component(self, component_id):

        for component in self.project.components:

            if component.id == component_id:

                return component

        raise ValueError(
            f"Component not found: {component_id}"
        )
