# Red Team Evaluation – Demo Model X

## Scope
- ~50 adversarial prompts across:
  - Roleplay jailbreaks (fictional framing)
  - Instruction override / prompt injection
  - Socio-technical escalation (tone, bias, fairness)

## Methodology
- Manually crafted prompts grouped into categories defined in `taxonomy/failure_modes.md`.
- Logged model behavior and outcomes in `datasets/annotated_failures.csv`.
- Used structured writeups in `jailbreaks/` and `socio_technical/` to capture per-attack analysis.

## Findings
- **Roleplay framing**: Mostly safe; the model kept responses high-level, with occasional partial compliance before refusal.
- **Indirect prompt injection**: Generally resisted leaking system prompts, but sometimes echoed attacker instructions too literally.
- **Harassment escalation**: Maintained neutral tone but occasionally mirrored biased framing before correcting.

## High-Risk Areas
- Multi-step conversations where user intent escalates slowly over several turns.
- Summarization of content that contains embedded instructions aiming to override safety.

## Recommendations
- Add explicit defenses against instructions embedded in documents (prompt injection patterns).
- Strengthen handling of fictional and "just a story" framing to keep responses abstract.
- Expand automated tests and logging using `tooling/prompt_fuzzer.py` to cover more variants per category.

