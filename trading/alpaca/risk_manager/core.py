"""
═══════════════════════════════════════════════════════════════════════════
RISK MANAGER - NIVEL INSTITUCIONAL
═══════════════════════════════════════════════════════════════════════════
Sistema de gestión de riesgo multi-capas con protecciones tipo hedge fund.

Características avanzadas:
- Kelly Criterion dinámico para sizing óptimo
- Value at Risk (VaR) en tiempo real
- Circuit breakers automáticos
- Correlación entre posiciones
- Drawdown protection con halting automático
- Exposure limits por sector/activo
"""

import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum


class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
    HALT = "halt_trading"


@dataclass
class PositionLimits:
    """Límites por posición"""
    max_position_value: float = 10000.0  # Máximo $ por posición
    max_position_percent: float = 0.05   # 5% del portfolio
    stop_loss_percent: float = 0.08      # 8% stop loss
    take_profit_percent: float = 0.10    # 10% take profit
    trailing_stop_percent: float = 0.05  # 5% trailing


@dataclass
class PortfolioLimits:
    """Límites del portfolio"""
    max_total_exposure: float = 0.95      # 95% máximo invertido
    max_sector_exposure: float = 0.25     # 25% por sector
    max_drawdown_daily: float = 0.03      # 3% drawdown diario
    max_drawdown_total: float = 0.20      # 20% drawdown total
    max_open_positions: int = 10
    max_correlation: float = 0.7          # Máxima correlación entre posiciones


@dataclass
class RiskMetrics:
    """Métricas de riesgo en tiempo real"""
    current_drawdown: float = 0.0
    daily_drawdown: float = 0.0
    var_95: float = 0.0  # Value at Risk 95%
    portfolio_beta: float = 1.0
    sharpe_ratio: float = 0.0
    total_exposure: float = 0.0
    sector_exposure: Dict[str, float] = field(default_factory=dict)
    correlation_matrix: Dict[str, Dict[str, float]] = field(default_factory=dict)


class AdvancedRiskManager:
    """
    Gestor de riesgo institucional con múltiples capas de protección.

    Capas:
    1. Pre-trade: Valida si la operación cumple reglas
    2. In-trade: Monitorea posiciones abiertas
    3. Portfolio: Controla exposición total y correlaciones
    4. Circuit Breaker: Detiene trading si se violan umbrales
    """

    def __init__(
        self,
        initial_capital: float,
        position_limits: PositionLimits = None,
        portfolio_limits: PortfolioLimits = None,
    ):
        self.initial_capital = initial_capital
        self.current_capital = initial_capital
        self.peak_capital = initial_capital
        self.day_start_capital = initial_capital

        self.position_limits = position_limits or PositionLimits()
        self.portfolio_limits = portfolio_limits or PortfolioLimits()

        self.positions: Dict[str, Dict[str, Any]] = {}
        self.trade_history: List[Dict[str, Any]] = []
        self.daily_pnl: List[float] = []

        # Estado de circuit breakers
        self.trading_halted = False
        self.halt_reason: Optional[str] = None
        self.halt_until: Optional[datetime] = None

        # Métricas en tiempo real
        self.metrics = RiskMetrics()

    # ═══════════════════════════════════════════════════════════════════
    # CAPA 1: PRE-TRADE VALIDATION
    # ═══════════════════════════════════════════════════════════════════

    def can_open_position(
        self,
        symbol: str,
        side: str,
        quantity: float,
        price: float,
        sector: Optional[str] = None,
    ) -> Tuple[bool, str]:
        """
        Valida si se puede abrir una posición (pre-trade check).

        Returns:
            (bool, str): (Puede abrir, razón si es rechazado)
        """
        # Check 0: Trading halt
        if self.trading_halted:
            return False, f"Trading halt: {self.halt_reason}"

        # Check 1: Límite de posiciones abiertas
        if len(self.positions) >= self.portfolio_limits.max_open_positions:
            return False, f"Máximo de posiciones abiertas ({self.portfolio_limits.max_open_positions})"

        # Check 2: Tamaño de posición
        position_value = quantity * price
        if position_value > self.position_limits.max_position_value:
            return False, f"Posición excede máximo (${position_value:.2f} > ${self.position_limits.max_position_value:.2f})"

        # Check 3: Porcentaje del portfolio
        position_percent = position_value / self.current_capital
        if position_percent > self.position_limits.max_position_percent:
            return False, f"Posición excede {self.position_limits.max_position_percent*100:.1f}% del portfolio"

        # Check 4: Exposure del sector
        if sector:
            current_sector_exposure = self.metrics.sector_exposure.get(sector, 0)
            new_sector_exposure = current_sector_exposure + position_value
            max_sector_value = self.current_capital * self.portfolio_limits.max_sector_exposure
            if new_sector_exposure > max_sector_value:
                return False, f"Sector {sector} excede {self.portfolio_limits.max_sector_exposure*100:.1f}%"

        # Check 5: Correlación (si ya hay posiciones)
        if self.positions:
            corr_check = self._check_correlation_risk(symbol)
            if not corr_check[0]:
                return corr_check

        # Check 6: Kelly Criterion para sizing óptimo
        kelly_size = self._calculate_kelly_position(symbol)
        if quantity > kelly_size:
            return False, f"Size excede Kelly Criterion ({quantity} > {kelly_size:.0f} acciones)"

        return True, "OK"

    def _check_correlation_risk(self, symbol: str) -> Tuple[bool, str]:
        """Verifica si la nueva posición aumenta demasiado la correlación"""
        # Implementación simplificada - en producción usar datos reales
        if len(self.positions) < 2:
            return True, "OK"

        # Calcular correlación promedio con posiciones existentes
        correlations = []
        for existing_symbol in self.positions.keys():
            corr = self._get_correlation(symbol, existing_symbol)
            correlations.append(corr)

        avg_correlation = np.mean(correlations)
        if avg_correlation > self.portfolio_limits.max_correlation:
            return False, f"Correlación promedio muy alta ({avg_correlation:.2f} > {self.portfolio_limits.max_correlation:.2f})"

        return True, "OK"

    def _get_correlation(self, symbol1: str, symbol2: str) -> float:
        """Obtiene correlación histórica entre dos símbolos"""
        # TODO: Implementar con datos históricos reales
        # Por defecto, asumir correlación moderada
        same_sector_pairs = {
            ("TSLA", "RIVN"): 0.75,
            ("AAPL", "MSFT"): 0.70,
            ("JPM", "BAC"): 0.80,
        }
        pair = tuple(sorted([symbol1, symbol2]))
        return same_sector_pairs.get(pair, 0.50)

    def _calculate_kelly_position(self, symbol: str) -> float:
        """
        Calcula tamaño óptimo de posición usando Kelly Criterion.

        Fórmula: f* = (p * b - q) / b
        donde:
          p = probabilidad de ganar
          q = probabilidad de perder (1 - p)
          b = odds (ganancia promedio / pérdida promedio)
        """
        # Obtener win rate histórico del símbolo
        win_rate = self._get_historical_win_rate(symbol)
        avg_win = self._get_historical_avg_win(symbol)
        avg_loss = self._get_historical_avg_loss(symbol)

        if avg_loss == 0:
            return 0

        b = avg_win / avg_loss
        p = win_rate
        q = 1 - p

        # Kelly fraction
        kelly_fraction = (p * b - q) / b

        # Kelly medio (más conservador)
        kelly_fraction = kelly_fraction / 2

        # Calcular número de acciones
        position_value = self.current_capital * max(0, kelly_fraction)
        price = self._get_current_price(symbol)

        return position_value / price if price > 0 else 0

    # ═══════════════════════════════════════════════════════════════════
    # CAPA 2: IN-TRADE MONITORING
    # ═══════════════════════════════════════════════════════════════════

    def monitor_positions(self, current_prices: Dict[str, float]) -> List[Dict[str, Any]]:
        """
        Monitorea todas las posiciones y genera acciones requeridas.

        Returns:
            Lista de acciones: [{"symbol": "TSLA", "action": "SELL", "reason": "stop_loss"}]
        """
        actions = []

        for symbol, position in self.positions.items():
            current_price = current_prices.get(symbol, position["entry_price"])

            # Check stop loss
            sl_action = self._check_stop_loss(symbol, position, current_price)
            if sl_action:
                actions.append(sl_action)
                continue

            # Check take profit
            tp_action = self._check_take_profit(symbol, position, current_price)
            if tp_action:
                actions.append(tp_action)
                continue

            # Check trailing stop
            ts_action = self._check_trailing_stop(symbol, position, current_price)
            if ts_action:
                actions.append(ts_action)

        return actions

    def _check_stop_loss(self, symbol: str, position: Dict, current_price: float) -> Optional[Dict]:
        """Verifica si se activó el stop loss"""
        entry_price = position["entry_price"]
        stop_loss_price = entry_price * (1 - self.position_limits.stop_loss_percent)

        if current_price <= stop_loss_price:
            return {
                "symbol": symbol,
                "action": "SELL",
                "reason": "stop_loss",
                "priority": "CRITICAL",
                "message": f"Stop loss activado: ${current_price:.2f} <= ${stop_loss_price:.2f}",
            }
        return None

    def _check_take_profit(self, symbol: str, position: Dict, current_price: float) -> Optional[Dict]:
        """Verifica si se alcanzó el take profit"""
        entry_price = position["entry_price"]
        take_profit_price = entry_price * (1 + self.position_limits.take_profit_percent)

        if current_price >= take_profit_price:
            return {
                "symbol": symbol,
                "action": "SELL",
                "reason": "take_profit",
                "priority": "HIGH",
                "message": f"Take profit alcanzado: ${current_price:.2f} >= ${take_profit_price:.2f}",
            }
        return None

    def _check_trailing_stop(self, symbol: str, position: Dict, current_price: float) -> Optional[Dict]:
        """Verifica trailing stop dinámico"""
        entry_price = position["entry_price"]
        highest_price = max(entry_price, position.get("highest_price", entry_price))

        # Actualizar precio más alto
        if current_price > highest_price:
            position["highest_price"] = current_price
            highest_price = current_price

        # Calcular trailing stop
        trailing_stop_price = highest_price * (1 - self.position_limits.trailing_stop_percent)

        if current_price <= trailing_stop_price and current_price > entry_price:
            return {
                "symbol": symbol,
                "action": "SELL",
                "reason": "trailing_stop",
                "priority": "HIGH",
                "message": f"Trailing stop activado: ${current_price:.2f} <= ${trailing_stop_price:.2f}",
            }
        return None

    # ═══════════════════════════════════════════════════════════════════
    # CAPA 3: PORTFOLIO RISK
    # ═══════════════════════════════════════════════════════════════════

    def update_portfolio_metrics(self, positions_value: float) -> None:
        """Actualiza métricas del portfolio"""
        # Calcular exposición total
        self.metrics.total_exposure = positions_value / self.current_capital

        # Calcular drawdown
        self.peak_capital = max(self.peak_capital, self.current_capital)
        self.metrics.current_drawdown = (self.peak_capital - self.current_capital) / self.peak_capital

        # Calcular drawdown diario
        self.metrics.daily_drawdown = (self.day_start_capital - self.current_capital) / self.day_start_capital

        # Calcular VaR 95% (simplificado)
        if len(self.daily_pnl) > 20:
            self.metrics.var_95 = np.percentile(self.daily_pnl, 5)

    def check_circuit_breakers(self) -> Tuple[bool, Optional[str]]:
        """
        Verifica circuit breakers a nivel portfolio.

        Returns:
            (bool, str): (Trading permitido, razón de halt si aplica)
        """
        # Check 1: Drawdown diario
        if self.metrics.daily_drawdown >= self.portfolio_limits.max_drawdown_daily:
            self._trigger_halt(f"Daily drawdown: {self.metrics.daily_drawdown*100:.2f}%")
            return False, self.halt_reason

        # Check 2: Drawdown total
        if self.metrics.current_drawdown >= self.portfolio_limits.max_drawdown_total:
            self._trigger_halt(f"Max drawdown: {self.metrics.current_drawdown*100:.2f}%")
            return False, self.halt_reason

        # Check 3: Exposure total
        if self.metrics.total_exposure > self.portfolio_limits.max_total_exposure:
            return False, f"Exposure total muy alto: {self.metrics.total_exposure*100:.2f}%"

        return True, None

    def _trigger_halt(self, reason: str, duration_minutes: int = 30) -> None:
        """Activa circuit breaker - detiene trading"""
        self.trading_halted = True
        self.halt_reason = reason
        self.halt_until = datetime.now() + timedelta(minutes=duration_minutes)
        print(f"🛑 CIRCUIT BREAKER ACTIVADO: {reason}")
        print(f"   Trading reanuda en {duration_minutes} minutos")

    def check_resume_trading(self) -> bool:
        """Verifica si se puede reanudar trading después de halt"""
        if not self.trading_halted:
            return True

        if datetime.now() >= self.halt_until:
            self.trading_halted = False
            self.halt_reason = None
            self.halt_until = None
            print("✅ Trading reanudado")
            return True

        return False

    # ═══════════════════════════════════════════════════════════════════
    # CAPA 4: UTILIDADES Y MÉTRICAS
    # ═══════════════════════════════════════════════════════════════════

    def add_position(self, symbol: str, quantity: float, entry_price: float, sector: str = None):
        """Agrega una posición al tracking"""
        self.positions[symbol] = {
            "symbol": symbol,
            "quantity": quantity,
            "entry_price": entry_price,
            "current_price": entry_price,
            "highest_price": entry_price,
            "sector": sector,
            "entry_time": datetime.now(),
        }

    def remove_position(self, symbol: str, exit_price: float):
        """Remueve una posición y registra P&L"""
        position = self.positions.get(symbol, {})
        entry_price = position.get("entry_price", exit_price)
        quantity = position.get("quantity", 0)

        # Calcular P&L
        pnl = (exit_price - entry_price) * quantity
        pnl_percent = (exit_price - entry_price) / entry_price

        # Registrar en histórico
        self.trade_history.append({
            "symbol": symbol,
            "entry_price": entry_price,
            "exit_price": exit_price,
            "pnl": pnl,
            "pnl_percent": pnl_percent,
            "exit_time": datetime.now(),
        })

        # Actualizar capital
        self.current_capital += pnl
        self.daily_pnl.append(pnl_percent)

        # Remover posición
        del self.positions[symbol]

    def get_risk_report(self) -> Dict[str, Any]:
        """Genera reporte completo de riesgo"""
        return {
            "trading_halted": self.trading_halted,
            "halt_reason": self.halt_reason,
            "metrics": {
                "current_drawdown": f"{self.metrics.current_drawdown*100:.2f}%",
                "daily_drawdown": f"{self.metrics.daily_drawdown*100:.2f}%",
                "var_95": f"{self.metrics.var_95*100:.2f}%",
                "total_exposure": f"{self.metrics.total_exposure*100:.2f}%",
            },
            "positions": len(self.positions),
            "trade_history_count": len(self.trade_history),
            "win_rate": self._calculate_win_rate(),
        }

    def _calculate_win_rate(self) -> float:
        """Calcula win rate histórico"""
        if not self.trade_history:
            return 0.0
        wins = sum(1 for t in self.trade_history if t["pnl"] > 0)
        return wins / len(self.trade_history)

    # Métodos auxiliares para datos históricos (implementar con datos reales)
    def _get_historical_win_rate(self, symbol: str) -> float:
        return 0.55  # Placeholder

    def _get_historical_avg_win(self, symbol: str) -> float:
        return 0.08  # 8%

    def _get_historical_avg_loss(self, symbol: str) -> float:
        return 0.05  # 5%

    def _get_current_price(self, symbol: str) -> float:
        return 250.0  # Placeholder


# ═══════════════════════════════════════════════════════════════════════
# EJEMPLO DE USO
# ═══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # Inicializar risk manager
    rm = AdvancedRiskManager(initial_capital=50000)

    # Intentar abrir posición
    can_trade, reason = rm.can_open_position(
        symbol="TSLA",
        side="buy",
        quantity=10,
        price=250.0,
        sector="Automotive",
    )

    print(f"¿Puede abrir posición? {can_trade} - {reason}")

    # Agregar posición
    if can_trade:
        rm.add_position("TSLA", 10, 250.0, "Automotive")

    # Monitorear
        prices = {"TSLA": 240.0}  # Simular caída
        actions = rm.monitor_positions(prices)
        print(f"Acciones requeridas: {actions}")

        # Reporte de riesgo
        print(f"\nReporte de riesgo: {rm.get_risk_report()}")
