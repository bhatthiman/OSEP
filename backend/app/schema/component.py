from pydantic import BaseModel
from typing import Dict, Any


class Component(BaseModel):
    id: str
    type: str
    data: Dict[str, Any]
