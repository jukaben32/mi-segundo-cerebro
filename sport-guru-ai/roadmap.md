# 🏆 SportGuru AI — Hoja de Ruta (Roadmap)

## 📌 Visión General
Una plataforma de análisis deportivo de alta fidelidad que utiliza Inteligencia Artificial para predecir resultados en MLB, NBA y NFL. El valor reside en su **Tasa de Acierto Transparente** y su diseño minimalista y premium que democratiza el acceso a análisis de nivel "Vegas Shark" por solo $1.

## 📊 Módulos Principales

### 1. El Analista (Brain Engine)
- **Análisis Multi-Fuente**: Claude analiza datos de casas de apuestas (odds), clima, lesiones y sentimiento de "gurús" en redes sociales.
- **Predicción Estocástica**: No solo damos un ganador, damos un **Índice de Confianza %**.
- **Generación de "Picks"**: Un mini-artículo de una página que explica el "porqué" de la sugerencia.

### 2. El Contador de Aciertos (Hit Counter - CRÍTICO)
- **Validación Automática**: Un script (`validator.js`) que al final de cada jornada consulta los resultados reales y actualiza el contador.
- **Transparencia Visual**: Un widget en la landing page que muestra:
  - ✅ **Aciertos Totales** vs ❌ **Fallos Totales**.
  - 📈 **Retorno de Inversión (ROI)** proyectado si se hubieran seguido todos los picks.
  - 🔥 **Racha Actual** (ej. "7 aciertos seguidos").

### 3. Modelo de Negocio (Freemium de Trust)
- **Fase 1 (Acumulación de Confianza)**: 3-5 picks gratis diarios hasta alcanzar una racha de éxito verificable.
- **Fase 2 (Monetización)**: Una vez alcanzado un ROI positivo del X%, se activa el paywall de $1 para los "Picks Premium".
- **Pago en 1 Clic**: Integración con Stripe para pagar el dólar sin fricciones.

## 🛠️ Stack Tecnológico Proyectado
- **Frontend**: Next.js 15 (para máxima velocidad y SEO).
- **Backend (Serverless)**: Supabase (para guardar el contador de aciertos y usuarios).
- **IA**: Anthropic Claude 3.5 Sonnet (Maestro Analista).
- **Datos**: The Odds API (Premium) + Scrapers personalizados.

## 📅 Hitos Inmediatos
1. [ ] Crear arquitectura de la base de datos (Supabase) para el contador.
2. [ ] Configurar el "Analista" para que lea datos de MLB/NBA de hoy.
3. [ ] Diseñar el "Dashboard de Predicciones" con estética Cinematic/Premium.

---
*"No es una apuesta, es una inversión basada en datos."*
