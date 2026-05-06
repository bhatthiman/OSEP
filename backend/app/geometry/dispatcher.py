from app.schema.cylinder import CylinderComponent
from app.schema.head import HeadComponent

from app.geometry.cylinder_builder import build_cylinder
from app.geometry.head_builder import build_head


def build_component(component):

    if component.type == "cylinder":

        cylinder = CylinderComponent(
            id=component.id,
            type=component.type,
            **component.data
        )

        return build_cylinder(cylinder)

    elif component.type == "head":

        head = HeadComponent(
            id=component.id,
            type=component.type,
            **component.data
        )

        return build_head(head)

    raise ValueError(
        f"Unsupported component type: {component.type}"
    )
