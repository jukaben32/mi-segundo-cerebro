"""
Configuración para Trailing Stop Strategy - Tesla (TSLA)
"""

# Símbolo a operar
SYMBOL = "TSLA"

# Cantidad inicial de acciones
INITIAL_SHARES = 10

# Stop loss inicial (porcentaje)
STOP_LOSS_PERCENT = 10.0  # -10%

# Trailing stop - solo sube, nunca baja
TRAILING_TRIGGER_PERCENT = 10.0  # Cuando sube 10%, activa trailing
TRAILING_STEP_PERCENT = 5.0  # El piso sube 5% cada vez

# Ladder buys - compras en caídas
LADDER_BUY_LEVELS = [
    {"drop_percent": 20, "shares": 10},
    {"drop_percent": 30, "shares": 20},
    {"drop_percent": 40, "shares": 30},
    {"drop_percent": 50, "shares": 50},
]

# Horario de mercado (EST)
MARKET_HOURS = {
    "start": "09:30",
    "end": "16:00",
    "days": ["monday", "tuesday", "wednesday", "thursday", "friday"],
}

# Intervalo de chequeo (segundos)
CHECK_INTERVAL = 300  # 5 minutos
