# 📈 Alpaca Trading Bot - Nivel Institucional

> **Sistema de trading automatizado con arquitectura de hedge fund cuantitativo**

Este sistema integra **Multi-Agent AI, Risk Management avanzado, Backtesting con Walk-Forward Validation, Dashboard en tiempo real y Notificaciones multi-canal** para operar 3 estrategias principales mediante Alpaca API.

---

## 🎯 Estrategias Implementadas

### 1. 📊 Trailing Stop Bot
| Parámetro | Valor |
|-----------|-------|
| **Activos** | TSLA, NVDA, AMD (growth stocks) |
| **Stop Loss** | -8% inicial |
| **Trailing** | Sube 5% cada vez que el precio sube 10% |
| **Ladder Buys** | Compras escalonadas: -20% (10), -30% (20), -50% (50) |

### 2. 🏛️ Copy Trading Bot (Políticos)
| Parámetro | Valor |
|-----------|-------|
| **Fuente** | [Capitol Trades](https://capitoltrades.com) |
| **Político** | Michael McCaul (R-TX) |
| **Benchmark** | +34.8% vs +15% S&P 500 |
| **Delay** | 60 min después del trade (filtro de ruido) |

### 3. 🎡 Wheel Strategy (Opciones)
| Stage | Acción | Objetivo |
|-------|--------|----------|
| **1** | Sell Cash-Secured Puts | Cobrar prima, posible asignación |
| **2** | Sell Covered Calls | Generar ingreso sobre acciones |

**Rentabilidad objetivo:** $4,000-$5,000 por ciclo en Tesla

---

## 🏗️ Arquitectura de Nivel Superior

```
┌─────────────────────────────────────────────────────────────────────┐
│                     ALPACA TRADING BOT                              │
├─────────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌────────────┐ │
│  │   AI        │  │   Risk      │  │  Backtest   │  │ Dashboard  │ │
│  │  Multi-Agent│  │  Manager    │  │   Engine    │  │  Real-time │ │
│  │  System     │  │  (4 capas)  │  │  + WFA + MC │  │  + WebSocket│ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └────────────┘ │
├─────────────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │              ESTRATEGIAS                                      │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐   │   │
│  │  │ Trailing    │  │ Copy        │  │ Wheel               │   │   │
│  │  │ Stop        │  │ Trading     │  │ Strategy            │   │   │
│  │  └─────────────┘  └─────────────┘  └─────────────────────┘   │   │
│  └──────────────────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │              NOTIFICACIONES MULTI-CANAL                       │   │
│  │  Discord │ Slack │ Telegram │ Email │ Pushover │ SMS         │   │
│  └──────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 📁 Estructura de Carpetas Completa

```
alpaca/
├── main.py                        # Orquestador principal
├── alpaca_client.py               # Cliente API de Alpaca
├── scheduler.py                   # Programador de tareas
├── requirements.txt               # Dependencias completas
├── credentials.example.txt        # Template para credenciales
├── .gitignore                     # Protege credenciales
│
├── risk_manager/                  # 🛡️ Risk Management Institucional
│   └── core.py                    # 4 capas de protección:
│                                  #   1. Pre-trade validation
│                                  #   2. In-trade monitoring
│                                  #   3. Portfolio risk
│                                  #   4. Circuit breakers
│
├── backtester/                    # 📊 Backtesting Engine
│   └── engine.py                  # Walk-Forward + Monte Carlo
│
├── ai_agents/                     # 🤖 Multi-Agent AI System
│   └── multi_agent_system.py      # 5 agentes especializados:
│                                  #   1. Market Analyst (técnico)
│                                  #   2. Sentiment Analyst (news/social)
│                                  #   3. Fundamental Analyst
│                                  #   4. Risk Manager
│                                  #   5. Portfolio Manager (decisión)
│
├── dashboard/                     # 🖥️ Dashboard en Tiempo Real
│   ├── app.py                     # Flask + SocketIO
│   └── templates/
│       └── dashboard.html         # UI moderna con gráficos
│
├── notifications/                 # 🔔 Sistema de Notificaciones
│   └── webhooks.py                # Discord, Slack, Telegram, Email
│
├── trailing_stop/                 # Estrategia 1
│   ├── config.py
│   └── strategy.py
│
├── copy_trading/                  # Estrategia 2
│   ├── config.py
│   └── capitol_scraper.py
│
└── wheel_strategy/                # Estrategia 3
    ├── config.py
    └── options_trader.py
```

---

## ⚙️ Setup Inicial

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Crear cuenta en Alpaca
- URL: https://alpaca.markets
- Seleccionar **Paper Trading** (dinero ficticio)
- Generar API Keys en Dashboard

### 3. Configurar credenciales

```bash
cp credentials.example.txt credentials.txt
```

Editar `credentials.txt`:
```
ENDPOINT=https://paper-api.alpaca.markets
KEY_ID=tu_api_key_aqui
SECRET_KEY=tu_secret_key_aqui
```

### 4. Ejecutar el bot

```bash
# Modo demo (evalúa trade sin ejecutar)
python main.py

# Modo producción (inicia loop de trading)
python main.py --live
```

---

## 🧪 Componentes de Nivel Superior

### 1. Risk Manager Institucional

| Capa | Función |
|------|---------|
| **Pre-trade** | Valida tamaño, exposición, correlación |
| **In-trade** | Monitorea stops, trailing, take-profit |
| **Portfolio** | Controla drawdown, VaR, exposición total |
| **Circuit Breaker** | Detiene trading si se violan umbrales |

**Métricas clave:**
- Kelly Criterion para sizing óptimo
- VaR 95% en tiempo real
- Máximo drawdown: 3% diario, 20% total

### 2. Multi-Agent AI System

Cada agente analiza independientemente y vota:

| Agente | Peso | Análisis |
|--------|------|----------|
| Market Analyst | 30% | Técnico (SMA, RSI, MACD, Bollinger) |
| Sentiment Analyst | 20% | Noticias + redes sociales |
| Fundamental Analyst | 25% | Valoración, crecimiento, márgenes |
| Risk Manager | 25% | Riesgo específico y de mercado |

**Decisión final:** Portfolio Manager consolida votos y determina tamaño óptimo

### 3. Backtesting Engine

| Característica | Descripción |
|----------------|-------------|
| **Vectorizado** | Ultrarrápido con NumPy/Pandas |
| **Walk-Forward** | Validación en múltiples ventanas |
| **Monte Carlo** | 1000+ simulaciones para stress test |
| **Métricas** | Sharpe, Sortino, Calmar, VaR, CVaR |

### 4. Dashboard en Tiempo Real

- Precios live vía WebSocket
- P&L actualizado cada segundo
- Gráficos de equity curve
- Control manual de operaciones
- Alertas visuales

### 5. Notificaciones Multi-Canal

| Canal | Uso |
|-------|-----|
| Discord | Alertas generales |
| Slack | Notificaciones de equipo |
| Telegram | Alertas push rápidas |
| Email | Reportes end-of-day |
| Pushover | Alertas críticas |
| SMS | Emergencias (circuit breaker) |

---

## 🤖 Top 5 Repositorios de Alpaca Trading (2025-2026)

| Repo | Stars | Features | URL |
|------|-------|----------|-----|
| **AlpacaTradingAgent** | 160 | Multi-agent LLM, Web UI, Crypto | [github.com/huygiatrng/AlpacaTradingAgent](https://github.com/huygiatrng/AlpacaTradingAgent) |
| **AlpacaBot** | 7 | Reinforcement Learning (DQN) | [github.com/sapperskills/AlpacaBot](https://github.com/sapperskills/AlpacaBot) |
| **PocketTrader** | 4 | GUI Tkinter, EMA+RSI | [github.com/redayzarra/PocketTrader](https://github.com/redayzarra/PocketTrader) |
| **alpaca-api-scaffolding** | 5 | RSI+Volume, Docker | [github.com/makedirectory/alpaca-api-scaffolding](https://github.com/makedirectory/alpaca-api-scaffolding) |
| **alpaca-trading-bot** | 0 | ChatGPT integration | [github.com/kaisewhite/alpaca-trading-bot](https://github.com/kaisewhite/alpaca-trading-bot) |

---

## 📚 Recursos Adicionales

### Documentación Oficial
- [Alpaca API Docs](https://alpaca.markets/docs/)
- [Alpaca Python SDK](https://github.com/alpacahq/alpaca-py)

### Backtesting & Análisis
- [Backtrader Documentation](https://www.backtrader.com/docu/)
- [VectorBT Documentation](https://vectorbt.dev/)

### Referencias de Trading
- [Pineify Blog - Backtrader + Alpaca](https://pineify.app/resources/blog/backtrader-alpaca-integration-complete-algorithmic-trading-guide)
- [Trading Strategies Academy](https://trading-strategies.academy/archives/1842)

---

## ⚠️ Disclaimer

> **ADVERTENCIA DE RIESGO:** Este software es solo para fines **educativos y de investigación**.

- 🧪 **Siempre prueba en Paper Trading primero**
- 📉 **Resultados pasados no garantizan resultados futuros**
- 💸 **Nunca operes dinero que no puedas permitirte perder**
- ⚖️ **El autor NO es asesor financiero**
- 🔒 **Usa bajo tu propio riesgo**

### Riesgos Específicos

| Riesgo | Descripción |
|--------|-------------|
| **Tecnológico** | Bugs, fallos de conexión, latencia |
| **Mercado** | Volatilidad extrema, gap openings |
| **Overfitting** | Estrategia funciona solo en backtest |
| **Regulatorio** | Cambios en legislación de trading algorítmico |

---

## 🚀 Roadmap

### Fase 1: Foundation ✅
- [x] Estructura básica de carpetas
- [x] Estrategias principales
- [x] Alpaca client

### Fase 2: Advanced Features ✅
- [x] Risk Manager multi-capa
- [x] Multi-Agent AI System
- [x] Backtesting Engine
- [x] Dashboard en tiempo real
- [x] Sistema de notificaciones

### Fase 3: Production (Pendiente)
- [ ] Deployment en AWS/GCP
- [ ] Integración con datos reales (Polygon.io)
- [ ] Monitoring con Prometheus + Grafana
- [ ] CI/CD pipeline
- [ ] Logging centralizado

---

## 📞 Soporte

Para issues, preguntas o contribuciones:
1. Revisa la documentación completa
2. Prueba en modo Paper Trading
3. Consulta los ejemplos en cada módulo

---

*Basado en el tutorial: "Claude Just Changed Stock Trading Forever"*

**Creado con ❤️ para la comunidad de trading algorítmico**
