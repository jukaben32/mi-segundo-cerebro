---
nombre: Alpaca Markets
tipo: plataforma
tags: #herramienta #trading #alpaca #broker #api
fecha_creada: 2026-04-06
url: https://alpaca.markets
precio: Gratis (comisión 0 en acciones USA), API gratuita
---

## Qué es

Broker y plataforma de trading algorítmico con API REST/WebSocket. Permite operar acciones y opciones del mercado USA (NYSE, NASDAQ) de forma programática. Ofrece **paper trading** (dinero ficticio) para pruebas sin riesgo.

## SDK oficial actual

**`alpaca-py`** → https://github.com/alpacahq/alpaca-py
- ⚠️ El antiguo `alpaca-trade-api-python` está **deprecado** desde 2023
- Usa `alpaca-py` en todos los proyectos nuevos

## Capacidades de la API

| Función | Descripción |
|---------|-------------|
| Trading API | Órdenes, posiciones, portfolio |
| Market Data API | Datos históricos y streaming en tiempo real |
| Broker API | Para crear productos financieros sobre Alpaca |
| Paper Trading | Endpoint separado para pruebas sin dinero real |
| Options Trading | Contratos de opciones (desde 2024) |

## Endpoints

- **Live trading**: `https://api.alpaca.markets`
- **Paper trading**: `https://paper-api.alpaca.markets`
- **Market data**: `https://data.alpaca.markets`

## Autenticación

```python
from alpaca.trading.client import TradingClient

client = TradingClient(
    api_key="PKXXXXX",       # API Key ID
    secret_key="XXXXXXXX",   # Secret Key
    paper=True               # True = paper trading
)
```

## 🔗 Relacionado

- [[concepts/alpaca-trading-ecosystem]]
- [[entities/alpaca-py]]
- [[entities/alpaca-mcp-server]]
- [[sources/2026-04-06-alpaca-repos-research]]
