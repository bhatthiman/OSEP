from pathlib import Path

import cadquery as cq


def export_component_stl(
    solids,
    output_path
):

    shapes = []

    for solid in solids:

        # Workplane
        if hasattr(solid, "val"):

            shapes.append(
                solid.val()
            )

        # Already a CadQuery shape
        else:

            shapes.append(
                solid
            )

    compound = cq.Compound.makeCompound(
        shapes
    )

    cq.exporters.export(
        compound,
        str(output_path)
    )

    return output_path
