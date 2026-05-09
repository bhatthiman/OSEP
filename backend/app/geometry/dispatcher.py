from app.core.component_registry import registry


def build_component(component):

    schema_class = registry.get_schema(
        component.type
    )

    builder = registry.get_builder(
        component.type
    )

    typed_component = schema_class(
        id=component.id,
        type=component.type,
        **component.data
    )

    return builder(typed_component)
