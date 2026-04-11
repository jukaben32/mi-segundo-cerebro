# startup-claude-skills Workspace

This repository is a central library for **Antigravity** to execute specialized multi-agent development pipelines.

## 🎯 Global Purpose
To provide high-end, end-to-end autonomous development capabilities for tech startups.

## 🛠 Skills included:
- **fix-ticket** — End-to-end Jira bug fix pipeline (read, repro, fix, review, commit, deploy, update).
- **develop-team** — Feature development team with parallel research, planning, phased implementation, and PR creation.
- **review-team** — 5-agent PR review with "Devil's Advocate" adversarial filtering.
- **review-fix** — Automated review-fix loop with 8 parallel reviewers and auto-fixes.
- **playwright-qa-cli** — Headless browser QA testing with test user provisioning, navigation, and screenshots.

## ⚙️ Requirements (MCP tools):
- `mcp__jira__*` — Jira ticket management.
- `mcp__claude_ai_Vercel__*` — Deployment monitoring.
- `mcp__supabase__*` — Database operations.
- `playwright-cli` — Headless browser QA.

## 🤫 Workflow Rules:
1. **Always read `CONFIG.md`** inside each skill's subfolder before starting.
2. **Execute phases sequentially** as defined in the `SKILL.md`.
3. **Stop at user gates** (Phase 2 Research, Phase 5.5 QA Failures) to ensure alignment.
4. **Always commit and push** — local-only commits are incomplete.
5. **Phase tracking**: Use `Phase {N}: {Name}` headers and include the Phase Tracker table in summaries.

## 🧪 Quick Test:
`/fix-ticket PROJ-123`

---
*Created by Antigravity — Your Agentic AI Engineering Partner.*
