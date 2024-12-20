from fastapi import FastAPI, Depends
from .config.db import create_db_and_tables
from .controllers.user_controller import router as user_router
import uvicorn

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(user_router)

@app.get("/")
def read_root():
    return {"Hello": "World"}

def run():
    uvicorn.run("src.main:app", host="127.0.0.1", port=8000, reload=True)
