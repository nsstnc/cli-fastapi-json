class ModelGenerator:
    def __init__(self, schema):
        self.schema = schema

    def create_pydantic_model_code(self, schema, model_name='root'):
        kind = schema.get('properties', {}).get('kind', {}).get('default', model_name)

        nested_models = []

        def get_field_type(property, model_name, parent_name=""):
            property_type = property.get('type')

            if property_type == 'string':
                max_length = property.get('maxLength')
                pattern = property.get('pattern')
                if max_length and pattern:
                    return f"str = Field(max_length={max_length}, regex=r'{pattern}')"
                elif pattern:
                    return f"str = Field(regex=r'{pattern}')"
                elif max_length:
                    return f"str = Field(max_length={max_length})"
                else:
                    return 'str'
            elif property_type == 'integer':
                return 'int'
            elif property_type == 'number':
                return 'float'
            elif property_type == 'boolean':
                return 'bool'
            elif property_type == 'array':
                items = property.get('items', {})
                item_type = get_field_type(items, model_name)
                return f"List[{item_type}]"
            elif property_type == 'object':
                if 'properties' in property:
                    nested_model_name = f"{model_name}_{parent_name.capitalize()}"
                    nested_models.append((nested_model_name, property))
                    return nested_model_name
                else:
                    return 'Dict[str, Any]'
            else:
                return 'Any'

        def generate_model_code(model_name, schema):
            fields = []
            for name, property in schema.get('properties', {}).items():
                field_type = get_field_type(property, model_name, name)
                required = name in schema.get('required', [])
                field_declaration = f"{name}: {field_type}"
                if not required:
                    field_declaration += " = None"
                fields.append(field_declaration)

            model_code = f"class {model_name}(BaseModel):\n"
            for field in fields:
                model_code += f"    {field}\n"

            return model_code

        main_model_code = generate_model_code(kind, schema)

        all_models_code = [main_model_code]
        for nested_model_name, nested_schema in nested_models:
            all_models_code.append(generate_model_code(nested_model_name, nested_schema))

        return (kind,
                (f"from pydantic import BaseModel, Field\n"
                 f"from typing import *\n") +
                "\n\n".join(all_models_code[::-1]))
