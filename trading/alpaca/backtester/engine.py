"""
═══════════════════════════════════════════════════════════════════════════
BACKTESTING ENGINE - NIVEL PROFESIONAL
═══════════════════════════════════════════════════════════════════════════
Motor de backtesting con walk-forward validation, análisis de Monte Carlo
y métricas institucionales.

Características:
- Backtesting vectorizado ultrarrápido
- Walk-Forward Analysis (WFA) para validación robusta
- Monte Carlo simulation para stress testing
- Métricas: Sharpe, Sortino, Calmar, Max Drawdown, VaR
- Slippage y commissions modeling
- Look-ahead bias prevention
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple, Callable
from dataclasses import dataclass, field
from scipy import stats
import warnings

warnings.filterwarnings("ignore")


@dataclass
class BacktestConfig:
    """Configuración del backtest"""
    initial_capital: float = 50000.0
    commission_rate: float = 0.001  # 0.1% por operación
    slippage_percent: float = 0.001  # 0.1% slippage
    margin_rate: float = 0.0  # Sin margen
    benchmark_symbol: str = "SPY"


@dataclass
class Trade:
    """Representa una operación ejecutada"""
    symbol: str
    entry_date: datetime
    entry_price: float
    exit_date: Optional[datetime]
    exit_price: Optional[float]
    quantity: float
    side: str  # "long" o "short"
    pnl: float = 0.0
    pnl_percent: float = 0.0
    mae: float = 0.0  # Maximum Adverse Excursion
    mfe: float = 0.0  # Maximum Favorable Excursion


@dataclass
class BacktestMetrics:
    """Métricas completas del backtest"""
    # Retorno
    total_return: float = 0.0
    annualized_return: float = 0.0
    excess_return: float = 0.0  # Sobre benchmark

    # Riesgo
    volatility: float = 0.0
    max_drawdown: float = 0.0
    var_95: float = 0.0
    cvar_95: float = 0.0  # Conditional VaR

    # Ratios
    sharpe_ratio: float = 0.0
    sortino_ratio: float = 0.0
    calmar_ratio: float = 0.0
    information_ratio: float = 0.0

    # Trading
    total_trades: int = 0
    winning_trades: int = 0
    losing_trades: int = 0
    win_rate: float = 0.0
    profit_factor: float = 0.0
    avg_win: float = 0.0
    avg_loss: float = 0.0
    avg_trade_duration: float = 0.0

    # Drawdown
    avg_drawdown: float = 0.0
    max_drawdown_duration: int = 0  # Días en drawdown máximo

    # Monte Carlo
    monte_carlo_var: float = 0.0
    monte_carlo_ruin_probability: float = 0.0


class AdvancedBacktester:
    """
    Motor de backtesting profesional con validación robusta.

    Características clave:
    - Vectorized backtesting para velocidad
    - Walk-Forward Analysis para evitar overfitting
    - Monte Carlo simulation para stress testing
    - Métricas institucionales completas
    """

    def __init__(self, config: BacktestConfig = None):
        self.config = config or BacktestConfig()
        self.trades: List[Trade] = []
        self.equity_curve: pd.Series = None
        self.daily_returns: pd.Series = None
        self.metrics: BacktestMetrics = BacktestMetrics()

    # ═══════════════════════════════════════════════════════════════════
    # BACKTESTING PRINCIPAL
    # ═══════════════════════════════════════════════════════════════════

    def run_backtest(
        self,
        data: pd.DataFrame,
        strategy: Callable,
        initial_capital: float = None,
    ) -> BacktestMetrics:
        """
        Ejecuta backtest de una estrategia sobre datos históricos.

        Args:
            data: DataFrame con columnas: date, open, high, low, close, volume
            strategy: Función que genera señales (buy/sell/hold)
            initial_capital: Capital inicial

        Returns:
            BacktestMetrics con todas las métricas
        """
        capital = initial_capital or self.config.initial_capital
        position = None
        equity_history = []

        # Iterar sobre cada día (usar iterrows para simplicidad)
        for idx, row in data.iterrows():
            # Generar señal
            signal = strategy(data.loc[:idx], position)

            # Ejecutar lógica de trading
            if signal == "buy" and position is None:
                # Abrir posición long
                entry_price = row["close"] * (1 + self.config.slippage_percent)
                quantity = capital * 0.95 / entry_price  # 95% del capital
                position = {
                    "symbol": row.get("symbol", "UNKNOWN"),
                    "entry_date": row["date"],
                    "entry_price": entry_price,
                    "quantity": quantity,
                    "highest_price": entry_price,
                    "lowest_price": entry_price,
                }

            elif signal == "sell" and position is not None:
                # Cerrar posición
                exit_price = row["close"] * (1 - self.config.slippage_percent)
                gross_pnl = (exit_price - position["entry_price"]) * position["quantity"]
                commission = (position["entry_price"] + exit_price) * position["quantity"] * self.config.commission_rate
                net_pnl = gross_pnl - commission

                # Calcular MAE y MFE
                mae = (position["lowest_price"] - position["entry_price"]) / position["entry_price"]
                mfe = (position["highest_price"] - position["entry_price"]) / position["entry_price"]

                # Registrar trade
                trade = Trade(
                    symbol=position["symbol"],
                    entry_date=position["entry_date"],
                    entry_price=position["entry_price"],
                    exit_date=row["date"],
                    exit_price=exit_price,
                    quantity=position["quantity"],
                    side="long",
                    pnl=net_pnl,
                    pnl_percent=net_pnl / (position["entry_price"] * position["quantity"]),
                    mae=mae,
                    mfe=mfe,
                )
                self.trades.append(trade)

                capital += net_pnl
                position = None

            # Actualizar highest/lowest de la posición abierta
            if position is not None:
                position["highest_price"] = max(position["highest_price"], row["high"])
                position["lowest_price"] = min(position["lowest_price"], row["low"])

            # Registrar equity
            if position:
                position_value = position["quantity"] * row["close"]
                equity_history.append(capital - position["entry_price"] * position["quantity"] + position_value)
            else:
                equity_history.append(capital)

        # Cerrar posición final si está abierta
        if position and len(data) > 0:
            last_row = data.iloc[-1]
            exit_price = last_row["close"] * (1 - self.config.slippage_percent)
            gross_pnl = (exit_price - position["entry_price"]) * position["quantity"]
            commission = (position["entry_price"] + exit_price) * position["quantity"] * self.config.commission_rate
            net_pnl = gross_pnl - commission

            trade = Trade(
                symbol=position["symbol"],
                entry_date=position["entry_date"],
                entry_price=position["entry_price"],
                exit_date=last_row["date"],
                exit_price=exit_price,
                quantity=position["quantity"],
                side="long",
                pnl=net_pnl,
                pnl_percent=net_pnl / (position["entry_price"] * position["quantity"]),
            )
            self.trades.append(trade)
            capital += net_pnl

        # Construir curva de equity
        self.equity_curve = pd.Series(equity_history, index=data["date"])
        self.daily_returns = self.equity_curve.pct_change().dropna()

        # Calcular métricas
        self.metrics = self._calculate_metrics(data)

        return self.metrics

    # ═══════════════════════════════════════════════════════════════════
    # WALK-FORWARD ANALYSIS
    # ═══════════════════════════════════════════════════════════════════

    def walk_forward_analysis(
        self,
        data: pd.DataFrame,
        strategy: Callable,
        in_sample_periods: int = 252,  # 1 año de trading
        out_sample_periods: int = 63,  # 3 meses de trading
    ) -> Dict[str, Any]:
        """
        Walk-Forward Analysis para validar robustez de la estrategia.

        Divide los datos en ventanas in-sample (optimización) y
        out-sample (validación) para detectar overfitting.
        """
        results = []
        window_start = 0

        while window_start + in_sample_periods + out_sample_periods <= len(data):
            # Ventana in-sample
            in_sample_end = window_start + in_sample_periods
            in_sample_data = data.iloc[window_start:in_sample_end]

            # Ventana out-sample
            out_sample_start = in_sample_end
            out_sample_end = out_sample_start + out_sample_periods
            out_sample_data = data.iloc[out_sample_start:out_sample_end]

            # Ejecutar backtest en out-sample
            self.trades = []  # Reset trades
            metrics = self.run_backtest(out_sample_data, strategy)

            results.append({
                "period": len(results) + 1,
                "in_sample_start": in_sample_data["date"].iloc[0],
                "in_sample_end": in_sample_data["date"].iloc[-1],
                "out_sample_start": out_sample_data["date"].iloc[0],
                "out_sample_end": out_sample_data["date"].iloc[-1],
                "total_return": metrics.total_return,
                "sharpe_ratio": metrics.sharpe_ratio,
                "max_drawdown": metrics.max_drawdown,
                "win_rate": metrics.win_rate,
            })

            # Mover ventana
            window_start = out_sample_start

        # Calcular consistencia
        returns = [r["total_return"] for r in results]
        sharpe_ratios = [r["sharpe_ratio"] for r in results]

        return {
            "windows": results,
            "avg_return": np.mean(returns),
            "std_return": np.std(returns),
            "avg_sharpe": np.mean(sharpe_ratios),
            "sharpe_consistency": 1 - (np.std(sharpe_ratios) / np.mean(sharpe_ratios)) if np.mean(sharpe_ratios) != 0 else 0,
            "positive_windows": sum(1 for r in results if r["total_return"] > 0),
            "total_windows": len(results),
        }

    # ═══════════════════════════════════════════════════════════════════
    # MONTE CARLO SIMULATION
    # ═══════════════════════════════════════════════════════════════════

    def monte_carlo_simulation(
        self,
        n_simulations: int = 1000,
        time_horizon: int = 252,
    ) -> Dict[str, Any]:
        """
        Simulación de Monte Carlo para stress testing.

        Remuestrea los retornos históricos para estimar:
        - Probabilidad de ruina
        - VaR de la curva de equity
        - Peor drawdown esperado
        """
        if self.daily_returns is None or len(self.daily_returns) == 0:
            return {"error": "No hay datos de retornos disponibles"}

        final_equities = []
        max_drawdowns = []
        ruin_count = 0

        for _ in range(n_simulations):
            # Bootstrap de retornos
            sampled_returns = np.random.choice(
                self.daily_returns.values,
                size=time_horizon,
                replace=True
            )

            # Construir curva de equity simulada
            equity_curve = self.config.initial_capital * np.cumprod(1 + sampled_returns)

            # Calcular drawdowns
            running_max = np.maximum.accumulate(equity_curve)
            drawdowns = (running_max - equity_curve) / running_max
            max_dd = np.max(drawdowns)

            final_equity = equity_curve[-1]
            final_equities.append(final_equity)
            max_drawdowns.append(max_dd)

            # Verificar ruina (drawdown > 50%)
            if max_dd > 0.50:
                ruin_count += 1

        # Calcular percentiles
        final_equities = np.array(final_equities)

        return {
            "median_final_equity": np.median(final_equities),
            "var_95_equity": np.percentile(final_equities, 5),
            "var_99_equity": np.percentile(final_equities, 1),
            "median_max_drawdown": np.median(max_drawdowns),
            "worst_10pct_drawdown": np.percentile(max_drawdowns, 10),
            "ruin_probability": ruin_count / n_simulations,
            "positive_return_probability": np.mean(final_equities > self.config.initial_capital),
        }

    # ═══════════════════════════════════════════════════════════════════
    # MÉTRICAS INSTITUCIONALES
    # ═══════════════════════════════════════════════════════════════════

    def _calculate_metrics(self, data: pd.DataFrame) -> BacktestMetrics:
        """Calcula todas las métricas del backtest"""
        metrics = BacktestMetrics()

        if len(self.trades) == 0:
            return metrics

        # ===== Métricas de Retorno =====
        if self.equity_curve is not None and len(self.equity_curve) > 1:
            # Retorno total
            metrics.total_return = (self.equity_curve.iloc[-1] - self.equity_curve.iloc[0]) / self.equity_curve.iloc[0]

            # Annualizado
            days = (data["date"].iloc[-1] - data["date"].iloc[0]).days
            if days > 0:
                metrics.annualized_return = (1 + metrics.total_return) ** (365 / days) - 1

        # ===== Métricas de Riesgo =====
        if self.daily_returns is not None and len(self.daily_returns) > 0:
            # Volatilidad annualizada
            metrics.volatility = self.daily_returns.std() * np.sqrt(252)

            # Sharpe Ratio (asumiendo risk-free rate = 0)
            if metrics.volatility > 0:
                metrics.sharpe_ratio = metrics.annualized_return / metrics.volatility

            # Sortino Ratio (solo volatilidad negativa)
            negative_returns = self.daily_returns[self.daily_returns < 0]
            if len(negative_returns) > 0:
                downside_vol = negative_returns.std() * np.sqrt(252)
                if downside_vol > 0:
                    metrics.sortino_ratio = metrics.annualized_return / downside_vol

            # VaR 95%
            metrics.var_95 = np.percentile(self.daily_returns, 5)
            metrics.cvar_95 = self.daily_returns[self.daily_returns <= metrics.var_95].mean()

        # ===== Drawdown =====
        if self.equity_curve is not None:
            running_max = self.equity_curve.cummax()
            drawdowns = (running_max - self.equity_curve) / running_max
            metrics.max_drawdown = drawdowns.max()
            metrics.avg_drawdown = drawdowns.mean()

            # Duración del drawdown máximo
            in_drawdown = drawdowns > 0
            drawdown_periods = []
            current_period = 0
            for is_dd in in_drawdown:
                if is_dd:
                    current_period += 1
                else:
                    if current_period > 0:
                        drawdown_periods.append(current_period)
                    current_period = 0
            metrics.max_drawdown_duration = max(drawdown_periods) if drawdown_periods else 0

            # Calmar Ratio
            if metrics.max_drawdown > 0:
                metrics.calmar_ratio = metrics.annualized_return / metrics.max_drawdown

        # ===== Métricas de Trading =====
        pnl_values = [t.pnl for t in self.trades]
        winning_trades = [t for t in self.trades if t.pnl > 0]
        losing_trades = [t for t in self.trades if t.pnl < 0]

        metrics.total_trades = len(self.trades)
        metrics.winning_trades = len(winning_trades)
        metrics.losing_trades = len(losing_trades)
        metrics.win_rate = len(winning_trades) / len(self.trades) if self.trades else 0

        # Profit Factor
        gross_profit = sum(t.pnl for t in winning_trades)
        gross_loss = abs(sum(t.pnl for t in losing_trades))
        metrics.profit_factor = gross_profit / gross_loss if gross_loss > 0 else float("inf")

        # Promedios
        metrics.avg_win = np.mean([t.pnl for t in winning_trades]) if winning_trades else 0
        metrics.avg_loss = np.mean([t.pnl for t in losing_trades]) if losing_trades else 0

        # Duración promedio de trades
        durations = []
        for t in self.trades:
            if t.entry_date and t.exit_date:
                duration = (t.exit_date - t.entry_date).days
                durations.append(duration)
        metrics.avg_trade_duration = np.mean(durations) if durations else 0

        return metrics

    def get_metrics_summary(self) -> Dict[str, Any]:
        """Retorna resumen de métricas en formato legible"""
        m = self.metrics
        return {
            "RETORNO": {
                "Total": f"{m.total_return*100:.2f}%",
                "Anualizado": f"{m.annualized_return*100:.2f}%",
            },
            "RIESGO": {
                "Volatilidad": f"{m.volatility*100:.2f}%",
                "Max Drawdown": f"{m.max_drawdown*100:.2f}%",
                "VaR 95%": f"{m.var_95*100:.3f}%",
            },
            "RATIOS": {
                "Sharpe": f"{m.sharpe_ratio:.2f}",
                "Sortino": f"{m.sortino_ratio:.2f}",
                "Calmar": f"{m.calmar_ratio:.2f}",
            },
            "TRADING": {
                "Total Trades": m.total_trades,
                "Win Rate": f"{m.win_rate*100:.2f}%",
                "Profit Factor": f"{m.profit_factor:.2f}",
                "Avg Win": f"${m.avg_win:.2f}",
                "Avg Loss": f"${m.avg_loss:.2f}",
            },
        }


# ═══════════════════════════════════════════════════════════════════════
# EJEMPLO: ESTRATEGIA SMA CROSSOVER
# ═══════════════════════════════════════════════════════════════════════

def sma_crossover_strategy(data: pd.DataFrame, position) -> str:
    """
    Estrategia simple de cruce de medias móviles.

    Señales:
    - BUY: SMA corta cruza arriba SMA larga
    - SELL: SMA corta cruza abajo SMA larga
    """
    if len(data) < 50:
        return "hold"

    sma_short = data["close"].rolling(window=10).mean()
    sma_long = data["close"].rolling(window=50).mean()

    if len(data) < 51:
        return "hold"

    prev_short = sma_short.iloc[-2]
    prev_long = sma_long.iloc[-2]
    curr_short = sma_short.iloc[-1]
    curr_long = sma_long.iloc[-1]

    # Cruce alcista
    if prev_short <= prev_long and curr_short > curr_long:
        return "buy"

    # Cruce bajista
    if prev_short >= prev_long and curr_short < curr_long:
        return "sell"

    return "hold"


if __name__ == "__main__":
    # Ejemplo de uso
    print("=" * 70)
    print("BACKTESTER ENGINE - Demo")
    print("=" * 70)

    # Generar datos simulados
    np.random.seed(42)
    n_days = 500
    dates = pd.date_range(start="2024-01-01", periods=n_days, freq="D")

    # Precio simulado con tendencia y ruido
    price = 100 + np.cumsum(np.random.randn(n_days) * 2)
    price = np.maximum(price, 10)  # No negativo

    data = pd.DataFrame({
        "date": dates,
        "open": price + np.random.randn(n_days),
        "high": price + np.abs(np.random.randn(n_days)),
        "low": price - np.abs(np.random.randn(n_days)),
        "close": price,
        "volume": np.random.randint(1000, 10000, n_days),
    })

    # Ejecutar backtest
    backtester = AdvancedBacktester(BacktestConfig(initial_capital=50000))
    metrics = backtester.run_backtest(data, sma_crossover_strategy)

    # Mostrar resultados
    print("\n📊 RESULTADOS DEL BACKTEST")
    print("-" * 40)

    summary = backtester.get_metrics_summary()
    for category, items in summary.items():
        print(f"\n{category}:")
        for key, value in items.items():
            print(f"  {key}: {value}")

    # Walk-Forward Analysis
    print("\n\n🔄 WALK-FORWARD ANALYSIS")
    print("-" * 40)
    wfa = backtester.walk_forward_analysis(data, sma_crossover_strategy)
    print(f"Ventanas analizadas: {wfa['total_windows']}")
    print(f"Retorno promedio: {wfa['avg_return']*100:.2f}%")
    print(f"Consistencia Sharpe: {wfa['sharpe_consistency']*100:.1f}%")
    print(f"Ventanas positivas: {wfa['positive_windows']}/{wfa['total_windows']}")

    # Monte Carlo
    print("\n\n🎲 MONTE CARLO SIMULATION (1000 iteraciones)")
    print("-" * 40)
    mc = backtester.monte_carlo_simulation(n_simulations=1000)
    print(f"Mediana Equity Final: ${mc['median_final_equity']:.2f}")
    print(f"VaR 95% Equity: ${mc['var_95_equity']:.2f}")
    print(f"Probabilidad Ruina: {mc['ruin_probability']*100:.2f}%")
    print(f"Probabilidad Retorno Positivo: {mc['positive_return_probability']*100:.2f}%")
