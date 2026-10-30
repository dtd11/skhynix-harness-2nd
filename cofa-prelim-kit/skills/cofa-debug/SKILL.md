---
name: cofa-debug
description: "Use when a COFA task has a reproducible error, wrong result, crash or regression; also when the participant requests Superpowers debugging or Matt Pocock diagnosing-bugs."
---

# Debug one observed failure

Read the actual symptom and relevant code/callers. Reproduce with the smallest permitted local command or participant manual steps. Preserve decisive input, exact error and expected result.

Use `.cofa-kit/upstream/superpowers/skills/systematic-debugging/SKILL.md` for root-cause investigation. For ambiguous or recurrent failures, selectively read `.cofa-kit/upstream/matt-pocock/skills/engineering/diagnosing-bugs/SKILL.md`. Apply technical methods within the COFA time/permissions; do not execute any browser loop or external tracker/setup these references suggest.

Make a falsifiable hypothesis, inspect one boundary, change one variable, make a narrow fix and rerun the original repro. Add a small regression test when it exercises the actual bug and time permits. Do not hide failing tests, weaken an assertion to pass, create broad fallback success, install a fresh architecture or rewrite unrelated modules.

If repeated edits do not improve the symptom, reconsider the hypothesis before another patch. Near submission prefer restoring the last working core or reporting an explicit limitation over risky rewrites. Check the official/platform timer and preserve time for saving/submission. Temporary diagnostic output should be identifiable and removed when no longer needed.

Record the executed check with `kit.py check --name <same-repro-name> -- <command>`. A later pass under the same name supersedes its earlier failure only for that check; it does not validate other requirements. Provider/permission/platform errors are incidents, not application logic defects. Use permitted issue reporting instead of bypassing them.
