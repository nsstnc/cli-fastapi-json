from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import importlib
import os
from api.database import Base, engine

app = FastAPI(
    title="cli-fastapi-json",
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def include_all_routers(app, routers_dir):

    for filename in os.listdir(routers_dir):
        if filename.endswith('.py') and filename != '__init__.py':
            module_name = filename[:-3]

            module = importlib.import_module(f'api.routers.{module_name}')

            if hasattr(module, 'router'):
                app.include_router(module.router)


include_all_routers(app, 'api/routers')



@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    import uvicorn


    Base.metadata.create_all(bind=engine)
    uvicorn.run(app, host="localhost", port=8000)
