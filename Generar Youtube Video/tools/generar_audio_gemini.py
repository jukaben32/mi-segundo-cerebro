# Script: generar_audio_gemini.py
# Genera audio narrado usando la API de Gemini (requiere endpoint TTS)
# Uso: python generar_audio_gemini.py "Texto a narrar"

import os
import sys
import requests

API_KEY = os.getenv('GEMINI_API_KEY')
ENDPOINT = "https://texttospeech.googleapis.com/v1/text:synthesize?key=" + API_KEY

texto = sys.argv[1] if len(sys.argv) > 1 else "Texto de ejemplo para narrar."

headers = {"Content-Type": "application/json"}
data = {
    "input": {"text": texto},
    "voice": {"languageCode": "es-ES", "ssmlGender": "NEUTRAL"},
    "audioConfig": {"audioEncoding": "MP3"}
}

response = requests.post(ENDPOINT, headers=headers, json=data)
if response.ok:
    audio_content = response.json()['audioContent']
    import base64
    with open("audio_generado.mp3", "wb") as f:
        f.write(base64.b64decode(audio_content))
    print("Audio generado: audio_generado.mp3")
else:
    print("Error al generar audio:", response.text)
