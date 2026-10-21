from fastapi import FastAPI
from fastapi.responses import FileResponse
from pathlib import Path

app = FastAPI()
BASE_DIR = Path(__file__).resolve().parent
FILE_PATH = BASE_DIR / "home.html"

@app.get("/")
async def root():
     return FileResponse(FILE_PATH)
