"""
═══════════════════════════════════════════════════════════════════════════
TRADING DASHBOARD - TIEMPO REAL
═══════════════════════════════════════════════════════════════════════════
Dashboard web con Flask + SocketIO para monitoreo en tiempo real.

Características:
- Precios en tiempo real (WebSocket)
- P&L live de posiciones
- Gráficos de equity curve
- Alertas y notificaciones
- Control manual de operaciones
- Métricas de riesgo en vivo
"""

from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
from datetime import datetime, timedelta
import threading
import time
import random
import json

# ═══════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN
# ═══════════════════════════════════════════════════════════════════════

app = Flask(__name__)
app.config["SECRET_KEY"] = "trading-dashboard-secret"
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

# Estado global del trading
trading_state = {
    "is_market_open": False,
    "last_update": datetime.now().isoformat(),
    "account": {
        "total_value": 50000.0,
        "cash": 25000.0,
        "buying_power": 50000.0,
        "day_pnl": 0.0,
        "day_pnl_percent": 0.0,
        "total_pnl": 0.0,
    },
    "positions": [],
    "recent_trades": [],
    "risk_metrics": {
        "current_drawdown": 0.0,
        "var_95": 0.0,
        "portfolio_beta": 1.0,
        "sharpe_ratio": 0.0,
    },
}

# Historial para gráficos
equity_history = []
price_history = {"TSLA": [], "SPY": []}


# ═══════════════════════════════════════════════════════════════════════
# SIMULACIÓN DE DATOS (En producción: conectar a Alpaca WebSocket)
# ═══════════════════════════════════════════════════════════════════════

def simulate_market_data():
    """Simula datos de mercado en tiempo real"""
    base_price_tsla = 250.0
    base_price_spy = 450.0

    while True:
        # Simular movimiento de precios
        ts = datetime.now()

        # TSLA
        change_tsla = random.gauss(0, 0.002)
        base_price_tsla *= (1 + change_tsla)
        price_history["TSLA"].append({
            "time": ts.isoformat(),
            "price": round(base_price_tsla, 2),
            "change": round(change_tsla * 100, 3),
        })

        # SPY
        change_spy = random.gauss(0.0001, 0.001)
        base_price_spy *= (1 + change_spy)
        price_history["SPY"].append({
            "time": ts.isoformat(),
            "price": round(base_price_spy, 2),
            "change": round(change_spy * 100, 3),
        })

        # Mantener solo últimos 100 puntos
        for key in price_history:
            if len(price_history[key]) > 100:
                price_history[key] = price_history[key][-100:]

        # Actualizar estado
        trading_state["last_update"] = ts.isoformat()

        # Calcular P&L simulado
        if trading_state["positions"]:
            day_pnl = 0
            for pos in trading_state["positions"]:
                if pos["symbol"] == "TSLA":
                    pnl = (base_price_tsla - pos["avg_cost"]) * pos["quantity"]
                    day_pnl += pnl
            trading_state["account"]["day_pnl"] = day_pnl
            trading_state["account"]["day_pnl_percent"] = (
                day_pnl / trading_state["account"]["total_value"] * 100
            )
            trading_state["account"]["total_value"] = (
                trading_state["account"]["cash"] +
                sum(p["quantity"] * base_price_tsla for p in trading_state["positions"] if p["symbol"] == "TSLA")
            )

        # Emitir actualización
        socketio.emit("market_update", {
            "TSLA": price_history["TSLA"][-1],
            "SPY": price_history["SPY"][-1],
            "account": trading_state["account"],
            "timestamp": ts.isoformat(),
        })

        time.sleep(1)  # Actualizar cada segundo


# ═══════════════════════════════════════════════════════════════════════
# RUTAS WEB
# ═══════════════════════════════════════════════════════════════════════

@app.route("/")
def index():
    """Página principal del dashboard"""
    return render_template("dashboard.html")


@app.route("/api/status")
def get_status():
    """API: Estado actual del trading"""
    return jsonify(trading_state)


@app.route("/api/positions")
def get_positions():
    """API: Lista de posiciones"""
    return jsonify(trading_state["positions"])


@app.route("/api/trades")
def get_trades():
    """API: Historial de trades"""
    return jsonify(trading_state["recent_trades"])


@app.route("/api/prices/<symbol>")
def get_prices(symbol):
    """API: Historial de precios de un símbolo"""
    return jsonify(price_history.get(symbol.upper(), []))


@app.route("/api/risk")
def get_risk():
    """API: Métricas de riesgo"""
    return jsonify(trading_state["risk_metrics"])


# ═══════════════════════════════════════════════════════════════════════
# WEBSOCKET EVENTS
# ═══════════════════════════════════════════════════════════════════════

@socketio.on("connect")
def handle_connect():
    """Cliente conectado"""
    print(f"Cliente conectado: {request.sid}")
    emit("connected", {"status": "connected", "message": "Dashboard conectado"})


@socketio.on("disconnect")
def handle_disconnect():
    """Cliente desconectado"""
    print(f"Cliente desconectado: {request.sid}")


@socketio.on("subscribe")
def handle_subscribe(data):
    """Cliente se suscribe a símbolos específicos"""
    symbols = data.get("symbols", ["TSLA", "SPY"])
    print(f"Cliente {request.sid} se suscribe a: {symbols}")
    emit("subscribed", {"symbols": symbols})


@socketio.on("buy")
def handle_buy(data):
    """Orden de compra manual"""
    symbol = data.get("symbol")
    quantity = data.get("quantity")

    # Simular ejecución
    trade = {
        "id": f"BUY-{datetime.now().strftime('%H%M%S')}",
        "symbol": symbol,
        "side": "BUY",
        "quantity": quantity,
        "price": price_history.get(symbol, [{ "price": 0 }])[-1]["price"],
        "timestamp": datetime.now().isoformat(),
        "status": "filled",
    }

    trading_state["recent_trades"].append(trade)

    # Agregar/actualizar posición
    existing_pos = next((p for p in trading_state["positions"] if p["symbol"] == symbol), None)
    if existing_pos:
        total_qty = existing_pos["quantity"] + quantity
        existing_pos["avg_cost"] = (
            (existing_pos["avg_cost"] * existing_pos["quantity"] + trade["price"] * quantity)
            / total_qty
        )
        existing_pos["quantity"] = total_qty
    else:
        trading_state["positions"].append({
            "symbol": symbol,
            "quantity": quantity,
            "avg_cost": trade["price"],
            "current_price": trade["price"],
            "unrealized_pnl": 0,
        })

    emit("order_filled", trade)
    print(f"Orden ejecutada: {trade}")


@socketio.on("sell")
def handle_sell(data):
    """Orden de venta manual"""
    symbol = data.get("symbol")
    quantity = data.get("quantity")

    # Buscar posición
    pos = next((p for p in trading_state["positions"] if p["symbol"] == symbol), None)

    if pos and pos["quantity"] >= quantity:
        trade = {
            "id": f"SELL-{datetime.now().strftime('%H%M%S')}",
            "symbol": symbol,
            "side": "SELL",
            "quantity": quantity,
            "price": price_history.get(symbol, [{ "price": 0 }])[-1]["price"],
            "timestamp": datetime.now().isoformat(),
            "status": "filled",
        }

        trading_state["recent_trades"].append(trade)

        # Actualizar posición
        pos["quantity"] -= quantity
        if pos["quantity"] == 0:
            trading_state["positions"].remove(pos)

        emit("order_filled", trade)
        print(f"Orden ejecutada: {trade}")
    else:
        emit("order_error", {"error": "Posición insuficiente"})


# ═══════════════════════════════════════════════════════════════════════
# INICIAR
# ═══════════════════════════════════════════════════════════════════════

def start_simulation():
    """Inicia la simulación de mercado en thread separado"""
    thread = threading.Thread(target=simulate_market_data, daemon=True)
    thread.start()
    print("📊 Simulación de mercado iniciada")


if __name__ == "__main__":
    print("=" * 70)
    print("TRADING DASHBOARD - Tiempo Real")
    print("=" * 70)

    start_simulation()

    print("\n🌐 Dashboard disponible en: http://localhost:5000")
    print("📡 WebSocket activo para actualizaciones en tiempo real")

    socketio.run(app, debug=False, port=5000, host="0.0.0.0")
