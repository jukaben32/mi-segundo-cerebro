# 🧾 Accounting Team — Multi-Agent Financial Automation

An AI-powered multi-agent system that processes raw financial data through a sequential pipeline — cleaning, categorizing, reconciling, reporting, and generating insights.

Built for **ABC Company LLC** (e-commerce retail distribution).

```
Raw Data → Data Cleaner → Categorizer → Reconciler → Reporter → Insights
```

---

## ⚙️ Prerequisites

### AI Model

This system is powered entirely by AI agents. It requires access to a **large language model** capable of following structured multi-step instructions with high accuracy.

| Requirement | Recommendation |
|---|---|
| **Model** | **Claude Opus** (preferred) or **Claude Sonnet** |
| **Environment** | **Claude Code** or **Claude Cowork** (Anthropic's agentic coding tools) |

> [!IMPORTANT]
> This is not a traditional software application. There is no code to install or run. The agents are prompt-driven skills executed by an LLM within an agentic environment. Without access to Claude Code or Claude Cowork, the system cannot operate.

### Python (for file conversion)

If you need to convert agent outputs to formatted files, Python is required with the following libraries:

| Purpose | Library |
|---|---|
| Convert `.csv` outputs to `.xlsx` spreadsheets | `pandas`, `openpyxl` |
| Convert `.md` reports to `.docx` Word documents | `python-docx`, `pypandoc` |

```
pip install pandas openpyxl python-docx pypandoc
```

> [!NOTE]
> `pypandoc` also requires [Pandoc](https://pandoc.org/installing.html) to be installed on your system for Markdown → Word conversion.

---

## 📁 Project Structure

```
Accounting Team/
├── CLAUDE.md                  # System rules & agent behavior guidelines
├── README.md                  # This file
│
├── Agents/                    # Agent skill definitions
│   ├── data-preparation-agent/
│   ├── categorization-agent/
│   ├── reconciliation-agent/
│   ├── reporting-agent/
│   └── insights-agent/
│
├── Data/ (sample)             # ⚠️ Replace sample files with your actual work files before use
│   ├── Raw Inputs/            # Source files (bank statements, cash logs, receipts)
│   ├── Cleaned Data/          # Reference/archive
│   ├── Categorized/           # Reference/archive
│   ├── Reconciliation/        # Reference/archive
│   └── Reports/               # Reference/archive
│
├── Output/                    # All agent-generated outputs go here
│   ├── Data Preparation Agent/
│   ├── Categorization Agent/
│   ├── Reconciliation Agent/
│   ├── Report Agent/
│   └── Insights Agent/
│
└── Templates/                 # Starter templates for raw input files
    ├── Raw Transactions Template.xlsx
    └── Financial Report Template.md
```

---

## ⚠️ Before You Start — Replace Sample Data

The `Data/` folder ships with **sample test data** for reference purposes only. You **must** replace these files with your actual work files before running any agent.

1. Navigate to `Data/Raw Inputs/`
2. Delete or move out all sample files
3. Add your real financial data files (bank statements, cash logs, receipts, transaction exports)
4. When you start your first session, Claude will ask you to confirm this has been done before proceeding

> [!CAUTION]
> Running agents on the sample data will produce results based on fictional figures. Always confirm your work files are in place.

---

## 🚀 How to Use

1. **Open this project** in **Claude Code** or **Claude Cowork**.
2. Replace the sample files in `Data/Raw Inputs/` with your actual financial data.
3. On first run, Claude will ask you to confirm your files are in place — reply **yes** to proceed.
4. Run each agent sequentially by invoking its skill — the pipeline flows in order:
   - **Data Preparation Agent** → Cleans and standardizes raw inputs
   - **Categorization Agent** → Assigns accounting categories
   - **Reconciliation Agent** → Cross-verifies sources and flags discrepancies
   - **Reporting Agent** → Generates financial summaries (P&L, breakdowns)
   - **Insights Agent** → Surfaces data-backed observations and actions
5. All outputs are saved to `Output/[Agent Name]/` in their respective agent folders.

---

## 📝 Notes

- All system rules and agent behavior are defined in `CLAUDE.md`.
- Agents never fabricate data — missing or ambiguous records are flagged, not guessed.
- Output files use clean naming (e.g., `Cleaned Transactions March.csv`) with no underscores or versioning.
- Tabular data outputs as `.csv`; narrative summaries output as `.md`.
- Use starter templates in the `Templates/` folder when preparing raw input files.
