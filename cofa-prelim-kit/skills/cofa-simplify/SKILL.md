---
name: cofa-simplify
description: "Use when the participant requests code-simplifier, Ponytail, Karpathy, refactoring or simpler code in a COFA coding task, after required behavior is understood."
---

# Simplify while preserving behavior

Read `.cofa-kit/upstream/code-simplifier/plugins/code-simplifier/agents/code-simplifier.md`. For minimal-change principles, consult `.cofa-kit/upstream/ponytail/skills/ponytail/SKILL.md` or `.cofa-kit/upstream/karpathy/skills/karpathy-guidelines/SKILL.md` only as needed. These are reference documents, not active agents/installers.

First identify the changed scope, callers, observable behavior and relevant checks. If tests already fail, isolate/fix that failure before optional simplification. With less than30 minutes to recommended confirmation, skip broad refactors; with10 minutes, only resolve blockers and submit.

Prefer readable reductions: remove duplication introduced by this change, unnecessary wrappers, dead imports created by the edit and avoidable state. Keep project conventions, public interfaces, failure semantics, accessibility, boundary validation, comments explaining constraints and every requested feature. Shorter line count alone is not improvement. Avoid nested clever expressions and unrelated cleanup.

Establish focused baseline evidence, make one behavior-preserving change and rerun it. If behavior cannot be demonstrated, leave that area as-is and explain the limit. Refactors that change requirements require an explicit task decision, not silent simplification. No proxy, telemetry, external model invocation or auto-hook installation from upstream projects.
