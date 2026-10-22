from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from model import start_model, classify_image

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent

# 1. Monta a pasta 'view' para servir arquivos estáticos (CSS, JS, etc.)
app.mount("/view", StaticFiles(directory=str(BASE_DIR / "view")), name="view")

@app.get("/")
async def root():
    # Retorna o arquivo HTML que agora está dentro da pasta view
    return FileResponse(BASE_DIR / "view" / "home.html")

from fastapi import FastAPI, File, UploadFile

app = FastAPI()


# 1. Carrega o modelo ao iniciar a aplicação (substitua pelo seu arquivo principal)
# start_model()


@app.post("/model")
async def model(file: UploadFile = File(...)):
  start_model()
  try:
    resultado = classify_image(file.file)
    return {'success': True, 'prediction': resultado}

  except Exception as e:
    return {'success': False, 'error': str(e)}