# 🏛️ MEMORIA MAESTRA: IA Power Engine Hub & Segundo Cerebro
## Antigravity Architect System v4.0 (Superpowers Edition)

> "Calidad sobre Velocidad. Verificación sobre Suposición. Estructura sobre Caos."

### 🕵️‍♂️ PROTOCOLO SUPERPOWERS (OBLIGATORIO)
Este proyecto opera bajo el framework **Superpowers**. Antes de ejecutar cualquier tarea técnica, el agente DEBE seguir estos pasos:
1. **Brainstorming**: Usar `.agents/skills/superpowers/brainstorming` para definir el alcance y diseño.
2. **Planning**: Convertir el diseño en un plan detallado con `.agents/skills/superpowers/writing-plans`.
3. **Execution**: Lanzar la implementación usando TDD (Test-Driven Development).
4. **Code Review**: Todo cambio debe ser revisado por un sub-agente dedicado.

---

## 📁 Estructura del Ecosistema Unificado

| Directorio | Rol Estratégico | Contenido Clave |
|:---|:---|:---|
| **`🚀 Agents/`** | **Fábrica de Ejecución** | `autoclaw`, `agent-zero`, `hermes-agent`, `autoresearch`. Tus trabajadores autónomos. |
| **`💎 Clients/`** | **Centro de Valor (Revenue)** | `micheline-v2-beautera`, `legal`. Proyectos finales de clientes. |
| **`⚙️ Infrastructure/`** | **Motor del Sistema** | `tao_env`, `tools`. Herramientas de soporte y entornos de red. |
| **`🧠 wiki/`** | **Base de Conocimiento** | Solo escritura del LLM. `concepts/`, `entities/`, `sources/`. El cerebro de largo plazo. |
| **`📥 raw/`** | **Bandeja de Entrada** | Inmutable. Solo el humano coloca información aquí para ingerir. |
| **`🧩 templates/`** | **Estandarización** | Plantillas de Obsidian para el wiki. |
| **`📂 .Archive/`** | **Histórico y Respaldo** | Archivos antiguos y locks de versiones para mantener la raíz limpia. |
| **`🛡️ .System_Configs/`**| **Cuarentena Técnica** | Configuración de herramientas dot-prefixed agrupadas. |

---

## 🦾 Reglas de Oro para Agentes

1. **Fuente de Verdad**: Este `CLAUDE.md` es la referencia global.
2. **Uso de Skills**: Todas las habilidades deben leerse desde `.agents/skills/`.
3. **Persistencia**: Experimentos en `Agents/`, negocios en `Clients/`, y conocimiento puro en `wiki/`.
4. **Wiki Agent**: Cuando actúes como gestor de conocimiento, sigue los flujos de INGEST, QUERY y LINT definidos en el sistema de Wiki.

---

## 🔄 Flujos de Conocimiento (Wiki)

- **INGEST**: Leer de `raw/` → Resumir → Crear en `wiki/sources/` → Actualizar conceptos/entidades → Loguear.
- **QUERY**: Buscar en `wiki/index.md` → Sintetizar con citas `[[pagina]]` → Guardar análisis en `wiki/analyses/`.
- **LINT**: Revisar páginas huérfanas, contradicciones y claims obsoletos.

---

## 🎬 Remotion Hub & Video Marketing
- **Habilidad**: `.agents/skills/remotion-best-practices`
- **Herramientas**: `FFmpeg` para post-procesamiento.

---

> [!TIP]
> Si alguna herramienta de IA deja de reconocer su configuración, búscarla en `.System_Configs`.

*Unificación realizada por Antigravity - 2026-04-11*
