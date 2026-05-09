from pathlib import Path

from fastapi import APIRouter

from app.core.project_manager import ProjectManager

from app.exporters.preview_exporter import export_component_stl

router = APIRouter()

project_manager = ProjectManager()

BASE_DIR = Path(__file__).resolve().parents[4]

EXAMPLE_PROJECT = (
    BASE_DIR
    / "examples"
    / "simple_vessel.json"
)

@router.post("/load")
def load_project():

    project = project_manager.load_project(
        EXAMPLE_PROJECT
    )

    return project.model_dump()

#for update    
@router.patch(
    "/components/{component_id}"
)
def update_component(
    component_id: str,
    new_data: dict
):

    component = (
        project_manager.update_component(
            component_id,
            new_data
        )
    )

    solids = (
        project_manager.rebuild_component(
            component_id
        )
    )

    return {
        "component": component,
        "generated_solids": len(solids)
    }
#for geo
@router.get(
    "/components/{component_id}/geometry"
)
def get_component_geometry(
    component_id: str
):

    solids = (
        project_manager.generated_components.get(
            component_id
        )
    )

    if solids is None:

        solids = (
            project_manager.rebuild_component(
                component_id
            )
        )

    return {
        "component_id": component_id,
        "solid_count": len(solids)
    }
#preview
@router.get(
    "/components/{component_id}/preview"
)
def preview_component(
    component_id: str
):

    solids = (
        project_manager.generated_components.get(
            component_id
        )
    )

    if solids is None:

        solids = (
            project_manager.rebuild_component(
                component_id
            )
        )

    output_dir = Path("outputs")

    output_dir.mkdir(exist_ok=True)

    output_file = (
        output_dir
        / f"{component_id}.stl"
    )

    export_component_stl(
        solids,
        output_file
    )

    return {
        "preview_file": str(output_file)
    }
    
