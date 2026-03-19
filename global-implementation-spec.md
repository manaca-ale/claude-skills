---
name: global-implementation-spec
description: Generate a global implementation roadmap/spec from a Markdown task list (e.g. tasks_flora.md) by reading all tasks, mapping impacted files/modules in the current workspace, sequencing work by dependencies, and listing risks/DoD. Use when the user asks for a unified implementation plan across a repo (not code).
---

# Global Implementation Spec

## Goal

Produce a single, unified implementation strategy (no code) for a project based on a Markdown file containing pending tasks, and write the final spec to a Markdown file in the target workspace.

## Inputs To Confirm (Ask If Missing)

- Path to the tasks Markdown file (example: `c:\Flora-Docker\tasks_flora.md`).
- Workspace root to analyze (default: current working directory).
- Output Markdown path (default: `GLOBAL_IMPLEMENTATION_SPEC.md` in the workspace root).

## Workflow (Do This In Order)

1. Read ALL tasks in the tasks file.
2. Scan the workspace to understand the repo structure (top-level folders/files, languages, entrypoints).
3. For each task:
   - Identify the likely impacted area (frontend/backend/scripts/config/docs).
   - List affected files as concrete, workspace-relative paths when possible.
   - Note dependencies on other tasks (schema before API before UI, etc.).
4. Produce a unified roadmap that:
   - Deduplicates overlapping work across tasks.
   - Orders steps by dependency and risk.
   - Calls out conflicts and regression risks.
5. Write the spec to a Markdown file in the workspace (UTF-8), at the output path (default `GLOBAL_IMPLEMENTATION_SPEC.md`).

## Constraints (Hard Rules)

- No code dumps in chat.
- Focus on architecture, sequencing, and logic steps.
- Roadmap must be actionable enough for another agent to modify files directly.
- Use UTF-8 when reading files and reasoning about text.

## Evaluation Checklist (Before You Send)

- Accounted for every single task found in the tasks file.
- Implementation order is logical (data model/migrations before API, API before UI, etc.).
- File paths are correct for the workspace.
- Output `.md` file was created/updated in the workspace (UTF-8).

## Output Format (Markdown)

Write the following structure into the output `.md` file:

```
## Global Sprint Overview
[Brief summary of the total work to be done]

## Implementation Roadmap
### Step 1: Shared Dependencies / Infrastructure
- [Changes that affect multiple tasks or base config]

### Step 2: Task-by-Task Breakdown
#### Task: [Task Name 1]
- **Affected Files**: `[path/to/file]`
- **Key Logic**: [Description of the core change]

#### Task: [Task Name 2]
- **Affected Files**: `[path/to/file]`
- **Key Logic**: [Description of the core change]

## Global Definition of Done
- [ ] [Unified testing strategy]
- [ ] [UTF-8 encoding check across all files]

## Conflict Risks
- [Identify tasks that might overlap or break existing features]
```
