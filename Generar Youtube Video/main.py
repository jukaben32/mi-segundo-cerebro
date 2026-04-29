# Script maestro: main.py
# Ejecuta todo el flujo automático para generar un short de YouTube
# Uso: python main.py "prompt o tema"


import os
import sys
import subprocess
from tools.logger import log

def run_step(cmd, desc):
    log(f"Iniciando: {desc}")
    try:
        subprocess.run(cmd, check=True)
        log(f"Completado: {desc}")
    except Exception as e:
        log(f"Error en {desc}: {e}")
        sys.exit(1)

prompt = sys.argv[1] if len(sys.argv) > 1 else "Crea un guion para un video viral de finanzas."

# 1. Generar guion
run_step(["python", "tools/generar_guion_gemini.py", prompt], "Generar guion con Gemini")

# 2. Generar imagen
run_step(["python", "tools/generar_imagenes_gemini.py", "Ilustración estilo stickman sobre finanzas"], "Generar imagen con Gemini")

# 3. Generar audio
with open("guion.txt", encoding="utf-8") as f:
    texto_guion = f.read()
run_step(["python", "tools/generar_audio_gemini.py", texto_guion], "Generar audio con Gemini")

# 4. Generar subtítulos
run_step(["python", "tools/generar_subtitulos_whisper.py", "audio_generado.mp3"], "Generar subtítulos con Whisper")

# 5. Ensamblar video
run_step(["python", "tools/ensamblar_video_ffmpeg.py", "imagen_generada.png", "audio_generado.mp3", "subtitulos.srt"], "Ensamblar video final con FFmpeg")

log("✅ ¡Video generado automáticamente! Revisa el archivo video_final.mp4")
