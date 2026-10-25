from fastapi import FastAPI
from src.routes import router
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()

app.mount("/static", StaticFiles(directory="src/static"), name="static")

app.include_router(router)


