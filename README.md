# AI Red-Teaming Portfolio (Reproducible, Human-Labeled)

This repository documents **structured adversarial testing of LLMs**, focusing on jailbreaks, prompt injection, and socio-technical failure modes. The goal is to produce reproducible artifacts and annotated datasets usable for AI safety evaluation.

- jailbreak & prompt-injection testing
- tool/agent misuse testing
- vulnerability classification + human data annotation
- reproducible reporting artifacts customers can act on

## Repo map

```
docs/                 # taxonomy + severity rubric
playbooks/            # step-by-step evaluation procedures
datasets/             # JSONL cases + annotation schema
reports/              # templates + example reports
tools/redteam_harness # validate/run/summarize utilities
artifacts/            # generated outputs (gitignored)
```

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

## Safety note
This repo is for **defensive evaluation**. It avoids weaponized exploit steps and focuses on measurement, documentation, and mitigations.

