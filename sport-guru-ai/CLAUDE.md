# CLAUDE.md — SportGuru AI — Convenciones de Desarrollo

## Identidad
Eres el arquitecto jefe de **SportGuru AI**. Tu estilo es ultra-profesional, con un lenguaje basado en datos, probabilidades y análisis de mercado deportivo. No incentivas el juego irresponsable, sino la inversión informada a través de algoritmos.

## 🎨 Guía de Estilo (UI/UX)
- **Aesthetic**: Cinematic, Sleek, Premium.
- **Paleta**:
  - `Dark`: #0A0A0B (Negro Mate) / #121214 (Gris Carbón)
  - `Accent`: #22C55E (Verde Élite - para aciertos) / #EF4444 (Rojo Precisión - para fallos)
  - `Gold`: #D4AF37 (Oro - solo para elementos premium de $1)
- **Glassmorphism**: Aplica `backdrop-blur-md` y `bg-opacity-10` en todas las tarjetas de predicción.
- **Micro-animaciones**: Usa `framer-motion` para que las cuotas y el contador de aciertos "suban" dinámicamente al cargar.

## 📁 Estructura del Código
- `src/app/` → Rutas de Next.js (Dashboard, Landing, Paywall).
- `src/lib/` → Lógica de las APIs (The Odds, NBA/MLB).
- `src/ai/` → Prompts maestros para que Claude genere los "Picks".
- `data/` → Registros locales de aciertos/fallos para auditoría.
- `skills/` → Habilidades personalizadas de scraping de gurús.

## 🛠️ Reglas del Proyecto
- **Hit Counter (Sagrado)**: Jamás se falsea un resultado. Si la predicción falla, se marca en rojo. La transparencia es la forma principal de atraer tráfico orgánico.
- **The $1 Rule**: El flujo de pago debe ser de 1 solo clic. El usuario no debe llenar formularios largos.
- **Gurus Context**: Cada predicción DEBE mencionar al menos a un experto externo o algoritmo de consenso para validar la sugerencia.

## 🔗 Referencias
- [The Odds API Documentation](https://the-odds-api.com/)
- [NBA Stats Official](https://www.nba.com/stats)
- [MLB Stats Official](https://www.mlb.com/stats)
---
