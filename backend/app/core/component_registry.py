class ComponentRegistry:

    def __init__(self):

        self.builders = {}
        self.schemas = {}

    def register(
        self,
        component_type,
        schema_class,
        builder_function
    ):

        self.builders[component_type] = builder_function
        self.schemas[component_type] = schema_class

    def get_builder(self, component_type):

        return self.builders[component_type]

    def get_schema(self, component_type):

        return self.schemas[component_type]

    def get_component_types(self):

        return list(self.schemas.keys())

# -----------------------------------
# Global Registry Instance
# -----------------------------------

registry = ComponentRegistry()


# -----------------------------------
# Register Existing Components
# -----------------------------------

from app.schema.cylinder import CylinderComponent
from app.schema.head import HeadComponent

from app.geometry.cylinder_builder import build_cylinder
from app.geometry.head_builder import build_head


registry.register(
    "cylinder",
    CylinderComponent,
    build_cylinder
)

registry.register(
    "head",
    HeadComponent,
    build_head
)
