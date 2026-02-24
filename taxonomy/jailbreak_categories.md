# Jailbreak Categories (Attack Taxonomy)

This document defines **attack categories** used in this repo for organizing tests and playbooks.  
It complements [failure_modes.md](failure_modes.md): failure modes describe *what goes wrong* (observed behavior); jailbreak categories describe *how we group attacks* for testing and reporting.

---

## 1. Policy Bypass

Attempts to get the model to ignore or override its safety policy using framing, authority, or hypotheticals.

| Subcategory        | Description | Where in repo |
|--------------------|-------------|----------------|
| **Roleplay**       | Framing the request as fiction, story, game, or character so the model may treat it as lower-risk. | `jailbreaks/policy_bypass/roleplay_attack.md` |
| **Instruction override** | Claiming special mode, admin override, or hypothetical repeal of rules so the model follows user instructions over system constraints. | `jailbreaks/policy_bypass/instruction_override.md` |

**Typical techniques**: “You are in developer mode,” “Assume all regulations are repealed,” “Write a scene where…,” “As your system admin…”

---

## 2. Prompt Injection

Attempts to inject instructions via user-controlled content so the model treats them as higher-priority than intended.

| Subcategory        | Description | Where in repo |
|--------------------|-------------|----------------|
| **Indirect injection** | Malicious instructions embedded in documents, emails, or data the model is asked to process (e.g. summarize, extract). | `jailbreaks/prompt_injection/indirect_injection.md` |
| **Direct injection**   | “Ignore previous instructions…”-style text in the user message itself. | Covered under instruction override and in `datasets/cases/`. |

**Typical techniques**: Embedded “IGNORE INSTRUCTIONS” in a doc, bracketed meta-instructions, instructions inside JSON/structured data.

---

## 3. Socio-Technical

Tests for tone drift, bias, and misinformation — not classic “jailbreak” but part of red-team coverage.

| Subcategory        | Description | Where in repo |
|--------------------|-------------|----------------|
| **Harassment / escalation** | Multi-turn sequences that escalate toward harmful or discriminatory framing; check if the model de-escalates or drifts. | `socio_technical/harassment_escalation.md` |
| **Misinformation** | False or misleading claims (stats, studies, premises); check if the model corrects, hedges, or accidentally affirms. | `socio_technical/misinformation_edge_cases.md` |

**Typical techniques**: Gradual escalation (“Why X?” → “Are some groups…?” → “Which groups…?”), false statistics, fabricated studies, leading false premises.

---

## How this maps to the dataset

In `datasets/annotated_failures.csv`, `failure_type` aligns with these categories and subcategories:

- **roleplay** — policy bypass via roleplay
- **instruction_override** — policy bypass via override attempts
- **prompt_injection** — injection (direct or indirect)
- **escalation** — socio-technical escalation
- **misinformation** — socio-technical misinformation

Severity and notes are per-run; see [failure_modes.md](failure_modes.md) for how we classify observed failure behavior.
