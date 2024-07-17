from Validator import Validator
from ModelGenerator import ModelGenerator

import click
import json
import os



@click.group()
def main():
    pass

@main.command()
@click.option('--json-schema', type=click.Path(exists=True), required=True, help="Маршрут до файла JSON Schema")
def gen_models(json_schema):
    with open(json_schema, 'r') as f:
        schema = json.load(f)

    generator = ModelGenerator(schema)
    filename, model_code = generator.create_pydantic_model_code(generator.schema)
    try:
        with open(f"api/models/{filename}.py", 'w') as file:
            file.write(model_code)
    except:
        print("Не удалось сохранить файл модели")


@main.command()
def gen_rest():
    models_path = 'api/models/'

if __name__ == '__main__':
    main()