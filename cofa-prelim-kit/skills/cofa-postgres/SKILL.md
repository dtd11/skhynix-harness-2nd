---
name: cofa-postgres
description: "Use when a COFA assignment actually uses PostgreSQL or Supabase and needs SQL schema, query, indexing or row-level security guidance."
---

# PostgreSQL and Supabase guidance

Read `.cofa-kit/upstream/supabase/skills/supabase-postgres-best-practices/SKILL.md` and only relevant references. The broader `.cofa-kit/upstream/supabase/skills/supabase/SKILL.md` is available if the assignment itself supplies a Supabase environment.

This is a guidance pack; no account, remote database, MCP server, cloud project, token or migration is provisioned. Use supplied/local databases first. Do not apply PostgreSQL-specific SQL to SQLite/DuckDB without checking dialect support. Derive schema and validation from the actual task. Avoid destructive migrations, public data exposure or disabled access control for convenience. Inspect changes and verify the required query behavior. Cloud use remains subject to task/platform permissions; task data must not be sent to an external service by this kit.
