from pydantic import BaseModel, constr
from typing import *
class MyKind(BaseModel):
    kind: constr(max_length=32)
    name: constr(max_length=128)
    version: constr(regex=r'^\d+\.\d+\.\d+(-[a-zA-Z0-9]+(\.[a-zA-Z0-9]+)*)?(\+[a-zA-Z0-9]+(\.[a-zA-Z0-9]+)*)?$')
    description: constr(max_length=4096)
    configuration: dict
