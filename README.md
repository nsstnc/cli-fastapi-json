# CLI генератор Pydantic моделей и REST API контроллеров

## Обзор
Проект включает в себя CLI приложение, которое предоставляет набор инструментов для разработки и управления FastAPI проектом. Он же в свою очередь предоставляет интерфейс для взаимодействия с базой данных и системой сообщений.



## Возможности

CLI приложение позволяет:
- Генерировать Pydantic модели на основе их описания в виде JSON Schema
- Генерировать код контроллеров FastAPI REST приложения
- Создавать базу данных PostgresSQL
- Задавать конфигурацию заранее подготовленного RabbitMQ сервера, на который будут отправляться сообщения
- Создавать и применять миграции базы данных с помощью Alembic
- Сохранять изменения в удаленном репозитории Git
- Присваивать новую версию (tag) проекту с помощью Git


REST FastAPI приложение позволяет:
- Автоматически отправлять сообщения в брокер RabbitMQ после выполнения POST, PUT и DELETE запросов
- Добавлять в базу данных JSON документы, валидные к моделям, которые были сгенерированы через CLI приложение
- Изменять записи в базе данных
- Удалять записи из базы данных

## Стек технологий

- **Backend**: Python, FastAPI, PostgreSQL, SQLAlchemy, Alembic, Click, Pydantic, RabbitMQ
- **Frontend**: FastAPI Swagger

## Установка

1. Клонировать репозиторий

    ```bash
    git clone https://github.com/nsstnc/cli-fastapi-json.git
    cd cli-fastapi-json
    ```

2. Настроить виртуальное окружение

    ```bash
    python3 -m venv venv  # `python -m venv venv` на Windows
    ```
   ```bash
    venv/bin/activate  # `venv/Scripts/activate` на Windows
    ```
3. Установить зависимости

   ```bash
    pip install -r requirements.txt
    ```

## Использование





## Принцип работы приложений


## Архитектура проекта


## Файловая структура
```
cli-fastapi-json/  
├── markdown-images/ # Папка с изображениями для README.md файла  
├── alembic/ # Папка с файлами alembic  
   └── versions/ # Миграции alembic
   └── env.py # Основной файл конфигурации Alembic
   └── README
   └── script.py.mako # Шаблон для новых файлов миграций
├── api/ # Директория FastAPI приложения
   └── models/ # Папка с Pydantic моделями
   └── routers/ # Папка с контроллерами REST API
   └── database.py # Файл с настройкой подключения к БД и генератором сессий
   └── db_models.py # SQLAlchemy модели для таблиц БД
   └── main.py # Основной файл FastAPI приложения
   └── rabbitmq.py # Файл с настройкой подключения к RabbitMQ и методами для отправки сообщений
├── cli/ # Директория CLI приложения
   └── create_database.py # Скрипт, для создания базы данных PostgreSQL
   └── main.py # Основной файл CLI приложения
   └── ModelGenerator.py # Класс-генератор моделей Pydantic
   └── router_template.py.jinja # Jinja шаблон контроллеров для FastAPI приложения
   └── RouterGenerator.py # Класс-генератор контроллеров FastAPI
├── venv/ # Файлы виртуального окружения
├── .env # Файл с переменными окружения (записан в .gitignore и создается автоматически)  
├── .gitignore
├── alembic.ini # Конфигурация alembic
├── README.md # Документация
├── requirements.txt # Файл с зависимостями
├── run_api.bat # Скрипт для запуска приложения Fast API на Windows
├── run_api.sh # Скрипт для запуска приложения Fast API на UNIX-системах
```
