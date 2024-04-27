from pydantic import BaseModel, constr
from typing import List

class CheckValues(BaseModel):
    values: List[constr(max_length=256, strip_whitespace=True)]
    
    class Config:
        max_items = 1024

class Rule(BaseModel):
    class Config:
        extra='allow'