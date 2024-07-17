from Validator import Validator
from ModelGenerator import ModelGenerator
from RouterGenerator import RouterGenerator

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
    routers_path = 'api/routers/'

    if not os.path.exists(routers_path):
        os.makedirs(routers_path)

    if not os.path.exists(models_path):
        os.makedirs(models_path)

    for filename in os.listdir(models_path):
        if filename.endswith('.py'):
            model_name = filename[:-3]
            generator = RouterGenerator(model_name)
            code = generator.render_router()
            with open(f'{routers_path}/{model_name}.py', 'w') as f:
                f.write(code)

if __name__ == '__main__':
    main()