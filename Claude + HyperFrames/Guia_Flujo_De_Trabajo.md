# Flujo de Trabajo: Edición de Video con Claude Code, HyperFrames y video-use

Esta guía detalla el proceso completo para automatizar la edición de videos y la creación de gráficos en movimiento (motion graphics) utilizando inteligencia artificial, basándose en la transcripción del video.

## 🛠️ Stack Tecnológico

1.  **Claude Code**: El "Cerebro" u orquestador de todo el proceso. Se puede usar a través de la aplicación de escritorio de Claude o como extensión en VS Code.
2.  **video-use**: Herramienta encargada de analizar el video sin procesar, identificar errores, pausas y palabras de relleno, y recortarlos automáticamente.
3.  **HyperFrames** (o alternativamente **Remotion**): Motor para generar gráficos en movimiento y animaciones (como tarjetas de cristal líquido o subtítulos estilo karaoke) utilizando HTML/CSS.
4.  **11 Labs API / OpenAI Whisper API**: Motor de transcripción para obtener los tiempos exactos (timestamps) palabra por palabra, lo cual es crítico para sincronizar las animaciones.

## 🚀 Configuración Inicial

1.  Instala **Claude Desktop App** (o usa VS Code si prefieres ver todos tus archivos).
2.  Clona o proporciona a Claude los repositorios necesarios para obtener las "habilidades" (skills):
    *   Kit de estudiante de Hyperframes: `https://github.com/nateherkai/hyperframes-student-kit.git`
    *   Video-use: `https://github.com/browser-use/video-use.git`
3.  Configura tus claves de API (por ejemplo, la de 11 Labs para transcripciones precisas) en un archivo `.env` en la raíz de tu proyecto.

---

## 🎬 Flujo de Trabajo Paso a Paso

### Paso 1: Grabación en Crudo
Graba tu video de forma natural. No te preocupes por equivocarte, dejar silencios o hacer tomas falsas.

### Paso 2: Recorte y Transcripción Automática
*   Copia tu archivo en crudo (ej. `raw_video.mp4`) a tu carpeta de proyecto.
*   Pídele a Claude Code que use `video-use` para limpiar el video:
    > *"Analiza este video, elimina cualquier palabra de relleno, silencios o tomas falsas y prepara el video para HyperFrames."*
*   El sistema te mostrará un resumen de lo que va a cortar (ej. cortes en el segundo 12, eliminar un tartamudeo) y te pedirá confirmación.
*   **Resultado**: Un video limpio (`edited.mp4`) y un archivo JSON con la transcripción que incluye las marcas de tiempo exactas por cada palabra.

### Paso 3: Planificación de Motion Graphics (Beats)
*   Usa lenguaje natural para dictarle a Claude dónde y cómo quieres que aparezcan los gráficos.
    > *"Cuando diga 'este es un video de ejemplo', quiero que aparezca una tarjeta estilo 'liquid glass' en la mitad izquierda de la pantalla con el texto en formato karaoke..."*
*   Pon a Claude en **Modo Planificación (Plan Mode)**.
*   Claude generará una línea de tiempo dividida en "Beats" (escenas) con sus anclajes de tiempo basados en las palabras exactas que pronunciaste. Revisa este plan y pide cambios si es necesario (ej. *"Añade una escena extra al final que diga 'Gracias por ver'"*).

### Paso 4: Revisión Visual y Ajustes
*   Claude generará el código de las animaciones.
*   Abre el servidor local (localhost) para previsualizar el resultado.
*   Verás un **Editor de Línea de Tiempo** en el navegador. Puedes arrastrar, acortar o alargar los elementos visuales manualmente si necesitas hacer ajustes rápidos de sincronización.
*   Si hay errores visuales, pídele a Claude que los arregle:
    > *"La tarjeta de la izquierda está tapando mi cara, hazla más pequeña. También, elimina el patrón de cuadrícula del fondo."*

### Paso 5: Renderizado Final
*   Una vez que estés contento con la previsualización, pídele a Claude que renderice el video final.

---

## 💡 Mejores Prácticas y Consejos

*   **Verificación Visual (Screenshots)**: Pídele a Claude que tome capturas de pantalla de lo que está haciendo para que él mismo verifique visualmente que las animaciones se ven bien antes de presentártelas.
*   **Ahorro de Tokens**: Ser muy específico desde el principio evita que Claude cometa errores que cuestan iteraciones y, por ende, tokens (el ejemplo del video consumió ~238,000 tokens).
*   **Crea "Filosofías de Diseño" (Plantillas)**: Una vez que encuentres un estilo que te guste, dile a Claude que cree un archivo markdown documentando ese estilo (ej. `estilo_lecciones.md`). En el futuro, solo tendrás que decirle: *"Edita este video usando la filosofía de diseño de lecciones"*, y el proceso será casi automático.
