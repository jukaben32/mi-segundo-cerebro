# 🌟 Guía: Seedream 4.0 a 4K (Frame to Frame + Upscale Masivo)

Esta guía documenta la infraestructura para crear una **Cadena de Montaje Cinematográfica Autónoma**. 

La magia aquí consiste en solucionar el principal problema del video generado con IA: los parches, la inconsistencia entre clips separados y la baja resolución nativa (generalmente bloqueada en 1080p). Este flujo lo centraliza todo en Airtable.

## 1. Arquitectura del Flujo (Dos Motores)
El workflow `seedream-4k-upscale-workflow.json` está mecánicamente dividido en dos hemisferios operativos:

### Fase A: Creación de la Escena ("Casting & Grabación")
1. **Punto de Inicio:** Un Action Button en Airtable llama al Webhook `1080p Webhook`.
2. **Adquisición:** n8n busca en Airtable filas marcadas como *"1080p Standby"*. Extrae: `First Frame` (ej. de Seedream), `Last Frame`, y el `Video Prompt`.
3. **Grabación (Minimax/Hailuo):** Se hace POST a `Minimax (image-to-video)` en Fal.ai. El modelo interpola qué debe pasar entre ambos fotogramas basándose en el prompt.
4. **Almacenamiento Draft:** El resultado de 1080p (draft) se pega en Airtable y se cambia el status a *"4k Standby"*. 
5. *(Humano revisa en Airtable: si le gusta el movimiento de cámara, aprueba para pasar a la Fase B).*

### Fase B: Post-Producción ("Stitch & Upscale a 4K")
1. **Punto de Inicio:** Otro botón en Airtable ("Create 4K Video") llama al Webhook `4k Webhook`.
2. **Agrupación (Stitch):** n8n recoge todos los clips que aprobas te y los envía a la API de **FFmpeg** en Fal.ai. Las escenas cortas se convierten en 1 solo plano maestro continuo.
3. **Remasterización (Upscale):** El video consolidado se envía a **Topaz** API (también vía Fal.ai) para multiplicar su peso a 4K - 60 FPS (H.264).
4. **Entrega Final:** n8n actualiza la fila de Airtable con el status *"Completed"* y adjunta el MP4 gigante, listo para monetizar.

## 2. Los Costos Radiales del Motor
Este nivel de posproducción conlleva micro-gastos, pero en masa, es mucho más barato que producir video tradicionalmente:
*   **Seedream V4** (Aproximadamente $0.03 por imagen).
*   **Minimax** (Aproximadamente $0.08 por segundo de video generado).
*   **FFmpeg** ($0.0002 por segundo para la unión).
*   **Topaz** ($0.033 por segundo para subir a 4K).
*   **Total Aproximado:** Unos ~$0.68 USD por cada clip final masterizado de 6 segundos.

## 3. Dinámica del "Chain-Linking" (Consistencia Extrema)
El secreto para hacer una película de 1 minuto sin que el personaje mute o el escenario cambie es enlazar en cadena.
*   El **Last Frame** de la Escena 1, **debes subirlo como el First Frame** de la Escena 2 en Airtable.
*   Esto asegura que cuando FFmpeg las pegue, parezca una toma continua rodada por un dron o una grúa cinematográfica.
