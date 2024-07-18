from pydantic import BaseModel, Field
from typing import *
class mykind_Configuration(BaseModel):
    specification: Dict[str, Any]
    settings: Dict[str, Any]


class mykind(BaseModel):
    kind: str = Field(max_length=32)
    name: str = Field(max_length=128)
    version: str = Field(regex=r'^\d+\.\d+\.\d+(-[a-zA-Z0-9]+(\.[a-zA-Z0-9]+)*)?(\+[a-zA-Z0-9]+(\.[a-zA-Z0-9]+)*)?$')
    description: str = Field(max_length=4096)
    configuration: mykind_Configuration
