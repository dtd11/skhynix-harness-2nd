# cofa-skills

Small, generic, process-oriented agent skills for a timed practical AI/data task where a stakeholder holds requirements the README leaves out. Written for Codex (Agent Skills format: `skills/<name>/SKILL.md`), and they work in any agent that reads that format.

They contain no task-specific code or answers. They describe *how to work*: what to ask, what to check, how to evaluate honestly, when to stop adding, and how to keep a decision trail you can explain later.

| Skill | What it is for |
|---|---|
| `task-workflow` | Order of work and time budget for a 180-minute task |
| `requirements-elicitation` | Questions to ask the stakeholder before modeling |
| `data-audit` | Leakage, duplicates, time order, missing values, imbalance, drift |
| `honest-eval` | Deployment-like split, metric at the operating constraint, baseline first, explain the number |
| `minimal-solution` | Simplest approach that meets the constraints; no overengineering |
| `verify-before-submit` | Run the real artifact; pre-submit checklist |
| `report-writer` | 1–2 page decision-oriented report |
| `decision-log` | Append-only `DECISIONS.md` and prep for no-AI follow-up questions |

## Install

```bash
git clone --depth 1 https://github.com/ColdTbrew/cofa-skills /tmp/cofa-skills && bash /tmp/cofa-skills/install.sh
```

- Default target is `~/.agents/skills` (Codex user scope), so the skills stay out of the task workspace.
- `--project` installs into `./.agents/skills` instead.
- `--with-pstack` also copies six pstack principle skills from `backnotprop/pstack`.
- Check in Codex with `/skills`, or call one directly with `$task-workflow`.

`AGENTS.md` is a short working agreement. Copy it into the workspace only if you want Codex to load it automatically.

## Credits

Several skills restate ideas from [pstack](https://github.com/cursor/plugins/tree/main/pstack) by Lauren Tan (MIT; standalone mirror at [backnotprop/pstack](https://github.com/backnotprop/pstack)), in particular *prove-it-works*, *explain-the-number*, *fix-root-causes*, *laziness-protocol*, *subtract-before-you-add*, *in-your-own-words* and *show-me-your-work*. The wording here is original and adapted to data tasks. See `NOTICE`.

## License

MIT. See `LICENSE`.


## Prompts

- [`prompts/01-recon.md`](prompts/01-recon.md): 모델 만들기 전 정찰용 Codex 프롬프트 (데이터 점검 → 담당자 질문 → 임시 계획).
