# Generador Automático de Shorts para YouTube

Este sistema te permite crear videos cortos (shorts) de YouTube de forma 100% automática, usando inteligencia artificial (Gemini, Whisper) o solo edición con FFmpeg, según tus necesidades y presupuesto.

## Estructura del Proyecto

- **tools/**: Scripts para cada tarea (guion, imágenes, audio, video, subtítulos).
- **flows/**: Flujos completos (con IA, sin IA, híbrido).
- **plantillas/**: Ejemplos de prompts, imágenes y audios.
- **config/**: Ejemplo de archivo de configuración.

## Requisitos
- Python 3.11+
- Poetry
- FFmpeg
- Whisper (y modelo GGML Small)
- API Key de Gemini (Google AI Studio)

## Instalación Rápida
1. Clona el repositorio.
2. Instala dependencias con Poetry y FFmpeg.
3. Copia el archivo de ejemplo de configuración y agrega tu API Key de Gemini.

## Flujos Disponibles
- **Con IA:** Genera guion, imágenes, audio, subtítulos y ensambla el video automáticamente.
- **Sin IA:** Usa imágenes y audio propios, y FFmpeg para crear videos virales sin gastar créditos de IA.
- **Híbrido:** Elige qué partes automatizar con IA y cuáles con recursos propios.


## Ejecución paso a paso

### Opción 1: Usar el script maestro (recomendado)

1. Instala dependencias:
	```
	pip install -r requirements.txt
	```
2. (Opcional) Activa tu entorno virtual o usa `poetry shell` si prefieres Poetry.
3. Copia tu API Key de Gemini en `config/ejemplo_config.env` y renómbralo a `.env` si lo deseas.
4. Ejecuta el flujo completo con:
	```
	python main.py "Crea un guion para un video viral de finanzas"
	```
	Puedes cambiar el texto entre comillas por el tema que quieras.

### Opción 2: Ejecutar cada paso manualmente

1. Genera el guion:
	```
	python tools/generar_guion_gemini.py "Crea un guion para un video viral de terror"
	```
2. Genera la imagen:
	```
	python tools/generar_imagenes_gemini.py "Ilustración estilo terror"
	```
3. Genera el audio:
	```
	python tools/generar_audio_gemini.py "(Pega aquí el guion generado)"
	```
4. Genera los subtítulos:
	```
	python tools/generar_subtitulos_whisper.py audio_generado.mp3
	```
5. Ensambla el video:
	```
	python tools/ensamblar_video_ffmpeg.py imagen_generada.png audio_generado.mp3 subtitulos.srt
	```

### Opción 3: Usar Makefile (si tienes make instalado)

```
make run
```

### Opción 4: Test automático

Ejecuta el test básico para validar el flujo:
```
python tests/test_flujo_basico.py
```

---

## Subir el video automáticamente a YouTube

1. Configura tus credenciales de Google (ver instrucciones en tools/subir_a_youtube.py).
2. Ejecuta:
	```
	python tools/subir_a_youtube.py video_final.mp4 "Título del video" "Descripción del video"
	```

---

## Consejos
- Si tienes errores, revisa el archivo log.txt para ver en qué paso falló.
- Puedes cambiar imágenes y audios de ejemplo en las carpetas plantillas/imagenes_ejemplo y plantillas/audios_ejemplo.
- Integra con n8n siguiendo la guía en README_EXTRA.md.

---

## ¿Cómo cambiar el estilo del contenido?
- Cambia las imágenes de referencia en `plantillas/imagenes_ejemplo/`.
- Cambia la música en `plantillas/audios_ejemplo/`.
- Modifica los prompts en `plantillas/prompts_finanzas.txt` o crea nuevos.

---

## Créditos y Licencia
Proyecto de código abierto inspirado en los sistemas de Hans1801 y la comunidad de automatización de contenido.
