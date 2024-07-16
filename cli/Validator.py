from jsonschema import Draft7Validator, ValidationError


class Validator:
    def __init__(self, schema):
        self.validator = Draft7Validator(schema)

    def validate(self, data):
        try:
            self.validator.validate(data)
        except ValidationError as e:
            raise ValueError(f"Ошибка валидации JSON Schema: {e.message}")
