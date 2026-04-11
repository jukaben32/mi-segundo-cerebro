# Concept: TradingView CDP Bridge (MCP)

## Overview
The **TradingView CDP Bridge** is a technical method to grant an LLM (like Claude) programmatic access to the TradingView Desktop application. Unlike traditional APIs, this bridge leverages the **Chrome DevTools Protocol (CDP)**, allowing the agent to "see" what is rendered in the Electron-based app.

## Implementation Details
- **Port**: 9222 (local only).
- **Communication**: Model Context Protocol (MCP) using a Node.js server.
- **Data Access**: Reads internal app state, including the `DataWindow`, Pine Script drawings (lines, tables, boxes), and the Strategy Tester results.
- **Workflow**: Enables an "AI-in-the-loop" development cycle where Claude writes, injects, and debugs Pine Script directly in the TradingView editor.

## Advantages
- **Privacy**: No data leaves the local machine (app to local process communication).
- **Depth**: Can read protected or proprietary indicators as long as they draw data on the chart.
- **Speed**: Automates repetitive charting tasks (backtesting logs, screenshot capture, multi-symbol streaming).

## Technical Requirements
1. **TradingView Desktop** (must be the desktop version, not web).
2. **Launch Flag**: `--remote-debugging-port=9222`.
3. **Node.js Environment**: To run the MCP server.

## References
- Source: [[tradingview-mcp-info]]
- Repo: [tradingview-mcp](https://github.com/tradesdontlie/tradingview-mcp)
