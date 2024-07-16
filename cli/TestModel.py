from pydantic import BaseModel
from typing import *
class TestModel(BaseModel):
    name: str
    age: int
    address: dict = None
    hobbies: list = None
