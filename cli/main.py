from ModelGenerator import ModelGenerator
from RouterGenerator import RouterGenerator
from jsonschema import Draft7Validator, exceptions
import click
import json
from json import JSONDecodeError
import os
from create_database import *
import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))


@click.group()
def main():
    pass

@main.command(help="Генерация моделей Pydantic из файла JSON Schema")
@click.option('--json-schema', type=click.Path(exists=True), required=True, help="Маршрут до файла JSON Schema")
def gen_models(json_schema):

    try:
        with open(json_schema, 'r') as f:
            schema = json.load(f)
        Draft7Validator.check_schema(schema)
    except exceptions.SchemaError as e:
        click.echo(f"Ошибка валидации JSON Schema: {e.message}")
        return
    except JSONDecodeError as e:
        click.echo(f"Ошибка открытия JSON Schema: {str(e)}")
        return

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


@main.command(help="Генерация REST контроллеров для всех моделей, созданных из JSON Schema")
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
@main.command(help="Присваивание тега новой версии приложения")
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


@main.command(help="Создание базы данных")
@click.option('--user', prompt='Имя пользователя', help='Имя пользователя для подключения к БД')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='Пароль для подключения к БД')
@click.option('--host', prompt='Хост', default='localhost', show_default=True, help='Хост БД')
@click.option('--port', prompt='Порт', default='5432', show_default=True, help='Порт БД')
@click.option('--dbname', prompt='Имя базы данных', help='Имя новой базы данных')
def create_db(user, password, host, port, dbname):
    create_database(user, password, host, port, dbname)
    write_to_env_file(user, password, host, port, dbname)

    from dotenv import load_dotenv
    load_dotenv()

    from api.database import Base, engine
    Base.metadata.create_all(bind=engine)

    subprocess.run(['alembic', 'revision', f'--message="Initial migration"', '--autogenerate'], check=True)
    click.echo("Первая миграция базы данных успешно создана")
    subprocess.run(['alembic', 'upgrade', 'head'], check=True)
    click.echo("Первая миграция базы данных успешно применена")


@main.command(help="Создание новой миграции alembic")
@click.option('--message', prompt='Описание миграции', help='Описание миграции')
def migrate(message):
    subprocess.run(['alembic', 'revision', f'--message={message}', '--autogenerate'], check=True)
    click.echo("Миграция базы данных успешно создана")

@main.command(help="Применение всех миграций alembic")
def upgrade():
    subprocess.run(['alembic', 'upgrade', 'head'], check=True)
    click.echo("Миграция базы данных успешно применена")



if __name__ == '__main__':
    main()