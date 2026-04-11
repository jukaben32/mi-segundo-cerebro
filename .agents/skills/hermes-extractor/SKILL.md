---
name: hermes-skill-extractor
description: A metacognitive skill that analyzes past conversation execution traces to autonomously create or improve reusable skills, preventing repetitive prompt engineering and avoiding past mistakes.
---

# Hermes Skill Extractor (Metacognitive Skill)

This skill is designed to act on the principle of **GEPA** (Generic Evolution of Prompt Architectures) and the core philosophy of the Hermes agent. When invoked, you (the agent) will stop "doing" and start "reflecting." 

Your goal is to extract the successful procedural memory from a recent conversation or task execution, identify why it succeeded (and why previous attempts failed), and write it down as a highly structured, reusable `SKILL.md` file.

## 🚀 When to use this skill
This skill should be invoked **at the end** of a successful but complex task (e.g., after 5+ tool calls, a heavy debugging session, or an `autoresearch` win).

---

## 🛠️ Step-by-Step Execution

### 1. Analyze the Trajectory (Execution Traces)
- Read the recent conversation history or look at the files that were modified.
- Identify the **Goal**: What was the user trying to achieve?
- Identify the **Mistakes**: What tool calls failed? Which approaches led to errors or dead ends?
- Identify the **Breakthrough**: What was the specific sequence of actions, tool calls, or code changes that finally solved the problem?

### 2. Generalize the Workflow
- Strip away the project-specific details (like specific variable names or temporary file paths) and extract the **generic logic**.
- Turn the breakthrough into a highly structured recipe that any agent could follow in the future.

### 3. Check for Existing Skills
- Before creating a new file, check if a similar skill already exists in the `misProyectos/skills/` folder.
- **If it exists:** Propose an update to the existing `SKILL.md` file to append the newly learned edge cases, fixed mistakes, or optimized prompts to its instructions.
- **If it doesn't exist:** Create a new folder (e.g., `misProyectos/skills/[skill-name]`) and a `SKILL.md` file inside it.

### 4. Write the `SKILL.md` File
The procedural memory you write must follow this strict format:

```markdown
---
name: [skill-name]
description: [Short definition of what this skill does]
---

# Skill: [Skill Name]

## 🎯 Purpose
[Explain exactly when and why an agent should use this skill]

## 🧠 Lessons Learned (GEPA Insights)
- **What fails:** [List the approaches that failed in the past so the agent avoids them]
- **What works:** [Explain the proven approach discovered during extraction]

## ⚙️ Execution Steps
1. **[Step 1]**: [Actionable instruction]
2. **[Step 2]**: [Actionable instruction]
...

## 🔧 Tools Involved
- [List the specific tools needed, e.g., `run_command`, `replace_file_content`]
```

---

## ⚠️ Agent Directives
- **Zero-Shot Reusability:** The generated skill must be written so clearly that an agent reading it for the first time *months from now* can execute the task perfectly on the first try.
- **Emphasize MISTAKES:** The most important part of this skill is teaching the future agent what NOT to do based on the execution traces you analyzed.
- **Autonomy:** Once you generate the `SKILL.md`, report back to the user with a summary of what you learned and saved. You do not need the user to write the markdown for you.
