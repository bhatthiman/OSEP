from pydantic import BaseModel
from typing import List


class Plate(BaseModel):
    id: str
    start_angle: float
    sweep_angle: float


class CylinderGeometry(BaseModel):
    inside_diameter: float
    length: float
    nominal_thickness: float


class CylinderSegment(BaseModel):
    id: str
    geometry: CylinderGeometry
    material_id: str
    plates: List[Plate]


class CylinderComponent(BaseModel):
    id: str
    type: str
    role: str
    segments: List[CylinderSegment]
