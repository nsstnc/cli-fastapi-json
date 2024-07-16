from pydantic import BaseModel

class TestModel(BaseModel):
    name: str
    age: int
    address: Any = None
    hobbies: list = None
