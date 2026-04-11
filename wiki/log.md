# 📓 Log — Mi Segundo Cerebro

> Historial cronológico de operaciones. Append-only. Nunca editar entradas pasadas.
> Tip: `grep "^## \[" log.md | tail -10` para ver los últimos 10 eventos.

---

## [2026-04-06] setup | Inicialización del LLM Wiki

- **Acción**: Setup inicial del sistema LLM Wiki basado en el patrón de Andrej Karpathy
- **Estructura creada**:
  - `raw/` → fuentes originales inmutables
  - `wiki/concepts/` → páginas de conceptos
  - `wiki/entities/` → personas, tools, orgs
  - `wiki/sources/` → una página por fuente ingerida
  - `wiki/analyses/` → análisis y síntesis de queries
  - `wiki/index.md` → catálogo navegable
  - `wiki/log.md` → este archivo
- **CLAUDE.md**: Actualizado con workflows Ingest / Query / Lint
- **Notas**: Migración desde estructura previa de Obsidian vault manteniendo templates/

---

## [2026-04-06] ingest | LLM Wiki — Andrej Karpathy Gist + YouTube Transcript

- **Fuente**: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
- **Tipo**: Gist técnico + transcripción de YouTube
- **Páginas wiki creadas**:
  - `sources/2026-04-06-llm-wiki-karpathy.md`
  - `concepts/llm-wiki-karpathy.md`
  - `entities/andrej-karpathy.md`
  - `entities/obsidian.md`
  - `entities/claude-code.md`
- **Páginas actualizadas**: `index.md`
- **Takeaways clave**: Patrón de 3 capas (raw/wiki/schema), operaciones Ingest/Query/Lint, wiki como artefacto compuesto que acumula conocimiento vs RAG efímero

---

## [2026-04-08] ingest | AI Ad Strategy Team (Claude Code) & MisProyectos Sync

- **Fuente**: https://github.com/zubair-trabzada/ai-marketing-claude.git + User Video Transcription
- **Tipo**: Video Transcript + Marketing Skill System
- **Páginas wiki creadas**:
  - `raw/video-transcription-ad-strategy.md`
  - `wiki/sources/ad-strategy-tool.md`
- **Operaciones**:
  - Instalación de skills en `~/.claude/skills` y `~/.claude/agents` para Claude Code.
  - Sincronización masiva de proyectos de `MisProyectos` a `mi-segundo-cerebro` para persistencia en el repositorio de conocimiento.
- **Notas**: Se configuró el folder `Publicidad/` con el repositorio de marketing automation.

---

## [2026-04-08] ingest | n8n Workflow Builder Skill

- **Fuente**: [[n8n-workflow-builder-prompt]] (Google Drive content)
- **Tipo**: Prompt Engineering / Automation
- **Páginas wiki creadas**:
  - `wiki/concepts/n8n-workflow-builder.md`
  - `raw/n8n-workflow-builder-prompt.md`
- **Operaciones**:
  - Creación de Skill `n8n-workflow-builder` en `MisProyectos/`.
  - Instalación en `~/.claude/skills/n8n-workflow-builder/SKILL.md`.
- **Takeaways clave**: Protocolo de clarificación antes de generación de JSON, modularidad para credenciales, alineación con la estructura de n8n.

---

## [2026-04-08] ingest | TradingView MCP Bridge

- **Fuente**: [[tradingview-mcp-info]] (GitHub + Research)
- **Tipo**: Trading Automation / MCP Bridge
- **Páginas wiki creadas**:
  - `wiki/concepts/tradingview-mcp.md`
  - `raw/tradingview-mcp-info.md`
- **Operaciones**:
  *   Clonación de `tradingview-mcp` en `trading/`.
  *   Instalación de dependencias (npm install).
  *   Configuración en `~/.claude/settings.json`.
- **Takeaways clave**: Uso de CDP (puerto 9222) para leer estado interno de TradingView Desktop, capacidad de leer dibujos de Pine (lineas, tablas) y automatizar el ciclo de desarrollo de scripts.
