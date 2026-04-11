"""
═══════════════════════════════════════════════════════════════════════════
MULTI-AGENT AI TRADING SYSTEM
═══════════════════════════════════════════════════════════════════════════
Sistema multi-agente con LLMs especializados para toma de decisiones
de trading inspirado en hedge funds cuantitativos modernos.

Arquitectura de 5 agentes especializados:
1. MARKET ANALYST - Análisis técnico y de momentum
2. SENTIMENT ANALYST - Análisis de sentimiento (noticias, redes)
3. FUNDAMENTAL ANALYST - Análisis fundamental y macro
4. RISK MANAGER - Evaluación de riesgo pre-trade
5. PORTFOLIO MANAGER - Decisión final y sizing

Cada agente tiene un "voto" ponderado y el Portfolio Manager
toma la decisión final basada en el consenso.
"""

import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
import json


class Signal(Enum):
    STRONG_BUY = 2
    BUY = 1
    HOLD = 0
    SELL = -1
    STRONG_SELL = -2


@dataclass
class AgentDecision:
    """Decisión de un agente individual"""
    agent_name: str
    signal: Signal
    confidence: float  # 0.0 a 1.0
    reasoning: str
    supporting_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ConsensusDecision:
    """Decisión consensuada del comité de agentes"""
    final_signal: Signal
    final_confidence: float
    agent_votes: List[AgentDecision]
    weighted_score: float  # -2.0 a +2.0
    recommended_position_size: float  # 0.0 a 1.0
    reasoning_summary: str


class MarketAnalystAgent:
    """
    Agente especializado en análisis técnico.

    Analiza:
    - Tendencias (SMA, EMA, MACD)
    - Momentum (RSI, Stochastic)
    - Volatilidad (Bollinger Bands, ATR)
    - Volumen (OBV, VWAP)
    - Patrones de velas
    """

    def __init__(self):
        self.indicators = {}

    def analyze(self, price_data: Dict[str, Any]) -> AgentDecision:
        """Analiza datos de precio y genera señal"""
        signals = []
        confidences = []
        reasonings = []

        # Análisis de tendencia
        trend_signal, trend_conf = self._analyze_trend(price_data)
        signals.append(trend_signal)
        confidences.append(trend_conf)
        reasonings.append(f"Tendencia: {'alcista' if trend_signal > 0 else 'bajista'}")

        # Análisis de momentum
        mom_signal, mom_conf = self._analyze_momentum(price_data)
        signals.append(mom_signal)
        confidences.append(mom_conf)
        reasonings.append(f"Momentum: {'positivo' if mom_signal > 0 else 'negativo'}")

        # Análisis de volatilidad
        vol_signal, vol_conf = self._analyze_volatility(price_data)
        signals.append(vol_signal)
        confidences.append(vol_conf)
        reasonings.append(f"Volatilidad: {'expansión' if vol_signal > 0 else 'contracción'}")

        # Decisión ponderada
        weighted_signal = np.average(signals, weights=confidences)
        avg_confidence = np.mean(confidences)

        # Mapear a Signal enum
        if weighted_signal >= 1.5:
            final_signal = Signal.STRONG_BUY
        elif weighted_signal >= 0.5:
            final_signal = Signal.BUY
        elif weighted_signal <= -1.5:
            final_signal = Signal.STRONG_SELL
        elif weighted_signal <= -0.5:
            final_signal = Signal.SELL
        else:
            final_signal = Signal.HOLD

        return AgentDecision(
            agent_name="Market Analyst",
            signal=final_signal,
            confidence=avg_confidence,
            reasoning="; ".join(reasonings),
            supporting_data={
                "trend_signal": trend_signal,
                "momentum_signal": mom_signal,
                "volatility_signal": vol_signal,
            }
        )

    def _analyze_trend(self, data: Dict) -> Tuple[int, float]:
        """Analiza tendencia usando SMA crossover"""
        if "sma_20" not in data or "sma_50" not in data:
            return 0, 0.3

        current_price = data.get("current_price", 0)
        sma_20 = data["sma_20"]
        sma_50 = data["sma_50"]

        # Precio sobre ambas medias = alcista
        if current_price > sma_20 > sma_50:
            return 1, 0.7
        # Precio bajo ambas medias = bajista
        elif current_price < sma_20 < sma_50:
            return -1, 0.7
        # Mixto = neutral
        else:
            return 0, 0.4

    def _analyze_momentum(self, data: Dict) -> Tuple[int, float]:
        """Analiza momentum usando RSI"""
        rsi = data.get("rsi", 50)

        if rsi < 30:
            return 1, 0.8  # Sobrevendido → posible rebote
        elif rsi > 70:
            return -1, 0.8  # Sobrecomprado → posible caída
        elif rsi < 40:
            return 1, 0.5
        elif rsi > 60:
            return -1, 0.5
        else:
            return 0, 0.3

    def _analyze_volatility(self, data: Dict) -> Tuple[int, float]:
        """Analiza volatilidad usando Bollinger Bands"""
        current_price = data.get("current_price", 0)
        bb_upper = data.get("bb_upper", 0)
        bb_lower = data.get("bb_lower", 0)

        if bb_upper == 0 or bb_lower == 0:
            return 0, 0.3

        # Precio cerca del límite inferior → posible rebote
        if current_price <= bb_lower * 1.01:
            return 1, 0.6
        # Precio cerca del límite superior → posible caída
        elif current_price >= bb_upper * 0.99:
            return -1, 0.6
        else:
            return 0, 0.3


class SentimentAnalystAgent:
    """
    Agente especializado en análisis de sentimiento.

    Analiza:
    - Noticias financieras (NLP)
    - Redes sociales (Twitter, Reddit)
    - Insider trading
    - Flujo de opciones
    - Short interest
    """

    def __init__(self):
        self.news_sentiment_cache = {}
        self.social_sentiment_cache = {}

    def analyze(self, symbol: str, context: Dict[str, Any]) -> AgentDecision:
        """Analiza sentimiento del mercado"""
        signals = []
        confidences = []

        # Sentimiento de noticias
        news_signal, news_conf = self._analyze_news_sentiment(symbol, context)
        signals.append(news_signal)
        confidences.append(news_conf)

        # Sentimiento de redes sociales
        social_signal, social_conf = self._analyze_social_sentiment(symbol)
        signals.append(social_signal)
        confidences.append(social_conf)

        # Flujo de opciones
        options_signal, options_conf = self._analyze_options_flow(symbol)
        signals.append(options_signal)
        confidences.append(options_conf)

        # Decisión ponderada
        weighted_signal = np.average(signals, weights=confidences)
        avg_confidence = np.mean(confidences)

        # Mapear a Signal enum
        if weighted_signal >= 1.5:
            final_signal = Signal.STRONG_BUY
        elif weighted_signal >= 0.5:
            final_signal = Signal.BUY
        elif weighted_signal <= -1.5:
            final_signal = Signal.STRONG_SELL
        elif weighted_signal <= -0.5:
            final_signal = Signal.SELL
        else:
            final_signal = Signal.HOLD

        return AgentDecision(
            agent_name="Sentiment Analyst",
            signal=final_signal,
            confidence=avg_confidence,
            reasoning=f"Sentimiento basado en noticias, redes y flujo de opciones",
            supporting_data={
                "news_sentiment": news_signal,
                "social_sentiment": social_signal,
                "options_flow": options_signal,
            }
        )

    def _analyze_news_sentiment(self, symbol: str, context: Dict) -> Tuple[int, float]:
        """Analiza sentimiento de noticias (simulado)"""
        # En producción: usar API de noticias + LLM para NLP
        news_score = context.get("news_sentiment_score", 0)

        if news_score > 0.5:
            return 1, min(0.9, 0.5 + news_score)
        elif news_score < -0.5:
            return -1, min(0.9, 0.5 + abs(news_score))
        else:
            return 0, 0.3

    def _analyze_social_sentiment(self, symbol: str) -> Tuple[int, float]:
        """Analiza sentimiento de redes sociales"""
        # En producción: usar APIs de Twitter/Reddit
        # Simulación basada en el símbolo
        bullish_symbols = ["TSLA", "NVDA", "AMD"]
        bearish_symbols = []

        if symbol in bullish_symbols:
            return 1, 0.5
        elif symbol in bearish_symbols:
            return -1, 0.5
        else:
            return 0, 0.3

    def _analyze_options_flow(self, symbol: str) -> Tuple[int, float]:
        """Analiza flujo inusual de opciones"""
        # En producción: conectar a API de opciones
        # Simulación: retorno neutral
        return 0, 0.4


class FundamentalAnalystAgent:
    """
    Agente especializado en análisis fundamental.

    Analiza:
    - Métricas de valoración (P/E, PEG, P/S)
    - Crecimiento (revenue, earnings)
    - Rentabilidad (márgenes, ROE, ROIC)
    - Salud financiera (deuda, cash flow)
    - Factores macro (tasas, inflación)
    """

    def __init__(self):
        self.sector_averages = {}

    def analyze(self, symbol: str, fundamentals: Dict[str, Any]) -> AgentDecision:
        """Analiza fundamentos de la empresa"""
        signals = []
        confidences = []

        # Valoración
        val_signal, val_conf = self._analyze_valuation(fundamentals)
        signals.append(val_signal)
        confidences.append(val_conf)

        # Crecimiento
        growth_signal, growth_conf = self._analyze_growth(fundamentals)
        signals.append(growth_signal)
        confidences.append(growth_conf)

        # Rentabilidad
        prof_signal, prof_conf = self._analyze_profitability(fundamentals)
        signals.append(prof_signal)
        confidences.append(prof_conf)

        # Decisión ponderada
        weighted_signal = np.average(signals, weights=confidences)
        avg_confidence = np.mean(confidences)

        # Mapear a Signal enum
        if weighted_signal >= 1.5:
            final_signal = Signal.STRONG_BUY
        elif weighted_signal >= 0.5:
            final_signal = Signal.BUY
        elif weighted_signal <= -1.5:
            final_signal = Signal.STRONG_SELL
        elif weighted_signal <= -0.5:
            final_signal = Signal.SELL
        else:
            final_signal = Signal.HOLD

        return AgentDecision(
            agent_name="Fundamental Analyst",
            signal=final_signal,
            confidence=avg_confidence,
            reasoning=f"Análisis fundamental: valoración, crecimiento, rentabilidad",
            supporting_data={
                "valuation_signal": val_signal,
                "growth_signal": growth_signal,
                "profitability_signal": prof_signal,
            }
        )

    def _analyze_valuation(self, data: Dict) -> Tuple[int, float]:
        """Analiza valoración usando P/E y PEG"""
        pe_ratio = data.get("pe_ratio", 25)
        peg_ratio = data.get("peg_ratio", 1.5)
        sector_pe = data.get("sector_pe", 25)

        score = 0

        # P/E comparado con el sector
        if pe_ratio < sector_pe * 0.8:
            score += 1
        elif pe_ratio > sector_pe * 1.2:
            score -= 1

        # PEG ratio (ideal < 1)
        if peg_ratio < 1:
            score += 1
        elif peg_ratio > 2:
            score -= 1

        if score >= 2:
            return 1, 0.8
        elif score <= -2:
            return -1, 0.8
        else:
            return 0, 0.5

    def _analyze_growth(self, data: Dict) -> Tuple[int, float]:
        """Analiza crecimiento de revenue y earnings"""
        revenue_growth = data.get("revenue_growth_yoy", 0.1)
        earnings_growth = data.get("earnings_growth_yoy", 0.1)

        avg_growth = (revenue_growth + earnings_growth) / 2

        if avg_growth > 0.20:
            return 1, 0.8
        elif avg_growth > 0.10:
            return 1, 0.5
        elif avg_growth < -0.10:
            return -1, 0.7
        else:
            return 0, 0.4

    def _analyze_profitability(self, data: Dict) -> Tuple[int, float]:
        """Analiza rentabilidad (márgenes, ROE)"""
        gross_margin = data.get("gross_margin", 0.3)
        operating_margin = data.get("operating_margin", 0.1)
        roe = data.get("roe", 0.15)

        score = 0

        if gross_margin > 0.5:
            score += 1
        if operating_margin > 0.2:
            score += 1
        if roe > 0.20:
            score += 1
        if roe < 0.05:
            score -= 1

        if score >= 2:
            return 1, 0.7
        elif score <= -1:
            return -1, 0.6
        else:
            return 0, 0.4


class RiskManagerAgent:
    """
    Agente especializado en gestión de riesgo.

    Evalúa:
    - Riesgo específico del activo
    - Condiciones del mercado general
    - Concentración del portfolio
    - Liquidez
    - Eventos catastróficos potenciales
    """

    def __init__(self):
        self.vix_threshold = 30
        self.max_correlation = 0.7

    def analyze(self, symbol: str, portfolio: Dict[str, Any], market_data: Dict) -> AgentDecision:
        """Evalúa riesgo de la operación"""
        signals = []
        confidences = []

        # Riesgo de mercado (VIX)
        market_signal, market_conf = self._analyze_market_risk(market_data)
        signals.append(market_signal)
        confidences.append(market_conf)

        # Riesgo específico del símbolo
        symbol_signal, symbol_conf = self._analyze_symbol_risk(symbol, market_data)
        signals.append(symbol_signal)
        confidences.append(symbol_conf)

        # Riesgo de concentración
        conc_signal, conc_conf = self._analyze_concentration_risk(symbol, portfolio)
        signals.append(conc_signal)
        confidences.append(conc_conf)

        # Promedio inverso (menor riesgo = señal más positiva)
        avg_risk = np.average(signals, weights=confidences)

        # Invertir: bajo riesgo = BUY, alto riesgo = SELL
        if avg_risk <= 0.3:
            final_signal = Signal.BUY  # Bajo riesgo, proceder
        elif avg_risk <= 0.5:
            final_signal = Signal.HOLD
        elif avg_risk <= 0.7:
            final_signal = Signal.SELL  # Riesgo moderado-alto
        else:
            final_signal = Signal.STRONG_SELL  # Riesgo extremo

        return AgentDecision(
            agent_name="Risk Manager",
            signal=final_signal,
            confidence=np.mean(confidences),
            reasoning=f"Evaluación de riesgo: mercado, símbolo, concentración",
            supporting_data={
                "market_risk": market_signal,
                "symbol_risk": symbol_signal,
                "concentration_risk": conc_signal,
            }
        )

    def _analyze_market_risk(self, data: Dict) -> Tuple[float, float]:
        """Analiza riesgo del mercado (VIX, breadth, etc.)"""
        vix = data.get("vix", 20)

        if vix > self.vix_threshold:
            return 0.9, 0.9  # Alto riesgo
        elif vix > 25:
            return 0.7, 0.7
        elif vix < 15:
            return 0.2, 0.8  # Bajo riesgo
        else:
            return 0.5, 0.5

    def _analyze_symbol_risk(self, symbol: str, data: Dict) -> Tuple[float, float]:
        """Analiza riesgo específico del símbolo"""
        volatility = data.get("volatility", 0.3)
        beta = data.get("beta", 1.0)
        market_cap = data.get("market_cap", 100)  # En billones

        risk_score = 0

        # Alta volatilidad = más riesgo
        if volatility > 0.5:
            risk_score += 0.3
        elif volatility > 0.3:
            risk_score += 0.15

        # Beta alto = más riesgo
        if beta > 1.5:
            risk_score += 0.3
        elif beta > 1.2:
            risk_score += 0.15

        # Small cap = más riesgo
        if market_cap < 2:
            risk_score += 0.2
        elif market_cap < 10:
            risk_score += 0.1

        return min(risk_score, 1.0), 0.7

    def _analyze_concentration_risk(self, symbol: str, portfolio: Dict) -> Tuple[float, float]:
        """Analiza riesgo de concentración"""
        current_positions = portfolio.get("positions", {})

        # Si ya hay mucha exposición al símbolo → alto riesgo
        if symbol in current_positions:
            position_value = current_positions[symbol].get("value", 0)
            portfolio_value = portfolio.get("total_value", 1)
            position_percent = position_value / portfolio_value

            if position_percent > 0.20:
                return 0.9, 0.9  # Muy concentrado
            elif position_percent > 0.10:
                return 0.6, 0.7

        return 0.3, 0.5


class PortfolioManagerAgent:
    """
    Agente Portfolio Manager - Toma la decisión final.

    Coordina las decisiones de todos los agentes y toma
    la decisión final de trading con sizing óptimo.
    """

    def __init__(self):
        self.market_analyst = MarketAnalystAgent()
        self.sentiment_analyst = SentimentAnalystAgent()
        self.fundamental_analyst = FundamentalAnalystAgent()
        self.risk_manager = RiskManagerAgent()

        # Ponderaciones de cada agente
        self.agent_weights = {
            "Market Analyst": 0.30,
            "Sentiment Analyst": 0.20,
            "Fundamental Analyst": 0.25,
            "Risk Manager": 0.25,
        }

    def make_decision(
        self,
        symbol: str,
        price_data: Dict,
        fundamentals: Dict,
        portfolio: Dict,
        market_data: Dict,
    ) -> ConsensusDecision:
        """
        Coordina el comité de agentes y produce decisión final.

        Proceso:
        1. Cada agente analiza independientemente
        2. Se recopilan todos los votos
        3. Se calcula score ponderado
        4. Se determina señal final y tamaño de posición
        """
        agent_votes: List[AgentDecision] = []

        # 1. Market Analyst
        market_decision = self.market_analyst.analyze(price_data)
        agent_votes.append(market_decision)

        # 2. Sentiment Analyst
        sentiment_context = {"news_sentiment_score": market_data.get("news_sentiment", 0)}
        sentiment_decision = self.sentiment_analyst.analyze(symbol, sentiment_context)
        agent_votes.append(sentiment_decision)

        # 3. Fundamental Analyst
        fundamental_decision = self.fundamental_analyst.analyze(symbol, fundamentals)
        agent_votes.append(fundamental_decision)

        # 4. Risk Manager
        risk_decision = self.risk_manager.analyze(symbol, portfolio, market_data)
        agent_votes.append(risk_decision)

        # 2. Calcular score ponderado
        weighted_score = 0.0
        for vote in agent_votes:
            signal_value = vote.signal.value  # -2 a +2
            weight = self.agent_weights[vote.agent_name]
            confidence = vote.confidence
            weighted_score += signal_value * weight * confidence

        # 3. Determinar señal final
        if weighted_score >= 1.5:
            final_signal = Signal.STRONG_BUY
        elif weighted_score >= 0.5:
            final_signal = Signal.BUY
        elif weighted_score <= -1.5:
            final_signal = Signal.STRONG_SELL
        elif weighted_score <= -0.5:
            final_signal = Signal.SELL
        else:
            final_signal = Signal.HOLD

        # 4. Calcular tamaño de posición recomendado
        position_size = self._calculate_position_size(
            final_signal, weighted_score, portfolio
        )

        # 5. Generar resumen de razonamiento
        reasoning_summary = self._generate_reasoning_summary(agent_votes)

        return ConsensusDecision(
            final_signal=final_signal,
            final_confidence=abs(weighted_score) / 2,  # Normalizar a 0-1
            agent_votes=agent_votes,
            weighted_score=weighted_score,
            recommended_position_size=position_size,
            reasoning_summary=reasoning_summary,
        )

    def _calculate_position_size(
        self,
        signal: Signal,
        weighted_score: float,
        portfolio: Dict,
    ) -> float:
        """Calcula tamaño óptimo de posición"""
        base_size = 0.05  # 5% base

        # Ajustar por fuerza de señal
        signal_multiplier = {
            Signal.STRONG_BUY: 2.0,
            Signal.BUY: 1.0,
            Signal.HOLD: 0.0,
            Signal.SELL: 0.0,
            Signal.STRONG_SELL: 0.0,
        }

        multiplier = signal_multiplier.get(signal, 0)
        confidence_adjustment = min(abs(weighted_score) / 2, 1.0)

        position_size = base_size * multiplier * (0.5 + confidence_adjustment * 0.5)

        # Límites
        max_position = portfolio.get("max_position_percent", 0.10)
        return min(position_size, max_position)

    def _generate_reasoning_summary(self, votes: List[AgentDecision]) -> str:
        """Genera resumen ejecutivo del razonamiento"""
        summaries = []
        for vote in votes:
            summaries.append(f"{vote.agent_name}: {vote.reasoning}")
        return " | ".join(summaries)


# ═══════════════════════════════════════════════════════════════════════
# ORQUESTADOR PRINCIPAL
# ═══════════════════════════════════════════════════════════════════════

class MultiAgentTradingSystem:
    """
    Sistema principal que orquesta todos los agentes.

    Uso:
        system = MultiAgentTradingSystem()
        decision = system.evaluate_trade("TSLA")
        if decision.final_signal in [Signal.BUY, Signal.STRONG_BUY]:
            execute_trade(...)
    """

    def __init__(self):
        self.portfolio_manager = PortfolioManagerAgent()

    def evaluate_trade(
        self,
        symbol: str,
        price_data: Dict = None,
        fundamentals: Dict = None,
        portfolio: Dict = None,
        market_data: Dict = None,
    ) -> ConsensusDecision:
        """Evalúa si se debe abrir una posición"""

        # Datos por defecto (en producción, obtener de APIs reales)
        price_data = price_data or {
            "current_price": 250.0,
            "sma_20": 245.0,
            "sma_50": 240.0,
            "rsi": 55,
            "bb_upper": 260.0,
            "bb_lower": 230.0,
        }

        fundamentals = fundamentals or {
            "pe_ratio": 25,
            "peg_ratio": 1.2,
            "sector_pe": 22,
            "revenue_growth_yoy": 0.15,
            "earnings_growth_yoy": 0.18,
            "gross_margin": 0.40,
            "operating_margin": 0.15,
            "roe": 0.18,
        }

        portfolio = portfolio or {
            "total_value": 50000,
            "positions": {},
            "cash": 25000,
            "max_position_percent": 0.10,
        }

        market_data = market_data or {
            "vix": 18,
            "news_sentiment": 0.2,
            "spy_price": 450,
            "spy_change": 0.005,
        }

        return self.portfolio_manager.make_decision(
            symbol=symbol,
            price_data=price_data,
            fundamentals=fundamentals,
            portfolio=portfolio,
            market_data=market_data,
        )


# ═══════════════════════════════════════════════════════════════════════
# DEMO
# ═══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 70)
    print("MULTI-AGENT AI TRADING SYSTEM - Demo")
    print("=" * 70)

    system = MultiAgentTradingSystem()

    # Evaluar trade en TSLA
    print("\n🔍 Evaluando TSLA...\n")

    decision = system.evaluate_trade("TSLA")

    print(f"{'='*50}")
    print(f"DECISIÓN DEL COMITÉ")
    print(f"{'='*50}")
    print(f"Señal Final: {decision.final_signal.name}")
    print(f"Confianza: {decision.final_confidence*100:.1f}%")
    print(f"Score Ponderado: {decision.weighted_score:.2f}")
    print(f"Tamaño de Posición: {decision.recommended_position_size*100:.1f}%")
    print(f"\n📋 Resumen:")
    print(f"{decision.reasoning_summary}")

    print(f"\n{'='*50}")
    print(f"VOTOS INDIVIDUALES")
    print(f"{'='*50}")

    for vote in decision.agent_votes:
        print(f"\n{vote.agent_name}:")
        print(f"  Señal: {vote.signal.name}")
        print(f"  Confianza: {vote.confidence*100:.1f}%")
        print(f"  Razón: {vote.reasoning}")
