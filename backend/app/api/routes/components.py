from fastapi import APIRouter

from app.core.component_registry import (
    registry
)

router = APIRouter()


@router.get("/")
def get_components():

    return registry.get_component_types()


@router.get("/{component_type}/schema")
def get_component_schema(
    component_type: str
):

    schema = registry.get_schema(
        component_type
    )

    return schema.model_json_schema()
