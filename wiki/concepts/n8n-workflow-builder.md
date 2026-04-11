# Concept: n8n Workflow Builder (Claude Code)

## Overview
The **n8n Workflow Builder** is a specialized capability (Skill) for Claude Code designed to guide users in creating production-ready n8n workflows. It focuses on generating valid JSON structures that can be imported directly into an n8n instance.

## Methodology
The builder follows a specific interaction pattern:
1. **Clarification Phase**: Asks targeted questions to resolve ambiguities in triggers, endpoints, and data mappings.
2. **JSON Generation**: Produces the technical JSON object representing nodes and connections.
3. **Documentation**: Explains the workflow logic and configuration steps (credentials, etc.).

## Key Rules
- **Non-guess Policy**: Never assumes technical details; always verifies with the user.
- **Structural Integrity**: JSON must conform to n8n's internal schema.
- **Security Awareness**: Identifies where sensitive credentials belong without asking for them.

## References
- Original Prompt: [[n8n-workflow-builder-prompt]]
- Implementation: `~/.claude/skills/n8n-workflow-builder/SKILL.md`

## Use Cases
- Automating lead generation (Typeform -> Slack/CRM).
- Monitoring price drops or web changes.
- Scheduled news or weather alerts.
- Inbox to CRM synchronization.
