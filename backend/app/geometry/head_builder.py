import cadquery as cq

from app.schema.head import HeadComponent


def build_head(component: HeadComponent):

    geo = component.geometry

    inside_radius = geo.inside_diameter / 2
    thickness = geo.nominal_thickness

    outside_radius = inside_radius + thickness

    z_scale = 0.5

    solids = []

    # --------------------------
    # Create outer ellipsoid
    # --------------------------

    outer = (
        cq.Solid.makeSphere(outside_radius)
        .transformGeometry(
            cq.Matrix([
                [1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, z_scale, 0]
            ])
        )
    )

    # --------------------------
    # Create inner ellipsoid
    # --------------------------

    inner = (
        cq.Solid.makeSphere(inside_radius)
        .transformGeometry(
            cq.Matrix([
                [1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, z_scale, 0]
            ])
        )
    )

    head_shell = outer.cut(inner)

    # --------------------------
    # Keep only upper half
    # --------------------------

    upper_cut = (
        cq.Workplane("XY")
        .box(
            outside_radius * 4,
            outside_radius * 4,
            outside_radius * 2
        )
        .translate((0, 0, outside_radius * z_scale / 2))
    )

    head_shell = head_shell.intersect(upper_cut.val())

    # --------------------------
    # Crown region
    # --------------------------

    crown_percent = (
        component.fabrication.crown.diameter_percent
    )

    crown_radius = (
        geo.inside_diameter
        * crown_percent
        / 100
    ) / 2

    crown_cut = (
        cq.Workplane("XY")
        .cylinder(
            outside_radius * 2,
            crown_radius
        )
        .translate((0, 0, outside_radius * z_scale / 2))
    )

    crown_piece = head_shell.intersect(crown_cut.val())

    solids.append(crown_piece)

    # --------------------------
    # Petal regions
    # --------------------------

    for petal in component.fabrication.petals:

        sector = (
            cq.Workplane("XY")
            .cylinder(
                outside_radius * 2,
                outside_radius,
                angle=petal.sweep_angle
            )
            .rotate(
                (0, 0, 0),
                (0, 0, 1),
                petal.start_angle
            )
            .translate((0, 0, outside_radius * z_scale / 2))
        )

        outer_ring = (
            cq.Workplane("XY")
            .cylinder(
                outside_radius * 2,
                outside_radius
            )
            .cut(
                cq.Workplane("XY")
                .cylinder(
                    outside_radius * 2,
                    crown_radius
                )
            )
            .translate((0, 0, outside_radius * z_scale / 2))
        )

        petal_volume = sector.intersect(outer_ring)

        petal_piece = head_shell.intersect(
            petal_volume.val()
        )

        solids.append(petal_piece)

    return solids
