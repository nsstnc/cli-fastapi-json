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
        click.echo(f"Создана модель {filename}")
        # TODO включить применение изменений в репозиторий гит
        # commit_changes(f"Created model {filename}")
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

    created_routers = []

    for filename in os.listdir(models_path):
        if filename.endswith('.py'):
            model_name = filename[:-3]
            generator = RouterGenerator(model_name)
            code = generator.render_router()
            with open(f'{routers_path}/{model_name}.py', 'w') as f:
                f.write(code)
            click.echo(f"Создан роутер {model_name}")
            created_routers.append(model_name)
    # TODO включить применение изменений в репозиторий гит
    # commit_changes("Created REST routers: " + ", ".join(created_routers))


import subprocess
@main.command()
@click.argument('version')
def create_tag(version):
    try:
        subprocess.run(['git', 'tag', version], check=True)
        subprocess.run(['git', 'push', 'origin', version], check=True)
        click.echo(f"Создан и отправлен тег: {version}")
    except subprocess.CalledProcessError as e:
        click.echo(f"Ошибка во время создания тега: {e}")

def commit_changes(message):
    try:
        subprocess.run(['git', 'add', '.'], check=True)
        subprocess.run(['git', 'commit', '-m', message], check=True)
        subprocess.run(['git', 'push'], check=True)
        click.echo("Изменения отправлены в удаленный репозиторий")
    except subprocess.CalledProcessError as e:
        click.echo(f"Ошибка выполнения команд Git: {e}")

if __name__ == '__main__':
    main()