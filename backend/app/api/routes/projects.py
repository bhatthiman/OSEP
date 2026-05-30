import time

from pathlib import Path

from fastapi import APIRouter

from app.core.project_manager import ProjectManager

from app.exporters.preview_exporter import export_component_stl

from app.schema.project import (
    Project,
    ProjectInfo
)

router = APIRouter()

project_manager = ProjectManager()

BASE_DIR = Path(__file__).resolve().parents[4]

EXAMPLE_PROJECT = (
    BASE_DIR
    / "examples"
    / "simple_vessel.json"
)

# --------------------------------------------------
# Load Project
# --------------------------------------------------

@router.post("/load")
def load_project():

    project = project_manager.load_project(
        EXAMPLE_PROJECT
    )

    return project.model_dump()


# --------------------------------------------------
# Update Component
# --------------------------------------------------

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

    # ------------------------------------------
    # Generate unique preview filename
    # ------------------------------------------

    revision = int(time.time())

    output_dir = Path("outputs")

    output_dir.mkdir(exist_ok=True)

    filename = (
        f"{component_id}_{revision}.stl"
    )

    output_file = (
        output_dir / filename
    )

    export_component_stl(
        solids,
        output_file
    )

    return {
        "component_id": component_id,
        "generated_solids": len(solids),
        "preview_url": (
            f"/outputs/{filename}"
        ),
        "revision": revision
    }


# --------------------------------------------------
# Get Geometry Info
# --------------------------------------------------

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


# --------------------------------------------------
# Generate Preview
# --------------------------------------------------

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

    revision = int(time.time())

    output_dir = Path("outputs")

    output_dir.mkdir(exist_ok=True)

    filename = (
        f"{component_id}_{revision}.stl"
    )

    output_file = (
        output_dir / filename
    )

    export_component_stl(
        solids,
        output_file
    )

    return {
        "preview_file": (
            f"/outputs/{filename}"
        ),
        "revision": revision
    }
    
# --------------------------------------------------
@router.get("/active")
def get_active_project():

    if project_manager.project is None:
        return None

    return project_manager.project.model_dump()
    
from app.schema.component import Component

# --------------------------------------------------
# Add Empty Component
# --------------------------------------------------

@router.post("/components")
def add_component(
    payload: dict
):

    if project_manager.project is None:

        raise ValueError(
            "No active project"
        )

    component = Component(**payload)

    project_manager.project.components.append(
        component
    )

    return component.model_dump()
    from app.schema.project import (
    Project,
    ProjectInfo
)

# --------------------------------------------------
# Create Empty Project
# --------------------------------------------------

@router.post("/new")
def new_project():

    project = Project(
        project=ProjectInfo(
            name="Untitled"
        ),
        components=[]
    )

    project_manager.project = project

    return project.model_dump()

# --------------------------------------------------
# Full Project Preview
# --------------------------------------------------

@router.get("/preview")
def preview_project():

    assembly = (
        project_manager.rebuild_project()
    )

    solids = []

    for component_solids in (
        project_manager.generated_components.values()
    ):

        solids.extend(component_solids)

    revision = int(time.time())

    output_dir = Path("outputs")

    output_dir.mkdir(exist_ok=True)

    filename = (
        f"project_{revision}.stl"
    )

    output_file = (
        output_dir / filename
    )

    export_component_stl(
        solids,
        output_file
    )

    return {
        "preview_file":
            f"/outputs/{filename}"
    }
from app.schema.project import (
    Project,
    ProjectInfo
)

# --------------------------------------------------
# Save Project
# --------------------------------------------------

@router.post("/save/{filename}")
def save_project(filename: str):

    if project_manager.project is None:
        raise ValueError("No active project")

    filepath = (
        BASE_DIR
        / "examples"
        / f"{filename}.json"
    )

    project_manager.save_project(filepath)

    return {
        "status": "saved",
        "filepath": str(filepath)
    }
