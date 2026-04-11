"""
═══════════════════════════════════════════════════════════════════════════
ALPACA TRADING BOT - ORQUESTADOR PRINCIPAL
═══════════════════════════════════════════════════════════════════════════
Sistema de trading institucional multi-estrategia con:
- Multi-Agent AI Decision System
- Advanced Risk Management
- Backtesting Engine con Walk-Forward Validation
- Real-time Dashboard
- Multi-Channel Notifications

Estrategias soportadas:
1. Trailing Stop (Tesla, growth stocks)
2. Copy Trading (Políticos del Congreso)
3. Wheel Strategy (Opciones)

═══════════════════════════════════════════════════════════════════════════
"""

import sys
import time
import json
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from pathlib import Path

# Agregar ruta al path
sys.path.insert(0, str(Path(__file__).parent))

# Importar componentes principales
from risk_manager.core import AdvancedRiskManager, PositionLimits, PortfolioLimits
from backtester.engine import AdvancedBacktester, BacktestConfig
from ai_agents.multi_agent_system import MultiAgentTradingSystem, Signal
from notifications.webhooks import (
    NotificationManager,
    TradeAlert,
    RiskAlert,
    setup_notification_manager,
)
from alpaca_client import AlpacaClient
from scheduler import TradingScheduler


# ═══════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN PRINCIPAL
# ═══════════════════════════════════════════════════════════════════════

class TradingBotConfig:
    """Configuración global del bot"""

    # Capital y riesgo
    INITIAL_CAPITAL = 50000.0
    MAX_POSITION_PERCENT = 0.10  # 10% máximo por posición
    MAX_DAILY_DRAWDOWN = 0.03    # 3% drawdown diario máximo
    MAX_TOTAL_DRAWDOWN = 0.20    # 20% drawdown total máximo

    # Estrategias activas
    STRATEGIES = {
        "trailing_stop": {
            "enabled": True,
            "symbols": ["TSLA", "NVDA", "AMD"],
            "initial_shares": 10,
            "stop_loss_percent": 0.08,
            "trailing_stop_percent": 0.05,
        },
        "copy_trading": {
            "enabled": False,  # Requiere configuración adicional
            "politician": "Michael McCaul",
        },
        "wheel_strategy": {
            "enabled": True,
            "symbols": ["TSLA", "AAPL", "MSFT"],
            "target_premium": 500,
        },
    }

    # Notificaciones
    NOTIFICATIONS = {
        "discord_webhook": None,  # Configurar en .env
        "telegram_token": None,
        "telegram_chat_id": None,
        "email_enabled": False,
    }

    # Trading hours
    MARKET_OPEN = "09:30"
    MARKET_CLOSE = "16:00"

    # Check interval (segundos)
    CHECK_INTERVAL = 300  # 5 minutos


# ═══════════════════════════════════════════════════════════════════════
# ORQUESTADOR PRINCIPAL
# ═══════════════════════════════════════════════════════════════════════

class AlpacaTradingBot:
    """
    Orquestador principal del sistema de trading.

    Coordina:
    - Risk Manager
    - Multi-Agent AI System
    - Estrategias individuales
    - Notificaciones
    - Dashboard
    """

    def __init__(self, config: TradingBotConfig = None):
        self.config = config or TradingBotConfig()

        print("=" * 70)
        print("ALPACA TRADING BOT - Institucional")
        print("=" * 70)

        # Inicializar componentes
        print("\n📦 Inicializando componentes...")

        # 1. Risk Manager
        self.risk_manager = AdvancedRiskManager(
            initial_capital=self.config.INITIAL_CAPITAL,
            position_limits=PositionLimits(
                max_position_percent=self.config.MAX_POSITION_PERCENT,
                stop_loss_percent=self.config.STRATEGIES["trailing_stop"]["stop_loss_percent"],
                trailing_stop_percent=self.config.STRATEGIES["trailing_stop"]["trailing_stop_percent"],
            ),
            portfolio_limits=PortfolioLimits(
                max_drawdown_daily=self.config.MAX_DAILY_DRAWDOWN,
                max_drawdown_total=self.config.MAX_TOTAL_DRAWDOWN,
            ),
        )
        print("  ✅ Risk Manager inicializado")

        # 2. Multi-Agent AI System
        self.ai_system = MultiAgentTradingSystem()
        print("  ✅ AI Multi-Agent System inicializado")

        # 3. Backtester
        self.backtester = AdvancedBacktester(
            BacktestConfig(initial_capital=self.config.INITIAL_CAPITAL)
        )
        print("  ✅ Backtest Engine inicializado")

        # 4. Alpaca Client (puede fallar si no hay credenciales)
        try:
            self.alpaca = AlpacaClient()
            print("  ✅ Alpaca Client conectado")
        except FileNotFoundError:
            print("  ⚠️  Alpaca Client: Sin credenciales (modo simulación)")
            self.alpaca = None

        # 5. Notification Manager
        self.notifications = setup_notification_manager(self.config.NOTIFICATIONS)
        print("  ✅ Notification Manager inicializado")

        # 6. Scheduler
        self.scheduler = TradingScheduler()
        print("  ✅ Trading Scheduler inicializado")

        # Estado del bot
        self.is_running = False
        self.current_positions: Dict[str, Any] = {}

        print("\n✅ Sistema listo para operar\n")

    # ═══════════════════════════════════════════════════════════════════
    # MÉTODOS PÚBLICOS
    # ═══════════════════════════════════════════════════════════════════

    def start(self):
        """Inicia el bot de trading"""
        print("\n🚀 Iniciando Alpaca Trading Bot...")
        print(f"   Capital inicial: ${self.config.INITIAL_CAPITAL:,.2f}")
        print(f"   Estrategias activas: {self._get_active_strategies()}")
        print(f"   Check interval: {self.config.CHECK_INTERVAL}s")
        print("\n" + "=" * 70 + "\n")

        self.is_running = True

        # Programar tareas
        self._schedule_tasks()

        # Iniciar loop principal
        try:
            self.scheduler.run_loop()
        except KeyboardInterrupt:
            print("\n\n🛑 Deteniendo bot por usuario...")
            self.stop()

    def stop(self):
        """Detiene el bot de trading"""
        self.is_running = False
        self.scheduler.stop()
        print("✅ Bot detenido")

    def evaluate_trade(self, symbol: str) -> Dict[str, Any]:
        """
        Evalúa si se debe abrir una posición en un símbolo.

        Proceso:
        1. AI Multi-Agent System genera recomendación
        2. Risk Manager valida la operación
        3. Se retorna decisión final

        Returns:
            Dict con: should_trade (bool), reason (str), size (float)
        """
        print(f"\n🔍 Evaluando trade en {symbol}...")

        # 1. Obtener decisión de AI
        ai_decision = self.ai_system.evaluate_trade(symbol)

        print(f"   AI Signal: {ai_decision.final_signal.name}")
        print(f"   AI Confidence: {ai_decision.final_confidence*100:.1f}%")
        print(f"   Recommended Size: {ai_decision.recommended_position_size*100:.1f}%")

        # 2. Validar con Risk Manager
        if ai_decision.final_signal in [Signal.BUY, Signal.STRONG_BUY]:
            price = self._get_current_price(symbol)
            quantity = int(
                (self.config.INITIAL_CAPITAL * ai_decision.recommended_position_size)
                / price
            )

            can_trade, reason = self.risk_manager.can_open_position(
                symbol=symbol,
                side="buy",
                quantity=quantity,
                price=price,
            )

            print(f"   Risk Check: {'✅ OK' if can_trade else '❌ RECHAZADO'} - {reason}")

            return {
                "should_trade": can_trade,
                "reason": reason,
                "size": quantity if can_trade else 0,
                "ai_signal": ai_decision.final_signal.name,
                "ai_confidence": ai_decision.final_confidence,
            }

        return {
            "should_trade": False,
            "reason": f"AI signal: {ai_decision.final_signal.name}",
            "size": 0,
            "ai_signal": ai_decision.final_signal.name,
            "ai_confidence": ai_decision.final_confidence,
        }

    def execute_trade(self, symbol: str, side: str, quantity: float) -> bool:
        """Ejecuta una operación"""
        print(f"\n📋 Ejecutando: {side} {quantity} {symbol}")

        if self.alpaca is None:
            print("   ⚠️  Modo simulación - no se ejecuta realmente")
            return True

        try:
            # Ejecutar orden
            order = self.alpaca.submit_order(
                symbol=symbol,
                qty=quantity,
                side=side.lower(),
                type="market",
                time_in_force="gtc",
            )

            # Registrar en risk manager
            if side.upper() == "BUY":
                price = float(order.get("avg_fill_price", 0))
                self.risk_manager.add_position(symbol, quantity, price)

            # Notificar
            alert = TradeAlert(
                symbol=symbol,
                side=side.upper(),
                quantity=quantity,
                price=float(order.get("avg_fill_price", 0)),
            )
            self.notifications.send_trade_alert(alert)

            print(f"   ✅ Orden ejecutada: {order.get('id', 'N/A')}")
            return True

        except Exception as e:
            print(f"   ❌ Error ejecutando orden: {e}")
            return False

    def run_backtest(self, symbol: str, strategy_func, data: Any) -> Dict[str, Any]:
        """Ejecuta backtest de una estrategia"""
        print(f"\n📊 Ejecutando backtest para {symbol}...")

        metrics = self.backtester.run_backtest(data, strategy_func)

        # Walk-Forward Analysis
        wfa = self.backtester.walk_forward_analysis(data, strategy_func)

        # Monte Carlo
        mc = self.backtester.monte_carlo_simulation(n_simulations=1000)

        # Mostrar resultados
        print("\n" + "=" * 50)
        print("RESULTADOS DEL BACKTEST")
        print("=" * 50)

        summary = self.backtester.get_metrics_summary()
        for category, items in summary.items():
            print(f"\n{category}:")
            for key, value in items.items():
                print(f"  {key}: {value}")

        print(f"\n🔄 Walk-Forward Analysis:")
        print(f"  Ventanas: {wfa['total_windows']}")
        print(f"  Retorno promedio: {wfa['avg_return']*100:.2f}%")
        print(f"  Consistencia Sharpe: {wfa['sharpe_consistency']*100:.1f}%")

        print(f"\n🎲 Monte Carlo Simulation:")
        print(f"  Mediana Equity Final: ${mc['median_final_equity']:,.2f}")
        print(f"  Probabilidad Ruina: {mc['ruin_probability']*100:.2f}%")

        return {
            "metrics": summary,
            "walk_forward": wfa,
            "monte_carlo": mc,
        }

    def get_status(self) -> Dict[str, Any]:
        """Retorna estado actual del bot"""
        risk_report = self.risk_manager.get_risk_report()

        return {
            "is_running": self.is_running,
            "capital": self.risk_manager.current_capital,
            "positions": len(self.risk_manager.positions),
            "trading_halted": risk_report["trading_halted"],
            "halt_reason": risk_report.get("halt_reason"),
            "metrics": risk_report["metrics"],
            "win_rate": risk_report["win_rate"],
        }

    # ═══════════════════════════════════════════════════════════════════
    # MÉTODOS PRIVADOS
    # ═══════════════════════════════════════════════════════════════════

    def _get_active_strategies(self) -> str:
        """Retorna lista de estrategias activas"""
        active = [
            name for name, cfg in self.config.STRATEGIES.items()
            if cfg.get("enabled", False)
        ]
        return ", ".join(active) if active else "Ninguna"

    def _schedule_tasks(self):
        """Programa tareas periódicas"""
        # Check de trailing stop cada 5 minutos
        self.scheduler.schedule_market_hours(
            self._check_trailing_stops,
            interval_minutes=5,
        )

        # Check de wheel strategy cada 15 minutos
        self.scheduler.schedule_market_hours(
            self._check_wheel_positions,
            interval_minutes=15,
        )

        # Risk check cada hora
        self.scheduler.schedule_market_hours(
            self._check_risk_limits,
            interval_minutes=60,
        )

        # End-of-day report
        self.scheduler.schedule.every().day.at("16:05").do(
            self._end_of_day_report
        )

    def _check_trailing_stops(self):
        """Verifica trailing stops de posiciones abiertas"""
        print("\n📊 Verificando trailing stops...")

        # Obtener precios actuales (simulado en demo)
        current_prices = {
            symbol: self._get_current_price(symbol)
            for symbol in self.risk_manager.positions.keys()
        }

        # Verificar stops
        actions = self.risk_manager.monitor_positions(current_prices)

        for action in actions:
            print(f"   ⚠️  {action['symbol']}: {action['reason']}")
            print(f"       Acción: {action['action']}")

            if action["action"] == "SELL":
                self.execute_trade(
                    action["symbol"],
                    "SELL",
                    self.risk_manager.positions[action["symbol"]]["quantity"],
                )

    def _check_wheel_positions(self):
        """Verifica posiciones de wheel strategy"""
        print("\n🎡 Verificando wheel strategy...")
        # Implementación específica de wheel strategy

    def _check_risk_limits(self):
        """Verifica límites de riesgo"""
        print("\n🛡️  Verificando límites de riesgo...")

        # Actualizar métricas
        positions_value = sum(
            pos["quantity"] * self._get_current_price(pos["symbol"])
            for pos in self.risk_manager.positions.values()
        )
        self.risk_manager.update_portfolio_metrics(positions_value)

        # Check circuit breakers
        can_trade, reason = self.risk_manager.check_circuit_breakers()

        if not can_trade:
            print(f"   🚨 CIRCUIT BREAKER: {reason}")
            # Notificar alerta crítica
            alert = RiskAlert(
                alert_type="circuit_breaker",
                current_value=0,
                threshold=0,
                message=reason,
                severity="critical",
            )
            self.notifications.send_risk_alert(alert)

    def _get_current_price(self, symbol: str) -> float:
        """Obtiene precio actual de un símbolo"""
        if self.alpaca:
            quote = self.alpaca.get_quote(symbol)
            return float(quote.get("ask_price", 0))

        # Simulado para demo
        import random
        base_prices = {"TSLA": 250, "NVDA": 450, "AMD": 120, "AAPL": 175, "MSFT": 380}
        return base_prices.get(symbol, 100) * (1 + random.gauss(0, 0.01))

    def _end_of_day_report(self):
        """Genera reporte end-of-day"""
        print("\n" + "=" * 70)
        print("END-OF-DAY REPORT")
        print("=" * 70)

        status = self.get_status()

        print(f"Capital: ${status['capital']:,.2f}")
        print(f"Posiciones abiertas: {status['positions']}")
        print(f"Win Rate: {status['win_rate']*100:.1f}%")
        print(f"Drawdown: {status['metrics']['current_drawdown']}")

        # Notificar por email/discord
        # ...


# ═══════════════════════════════════════════════════════════════════════
# PUNTO DE ENTRADA
# ═══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # Crear bot
    bot = AlpacaTradingBot()

    # Ejemplo: Evaluar trade en TSLA
    print("\n" + "=" * 70)
    print("DEMO: Evaluando trade en TSLA")
    print("=" * 70)

    result = bot.evaluate_trade("TSLA")
    print(f"\nDecisión: {'TRADE' if result['should_trade'] else 'NO TRADE'}")
    print(f"Razón: {result['reason']}")
    print(f"Tamaño recomendado: {result['size']} acciones")

    # Ejemplo: Obtener estado
    print("\n" + "=" * 70)
    print("ESTADO DEL SISTEMA")
    print("=" * 70)

    status = bot.get_status()
    for key, value in status.items():
        print(f"  {key}: {value}")

    # Para iniciar el bot en producción:
    # bot.start()
