---
nombre: Claude Code
tipo: herramienta
tags: #herramienta #ia #agente #anthropic
fecha_creada: 2026-04-06
url: https://claude.ai/code
---

## Qué es

Agente de coding de Anthropic. En el contexto del LLM Wiki, actúa como el **LLM maintainer**: lee fuentes de `raw/`, escribe y actualiza páginas del `wiki/`, mantiene el `index.md` y el `log.md`.

## Rol en este segundo cerebro

- **Ingest**: procesa nuevas fuentes y popula el wiki
- **Query**: responde preguntas buscando en index + páginas relevantes
- **Lint**: health-check periódico del wiki

## Workflow recomendado

1. Abrir `mi-segundo-cerebro/` en VS Code o terminal
2. Ejecutar Claude Code apuntando a esta carpeta
3. Claude lee `CLAUDE.md` automáticamente (schema del proyecto)
4. Dar comando de ingest, query o lint

## 🔗 Relacionado

- [[concepts/llm-wiki-karpathy]]
- [[entities/obsidian]]
