from pathlib import Path

import cadquery as cq


def export_component_stl(
    solids,
    output_path
):

    compound = cq.Compound.makeCompound(
        [solid.val() for solid in solids]
    )

    cq.exporters.export(
        compound,
        str(output_path)
    )

    return output_path
