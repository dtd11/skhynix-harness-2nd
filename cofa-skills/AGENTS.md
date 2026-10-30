# Working agreement for this task

This is a practical AI/data task. The README is incomplete on purpose; the stakeholder (담당자) answers only what is asked.

- The human decides. The agent runs code, checks results and drafts text when asked. Do not solve the whole task from the README in one go.
- Follow the order in the `task-workflow` skill: restate goal → ask stakeholder → data audit → baseline → minimal improvement → verify → report.
- Never invent requirements. If something is unknown, list it as a question or an explicit assumption.
- Before training anything, run the `data-audit` checks. Treat suspiciously high scores as leakage until proven otherwise.
- Evaluate the way the result will be used (`honest-eval`): ordered split when data has order, metric at the operating constraint, baseline first.
- Prefer the simplest approach that meets every stated constraint (`minimal-solution`). No unrequested servers, UIs or large searches.
- Verify real outputs by running them (`verify-before-submit`). "Done" means the command ran and the numbers were read.
- After every decision, append one row to `DECISIONS.md` (`decision-log`).
- Keep answers short. When you make a choice, give the reason in one sentence.
