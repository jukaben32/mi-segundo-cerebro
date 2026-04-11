# 🧩 Setup: Alpaca MCP Server

El **Alpaca MCP Server** permite integrar las herramientas de trading de Alpaca directamente con asistentes AI como Claude, Cursor y VS Code.

---

## 📋 Requisitos

- **Python 3.10+**
- **uv** instalado: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- **API Keys de Alpaca** (gratis en paper trading)

---

## 🔑 Obtener API Keys

1. Ve a https://app.alpaca.markets/paper/dashboard/overview
2. Crea una cuenta gratuita de paper trading
3. Genera las API Keys desde el dashboard

---

## ⚙️ Configuración en Claude Desktop (Windows)

Edita el archivo:
```
C:\Users\hp\AppData\Roaming\Claude\claude_desktop_config.json
```

Agrega:
```json
{
  "mcpServers": {
    "alpaca": {
      "command": "uvx",
      "args": ["alpaca-mcp-server"],
      "env": {
        "ALPACA_API_KEY": "tu_api_key_aqui",
        "ALPACA_SECRET_KEY": "tu_secret_key_aqui",
        "ALPACA_PAPER_TRADE": "true"
      }
    }
  }
}
```

Reinicia Claude Desktop.

---

## ⚙️ Configuración en Claude Code (CLI)

Ejecuta este comando en la terminal:

```bash
claude mcp add alpaca --scope user --transport stdio uvx alpaca-mcp-server \
  --env ALPACA_API_KEY=tu_api_key_aqui \
  --env ALPACA_SECRET_KEY=tu_secret_key_aqui \
  --env ALPACA_PAPER_TRADE=true
```

Verifica con `/mcp` en Claude Code.

---

## ⚙️ Configuración en Cursor

Edita `~/.cursor/mcp.json` o usa el [Cursor Directory](https://cursor.directory/mcp/alpaca):

```json
{
  "mcpServers": {
    "alpaca": {
      "command": "uvx",
      "args": ["alpaca-mcp-server"],
      "env": {
        "ALPACA_API_KEY": "tu_api_key_aqui",
        "ALPACA_SECRET_KEY": "tu_secret_key_aqui",
        "ALPACA_PAPER_TRADE": "true"
      }
    }
  }
}
```

---

## ⚙️ Configuración en VS Code

Crea `.vscode/mcp.json` en tu proyecto:

```json
{
  "mcp": {
    "servers": {
      "alpaca": {
        "type": "stdio",
        "command": "uvx",
        "args": ["alpaca-mcp-server"],
        "env": {
          "ALPACA_API_KEY": "tu_api_key_aqui",
          "ALPACA_SECRET_KEY": "tu_secret_key_aqui",
          "ALPACA_PAPER_TRADE": "true"
        }
      }
    }
  }
}
```

---

## 🛠️ Herramientas Disponibles

### Account & Portfolio
- `get_account_info` — Saldo, margen, estado de cuenta
- `get_portfolio_history` — Historial de equity y P/L
- `get_account_activities` — Actividad de la cuenta

### Trading (Órdenes)
- `get_orders` — Listar órdenes con filtros
- `place_stock_order` — Comprar/vender acciones
- `place_option_order` — Órdenes de opciones
- `cancel_order_by_id` — Cancelar orden
- `cancel_all_orders` — Cancelar todas las órdenes

### Posiciones
- `get_all_positions` — Todas las posiciones abiertas
- `close_position` — Cerrar posición específica
- `close_all_positions` — Liquidar todo el portfolio

### Market Data
- `get_stock_bars` — Velas históricas
- `get_stock_latest_quote` — Cotización en tiempo real
- `get_market_movers` — Mayores ganadores/perdedores

### Opciones
- `get_option_contracts` — Contratos disponibles
- `get_option_snapshot` — Snapshot con Griegas e IV
- `get_option_chain` — Cadena completa de opciones

---

## 📝 Ejemplos de Prompts

**Básicos:**
```
¿Cuál es mi saldo actual y poder de compra en Alpaca?
Muestra mis posiciones actuales
Compra 5 acciones de AAPL al precio de mercado
Vende 5 acciones de TSLA con límite en $300
Cancela todas las órdenes abiertas
```

**Opciones:**
```
Muéstrame contratos de opciones de AAPL que vencen el próximo mes
Obtén la cadena de opciones para SPY
Coloca una orden de compra para 1 call de AAPL
```

**Market Data:**
```
Obtén las velas diarias de NVDA de los últimos 5 días
¿Cuál fue el precio de cierre de TSLA ayer?
Muéstrame los mayores ganadores del día
```

---

## 🧪 Testing

Ejecuta tests locales:

```bash
cd alpaca-mcp-server
pytest tests/test_integrity.py tests/test_server_construction.py -v
```

Para tests de integración (requiere API keys):

```bash
ALPACA_API_KEY=... ALPACA_SECRET_KEY=... pytest tests/ -m integration -v
```

---

## ⚠️ Live Trading

Por defecto, el servidor usa **Paper Trading**. Para live trading:

```json
{
  "env": {
    "ALPACA_API_KEY": "tu_live_api_key",
    "ALPACA_SECRET_KEY": "tu_live_secret_key",
    "ALPACA_PAPER_TRADE": "false"
  }
}
```

---

## 🔗 Recursos

- [Documentación Oficial](https://github.com/alpacahq/alpaca-mcp-server)
- [Alpaca API Docs](https://docs.alpaca.markets/)
- [Python SDK](https://alpaca.markets/sdks/python/)

---

## 🆘 Troubleshooting

| Problema | Solución |
|----------|----------|
| `uvx: command not found` | Instala uv: https://docs.astral.sh/uv/getting-started/installation/ |
| Sin credenciales | Verifica `ALPACA_API_KEY` y `ALPACA_SECRET_KEY` en el `env` |
| El cliente no detecta cambios | Reinicia Claude/Cursor/VS Code |
| Tools no aparecen | Inicia una nueva sesión/chat |

---

*Setup creado para integración con el Alpaca Trading Bot*
