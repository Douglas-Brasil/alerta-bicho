import numpy as np
from PIL import Image, ImageOps
import tensorflow as tf

def start_model(model_path='/model/keras_model.h5', labels_path='labels.txt'):
     """Carrega o modelo e os rótulos uma única vez na inicialização."""
     global model, class_names

     if model is None:
          print('Carregando o modelo...')
          model = tf.keras.models.load_model(model_path)

     with open(labels_path, 'r', encoding='utf-8') as f:
          # O arquivo labels.txt geralmente inclui índices (ex: "0 Gato"),
          # então limpamos o texto para pegar apenas o nome da classe.
          class_names = [line.strip().split(' ', 1)[-1] for line in f.readlines()]
     print('Modelo carregado com sucesso!')


def classify_image(image_file):
     """Classifica a imagem utilizando o modelo já carregado."""
     global model, class_names

     if model is None or not class_names:
          raise RuntimeError(
               "O modelo ainda não foi carregado. Chame a função 'start_model()'"
               ' primeiro.'
          )

     # Cria um array no formato exigido pelo modelo (1, 224, 224, 3)
     data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

     # Abre a imagem usando o Pillow
     image = Image.open(image_file).convert('RGB')

     # Redimensiona e corta a imagem para o tamanho padrão da Teachable Machine (224x224)
     size = (224, 224)
     image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

     # Converte a imagem em um array numpy
     image_array = np.asarray(image)

     # Normaliza a imagem para a escala esperada pelo modelo (-1 a 1)
     normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

     # Insere a imagem normalizada no array de dados
     data[0] = normalized_image_array

     # Realiza a predição
     prediction = model.predict(data)
     index = np.argmax(prediction)
     class_name = class_names[index]
     confidence_score = float(prediction[0][index])

     return {
          'class': class_name,
          'confidence': round(confidence_score * 100, 2),  # Porcentagem
     }