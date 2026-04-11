---
# LLM Wiki — Patrón de Base de Conocimiento Personal

tags: #ia #knowledge-management #llm #obsidian #segundo-cerebro
fecha_creada: 2026-04-06
fuentes: 1
---

## Qué es

Un sistema donde el LLM **construye y mantiene** una wiki persistente de markdown interconectados, en lugar de recuperar información de scratch en cada query (RAG tradicional).

**La diferencia clave**: el conocimiento se *compila una vez* y se mantiene actualizado. No se re-deriva en cada pregunta.

## Las 3 Capas

```
raw/        → Fuentes originales (inmutables). Solo el humano escribe aquí.
wiki/       → Wiki generada y mantenida por el LLM. Solo el LLM escribe aquí.
CLAUDE.md   → Schema: instrucciones de cómo funciona el sistema.
```

## Las 3 Operaciones

### 1. Ingest
- Humano dropea fuente en `raw/`
- LLM lee, extrae, discute takeaways con el humano
- LLM crea/actualiza 10-15 páginas del wiki
- Actualiza `index.md` y `log.md`

### 2. Query
- Humano hace pregunta
- LLM lee `index.md` → encuentra páginas relevantes → sintetiza respuesta con citas
- **Regla de oro**: si la respuesta es valiosa, se guarda como página en `wiki/analyses/`

### 3. Lint
- Periódicamente: LLM hace health-check del wiki
- Busca: contradicciones, páginas huérfanas, datos obsoletos, gaps para investigar
- Sugiere nuevas fuentes a ingerir

## Por qué funciona mejor que RAG

| Dimensión | LLM Wiki | RAG clásico |
|-----------|----------|-------------|
| Infraestructura | Solo markdown | Embeddings + vector DB |
| Costo | Solo tokens | Compute + storage |
| Mantenimiento | `lint` periódico | Re-embed cuando cambia |
| Escala | ~100s de fuentes | Millones de docs |
| Relaciones | Links explícitos | Similitud por proximidad |
| Síntesis | Ya compilada | Re-derivada cada query |

## Cuándo usar cada uno

- **LLM Wiki**: conocimiento personal, research profundo, cientos de fuentes, relaciones semánticas ricas
- **RAG tradicional**: millones de documentos, búsqueda por texto, enterprise-scale

## Herramientas complementarias

- **[[entities/obsidian]]**: IDE visual para ver el graph view del wiki
- **Obsidian Web Clipper**: extensión Chrome → convierte artículos a markdown en `raw/`
- **[[entities/claude-code]]**: El LLM que mantiene el wiki
- **qmd**: CLI de búsqueda sobre markdown (BM25 + vector + LLM reranking)

## Insights de la comunidad (Gist comments)

- **Pipeline de 5 pasos** (xoai): diff → summarize → extract concepts → write articles → images
- **Ontología es lo más difícil**: deduplicación de conceptos (¿"attention mechanism" == "self-attention"?)
- **Outputs duales**: toda query produce (1) respuesta + (2) actualización de wiki relevante
- **Multi-agent**: si todos los agentes (Cursor, Claude, Codex) leen el mismo wiki, las correcciones se propagan

## 🔗 Relacionado

- [[entities/andrej-karpathy]]
- [[entities/obsidian]]
- [[entities/claude-code]]
- [[sources/2026-04-06-llm-wiki-karpathy]]
