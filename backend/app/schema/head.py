from pydantic import BaseModel
from typing import List


class HeadGeometry(BaseModel):
    inside_diameter: float
    nominal_thickness: float


class CrownPiece(BaseModel):
    type: str
    diameter_percent: float


class Petal(BaseModel):
    id: str
    start_angle: float
    sweep_angle: float


class HeadFabrication(BaseModel):
    crown: CrownPiece
    petals: List[Petal]


class HeadComponent(BaseModel):
    id: str
    type: str

    role: str

    head_type: str

    geometry: HeadGeometry

    fabrication: HeadFabrication

    material_id: str
