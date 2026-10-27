from pathlib import Path
import numpy as np
from PIL import Image, ImageOps
from ai_edge_litert.interpreter import Interpreter
from src.models.auth import AuthSupaBase
from fastapi import FastAPI, File, UploadFile
from src.models.AI import get_animal_by_id

# Diretório onde este arquivo está localizado
BASE_DIR = Path(__file__).resolve().parent.parent

# Variáveis globais
# Confiança mínima (%) para aceitar a classificação
MIN_CONFIDENCE = 85

model = None
class_names = []
input_details = None
output_details = None


def classify(file: UploadFile = File(...)):
    try:
        start_model()
        resultado = classify_image(file.file)

        print("Resultado da classificação:", resultado)

        if resultado["confidence"] < MIN_CONFIDENCE:
            return {
                "success": False,
                "low_confidence": True,
                "confidence": resultado["confidence"],
                "error": "Não consegui identificar o animal com segurança. "
                         "Tente outra foto, com boa luz e o animal bem visível."
            }

        animal = get_animal_by_id(int(resultado["class"]))

        return {
            "success": True,
            "prediction": animal
        }

    except Exception as e:
        print("Erro ao classificar imagem:", repr(e))
        return {
            "success": False,
            "error": str(e)
        }

def start_model():
    """Carrega o modelo TensorFlow Lite e os rótulos das classes."""
    global model, class_names, input_details, output_details

    if model is None:
        model_path = BASE_DIR / "AI" / "model_unquant.tflite"
        labels_path = BASE_DIR / "AI" / "labels.txt"

        print(f"Carregando modelo de: {model_path}")

        if not model_path.exists():
            raise FileNotFoundError(
                f"Arquivo do modelo não encontrado em: {model_path}"
            )

        if not labels_path.exists():
            raise FileNotFoundError(
                f"Arquivo de rótulos não encontrado em: {labels_path}"
            )

        # Inicializa o interpretador TensorFlow Lite
        model = Interpreter(model_path=str(model_path))
        model.allocate_tensors()

        input_details = model.get_input_details()
        output_details = model.get_output_details()

        # Carrega os nomes das classes
        with open(labels_path, "r", encoding="utf-8") as f:
            class_names = [
                line.strip().split(" ", 1)[-1]
                for line in f
                if line.strip()
            ]

        print("Modelo carregado com sucesso!")


def classify_image(image_file):
    """Classifica uma imagem utilizando o modelo TensorFlow Lite."""
    global model, class_names, input_details, output_details

    if model is None:
        start_model()

    # Abre e prepara a imagem
    image = Image.open(image_file).convert("RGB")

    image = ImageOps.fit(
        image,
        (224, 224),
        method=Image.Resampling.LANCZOS
    )

    # Normaliza os pixels entre -1 e 1
    image_array = np.asarray(image, dtype=np.float32)
    normalized_image_array = (image_array / 127.5) - 1

    # Adiciona a dimensão do lote: (1, 224, 224, 3)
    data = np.expand_dims(normalized_image_array, axis=0)

    # Executa a classificação
    model.set_tensor(input_details[0]["index"], data)
    model.invoke()

    prediction = model.get_tensor(output_details[0]["index"])[0]

    # Obtém a classe com maior probabilidade
    index = int(np.argmax(prediction))
    class_name = class_names[index]
    confidence_score = float(prediction[index])

    return {
        "class": class_name,
        "confidence": round(confidence_score * 100, 2)
    }

