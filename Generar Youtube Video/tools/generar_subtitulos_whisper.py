# Script: generar_subtitulos_whisper.py
# Genera subtítulos usando Whisper (requiere modelo descargado)
# Uso: python generar_subtitulos_whisper.py audio_generado.mp3

import sys
import os

# Instala openai-whisper si no lo tienes: pip install -U openai-whisper
import whisper

modelo = os.getenv('WHISPER_MODEL_PATH', 'small')
archivo_audio = sys.argv[1] if len(sys.argv) > 1 else "audio_generado.mp3"

model = whisper.load_model(modelo)
result = model.transcribe(archivo_audio)

with open("subtitulos.srt", "w", encoding="utf-8") as f:
    f.write(result["text"])
print("Subtítulos generados: subtitulos.srt")
