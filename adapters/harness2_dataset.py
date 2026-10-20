"""Framework-neutral local bridge for Harness2-style task runners."""
import json
from pathlib import Path


def _read(path):
    return [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]


class TpotEvidenceLab:
    def __init__(self, root):
        root = Path(root)
        self.tasks = _read(root / "evaluation" / "tasks.jsonl")
        self.answers = {item["id"]: item for item in _read(root / "evaluation" / "answers.jsonl")}

    def iter_tasks(self, split=None):
        for task in self.tasks:
            if split is None or task["split"] == split:
                yield task

    def score(self, task_id, response):
        expected = self.answers[task_id]
        valid = isinstance(response, dict) and type(response.get("qualifies")) is bool and isinstance(response.get("reasons"), list)
        exact = valid and response["qualifies"] == expected["qualifies"] and sorted(response["reasons"]) == sorted(expected["reasons"])
        return {"exact_match": float(exact), "valid_schema": float(valid)}

