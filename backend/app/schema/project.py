from pydantic import BaseModel
from typing import List

from app.schema.component import Component


class ProjectInfo(BaseModel):
    name: str


class Project(BaseModel):
    project: ProjectInfo
    components: List[Component]
