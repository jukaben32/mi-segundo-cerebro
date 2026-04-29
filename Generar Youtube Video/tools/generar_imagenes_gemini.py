# Script: generar_imagenes_gemini.py
# Genera imágenes usando la API de Gemini Imagen (requiere endpoint específico)
# Uso: python generar_imagenes_gemini.py "Descripción de la imagen"

import os
import sys
import requests

API_KEY = os.getenv('GEMINI_API_KEY')
ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro-vision:generateImage?key=" + API_KEY

descripcion = sys.argv[1] if len(sys.argv) > 1 else "Ilustración estilo stickman sobre finanzas."

headers = {"Content-Type": "application/json"}
data = {"prompt": descripcion}

response = requests.post(ENDPOINT, headers=headers, json=data)
if response.ok:
    with open("imagen_generada.png", "wb") as f:
        f.write(response.content)
    print("Imagen generada: imagen_generada.png")
else:
    print("Error al generar imagen:", response.text)
