import json
from pathlib import Path

import cadquery as cq

from app.schema.project import Project
from app.geometry.cylinder_builder import build_cylinder


BASE_DIR = Path(__file__).resolve().parent

INPUT_FILE = BASE_DIR.parent / "examples" / "simple_vessel.json"
OUTPUT_FILE = BASE_DIR.parent / "outputs" / "simple_vessel.step"


with open(INPUT_FILE) as f:
    data = json.load(f)

project = Project(**data)

from app.geometry.dispatcher import build_component

all_geometry = []

for component in project.components:

    geometry = build_component(component)

    all_geometry.extend(geometry)

assembly = cq.Assembly()

for i, segment in enumerate(all_geometry):
    assembly.add(segment, name=f"segment_{i+1}")

assembly.save(str(OUTPUT_FILE))

print(f"STEP file generated: {OUTPUT_FILE}")
