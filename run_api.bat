@echo off


call venv\Scripts\activate



uvicorn api.main:app --host localhost --port 8000 --reload
pause