# Script: ensamblar_video_ffmpeg.py
# Ensambla imágenes, audio y subtítulos en un video usando FFmpeg
# Uso: python ensamblar_video_ffmpeg.py imagen_generada.png audio_generado.mp3 subtitulos.srt

import sys
import os

imagen = sys.argv[1] if len(sys.argv) > 1 else "imagen_generada.png"
audio = sys.argv[2] if len(sys.argv) > 2 else "audio_generado.mp3"
subtitulos = sys.argv[3] if len(sys.argv) > 3 else "subtitulos.srt"

output = "video_final.mp4"

# Comando FFmpeg para unir imagen, audio y subtítulos
cmd = f"ffmpeg -y -loop 1 -i {imagen} -i {audio} -vf subtitles={subtitulos} -c:v libx264 -tune stillimage -c:a aac -b:a 192k -shortest -pix_fmt yuv420p {output}"

print("Ejecutando:", cmd)
os.system(cmd)
print("Video generado:", output)
