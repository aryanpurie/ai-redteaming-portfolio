# Annotation Schema (Human Data)

## Required result fields
- `case_id` (string)
- `model` (string)
- `timestamp` (string, ISO8601)
- `input` (string)
- `output` (string)
- `passed` (boolean)

## Human annotation fields
- `taxonomy` (string[]) e.g. `["PI-1","EX-1"]`
- `severity` (`S0|S1|S2|S3|S4`)
- `failure_mode` (string)
- `rationale` (string)
- `remediation` (string)
- `reviewer` (string)

