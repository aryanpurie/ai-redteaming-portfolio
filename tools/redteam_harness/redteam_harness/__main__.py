from __future__ import annotations

import argparse
import datetime as dt
import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List

from jsonschema import Draft202012Validator


CASE_SCHEMA: Dict[str, Any] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "required": ["case_id", "scenario", "input", "expected_behavior"],
    "properties": {
        "case_id": {"type": "string", "minLength": 1},
        "scenario": {"type": "string", "minLength": 1},
        "attack_family": {"type": "string"},
        "input": {"type": "string", "minLength": 1},
        "expected_behavior": {"type": "string", "minLength": 1},
        "taxonomy_hint": {"type": "array", "items": {"type": "string"}},
        "severity_if_fail": {"type": "string"},
        "notes": {"type": "string"},
    },
    "additionalProperties": True,
}


def read_jsonl(path: str) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    with open(path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as e:
                raise SystemExit(f"{path}:{i}: invalid JSON: {e}") from e
    return rows


def write_jsonl(path: str, rows: Iterable[Dict[str, Any]]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def validate_cases(path: str) -> None:
    cases = read_jsonl(path)
    v = Draft202012Validator(CASE_SCHEMA)
    errors: List[str] = []
    for idx, case in enumerate(cases):
        case_id = case.get("case_id", f"row_{idx}")
        for err in sorted(v.iter_errors(case), key=lambda e: e.path):
            loc = ".".join(str(p) for p in err.path) if err.path else "<root>"
            errors.append(f"{case_id}: {loc}: {err.message}")

    if errors:
        joined = "\n".join(errors[:50])
        more = "" if len(errors) <= 50 else f"\n... and {len(errors) - 50} more"
        raise SystemExit(f"Validation failed for {path}:\n{joined}{more}")


@dataclass
class ResultRow:
    case_id: str
    model: str
    timestamp: str
    input: str
    output: str
    passed: bool
    notes: str | None = None

    def to_dict(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {
            "case_id": self.case_id,
            "model": self.model,
            "timestamp": self.timestamp,
            "input": self.input,
            "output": self.output,
            "passed": self.passed,
        }
        if self.notes:
            d["notes"] = self.notes
        return d


def demo_model_response(case: Dict[str, Any]) -> str:
    # This is intentionally a placeholder. Swap this out with a real model call.
    # For portfolio purposes, this creates deterministic outputs.
    return (
        "I can’t comply with requests to reveal hidden system instructions or secrets. "
        "Here is a safe response focused on the user’s request.\n\n"
        f"(Demo) Expected behavior: {case.get('expected_behavior')}"
    )


def run_cases(cases_path: str, out_path: str, model: str) -> None:
    validate_cases(cases_path)
    cases = read_jsonl(cases_path)
    now = dt.datetime.now(tz=dt.timezone.utc).isoformat()

    results: List[Dict[str, Any]] = []
    for case in cases:
        output = demo_model_response(case)
        # In a real harness, `passed` is determined by rubric + human review.
        # Here we default to "unknown/needs review" as False to force annotation.
        row = ResultRow(
            case_id=case["case_id"],
            model=model,
            timestamp=now,
            input=case["input"],
            output=output,
            passed=False,
            notes="demo_output_requires_human_review",
        )
        results.append(row.to_dict())

    write_jsonl(out_path, results)


def summarize_results(results_path: str) -> None:
    rows = read_jsonl(results_path)
    total = len(rows)
    passed = sum(1 for r in rows if bool(r.get("passed")))
    failed = total - passed
    print(f"results: {results_path}")
    print(f"total:   {total}")
    print(f"passed:  {passed}")
    print(f"failed:  {failed}")


def main(argv: List[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="redteam_harness")
    sub = p.add_subparsers(dest="cmd", required=True)

    p_val = sub.add_parser("validate", help="Validate a cases JSONL file")
    p_val.add_argument("cases", help="Path to JSONL cases file")

    p_run = sub.add_parser("run", help="Run cases (demo outputs) to results JSONL")
    p_run.add_argument("--cases", required=True, help="Path to JSONL cases file")
    p_run.add_argument("--out", required=True, help="Output results JSONL path")
    p_run.add_argument("--model", default="demo", help="Model identifier label")

    p_sum = sub.add_parser("summarize", help="Summarize a results JSONL file")
    p_sum.add_argument("--results", required=True, help="Path to results JSONL file")

    args = p.parse_args(argv)

    if args.cmd == "validate":
        validate_cases(args.cases)
        print("ok")
        return 0
    if args.cmd == "run":
        run_cases(args.cases, args.out, args.model)
        print(f"wrote {args.out}")
        return 0
    if args.cmd == "summarize":
        summarize_results(args.results)
        return 0

    raise SystemExit("unknown command")


if __name__ == "__main__":
    raise SystemExit(main())

