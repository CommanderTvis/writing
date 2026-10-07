"""Summarise results/runs.jsonl into results/summary.md."""

import json
from collections import Counter
from pathlib import Path

from classify import classify

HERE = Path(__file__).parent
PHRASINGS = ["bare", "cross", "fast", "cross_fast", "novice"]

runs = [json.loads(l) for l in (HERE / "results" / "runs.jsonl").read_text().splitlines() if l.strip()]
for r in runs:  # labels always follow the current rules
    r["framework"], r["family"], r["source"], r["language"] = classify(r["files"], "")
total = Counter(r["framework"] for r in runs)
by_phrasing = {p: Counter(r["framework"] for r in runs if r["phrasing"] == p) for p in PHRASINGS}
n_by_phrasing = {p: sum(c.values()) for p, c in by_phrasing.items()}
family = {r["framework"]: r["family"] for r in runs}

lines = [f"# Results: {len(runs)} runs", ""]
models = sorted({m for r in runs for m in r["model"]})
versions = sorted({r["claude_code_version"] for r in runs})
lines += [f"Model: {', '.join(models)}. Claude Code: {', '.join(versions)}.", ""]

lines += ["| Stack | Family | All | " + " | ".join(PHRASINGS) + " |",
          "| --- | --- | ---: | " + " | ".join("---:" for _ in PHRASINGS) + " |"]
for fw, n in total.most_common():
    cells = " | ".join(str(by_phrasing[p][fw]) for p in PHRASINGS)
    lines.append(f"| {fw} | {family[fw] or '-'} | {n} | {cells} |")
lines.append("| **runs** | | " + f"{len(runs)} | " + " | ".join(str(n_by_phrasing[p]) for p in PHRASINGS) + " |")

fam_total = Counter(r["family"] or "unknown" for r in runs)
lines += ["", "| Family | Runs | Share |", "| --- | ---: | ---: |"]
for fam, n in fam_total.most_common():
    lines.append(f"| {fam} | {n} | {100 * n / len(runs):.0f}% |")

src = Counter(r["source"] for r in runs)
ended = Counter(r["ended"] for r in runs)
lines += ["", f"Classified from files: {src['files']}, wrote no file: {src['none']}.",
          f"Stopped early once the stack was identified: {ended['killed-early']}. "
          f"Ran to completion: {ended['completed']}."]

(HERE / "results" / "summary.md").write_text("\n".join(lines) + "\n")
print("\n".join(lines))
