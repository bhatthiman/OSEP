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

component = project.components[0]

segments = build_cylinder(component)

assembly = cq.Assembly()

for i, segment in enumerate(segments):
    assembly.add(segment, name=f"segment_{i+1}")

assembly.save(str(OUTPUT_FILE))

print(f"STEP file generated: {OUTPUT_FILE}")
