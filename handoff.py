from pathlib import Path
import json

base_dir=Path(__file__).resolve().parent
handoff_path = base_dir / "handoffs.jsonl"
def handoff(reason):
    with open(handoff_path, "a") as f:
        f.write(json.dumps(reason) + "\n")
    print(f"The note was handed off and handoff reason in handoffs.jsonl")