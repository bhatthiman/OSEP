import cadquery as cq

def create_vessel():
    shell = (
        cq.Workplane("XY")
        .cylinder(3000, 1000)
    )

    top_head = (
        cq.Workplane("XY")
        .sphere(1000)
        .translate((0, 0, 1500))
    )

    bottom_head = (
        cq.Workplane("XY")
        .sphere(1000)
        .translate((0, 0, -1500))
    )

    vessel = shell.union(top_head).union(bottom_head)

    return vessel


if __name__ == "__main__":
    vessel = create_vessel()

    cq.exporters.export(vessel, "vessel.step")

    print("STEP file generated: vessel.step")
