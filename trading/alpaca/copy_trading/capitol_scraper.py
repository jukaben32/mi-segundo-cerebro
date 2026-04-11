"""
Scraper para Capitol Trades - Monitoreo de trades de congresistas

URL: https://capitoltrades.com
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional


class CapitolTradesScraper:
    def __init__(self, politician_url: str):
        self.base_url = "https://capitoltrades.com"
        self.politician_url = politician_url
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })

    def get_recent_trades(self, days_back: int = 7) -> List[Dict[str, Any]]:
        """Obtiene trades recientes del político"""
        trades = []

        try:
            response = self.session.get(self.politician_url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            # Buscar tabla de trades
            trade_table = soup.find("table", {"class": "trade-table"})
            if not trade_table:
                print("⚠️ No se encontró tabla de trades")
                return trades

            rows = trade_table.find("tbody").find_all("tr")
            cutoff_date = datetime.now() - timedelta(days=days_back)

            for row in rows:
                trade = self._parse_trade_row(row)
                if trade and trade["date"] >= cutoff_date:
                    trades.append(trade)

        except Exception as e:
            print(f"❌ Error scraping Capitol Trades: {e}")

        return trades

    def _parse_trade_row(self, row) -> Optional[Dict[str, Any]]:
        """Parsea una fila de la tabla de trades"""
        try:
            cells = row.find_all("td")
            if len(cells) < 5:
                return None

            return {
                "date": self._parse_date(cells[0].text.strip()),
                "ticker": cells[1].text.strip(),
                "type": cells[2].text.strip(),  # Buy/Sell
                "asset_type": cells[3].text.strip(),  # Stock/Option
                "value_range": cells[4].text.strip(),  # $1K-$15K, etc.
                "raw_row": row,
            }
        except Exception as e:
            print(f"⚠️ Error parseando fila: {e}")
            return None

    def _parse_date(self, date_str: str) -> datetime:
        """Parsea fecha de string a datetime"""
        try:
            return datetime.strptime(date_str, "%m/%d/%Y")
        except ValueError:
            return datetime.now() - timedelta(days=30)

    def get_politician_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas del político (win rate, retorno, etc.)"""
        # Implementación futura para obtener stats históricos
        return {
            "name": "Michael McCaul",
            "total_trades": 0,
            "win_rate": 0.0,
            "avg_return": 0.0,
        }


class TradeAnalyzer:
    """Analiza si vale la pena copiar un trade"""

    def __init__(self, scraper: CapitolTradesScraper):
        self.scraper = scraper

    def should_copy_trade(self, trade: Dict[str, Any]) -> bool:
        """Determina si un trade debe ser copiado"""
        # Filtros básicos
        if trade["type"] not in ["Buy", "Purchase"]:
            return False

        if not trade["ticker"] or trade["ticker"] == "N/A":
            return False

        # Aquí iría lógica más compleja de análisis
        return True

    def get_confidence_score(self, trade: Dict[str, Any]) -> float:
        """Calcula score de confianza para el trade (0-1)"""
        score = 0.5  # Base

        # Ajustar por tipo de activo
        if trade["asset_type"] == "Stock":
            score += 0.2
        elif trade["asset_type"] == "Option":
            score += 0.1

        # Ajustar por valor
        if "15K" in trade["value_range"] or "50K" in trade["value_range"]:
            score += 0.2

        return min(score, 1.0)
