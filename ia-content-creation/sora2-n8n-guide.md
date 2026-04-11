# 🚀 Guía: Sora 2 + n8n Automations (Text/Image to Video)

Esta guía documenta la integración del modelo rey de generación de video de OpenAI: **Sora 2**, utilizando **n8n** y **AirTable** como panel de control, a través de la interfaz de **Kie.AI**.

## 1. El Salto Evolutivo de Sora 2
Sora 2 hace cosas únicas que otros modelos aún no pueden mantener con fluidez:
- **Consistencia Brutal:** Mantiene la física, los reflejos, y hace "Quick Cuts" (cortes rápidos entre distintos planos) de forma coherente.
- **Sistema de "Personas":** Sora 2 permite inyectar caras específicas usando el símbolo arroba `@`. Por ejemplo, puedes escribir `@sama` en el prompt y el modelo renderizará al CEO de OpenAI (Sam Altman) con fidelidad absoluta. Cualquiera que suba su "Persona" a la app de Sora puede ser invocado en el prompt.

## 2. Arquitectura de la Automatización n8n
Este workflow permite gestionar toda la producción de contenido desde AirTable, sin abrir apps pesadas o interfaces nativas.

### Componentes Clave:
1. **AirTable (Panel de Control):** Una base de datos donde tienes Filas con: `Video_Prompt`, `First_Frame_Image_URL` (opcional), `Aspect_Ratio` (retrato o paisaje), y `Status` (Standby / Completed).
2. **n8n Webhook:** Cuando le das clic a un botón en AirTable, envía un Webhook a n8n.
3. **Kie.AI (Middle-man / Motor API):** Envías los datos de AirTable a la API de Kie.AI mediante Autenticación tipo *Header Auth -> Authorization: Bearer [API_KEY]*.
4. **Bucle de Peticiones (Polling Loop):** Kie.AI te devuelve un `Task ID`. Debido a que no soportan bien las respuestas síncronas para video, debes crear un loop en n8n que espere 1 minuto, consulte a Kie.AI si el video está listo, y si responde `Success`, procede.
5. **JSON Parse & Update:** Kie.AI devuelve la URL del video de forma enredada, por lo que usas un nodo "Parse" para pescar el enlace MP4 real y usas el nodo AirTable para regresarlo a tu base de datos y cambiar el Status final a `Completed`.

## 3. Best Practices (Mejores Prácticas) de Prompting para Sora 2

Sorprendentemente, la forma de escribirle a Sora 2 es opuesta a los sistemas antiguos:
- **"Menos es Más" (Consise Prompts):** A diferencia de Midjourney o Veo3 donde debes llenar un párrafo de detalles, **Sora 2 arroja peores resultados si el prompt es muy denso**. Su inteligencia es extremadamente intuitiva resolviendo cortes y ángulos. Es mejor ser directo sobre la acción y dejar que el director interno de la IA haga el resto de transiciones temporales.
- **Formato Sugerido:** Acción directa y clara + Descripción de iluminación + Personas involucradas. 
  > *Ejemplo:* "Have @sama being arrested for stealing Chase AI automations. Make it look like body cam footage."
