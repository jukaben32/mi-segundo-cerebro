---
nombre: alpaca-py
tipo: librería
tags: #herramienta #trading #alpaca #python #sdk
fecha_creada: 2026-04-06
url: https://github.com/alpacahq/alpaca-py
stars: ~1.5k
mantenimiento: activo (oficial Alpaca)
---

## Qué es

SDK oficial de Python para la API de Alpaca Markets. Reemplaza al deprecado `alpaca-trade-api-python`. Orientado a objetos, con validación de datos via Pydantic.

## Instalación

```bash
pip install alpaca-py
```

## Módulos principales

```python
from alpaca.trading.client import TradingClient       # Órdenes, portfolio
from alpaca.data.historical import StockHistoricalDataClient  # Datos históricos
from alpaca.data.live import StockDataStream          # Streaming en vivo
from alpaca.broker.client import BrokerClient         # Broker API
```

## Ejemplo básico — comprar acción

```python
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

client = TradingClient("API_KEY", "SECRET_KEY", paper=True)

order = client.submit_order(
    MarketOrderRequest(
        symbol="AAPL",
        qty=1,
        side=OrderSide.BUY,
        time_in_force=TimeInForce.GTC
    )
)
```

## Ejemplo — obtener datos históricos

```python
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from datetime import datetime

data_client = StockHistoricalDataClient()

bars = data_client.get_stock_bars(
    StockBarsRequest(
        symbol_or_symbols=["AAPL", "MSFT"],
        timeframe=TimeFrame.Day,
        start=datetime(2024, 1, 1),
        end=datetime(2024, 12, 31)
    )
)
df = bars.df
```

## 🔗 Relacionado

- [[entities/alpaca-markets]]
- [[concepts/alpaca-trading-ecosystem]]
- [[sources/2026-04-06-alpaca-repos-research]]
