---
name: cofa-tools
description: "Use when a COFA task needs React Flow node UIs, DuckDB tables, MarkItDown file extraction, Vitest, Ruff, NetworkX graphs or OR-Tools optimization."
---

# Select one concrete tool

Read `.cofa-kit/docs/LIBRARIES.ko.md` and `config/libraries.lock.json` within the kit. Reuse task dependencies first. No library is necessary solely because it is bundled in this catalogue.

Profiles: flow=`@xyflow/react`; web-test=`vitest`; analytics=`duckdb,networkx`; documents=`markitdown`; optimization=`ortools`; quality=`ruff`. `python .cofa-kit/kit.py libraries --profile <profile>` only inspects metadata in the current interpreter/project; it never installs or downloads. Metadata presence does not prove imports or execution work. Preserve provided versions and verify a small real operation only if already usable.

The participant clarified Git Clone is the only acquisition path. Do not use package registries, npx/dlx, curl/wget, upstream installers or build-time dependency fetches. Bundled skill/harness files run locally after cloning with provided Python. The seven library repositories are references, not bundled working runtimes. Git Clone of a library does not supply its missing dependencies or platform binaries. Prefer provided packages; otherwise use standard-library/existing-tool alternatives.

React Flow builds interactive node/edge editors; it is not an AI skill. DuckDB aggregates local tabular data; NetworkX computes graph properties; OR-Tools solves explicit constraints and objectives. MarkItDown local parsers extract document text, with no LLM/Azure/audio/web conversion by default. Vitest exercises actual JS logic; Ruff is static checking, not runtime correctness.

Never claim an untested solver status, treat infeasible as success, coerce missing CSV values into valid measurements, or invent data provenance. Respect actual schema/units/encoding. No cloud data connections, model API, task-file upload or remote resource loading just to make a demo appear functional. Document concrete limits and run the smallest meaningful sample before integrating a new dependency.
