from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent

# 1. Monta a pasta 'view' para servir arquivos estáticos (CSS, JS, etc.)
app.mount("/view", StaticFiles(directory=str(BASE_DIR / "view")), name="view")

@app.get("/")
async def root():
    # Retorna o arquivo HTML que agora está dentro da pasta view
    return FileResponse(BASE_DIR / "view" / "home.html")