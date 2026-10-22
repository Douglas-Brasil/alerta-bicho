from fastapi import FastAPI, File, UploadFile
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



@app.post("/model")
async def classify(file: UploadFile = File(...)):
    try:
        start_model()
        resultado = classify_image(file.file)

        print("Resultado da classificação:", resultado)

        return {
            "success": True,
            "prediction": resultado
        }

    except Exception as e:
        print("Erro ao classificar imagem:", repr(e))
        return {
            "success": False,
            "error": str(e)
        }
