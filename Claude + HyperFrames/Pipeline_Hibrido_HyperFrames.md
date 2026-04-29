# Blueprint: Pipeline Híbrido "Clonar Canales" + HyperFrames

Este documento preserva la estrategia de producción de élite (Estilo ColdFusion/Apple) utilizando la combinación de video generado por IA y animaciones generadas por código.

## 1. Concepto Central: El Enfoque Híbrido
Para mantener la más alta calidad visual (4K real) y reducir los costos de generación (de ~$60 a ~$15-$25 por video):
- **NO generamos texto ni gráficos con IAs de video** (Kling/Runway) para evitar alucinaciones, "morphing" y tipografía ilegible.
- **USAMOS IAs de video (Kling/Runway)** EXCLUSIVAMENTE para generar "B-Roll atmosférico" (fondos cinemáticos, oscuros, texturas en movimiento, ciudades, servidores).
- **USAMOS HyperFrames (Código HTML/React)** para generar toda la capa de información: Tarjetas de cristal líquido (liquid glass), gráficos de datos, textos en pantalla (karaoke) y código fuente.

## 2. El Flujo de Trabajo (Pipeline)

1. **Guion (El Cerebro):** Se genera el guion documental de alta calidad.
2. **Locución y Timestamps (ElevenLabs/Whisper):** Se convierte el guion a voz. Se extrae obligatoriamente el archivo JSON con las marcas de tiempo (timestamps) exactas por palabra.
3. **B-Roll Atmosférico:** Se generan 2 o 3 clips de fondo continuos y cinemáticos (Runway/Kling) que servirán como base del video.
4. **Orquestación (Antigravity):**
   - El agente lee el guion y el JSON de tiempos.
   - Programa los "Beats" (escenas de HyperFrames) superpuestos en los momentos exactos.
   - Aplica la "Filosofía de Diseño" del canal (modo oscuro, fuente Inter/SF Pro, animaciones sedosas a 60fps).
5. **Renderizado Local:** HyperFrames une el audio, el B-Roll de fondo y renderiza localmente los gráficos programados en un MP4 final a costo cero de renderizado en la nube.

## 3. Filosofía de Diseño (Design Philosophy)
*   **Estética:** Premium Tech Documentary. Minimalista, sombras profundas, transparencias sutiles.
*   **Tipografía:** Limpia, sans-serif moderna (Inter).
*   **Colores:** Fondos oscuros (Graphite, Negro profundo) con acentos de color vibrantes (Naranja, Cyan, Púrpura) para los datos clave.
*   **Animaciones:** Revelaciones suaves, zoom in/out cinemáticos (sin cortes bruscos).

*Nota para el agente Antigravity: Consultar este Blueprint siempre que el usuario inicie un ciclo de producción para el proyecto "Clonar Canales" utilizando HyperFrames.*
