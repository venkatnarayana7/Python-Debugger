from pydantic import BaseModel
from typing import List

class FixPacket(BaseModel):
    reproduction_script: str
    candidates: List[str]
