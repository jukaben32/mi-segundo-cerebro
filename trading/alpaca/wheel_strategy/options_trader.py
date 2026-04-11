"""
Wheel Strategy - Implementación principal

Stage 1: Vender Puts (cash-secured)
Stage 2: Vender Covered Calls (sobre acciones asignadas)
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List


class WheelStrategy:
    def __init__(self, alpaca_client, config: Dict[str, Any]):
        self.client = alpaca_client
        self.config = config
        self.stage = 1  # 1 = Puts, 2 = Calls
        self.shares_owned: int = 0
        self.cost_basis: float = 0.0
        self.open_contracts: List[Dict[str, Any]] = []
        self.total_premiums_collected: float = 0.0

    def get_current_price(self) -> float:
        """Obtiene precio actual del símbolo"""
        quote = self.client.get_quote(self.config["SYMBOL"])
        return float(quote["ask_price"])

    # ========== STAGE 1: VENDER PUTS ==========

    def sell_cash_secured_put(self) -> Optional[Dict[str, Any]]:
        """
        Stage 1: Vende put cash-secured
        - Strike ~10% debajo del precio actual
        - Expiración 2-4 semanas
        """
        current_price = self.get_current_price()
        strike_price = current_price * (1 - self.config["PUT_SETTINGS"]["strike_offset_percent"] / 100)

        # Calcular días hasta expiración
        target_days = (self.config["PUT_SETTINGS"]["expiration_days_min"] +
                       self.config["PUT_SETTINGS"]["expiration_days_max"]) // 2
        expiration = datetime.now() + timedelta(days=target_days)

        # Verificar que hay cash suficiente
        cash_available = float(self.client.get_account()["cash"])
        required_cash = strike_price * 100  # 1 contrato = 100 acciones

        if cash_available < required_cash:
            print(f"❌ Cash insuficiente: ${cash_available:.2f} < ${required_cash:.2f}")
            return None

        # Buscar opción disponible
        option_chain = self.client.get_option_chain(self.config["SYMBOL"])
        put_contract = self._find_best_contract(
            option_chain,
            strike_price,
            expiration,
            "put"
        )

        if not put_contract:
            print("⚠️ No se encontró contrato adecuado")
            return None

        # Vender el put
        order = self.client.submit_order(
            symbol=put_contract["symbol"],
            qty=1,
            side="sell_to_open",
            type="limit",
            limit_price=put_contract["bid"],
            time_in_force="day",
            asset_class="option",
        )

        self.open_contracts.append({
            "type": "put",
            "symbol": put_contract["symbol"],
            "strike": strike_price,
            "premium": put_contract["bid"] * 100,
            "expiration": expiration,
        })

        self.total_premiums_collected += put_contract["bid"] * 100
        print(f"📉 Put vendido: Strike ${strike_price:.2f}, Prima ${put_contract['bid'] * 100:.2f}")

        return order

    # ========== STAGE 2: VENDER CALLS ==========

    def sell_covered_call(self) -> Optional[Dict[str, Any]]:
        """
        Stage 2: Vende covered call sobre acciones poseídas
        - Strike ~10% arriba del costo base
        - Expiración 2-4 semanas
        """
        if self.shares_owned < 100:
            print(f"⚠️ Se necesitan 100 acciones, tienes {self.shares_owned}")
            return None

        strike_price = self.cost_basis * (1 + self.config["CALL_SETTINGS"]["strike_offset_percent"] / 100)

        target_days = (self.config["CALL_SETTINGS"]["expiration_days_min"] +
                       self.config["CALL_SETTINGS"]["expiration_days_max"]) // 2
        expiration = datetime.now() + timedelta(days=target_days)

        option_chain = self.client.get_option_chain(self.config["SYMBOL"])
        call_contract = self._find_best_contract(
            option_chain,
            strike_price,
            expiration,
            "call"
        )

        if not call_contract:
            return None

        order = self.client.submit_order(
            symbol=call_contract["symbol"],
            qty=1,
            side="sell_to_open",
            type="limit",
            limit_price=call_contract["bid"],
            time_in_force="day",
            asset_class="option",
        )

        self.open_contracts.append({
            "type": "call",
            "symbol": call_contract["symbol"],
            "strike": strike_price,
            "premium": call_contract["bid"] * 100,
            "expiration": expiration,
        })

        self.total_premiums_collected += call_contract["bid"] * 100
        print(f"📈 Call vendido: Strike ${strike_price:.2f}, Prima ${call_contract['bid'] * 100:.2f}")

        return order

    # ========== UTILIDADES ==========

    def _find_best_contract(self, chain: List[Dict], target_strike: float,
                           target_exp: datetime, option_type: str) -> Optional[Dict]:
        """Encuentra el mejor contrato según strike y expiración"""
        best_contract = None
        best_bid = 0

        for contract in chain:
            if contract["type"] != option_type:
                continue

            # Verificar strike cercano
            strike_diff = abs(contract["strike"] - target_strike) / target_strike
            if strike_diff > 0.05:  # Máximo 5% de diferencia
                continue

            # Verificar expiración
            exp_diff = abs((contract["expiration"] - target_exp).days)
            if exp_diff > 7:  # Máximo 7 días de diferencia
                continue

            # Seleccionar mejor bid
            if contract["bid"] > best_bid:
                best_bid = contract["bid"]
                best_contract = contract

        return best_contract

    def check_close_early(self, current_price: float) -> Optional[Dict[str, Any]]:
        """Cierra contratos con 50% de ganancia antes de expiración"""
        for contract in self.open_contracts[:]:
            current_value = self._get_contract_value(contract)
            if current_value <= contract["premium"] * 0.5:
                # Cerrar posición
                self.client.submit_order(
                    symbol=contract["symbol"],
                    qty=1,
                    side="buy_to_close",
                    type="market",
                    time_in_force="day",
                    asset_class="option",
                )
                self.open_contracts.remove(contract)
                print(f"✅ Contrato cerrado temprano con 50% ganancia")

        return None

    def _get_contract_value(self, contract: Dict) -> float:
        """Obtiene valor actual del contrato"""
        # Implementación real necesitaría fetch del precio actual
        return 0.0

    def get_status(self) -> Dict[str, Any]:
        """Retorna estado de la estrategia"""
        return {
            "stage": self.stage,
            "shares_owned": self.shares_owned,
            "cost_basis": self.cost_basis,
            "open_contracts": len(self.open_contracts),
            "total_premiums": self.total_premiums_collected,
            "strategy": "wheel",
        }
