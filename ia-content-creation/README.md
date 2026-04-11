# 🤖 AI Content Creation Arsenal (Video & Imagen Cinemática)

Este directorio, `ia-content-creation`, contiene la mina de oro para producir contenido viral publicitario de calidad Hollywood utilizando Modelos de Inteligencia Artificial (Nano Banana, Veo 3, Midjourney) y flujos automatizados de n8n.

## 🎯 ¿Qué tenemos aquí?

### 1. El Prompt del Director (Cinematographer AI)
`cinematographer-system-prompt.txt`
Es un "Super Prompt" diseñado para inyectar en ChatGPT-4 o Claude. 
**Te guiará paso a paso por 3 Fases Automáticas:**
- **Fase 1:** Diseño de Personaje Base (Mantener consistencia gráfica sin detalles sueltos). Un solo Hero Image que guiará el resto.
- **Fase 2:** Rejilla Narrativa de 9 Tomas (The 9-Shot Narrative Grid). Transforma el personaje en 9 posiciones estratégicas y de tensión dramática.
- **Fase 3:** Generación de Movimiento (Image-to-Video). Te lanza las instrucciones exactas que le meterás a las IAs de video describiendo movimiento de cámara, acción y factores ambientales.

### 2. Flujo n8n (Nano Banana + Veo 3 Bot)
`nano-veo-n8n-workflow.json`
El código fuente de n8n para importar la automatización definitiva en tu servidor o local. Este sistema hace lo siguiente:
- **Telegram Bot:** Recibes o tomas una foto desde tu teléfono y se la pasas a Telegram.
- **Nano Banana (Vía Kie.AI):** La IA rediseña la imagen respetando tu cara y fondo (Consistencia Total de Character).
- **Proceso de Aprobación:** Telegram te pregunta si apruebas la edición. Si sí, te pide el "Prompt de Video". Si no, te permite deshacer la edición.
- **Veo 3 Fast (Vía Kie.AI):** El sistema pasa tu foto editada a Veo 3 que mágicamente anima el video y te lo devuelve como MP4 directo a tu Telegram.
- ¡Todo 100% automatizado, ideal para generar anuncios masivos en el móvil durante tu tiempo muerto!

### 3. Notas Metodológicas Extraídas (Transcripts)
**A. Controlando el "Tragamonedas" del Video AI:**
- La clave no es lanzar prompts y rezar; es usar una **"Foundational Image"** (Imagen Fundación). De ahí se saca la consistencia.
- Con "Nano Banana" (Gemini 2.5 Flash Image) la edición de personajes y fondos mantiene asombrosa fidelidad de rasgos frente al viejo ChatGPT.
- *Tip de Frame-To-Frame:* En IA avanzadas se inserta un frame inicial (ej. un rostro quieto) y un frame final (ej. el robot revelado), y se pide animar la interpolación. Midjourney da los mejores resultados para las fotos base, luego Veo 3 las anima.
- Edición: El salto "transicional" es genial si lo recortas y le aplicas Speed x3 y sonidos industriales en CapCut.

**B. Nano Banana es "El Asesino de Photoshop":**
- Velocidad asombrosa (6 segundos vs minutos de GPT4).
- Genial para creación de Modelos UGC (User Generated Content). Puedes colocar tu producto en las manos de diferentes modelos sintéticos. 

### 4. Guía JSON de Videos Explosivos (Viral "Reveal" Ads)
`viral-exploding-videos-guide.md`
La técnica precisa de estructuración JSON para generar revelaciones de productos asombrosas en IA.
- Fuerza a la IA (Veo 3) a obedecer cambios de escenas cinemáticas separando por variables: `<globals>`, `<parameters>` y una `<sequence>` rigurosa.
- Modela un flujo de cámara que comienza en tensión, explota en el segundo tres, e ilumina un cuarto completo.

### 5. Sora 2: Integración Empresarial con AirTable y n8n
`sora2-n8n-guide.md`
Documentación sobre cómo escalar el nuevo modelo dominante de OpenAi.
- Sistema de **Personas**: Invocación de personalidades exactas nombrando `@usuario`.
- Arquitectura descentralizada: Envía Prompts base, Aspect Ratios y Fotos Iniciales desde AirTable directo a Kie.AI, recuperando automáticamente el MP4 cuando el "bucle de espera de Webhook" se completa.
- **Regla de Oro en Sora 2 ("Menos es Más"):** Evita prompts extensivos; el director algorítmico interno es avanzado, basta con describir acciones muy puntuales y dinámicas (ej: *body cam footage*).

### 6. Wan 2.5: El Rival Sin Regulaciones (Audio Integrado)
`wan2.5-n8n-guide.md` & `wan2.5-n8n-workflow.json` (Flujo guardado internamente)
El flujo secreto para usar al máximo rival de Veo 3 para marketing hostil / radical.
- Capacidades de **Cero Censura** para "colocar" a personalidades famosas realizando scripts propios o patrocinando productos.
- Flujo en tres ramas ("Midjourney -> Nano Banana -> Raw Prompt -> n8n + Wan 2").
- Jamás usar expansores automáticos de prompts (cajas negras); delegar el armado a un LLM en texto.

### 7. Higgsfield Popcorn: Testing A/B Instantáneo
`popcorn-storyboard-guide.md`
La herramienta para crear el **First Frame** definitivo antes de hacer video.
- **Storyboarding en Lote:** Subes 1 foto de tu producto/modelo, das un solo comando automático y Popcorn arroja **7 escenas en escenarios totalmente distintos** de golpe.
- **Enfoque de Agencia:** Reduce las horas de testear prompts al crear un lote simultáneo de iteraciones, permitiéndote tomar la imagen publicitaria ganadora y llevarla a Sora/Veo3 mucho más rápido.

### 8. Nano Banana "Ad Machine" (Mega Fábrica de Anuncios Automática)
`nanobanana-ad-machine-guide.md` & `nanobanana-ad-machine-workflow.json`
El flujo definitivo en **n8n** para crear campañas enteras sin tocar un editor manual.
- Toma 1 imagen de producto y, conectando Airtable + Gemini + OpenRouter, ejecuta 50 variaciones publicitarias en 1 minuto.
- Permite usar ChatGPT para crear la "matriz de variaciones" de golpe. El LLM extrae la composición visual de tu foto base y obedece mutaciones de luz o entorno.

### 9. Google Veo 3 "Skeleton" (El Renderizado de Élite vía Fal.AI)
`veo3-n8n-skeleton-guide.md` & `veo3-n8n-skeleton-workflow.json`
El esqueleto base para integraciones de alta fidelidad sin pagar retenciones extremas a Google.
- Desvía la llamada a Veo 3 usando la API de **Fal.ai**.
- **Costo Premium:** ~$6 por cada 8 segundos de video. Recomendado rigurosamente solo para la etapa final del contenido.
- Usa un LLM intermediario para limpiar campos básicos (`Action`, `Style`) antes de crear el prompt técnico, empaquetando todo en un Workflow que entrega el MP4 a tu correo.

### 10. Frame to Frame (Técnica de Dirección Visual Acotada)
`frame-to-frame-guide.md`
Técnica de generación de contenido acotado entregando un "First Frame" y un "Last Frame" al modelo de video.
- Obliga a los motores a interpolar el movimiento y transformaciones exactas entre el punto A y el punto B.
- Compatible con **Hailuo, Veo 3.1, y Kling**.
- Ideal para transiciones de "Antes / Después" en productos, generadas en segundos con la ayuda de un LLM que conecte narrativamente la foto A con la B.

### 11. Motor de Películas Autónoma: Seedream + Topaz Upscaler 4K 60FPS
`seedream-4k-upscale-guide.md` & `seedream-4k-upscale-workflow.json`
El flujo definitivo de post-producción masiva automatizada con control absoluto desde Airtable.
- Toma fotogramas clave de Seedream/Nano Banana y los envía a **Minimax** para rellenar interpolación de video.
- Combina micro-escenas sueltas en una película continua usando la API de **FFmpeg**.
- Envía la película ensamblada a la prestigiosa IA de **Topaz** para escalar mágicamente a resolución 4K y 60 Cuadros Por Segundo limpios.
- Costo final consolidado de ~$0.68 por cada 6 segundos "masterizados", revolucionando la producción cara de estudio.

---

🔥 **Objetivo Creado:** Ahora dispones de la receta paso a paso para hiper-escalar *SportGuru AI* o cualquier otro emprendimiento usando marketing visual autónomo (Costo Cero / Elite API).
