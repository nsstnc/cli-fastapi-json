source venv/bin/activate

uvicorn api.main:app --host localhost --port 8001 --reload
