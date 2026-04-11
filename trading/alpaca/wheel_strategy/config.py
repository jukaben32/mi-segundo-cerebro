"""
Configuración para Wheel Strategy - Opciones

La "rueda" gira entre vender puts y covered calls.
"""

# Símbolo a operar
SYMBOL = "TSLA"

# Configuración Stage 1 - Vender Puts
PUT_SETTINGS = {
    "strike_offset_percent": 10,  # 10% debajo del precio actual
    "expiration_days_min": 14,  # 2 semanas
    "expiration_days_max": 30,  # 4 semanas
    "target_premium": 500,  # Prima objetivo mínima ($)
    "close_at_profit_percent": 50,  # Cerrar si gana 50% antes de expiración
}

# Configuración Stage 2 - Vender Calls
CALL_SETTINGS = {
    "strike_offset_percent": 10,  # 10% arriba del costo base
    "expiration_days_min": 14,
    "expiration_days_max": 30,
    "target_premium": 500,
    "close_at_profit_percent": 50,
}

# Reglas de riesgo
RISK_RULES = {
    "never_sell_put_without_cash": True,  # Siempre tener cash para asignación
    "never_sell_call_below_cost": True,  # Nunca vender call debajo del costo
    "max_contracts_open": 5,  # Máximo contratos abiertos simultáneos
}

# Horario de operación
MARKET_HOURS = {
    "start": "09:30",
    "end": "16:00",
    "days": ["monday", "tuesday", "wednesday", "thursday", "friday"],
}

# Intervalo de chequeo
CHECK_INTERVAL = 900  # 15 minutos durante mercado
