from pydantic import BaseModel
from typing import List

from app.schema.cylinder import CylinderComponent


class ProjectInfo(BaseModel):
    name: str


class Project(BaseModel):
    project: ProjectInfo
    components: List[CylinderComponent]
