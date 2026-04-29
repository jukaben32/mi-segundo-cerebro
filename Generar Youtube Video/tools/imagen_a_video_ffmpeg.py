# Script: imagen_a_video_ffmpeg.py
# Convierte una imagen y un audio en un video dinámico con efectos usando FFmpeg
# Uso: python imagen_a_video_ffmpeg.py imagen.png audio.mp3

import sys
import os

imagen = sys.argv[1] if len(sys.argv) > 1 else "plantillas/imagenes_ejemplo/ejemplo.png"
audio = sys.argv[2] if len(sys.argv) > 2 else "plantillas/audios_ejemplo/ejemplo.mp3"
output = "video_dinamico.mp4"

# Comando FFmpeg con zoom y rotación
cmd = f"ffmpeg -y -i {imagen} -i {audio} -filter_complex \"zoompan=z='min(zoom+0.0015,1.5)':d=125,rotate=0.05*t:c=none\" -c:v libx264 -c:a aac -b:a 192k -shortest -pix_fmt yuv420p {output}"

print("Ejecutando:", cmd)
os.system(cmd)
print("Video generado:", output)
