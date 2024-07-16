class ModelGenerator:
    def __init__(self, schema):
        self.schema = schema

    def create_pydantic_model_code(self, schema):
        kind = schema.get('properties', {}).get('kind', {}).get('default', 'DefaultModelName')

        fields = []

        for name, property in self.schema.get('properties', {}).items():
            type = property.get('type')
            constraints = []

            if type == 'string':
                max_length = property.get('maxLength')
                pattern = property.get('pattern')
                if max_length:
                    constraints.append(f"constr(max_length={max_length})")
                if pattern:
                    constraints.append(f"constr(regex=r'{pattern}')")
                if not constraints:
                    type = 'str'
                else:
                    type = ' | '.join(constraints)
            elif type == 'integer':
                type = 'int'
            elif type == 'number':
                type = 'float'
            elif type == 'boolean':
                type = 'bool'
            elif type == 'array':
                type = 'list'
            elif type == 'object':
                type = 'dict'
            else:
                type = 'Any'

            required = name in schema.get('required', [])
            field_declaration = f"{name}: {type}"
            if not required:
                field_declaration += " = None"

            fields.append(field_declaration)

        model_code = (f"from pydantic import BaseModel, constr\n"
                      f"from typing import *\n"
                      f"class {kind}(BaseModel):\n")
        for field in fields:
            model_code += f"    {field}\n"

        return kind, model_code
