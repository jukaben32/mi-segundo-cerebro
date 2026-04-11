"""
Trailing Stop Strategy - Implementación principal

Lógica:
1. Compra inicial de acciones al precio de mercado
2. Monitorea el precio cada 5 minutos durante horario de mercado
3. Si el precio sube, el stop loss sube (trailing)
4. Si el precio cae al stop loss, vende todo
5. Si el precio cae niveles de ladder, compra más
"""

from datetime import datetime
from typing import Optional, Dict, Any


class TrailingStopStrategy:
    def __init__(self, alpaca_client, config: Dict[str, Any]):
        self.client = alpaca_client
        self.config = config
        self.purchase_price: Optional[float] = None
        self.current_floor: Optional[float] = None
        self.shares_owned: int = 0
        self.total_invested: float = 0.0

    def execute_initial_buy(self, shares: int) -> Dict[str, Any]:
        """Compra inicial de acciones"""
        order = self.client.submit_order(
            symbol=self.config["SYMBOL"],
            qty=shares,
            side="buy",
            type="market",
            time_in_force="gtc",
        )
        self.shares_owned = shares
        self.purchase_price = float(order["avg_fill_price"])
        self.current_floor = self.purchase_price * (1 - self.config["STOP_LOSS_PERCENT"] / 100)
        self.total_invested = self.purchase_price * shares
        return order

    def check_trailing_stop(self, current_price: float) -> Optional[Dict[str, Any]]:
        """
        Verifica si debe ajustar el trailing stop o vender.
        El piso SOLO sube, nunca baja.
        """
        if not self.purchase_price or not self.current_floor:
            return None

        # Calcular precio actual del piso (10% arriba del precio de compra)
        trailing_trigger = self.purchase_price * (1 + self.config["TRAILING_TRIGGER_PERCENT"] / 100)

        # Si el precio actual supera el trigger, actualizamos el piso
        if current_price > trailing_trigger:
            new_floor = current_price * (1 - self.config["TRAILING_STEP_PERCENT"] / 100)
            if new_floor > self.current_floor:
                self.current_floor = new_floor
                print(f"📈 Trailing floor actualizado: ${self.current_floor:.2f}")

        # Verificar si tocó el piso → VENDER
        if current_price <= self.current_floor:
            return self.execute_sell_all()

        return None

    def check_ladder_buy(self, current_price: float) -> Optional[Dict[str, Any]]:
        """Verifica si debe ejecutar compras escalonadas en caídas"""
        if not self.purchase_price:
            return None

        drop_percent = ((self.purchase_price - current_price) / self.purchase_price) * 100

        for level in self.config["LADDER_BUY_LEVELS"]:
            if drop_percent >= level["drop_percent"]:
                return self.execute_buy(level["shares"])

        return None

    def execute_sell_all(self) -> Dict[str, Any]:
        """Vende todas las acciones cuando toca el stop loss"""
        if self.shares_owned <= 0:
            return {"status": "no_position"}

        order = self.client.submit_order(
            symbol=self.config["SYMBOL"],
            qty=self.shares_owned,
            side="sell",
            type="market",
            time_in_force="gtc",
        )

        pnl = (current_price - self.purchase_price) * self.shares_owned
        print(f"🛑 STOP LOSS ejecutado - PnL: ${pnl:.2f}")

        self.shares_owned = 0
        self.purchase_price = None
        self.current_floor = None
        return order

    def execute_buy(self, shares: int) -> Dict[str, Any]:
        """Ejecuta compra de acciones"""
        order = self.client.submit_order(
            symbol=self.config["SYMBOL"],
            qty=shares,
            side="buy",
            type="market",
            time_in_force="gtc",
        )
        self.shares_owned += shares
        print(f"📈 Ladder Buy: {shares} acciones")
        return order

    def get_status(self) -> Dict[str, Any]:
        """Retorna el estado actual de la estrategia"""
        return {
            "symbol": self.config["SYMBOL"],
            "shares_owned": self.shares_owned,
            "purchase_price": self.purchase_price,
            "current_floor": self.current_floor,
            "total_invested": self.total_invested,
            "strategy": "trailing_stop",
        }
