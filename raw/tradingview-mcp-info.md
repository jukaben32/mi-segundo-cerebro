# TradingView MCP Server - Info & Research

**GitHub:** https://github.com/tradesdontlie/tradingview-mcp.git
**Context:** Connects Claude Code to TradingView Desktop via Chrome DevTools Protocol (CDP) on port 9222.

## Overview

TradingView doesn't have a public API. This project uses the Electron debug interface (CDP) built into the desktop app to allow an LLM to interact with charts.

### How It Works
1. Launch TradingView Desktop with the `--remote-debugging-port=9222` flag.
2. The Node.js MCP server connects to this port.
3. Claude can read:
   - Symbol, timeframe, real-time OHLCV.
   - Indicator values and names.
   - **Pine Drawings**: line.new(), label.new(), table.new(), box.new().
   - Strategy tester results and trade lists.
   - Screenshots of any chart region.

### Capabilities
- **Pine Script Dev Loop**: Claude writes, injects, compiles, and fixes scripts automatically.
- **Streaming Data**: JSONL output from the charting app to local scripts.
- **Chart Tasks**: Automated symbol switching, screenshots, and layout setup via CLI (`tv` command).
- **Validation**: Verifying indicator math against live data.

---

## Video Transcription (Spanish Context)

0:00 Conecta Claude a Tradingview
0:02 Cloud, cambia el gráfico de Bitcoin en vela horaria y dime qué ves...
... [rest of the transcription provided in the prompt]
19:51 y nos vemos en el siguiente vídeo.
