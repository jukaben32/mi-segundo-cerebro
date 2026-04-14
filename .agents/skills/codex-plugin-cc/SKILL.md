---
name: codex-plugin-cc
description: Guía y mejores prácticas para utilizar el plugin oficial de OpenAI Codex dentro de Claude Code para flujos de trabajo multi-modelo.
metadata:
  tags: claude-code, codex, openai, multi-model, review, adversarial, plugin
---

## Cuándo usar esto

Usa esta guía cuando necesites configurar, utilizar o entender el plugin oficial de OpenAI Codex (`openai/codex-plugin-cc`) para Claude Code. Esta habilidad es fundamental para implementar flujos de trabajo multi-modelo ("Multi-Model Workflows") donde un modelo evalúa críticamente el código generado por otro, mitigando las fallas lógicas.

## Concepto Principal: El problema del autorrevisor

Cuando un modelo de IA (por ejemplo, Claude) revisa el código que él mismo acaba de escribir, sufre del "sesgo del generador": tiende a racionalizar y alabar sus propias decisiones incluso si un humano experto consideraría el código como mediocre.

Al incorporar la integración de **Codex (GPT-4.5/5)** vía este plugin, traes una **perspectiva externa con diferentes datos de entrenamiento y prioridades**. Opus/Sonnet son excepcionales en arquitectura e interpretación de la intención humana, mientras que Codex sobresale en seguir al pie de la letra las instrucciones y ejecutar pruebas estrictas sin flexibilidad, lo que lo convierte en el "abogado del diablo" perfecto.

## Instalación y Configuración

1. **Instalación:**
   - En Claude Code, abre el marketplace / panel de plugins.
   - Busca y añade el plugin `OpenAI/Codex plugin CC`.
2. **Setup Inicial:**
   - Ejecuta `/codex setup`.
   - Este comando manejará la autorización a través de tu cuenta de ChatGPT y te ofrecerá instalar la CLI subyacente de Codex si no la tienes.
3. **Autenticación:**
   - Si se requiere, ejecuta `/codex login` para abrir tu navegador y autenticar la cuenta.

## Los 3 Comandos Clave

### 1. `/codex review` (Revisión Estándar)
Ejecuta una revisión de código tradicional (de solo lectura) sobre los cambios sin confirmar o comparados contra otra rama. Detecta problemas y ofrece sugerencias.

### 2. `/codex adversarial review` (Revisión Adversaria)
**El comando más importante y revolucionario del plugin.** 
No es una revisión neutral. Codex asume un rol altamente crítico: buscará modelos de fallos ocultos, fallas arquitectónicas silenciadas, bugs de concurrencia y pondrá bajo presión todas tus decisiones de diseño.
- **Es dirigible:** Puedes pedirle a Codex que ataque un componente específico.
  *Ejemplo:* `/codex adversarial review focus on the retry logic and cache invalidation strategy`

### 3. `/codex rescue` (Agente de Rescate)
Delega la ejecución de una tarea prolongada o tediosa a Codex para que se ejecute en segundo plano (background) mientras continúas hablando con Claude. Las operaciones de este sub-agente las puedes monitorear con:
- `/codex status`
- `/codex result`
- `/codex cancel`

### ⚠️ Peligro: El "Review Gate"
Es una configuración que obliga a Codex a evaluar *automáticamente cada respuesta* que da Claude de manera estricta antes de mostrarla.
- **Riesgo:** Esto produce a menudo loops infinitos de "Claude escribe -> Codex se queja -> Claude intenta parcharlo", quemando masivamente tus tokens diarios de API. 
- **Recomendación:** Actívalo **solo** de forma muy intermitente y para las tareas más complejas de la aplicación.

## Limitaciones (Trade-Offs a conocer)

1. **Velocidad:** Codex tarda significativamente más que los modelos Opus/Sonnet en procesar la misma instrucción y generar los reviews.
2. **Extrema Rigidez:** A diferencia de Claude, Codex no tratará de adivinar "qué quisiste decir". Hará exactamente lo que le pidas, incluso si tu indicación es en sí misma errónea. Tus prompts a Codex deben ser absolutos y precisos.
3. **Costo / Uso:** Aunque la prueba es gratuita y se usa con la cuenta básica temporalmente, en un flujo de trabajo serio chocarás muy rápido con el límite de tokens gratuito. Implica a la larga ser suscriptor en múltiples modelos (Claude/Anthropic + ChatGPT Plus).
4. **Estado Beta:** Actualmente el plugin puede sufrir desconexiones de socket de red y problemas de rutas.

## Referencia Oficial
Repositorio del plugin: [https://github.com/openai/codex-plugin-cc](https://github.com/openai/codex-plugin-cc.git)
