from pydantic import BaseModel, Field
from typing import *
class MyKind(BaseModel):
    kind: str = Field(max_length=32)
    name: str = Field(max_length=128)
    version: str = Field(pattern=r'^\d+\.\d+\.\d+(-[a-zA-Z0-9]+(\.[a-zA-Z0-9]+)*)?(\+[a-zA-Z0-9]+(\.[a-zA-Z0-9]+)*)?$')
    description: str = Field(max_length=4096)
    configuration: dict
