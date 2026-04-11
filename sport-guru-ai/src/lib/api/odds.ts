export interface BookmakerOdd {
  bookmaker: string;
  price: string; // Ej: "+110", "-105"
  implied_probability: number;
}

export interface MatchupOdds {
  matchup: string;
  sport: string;
  market: string; // Ej: "Spread", "Moneyline"
  consensus: string; // La predicción de SportGuru
  bookmakers: BookmakerOdd[];
  arbitrage_opportunity: boolean;
}

/**
 * Cuando se conecte The Odds API, esta función hará el fetch real 
 * hacia https://api.the-odds-api.com/v4/sports/...
 * Por ahora, simula la extracción top-tier que pediste paralela a la predicción de Claude.
 */
export async function getLiveOddsMock(): Promise<MatchupOdds[]> {
  // Simula latencia de API (The Odds API / Pinnacle)
  await new Promise(resolve => setTimeout(resolve, 500));

  return [
    {
      matchup: "Lakers vs Warriors",
      sport: "NBA",
      market: "Spread (Lakers)",
      consensus: "Lakers +5.5",
      arbitrage_opportunity: true,
      bookmakers: [
        { bookmaker: "DraftKings", price: "-110", implied_probability: 52.38 },
        { bookmaker: "FanDuel", price: "-105", implied_probability: 51.22 },
        { bookmaker: "Pinnacle", price: "-115", implied_probability: 53.49 }
      ]
    }
  ];
}
