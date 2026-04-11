# 🎬 Guía: Wan 2.5 (Video Nativamente con Audio y SIN Censura)

Esta guía captura la arquitectura de **Wan 2.5**, el modelo de IA de generación de Video que compite frente a frente con Veo 3, destacándose por tener opciones de **Audio nativo en la generación** e **Inexistencia de Guardarraíles ("No Guardrails")**.

## 1. El Potencial de Wan 2.5 para Marketing (Commercial Use)
- **Audio Nativo Imbuido:** Al igual que Veo 3, Wan 2.5 produce diálogos y efectos de sonido en la misma generación matemática.
- **Cero Censuras o Derechos Estrictos ("No Guardrails"):** Literalmente puedes tomar la imagen de un actor o youtuber famoso y hacer que beba o promueva un producto comercial distinto como si fuera un anuncio sin que la IA rechace el prompt por copyright. Esto tiene repercusiones gigantescas (Ejemplo: *Dwayne The Rock Johnson promocionando tus gomas vitamínicas de marca local*).
- **Control Fino (Base Image + Custom Prompt):** Wan 2.5 funciona increíblemente bien dándole un Primer Fotograma ("First Frame").

## 2. Flujo Creativo "Best In Class"
El secreto no está en tirarle texto ciego al modelo, este es el *"Creative Workflow"*:
1. **Creación de la Imagen Base:** Usar **Midjourney** (es el mejor modelador de imágenes base). Un ejemplo de prompt: *"Close-up of a woman podcaster sitting at a desk in front of a microphone staring into the camera"*. (Alternativamente Nano Banana o C-Dream para consistencia).
2. **Post-Edición de Personaje (Opcional):** Pasar el First Frame por Nano Banana para cambiarle un objeto (ponerle una lata de tu Coca Cola, o que sostenga tu libro).
3. **Draft del Prompt en LLM Seguro:** Jamás uses el botón automático de "Optimize Prompt / Enable Prompt Expansion" de las plataformas, esconde el resultado y te hace perder control sobre adjetivos. Dile a Claude o ChatGPT: *"Tengo esta foto [Foto] de una podcaster, dame un Prompt potente para un Video AI describiendo acción visual, audio y emoción donde baje su taza de café y diga X cosa."*
4. **Alimentas todo a Wan 2.5 / Kie.AI.**

## 3. Integración en `n8n`
Al igual que con Sora 2, dispones del archivo:
`wan2.5-n8n-workflow.json`
- Mismo concepto central basado en **Airtable**: Status "Standby", disparo de Webhook, comunicación **Kie.AI API**, Bucle *"Wait 1 minute and check"* y actualización del campo.
- Soporta Resoluciones de `480p`, `720p`, y `1080p`. Costo estimado es apenas $0.10 ctvs por segundo en 1080p (y puede salir gratis si activas suscripciones nativas como Higsfield Premium temporal).
