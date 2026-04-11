# 🚀 Guía: Veo 3 + n8n Skeleton (Renderizado de Elite)

Esta guía documenta la infraestructura para ejecutar **Google Veo 3** sin tener que pagar los prohibitivos planes corporativos de $250/mes de Google AI Ultra, utilizando el acceso API de terceros (`Fal.ai`).

## 1. El Costo de la Elite
Advertencia de operación comercial: **Veo 3 es caro**. Utilizar esta API costará aproximadamente **$6.00 dólares por cada video de 8 segundos**. Se debe usar estrictamente para los anuncios publicitarios finales ganadores ("Hero Shots"), no para experimentación cruda (para eso existe Popcorn y Nano Banana).

## 2. Flujo Skeleton (Base Adaptable)
La automatización (`veo3-n8n-skeleton-workflow.json`) es un esqueleto puro. Su propósito es servir de base para conectarse a herramientas más complejas o CRMs:

1. **Trigger de Entrada (Formulario Nativo de n8n o Airtable):**
   Pide parámetros aislados para que el cliente o el equipo comercial no tenga que lidiar con la ingeniería de prompts. Solo rellenan: *Overview, Context, Action, Style*.
2. **"Prompt Engineer" Automático (OpenAI):**
   Toma esos 4 componentes básicos y redacta el *Prompt Cinemático* perfecto necesario para inyectar en el motor de Veo 3.
3. **Petición HTTP a Fal.AI:**
   Enviamos el texto formateado en JSON al motor `https://queue.fal.run/fal-ai/veo3`. (Requiere cargar saldo previamente en Fal.ai).
4. **Bucle de Espera (Wait Node):**
   Los generadores T2V (Text-to-Video) toman desde 90 segundos hasta 15 minutos en procesar la matemática visual. Se debe establecer un nodo de espera amplio (ej. 10m) antes de reclamarlo.
5. **Aterrizaje Final (Get Video + Gmail):**
   Realiza un `GET` a Fal.ai con el *Request ID* y expulsa el link MP4 descargable directamente a una bandeja de entrada (Gmail) o Slack/Teams.

## 3. Escalabilidad Agenciera
La belleza de este skeleton es que el Formulario inicial puede ser reemplazado por un frontend hecho en Lovable (React), vendiendo este generador corporativo disfrazado como un "SaaS privado" para clientes, donde ellos eligen estilos preestablecidos y la infraestructura tuya hace el puente con Veo 3.
