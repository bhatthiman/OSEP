import cadquery as cq

from app.schema.cylinder import CylinderComponent


def build_cylinder(component: CylinderComponent):

    z_offset = 0

    all_solids = []

    for segment in component.segments:

        geo = segment.geometry

        outer_radius = (
            geo.inside_diameter / 2
            + geo.nominal_thickness
        )

        inner_radius = geo.inside_diameter / 2

        for plate in segment.plates:

            outer = (
                cq.Workplane("XY")
                .cylinder(
                    geo.length,
                    outer_radius,
                    angle=plate.sweep_angle
                )
                .rotate(
                    (0, 0, 0),
                    (0, 0, 1),
                    plate.start_angle
                )
                .translate((0, 0, z_offset + geo.length / 2))
            )

            inner = (
                cq.Workplane("XY")
                .cylinder(
                    geo.length + 2,
                    inner_radius,
                    angle=plate.sweep_angle
                )
                .rotate(
                    (0, 0, 0),
                    (0, 0, 1),
                    plate.start_angle
                )
                .translate((0, 0, z_offset + geo.length / 2))
            )

            shell_plate = outer.cut(inner)

            all_solids.append(shell_plate)

        z_offset += geo.length

    return all_solids
