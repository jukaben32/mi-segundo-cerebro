---
name: voice-agent-infrastructure
description: Guía paso a paso para construir una infraestructura completa de agentes de voz IA (inbound y outbound) con CRM, programación de citas y dashboard de cliente. Adaptable a cualquier industria (inmobiliaria, clínicas, abogados, etc.).
---

# 🎙️ Infraestructura de Agente de Voz IA (Voice Agent System)

Esta habilidad te guía paso a paso para construir un sistema completo de agentes de voz con Inteligencia Artificial utilizando **Claude Code**, **Retell AI**, **Modal**, **Notion**, **Cal.com**, y **Twilio**. El sistema resultante será capaz de recibir llamadas (Inbound), realizar llamadas proactivas (Outbound), gestionar contactos en un CRM, agendar citas y ofrecer un Panel de Control (Dashboard) profesional al cliente final.

Este modelo es fácilmente adaptable a cualquier sector (inmobiliarias, clínicas dentales, despachos de abogados, gimnasios, agencias, etc.).

## 📋 Arquitectura del Sistema

*   **Voz y Telefonía**: Retell AI + Twilio (SIP Trunking).
*   **Backend y Automatizaciones**: Python alojado en Modal (Serverless).
*   **CRM y Base de Datos**: Notion (conectado vía MCP de Notion).
*   **Agenda de Citas**: Cal.com.
*   **Inteligencia y Análisis**: Anthropic API (Claude) para análisis y scoring post-llamada.
*   **Panel de Control**: Dashboard frontend con shadcn/ui y Tailwind.

---

## 🚀 Fases de Construcción (Guía Paso a Paso)

Ejecuta cada fase en orden interactuando con el usuario para desarrollar la infraestructura completa.

### Fase 1: Recolección y Configuración de Credenciales
Antes de escribir cualquier lógica de código, debes solicitar y configurar todas las claves de acceso de las APIs necesarias.

1.  Solicita al usuario que obtenga las siguientes credenciales (y guíalo si no sabe cómo):
    *   **Retell AI API Key**
    *   **Notion Integration Secret**
    *   **Cal.com API Key**
    *   **Anthropic API Key**
    *   **Twilio Account SID, Auth Token y Phone Number**
    *   **Modal** (requerirá autenticación vía CLI `modal setup`)
2.  Una vez recabadas, guarda todas las credenciales en un archivo `.env` en la raíz del proyecto.

### Fase 2: Inicialización del Proyecto Backend (Python + Modal)
1.  Crea la estructura base del proyecto utilizando Python y configurando la librería de Modal.
2.  Prepara los archivos necesarios para alojar endpoints (funciones web / llamadas a herramientas).
3.  Verifica que el entorno cargue correctamente las variables del archivo `.env`.

### Fase 3: Creación de la Estructura en el CRM (Notion)
Adapta esta fase a la industria requerida (Ej. Inmobiliaria: Propiedades, Abogados: Casos legales).
1.  Utiliza el MCP de Notion (o llamadas a la API) para crear las Bases de Datos necesarias en el espacio de trabajo del usuario.
2.  Estructuras básicas requeridas:
    *   **Inventario/Servicios** (Propiedades, paquetes, especialidades, etc.)
    *   **Leads/Clientes** (Esencial incluir campos: Estado del prospecto [ej. "Pendiente de llamar"], Resumen de llamada, y Temperatura [Hot/Warm/Cold])
    *   **Historial de Llamadas**
3.  Recupera los IDs de las bases de datos generadas y añádelos al archivo `.env`.

### Fase 4: Desarrollo de Automatizaciones (Tool Calling)
Desarrolla 5 funciones independientes en Python. Estas serán las herramientas (Tools) que el Agente de Retell podrá usar de forma dinámica en medio de la llamada.

1.  **Búsqueda e Información:** Buscar disponibilidad o resolver dudas leyendo información directamente de las tablas de Notion.
2.  **Registro de Nuevo Lead:** Guardar nombre, requerimientos y datos de contacto en la tabla de Leads.
3.  **Agendamiento:** Usar la API de Cal.com para registrar una cita y sincronizar el enlace en Notion.
4.  **Actualización de Estado:** Cambiar la temperatura o fase del prospecto dentro del embudo (ej. Cita Agendada).
5.  **Análisis Post-Llamada:** Un webhook que reciba la transcripción de la llamada cuando ésta termine, utilice la API de Anthropic (Claude 3.5 Sonnet) para generar un resumen y una calificación del lead (Lead Scoring), y lo guarde automáticamente en Notion.

### Fase 5: Despliegue Inicial en Modal (Producción)
1.  Sube y despliega las automatizaciones hacia Modal (`modal deploy`).
2.  Realiza pruebas unitarias (tests) o validaciones para confirmar que operen correctamente.
3.  Sincroniza los secretos (`modal secret create`) para que el código en la nube no dependa del `.env` local.
4.  Guarda la URL base expuesta en el despliegue.

### Fase 6: Creación del Agente Inbound (Retell AI)
1.  Emplea la API de Retell para instanciar el agente.
2.  Configura el recurso de idioma, el proveedor de LLM y la *System Prompt* adaptándola fuertemente a la identidad de la marca (ej. "Eres Sofía, recepcionista experta, mantén respuestas concisas, tono profesional y persuasivo").
3.  Integra a este agente las automatizaciones web publicadas en Modal configurándolas como "Custom Functions/Tools".
4.  Terminado esto, guarda el `agent_id` en el proyecto.

### Fase 7: Conexión Telefónica (Twilio)
1.  Asiste al usuario en la provisión de un número local desde Twilio vía API o interfaz.
2.  Interconecta el número recién adquirido con el Agente de Retell (configuración de SIP Trunk o Inbound Webhook).

### Fase 8: Automatización Outbound (Cron Job)
Añade la segunda capa del servicio: un agente que llama proactivamente a los prospectos.

1.  Crea un nuevo Agente en Retell con clonado de lógica pero con una *System Prompt* adaptada (Tono de reactivación, más directo).
2.  Desarrolla una función recurrente (Cron Job/Worker) en Modal configurada para ejecutarse periódicamente (ej. cada hora o media hora).
3.  Logica del proceso:
    *   Consultar a Notion por Leads con estado "Pendiente de llamar".
    *   Marcar su estatus temporalmente en "En Proceso" para evitar duplicar llamadas.
    *   Disparar llamadas activas pasando las variables del lead hacia la API de Retell (`retell.call.create`).
    *   **Provee también un script o comando de consola** que le permita al desarrollador/usuario disparar esta comprobación manualmente sin tener que esperar el cron.

### Fase 9: Desarrollo del Dashboard Profesional
Este será el punto de interacción final para el negocio/cliente dueño de este sistema.
1.  Construye una interfaz limpia usando Next.js, Tailwind CSS y shadcn/ui. (Aspecto premium, paleta de colores moderna, tipografía refinada).
2.  Elementos clave de la interfaz:
    *   **KPIs Generales:** Volumen de llamadas contestadas, Citas logradas, Tasa de conversión/éxito, Temperaturas del embudo.
    *   **Historial y CRM Ligero:** Visor del estado de los leads resumiendo a grandes rasgos lo que ocurre en Notion.
    *   **Panel de Control del Agente:** Inputs y botones para visualizar y modificar la *System Prompt*, nivel de creatividad u otros parámetros básicos sin necesidad de que el usuario final conozca o visite Retell AI.
    *   **Lanzador Manual Outbound:** Un botón que obligue la ejecución de la cola de reactivación de leads fríos.

---

## 🎯 Instrucciones de Comportamiento para Claude Code
Cuando el usuario solicite implementar un agente de voz (ej. "Necesito un agente para un dentista basado en tu modelo voice-agent-infrastructure"):
1. No te abrumes, ve fase por fase y detente a interactuar si falta contexto, llaves (keys) o se producen errores de APIs.
2. Aplica tu capacidad de "Contextualización": si es un gimnasio, no crees campos de "Casos legales" o "Propiedades" en Notion. Propón "Planes de membresía" o "Clases".
3. Reporta el avance con claridad usando las 9 fases.
