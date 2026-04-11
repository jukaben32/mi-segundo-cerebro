# 🍌 Guía: Nano Banana "Ad Machine" (Automatización en n8n)

Esta arquitectura está diseñada para resolver el problema de **ideación de material de marketing a gran escala**. Permite tomar 1 (una) imagen base (ej. el producto de *SportGuru AI* o *Max Gummies*) y mutarla en cientos de variaciones publicitarias, automatizando el proceso tedioso a través de n8n y Airtable.

## 1. El Problema que Resuelve
Normalmente, si quieres ver el mismo objeto en diferentes escenarios (playa, neón, invierno, cyberpunk) tienes que escribir y esperar uno por uno los prompts en la web de un generador. 
La "Máquina de Anuncios Nano Banana" permite:
- Generar masivamente ideas variando 8 parámetros distintos en bloque.
- Manejar todo el CMS de diseño sin salir de un tablero de AirTable.
- Devolver el arte 100% terminado de vuelta a la tabla, listo para revisar y aprobar (Hit/Miss ratio masivo que te garantiza al menos un arte ganador).

## 2. Componentes de la Arquitectura

1. **AirTable como Frontend:** 
   Se define una fila madre que contiene el `Target Image` (URL de la foto). 
   Debajo, creas múltiples mutaciones ingresando qué quieres alterar (Lighting, Atmosphere, Setting).
2. **Gemini 2.5 Flash / ChatGPT como "Analista Creativo":**
   Dentro de `n8n`, al disparar el webhook, el LLM *Analiza la foto base* sacando todo su jugo descriptivo. Luego ensambla un Mega Prompt Técnico altamente compatible con Nano Banana basándose en tus requests de Airtable.
3. **OpenRouter API como Puente a Nano Banana:**
   Para editar la foto, el flujo realiza una llamada API para crear el contenido visual. OpenRouter delega y ejecuta el prompt usando los parámetros del modelo. (Usa endpoints limitados gratuitos o centavos pagados).
4. **AirTable Upload:**
   n8n inyecta la obra generada de vuelta en tu Dashboard y marca el ticket como `Completed`.

## 3. Integración Directa
Tienes este flujo listo en tu carpeta como:
`nanobanana-ad-machine-workflow.json`

### Hack Masivo de Agencias: El Uso de "CustomGPT"
Para no escribir a mano las 100 variaciones de tablas de Airtable, se utiliza un Master prompt en ChatGPT: 
> *"Mantén este coche principal igual pero enloquece con la iluminación y los entornos de fondo de forma minimalista. Dame 20 variaciones tabuladas listas para pegarlas en Airtable."*

Pegas esos resultados en las columnas de AirTable, presionas 1 Botón de Webhook, y n8n te fabricará 20 publicidades de estudio en 1 minuto.
