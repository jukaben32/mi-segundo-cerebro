# Script: generar_guion_gemini.py
# Genera un guion usando la API de Gemini
# Uso: python generar_guion_gemini.py "Tu prompt aquí"

import os
import sys
import requests

API_KEY = os.getenv('GEMINI_API_KEY')
ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=" + API_KEY

prompt = sys.argv[1] if len(sys.argv) > 1 else "Crea un guion para un video viral de finanzas."

headers = {"Content-Type": "application/json"}
data = {"contents": [{"parts": [{"text": prompt}]}]}

response = requests.post(ENDPOINT, headers=headers, json=data)
if response.ok:
    result = response.json()
    guion = result['candidates'][0]['content']['parts'][0]['text']
    print("Guion generado:\n", guion)
    with open("guion.txt", "w", encoding="utf-8") as f:
        f.write(guion)
else:
    print("Error al generar guion:", response.text)
