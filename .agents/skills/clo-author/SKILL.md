---
name: "clo-author-research"
description: "Guía paso a paso para ejecutar el flujo de trabajo de investigación académica empírica utilizando el andamiaje Clo-Author dentro de Claude Code."
---

# Clo-Author: Architecture for Academic Research

Esta skill provee el flujo de trabajo para iniciar y desarrollar artículos de investigación empírica (ej. economía, finanzas) en Claude Code basado en la metodología de Clo-Author. 

El modelo fundamental se basa en "Pares Creador-Crítico" (Worker-Critic pairs), donde cada paso importante es generado por un agente y revisado automáticamente por otro antes de ser guardado en los directorios de tu proyecto (ej. `quality_reports`, `paper`).

## Pasos del Flujo de Trabajo (Workflow)

### 1. Configuración de Nuevo Proyecto (`/new-project` o prompt inicial)
Para empezar, dile a Claude que estás iniciando un proyecto.
**Prompt de ejemplo:** 
> "Estoy comenzando con un nuevo proyecto de investigación empírica en mi campo [tu campo] sobre [tu tema]. Lee CLAUDE.md y ayúdame a configurar la estructura del proyecto."

Esto configurará tu archivo base (`CLAUDE.md`), el perfil de tu dominio, y creará los subdirectorios si no existen.

### 2. Discover Interview: Entrevista de Mayéutica (`/discover interview`)
Realiza una "entrevista de investigación" donde hablas con el agente para definir la idea y contexto.
**Comando:** `/discover interview [tema corto]`
- El agente evaluará tu posición (ej. si hay variaciones de datos aplicables, qué papers estudiaste como inspiración).
- Guarda la información consolidada en la arquitectura del proyecto para que todos los demás agentes la lean.

### 3. Discover Literature: Revisión de Literatura Automatizada (`/discover literature`)
Automatiza la revisión del estado de arte según la entrevista.
**Comando:** `/discover literature [tema detallado]`
- El agente **Librarian** (Bibliotecario) realizará búsquedas online de la literatura relevante.
- Luego, el **Librarian Critic** revisará la selección usando un puntaje (buscando superar los 80/100). Validará novedad e impacto en la literatura.
- Todo esto se documentará automáticamente en `quality_reports/`.

### 4. Discover Data: Búsqueda de Fuentes de Datos (`/discover data`)
**Comando:** `/discover data [necesidad de datos]`
- El agente **Explorer** buscará datasets accesibles y restringidos que correspondan al contexto de tu investigación (espacial y temporal).
- El crítico documentará qué fuentes existen, los impedimentos y ventajas de cada una. Se guarda en tu espacio de trabajo de nuevo.

### 5. Strategize: Diseño de la Estrategia Empírica (`/strategize`)
**Comando:** `/strategize [pregunta de investigación]`
- Entra en análisis metodológico. Propone tests de robustez, variables instrumentales (si aplica) y tests de falsificación.
- Identificará carencias en tu planteamiento previo (ej. falta de "clusters", unidad de análisis no clara).

### 6. Ejecución y Redacción (Fases Avanzadas)
- `/analyze`: Análisis de datos con R/Python. Incluye un par Coder/Coder-Critic.
- `/write`: Redacción sección por sección del paper con LaTeX (`main.tex`).
- `/review --peer [revista]`: **Simulación de Peer Review**. Un editor simula una respuesta de revisión con distintos perfiles de referís o árbitros.

## Estructura de Directorios Clave generada
- `CLAUDE.md`: Perfil central de tu paper y directrices.
- `paper/`: Documentos de LaTeX (`main.tex`, `sections/`, `tables/`, `figures/`). Esta es tu "single source of truth".
- `quality_reports/`: Planes de trabajo, revisiones y bibliografía encontrada.
- `master_supporting_docs/, data/, explorations/, scripts/`: Trabajo en bruto.

## Buenas Prácticas
1. **Planifica primero:** Antes de crear una regresión o análisis de datos empíricos, pide a Claude un plan o usa un agente para planear.
2. **Revisión Continua:** Las revisiones automatizadas por el agente crítico evalúan si las tácticas sobrepasan 80/100.
3. **Paciencia y Acotación:** Si un comando está tomando demasiado (30 a 40 minutos), tú puedes pedir: *"Simplifica la revisión, un ejemplo rápido y limitado a 5/10 papers"* para ver la iteración.
