@echo off


call venv\Scripts\activate

start uvicorn api.main:app --host localhost --port 8001 --reload
pause