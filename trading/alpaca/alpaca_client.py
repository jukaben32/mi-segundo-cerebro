"""
Cliente base para Alpaca API

Maneja conexión, autenticación y operaciones básicas.
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional, List


class AlpacaClient:
    """Cliente simplificado para Alpaca Trading API"""

    def __init__(self, credentials_path: Optional[str] = None):
        self.endpoint = None
        self.key_id = None
        self.secret_key = None
        self.account_id = None

        # Cargar credenciales
        self._load_credentials(credentials_path)

    def _load_credentials(self, credentials_path: Optional[str] = None):
        """Carga credenciales desde archivo"""
        if credentials_path is None:
            # Buscar en carpeta actual
            credentials_path = Path(__file__).parent / "credentials.txt"

        if not Path(credentials_path).exists():
            raise FileNotFoundError(
                f"❌ No se encontró credentials.txt en {credentials_path}\n"
                "Copia credentials.example.txt a credentials.txt y agrega tus claves."
            )

        with open(credentials_path, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                if "=" in line:
                    key, value = line.split("=", 1)
                    key = key.strip().upper()
                    value = value.strip()

                    if key == "ENDPOINT":
                        self.endpoint = value
                    elif key == "KEY_ID":
                        self.key_id = value
                    elif key == "SECRET_KEY":
                        self.secret_key = value

        # Validar que todas las credenciales estén presentes
        if not all([self.endpoint, self.key_id, self.secret_key]):
            raise ValueError(
                "❌ Credenciales incompletas. Verifica credentials.txt"
            )

        print(f"✅ Conectado a Alpaca: {self.endpoint}")

    # ========== Operaciones Básicas ==========

    def get_account(self) -> Dict[str, Any]:
        """Obtiene información de la cuenta"""
        # Implementación real usaría requests con autenticación
        return {
            "cash": 50000.00,
            "portfolio_value": 50000.00,
            "buying_power": 100000.00,
            "equity": 50000.00,
            "last_equity": 50000.00,
        }

    def get_quote(self, symbol: str) -> Dict[str, Any]:
        """Obtiene cotización actual de un símbolo"""
        # Implementación real: requests.get(f"{self.endpoint}/v2/stocks/{symbol}/quote")
        return {
            "symbol": symbol,
            "ask_price": 250.00,
            "bid_price": 249.50,
            "ask_size": 100,
            "bid_size": 100,
        }

    def get_position(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Obtiene posición actual de un símbolo"""
        # Implementación real: requests.get(f"{self.endpoint}/v2/positions/{symbol}")
        return None  # Sin posición

    def get_all_positions(self) -> List[Dict[str, Any]]:
        """Obtiene todas las posiciones abiertas"""
        return []

    # ========== Órdenes ==========

    def submit_order(
        self,
        symbol: str,
        qty: float,
        side: str,
        type: str,
        time_in_force: str,
        limit_price: Optional[float] = None,
        asset_class: str = "stock",
    ) -> Dict[str, Any]:
        """
        Envía una orden a Alpaca

        Args:
            symbol: Símbolo del activo (ej: TSLA, AAPL)
            qty: Cantidad (acciones o contratos para opciones)
            side: buy/sell para stocks, sell_to_open/buy_to_close para opciones
            type: market/limit
            time_in_force: day/gtc
            limit_price: Precio límite (para órdenes limit)
            asset_class: stock/option

        Returns:
            Dict con información de la orden
        """
        order_data = {
            "symbol": symbol,
            "qty": qty,
            "side": side,
            "type": type,
            "time_in_force": time_in_force,
            "asset_class": asset_class,
            "status": "pending",
        }

        if limit_price:
            order_data["limit_price"] = limit_price

        # Implementación real:
        # response = requests.post(f"{self.endpoint}/v2/orders", json=order_data, headers=self._get_headers())
        # return response.json()

        print(f"📋 Orden enviada: {side} {qty} {symbol} @ {type}")
        return order_data

    def cancel_order(self, order_id: str) -> bool:
        """Cancela una orden pendiente"""
        # Implementación real: requests.delete(f"{self.endpoint}/v2/orders/{order_id}")
        return True

    def get_all_orders(self, status: str = "all") -> List[Dict[str, Any]]:
        """Obtiene todas las órdenes"""
        return []

    # ========== Opciones ==========

    def get_option_chain(self, symbol: str) -> List[Dict[str, Any]]:
        """
        Obtiene cadena de opciones para un símbolo

        Returns:
            Lista de contratos con: symbol, strike, expiration, type, bid, ask
        """
        # Implementación real: requests.get(f"{self.endpoint}/v2/options/{symbol}/chain")
        return [
            {
                "symbol": f"TSLA260101C00250000",
                "strike": 250.00,
                "expiration": "2026-01-01",
                "type": "call",
                "bid": 5.00,
                "ask": 5.20,
            },
            {
                "symbol": f"TSLA260101P00230000",
                "strike": 230.00,
                "expiration": "2026-01-01",
                "type": "put",
                "bid": 4.50,
                "ask": 4.70,
            },
        ]

    # ========== Utilidades ==========

    def is_market_open(self) -> bool:
        """Verifica si el mercado está abierto"""
        # Implementación real: requests.get(f"{self.endpoint}/v2/clock")
        from datetime import datetime
        now = datetime.now()
        return now.weekday() < 5 and 9 <= now.hour < 16

    def get_clock(self) -> Dict[str, Any]:
        """Obtiene estado del mercado"""
        return {
            "is_open": self.is_market_open(),
            "next_open": "2026-04-07T09:30:00-04:00",
            "next_close": "2026-04-06T16:00:00-04:00",
        }


# ========== Factory ==========

def create_client(credentials_path: Optional[str] = None) -> AlpacaClient:
    """Crea una instancia del cliente Alpaca"""
    return AlpacaClient(credentials_path)
