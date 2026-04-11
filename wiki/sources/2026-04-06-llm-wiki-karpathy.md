---
# Fuente: LLM Wiki — Andrej Karpathy

tags: #ia #knowledge-management #llm #segundo-cerebro
tipo: gist + transcripción-youtube
fecha_ingesta: 2026-04-06
url_original: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
autor: [[entities/andrej-karpathy]]
popularidad: 5000+ stars, 1308 forks
---

## Resumen

Karpathy publicó un patrón para construir bases de conocimiento personales usando LLMs. La idea: en lugar de RAG (recuperar de raw cada vez), el LLM **compila** las fuentes en un wiki de markdown persistente e interconectado. El wiki crece y se enriquece con cada fuente nueva.

## Puntos clave

1. **El wiki es un artefacto compuesto**: las relaciones ya están ahí, no se re-derivan
2. **3 capas**: `raw/` (inmutable) → `wiki/` (LLM escribe) → `schema` (CLAUDE.md)
3. **3 operaciones**: Ingest → Query → Lint
4. **No necesitas RAG infrastructure**: solo markdown + un LLM
5. **Obsidian como IDE**: el LLM es el programador, el wiki es el codebase

## Citas notables

> "The wiki keeps getting richer with every source you add and every question you ask."

> "Obsidian is the IDE; the LLM is the programmer; the wiki is the codebase."

> "LLMs don't get bored, don't forget to update a cross-reference, and can touch 15 files in one pass."

> "The human's job is to curate sources, direct the analysis, ask good questions, and think about what it all means. The LLM's job is everything else."

## Aplicaciones descritas

- Personal: goals, salud, psicología, journaling
- Research: papers, artículos, tesis en evolución
- Libros: wiki por capítulos (como Tolkien Gateway pero personal)
- Business: wiki interno mantenido por LLMs con Slack/meetings/docs
- Due diligence, trip planning, hobby deep-dives

## Herramientas mencionadas

- **[[entities/obsidian]]**: graph view, Dataview plugin, Marp para slides
- **Obsidian Web Clipper**: artículos → markdown → `raw/`
- **qmd**: búsqueda híbrida BM25/vector sobre markdown
- **[[entities/claude-code]]**: agente recomendado como LLM maintainer

## Implementaciones de la comunidad

- `sage-wiki` (xoai): pipeline de 5 passes, SQLite
- `obsidian-wiki` (Ar9av): setup de 1 config desde vault de Obsidian
- `second-brain` (zhiwehu): instalable con Claude Code
- `llm-wiki` (ekadetov): bundled como claude plugin
- `MindOS` (GeminiLight): multi-agent, todos leen el mismo wiki

## 🔗 Relacionado

- [[concepts/llm-wiki-karpathy]]
- [[entities/andrej-karpathy]]
- [[entities/obsidian]]
- [[entities/claude-code]]
