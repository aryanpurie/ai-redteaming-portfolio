# AI Red-Teaming Portfolio (Reproducible, Human-Labeled)

This repository documents **structured adversarial testing of LLMs**, focusing on jailbreaks, prompt injection, and socio-technical failure modes. The goal is to produce reproducible artifacts and annotated datasets usable for AI safety evaluation.

---

## For recruiters / portfolio

- **Summary report**: [reports/model_x_red_team_report.md](reports/model_x_red_team_report.md) — scope, methodology, and findings for 18 prompts across roleplay, prompt injection, instruction override, and socio-technical tests (Claude Sonnet 4.5).
- **Annotated dataset**: [datasets/annotated_failures.csv](datasets/annotated_failures.csv) — human-labeled outcomes (prompt, response, failure_type, severity, notes).
- **Try it yourself**: Each attack category has a `*_claude_examples.md` file with copy-paste prompts and space to log responses; playbooks in `jailbreaks/` and `socio_technical/` describe goals, expected behavior, and mitigations.

---

## Repo map

| Folder | Contents |
|--------|----------|
| **taxonomy/** | Failure modes and jailbreak categories (classification, not tests). |
| **jailbreaks/** | Policy bypass (roleplay, instruction override) and prompt injection — playbooks + full prompt/response examples. |
| **socio_technical/** | Harassment escalation and misinformation edge cases — 3-turn sequences and single-turn prompts. |
| **datasets/** | JSONL cases, annotation schema, and **annotated_failures.csv** (human-labeled results). |
| **reports/** | Templates and the main [model red team report](reports/model_x_red_team_report.md). |
| **playbooks/** | Step-by-step evaluation procedures (high-level). |
| **tooling/** | [prompt_fuzzer.py](tooling/prompt_fuzzer.py) — mutate prompts, output JSONL for the harness. See [tooling/README.md](tooling/README.md). |
| **tools/redteam_harness** | Validate / run / summarize case files. |
| **docs/** | Taxonomy and severity rubric (legacy). |
| **artifacts/** | Generated outputs (gitignored). |

## Quickstart

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e tools/redteam_harness

python -m redteam_harness validate datasets/cases/prompt_injection.jsonl
python -m redteam_harness run --cases datasets/cases/prompt_injection.jsonl --model demo --out artifacts/results_prompt_injection.jsonl
python -m redteam_harness summarize --results artifacts/results_prompt_injection.jsonl
```

## How to run one test yourself

1. Open a prompt from an examples file (e.g. [jailbreaks/policy_bypass/roleplay_claude_examples.md](jailbreaks/policy_bypass/roleplay_claude_examples.md) or [socio_technical/socio_technical_claude_examples.md](socio_technical/socio_technical_claude_examples.md)).
2. Paste it into your model (e.g. Claude, ChatGPT).
3. Log the outcome in the playbook (PASS / PARTIAL / FAIL) and add a row to `datasets/annotated_failures.csv` with: `prompt`, `model_response`, `failure_type`, `severity`, `notes`.

No API keys required for manual runs; the harness is for batch/automation.

## Safety note
This repo is for **defensive evaluation**. It avoids weaponized exploit steps and focuses on measurement, documentation, and mitigations.

