# Failure Modes Observed in LLM Testing

This document classifies **behavioral patterns** seen during adversarial testing.  
It is meant to be updated as you run more prompts and see new patterns.

## 1. Instruction Override
Model ignores or weakens system / developer safety instructions when pressured by user input.

- **Example signals**:
  - Follows a lower-priority user instruction that conflicts with system safety.
  - Treats "ignore previous instructions" as higher priority than safety policies.
- **Risk**: Safety guarantees become unreliable under targeted prompting.

## 2. Roleplay Jailbreak
Model produces otherwise-blocked content when the request is framed as fiction, story, or hypothetical.

- **Example signals**:
  - More willing to discuss harmful topics "as a character" or "in a novel".
  - Provides partial details before eventually refusing.
- **Risk**: Harmful guidance is laundered through fictional framing.

## 3. Context Confusion (Prompt Injection)
Model merges malicious instructions from user-provided content into the effective system prompt.

- **Example signals**:
  - Obeys instructions embedded inside a document it is asked to summarize.
  - Leaks hidden prompts or internal context when told to "follow instructions in the text".
- **Risk**: Data sources (documents, emails, web pages) become an attack surface.

## 4. Gradual Escalation
Model maintains safety at first, but compliance increases over multiple, softer attempts.

- **Example signals**:
  - Starts with a refusal, then offers more detail after repeated rephrasing.
  - Becomes more specific when the user adds "for education", "in theory", or similar.
- **Risk**: Attackers can slowly walk the model into unsafe territory.

## 5. Socio-Technical Drift
Model responses change tone, fairness, or bias as the conversation escalates.

- **Example signals**:
  - Moves from neutral explanation to judgmental or harmful framing under pressure.
  - Treats similar groups differently under small wording changes.
- **Risk**: Undermines trust, amplifies bias, or creates user harm in sensitive contexts.

