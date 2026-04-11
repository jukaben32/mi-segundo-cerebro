"""
Configuración para Copy Trading Bot - Políticos del Congreso

Fuente de datos: https://capitoltrades.com
"""

# Político con mejor performance (actualizable)
TARGET_POLITICIAN = {
    "name": "Michael McCaul",
    "party": "R",
    "state": "TX",
    "capitol_trades_url": "https://capitoltrades.com/politicians/michael-mccaull",
}

# Configuración de copia
COPY_SETTINGS = {
    "max_position_size": 5000,  # Máximo $ por trade
    "follow_delay_minutes": 60,  # Esperar 1h antes de copiar (filtro de ruido)
    "min_trade_confidence": 0.7,  # Mínima confianza para copiar
}

# Tipos de operaciones a copiar
COPY_TYPES = {
    "stocks": True,
    "options": True,
    "etfs": True,
}

# Filtros
FILTERS = {
    "min_value": 1000,  # No copiar trades menores a $1000
    "max_positions": 20,  # Máximo de posiciones abiertas
}

# Horario de chequeo
CHECK_INTERVAL = 3600  # 1 hora
CAPITOL_TRADES_CHECK = 86400  # 24 horas para nuevos trades
