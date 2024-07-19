@echo off


call venv\Scripts\activate



uvicorn api.main:app --host localhost --port 8001 --reload
pause