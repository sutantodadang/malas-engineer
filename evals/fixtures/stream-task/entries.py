import json
from pathlib import Path


def read_entries(filename):
    with Path(filename).open(encoding="utf-8") as source:
        return [json.loads(line) for line in source if line.strip()]
