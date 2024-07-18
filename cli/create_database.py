import click
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def create_database(user, password, host, port, dbname):
    try:
        connection = psycopg2.connect(user=user,
                                      password=password,
                                      host=host,
                                      port=port,
                                      database="postgres")

        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        cursor = connection.cursor()
        create_db_query = f"CREATE DATABASE {dbname};"
        cursor.execute(create_db_query)
        cursor.close()
        connection.close()
        print(f"База данных {dbname} создана")
    except Exception as error:
        print(f"Ошибка при создании базы данных: {error}")

def write_to_env_file(user, password, host, port, dbname):
    connection_string = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
    with open(".env", "w") as env_file:
        env_file.write(f"DATABASE_URL={connection_string}")
    print(f"Строка подключения записана в .env")