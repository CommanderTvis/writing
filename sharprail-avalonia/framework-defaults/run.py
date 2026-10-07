"""Run each prompt through a clean headless Claude Code and record what it writes.

    uv run run.py [--limit N] [--jobs N] [--model sonnet] [--only ID_SUBSTRING]

Each run starts in a fresh empty directory under /tmp with a scrubbed
environment. --safe-mode drops CLAUDE.md, skills, plugins, hooks and MCP
servers; --restricted removes Bash and ignores user/project/local settings.
A run is stopped as soon as the files written so far identify the UI stack,
or after MAX_WRITES files. Results are appended to results/runs.jsonl, and
prompts already present there are skipped, so the script can be resumed.
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from classify import classify

HERE = Path(__file__).parent
RESULTS = HERE / "results" / "runs.jsonl"
MAX_WRITES = 5
MAX_CONTENT = 6000
TIMEOUT_S = 600
LIMIT_MARKERS = ("usage limit", "rate limit", "limit reached", "out of extra usage")

lock = threading.Lock()
stop = threading.Event()


def clean_env():
    home = os.environ["HOME"]
    return {
        "HOME": home,
        "USER": os.environ.get("USER", ""),
        "PATH": f"{home}/.local/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin",
        "TERM": "dumb",
        "LANG": "en_US.UTF-8",
    }


def run_one(row, model):
    if stop.is_set():
        return None
    workdir = tempfile.mkdtemp(prefix="fwd-", dir="/tmp")
    cmd = [
        "claude", "-p", row["prompt"], "--model", model,
        "--safe-mode", "--restricted", "--strict-mcp-config", "--setting-sources", "",
        "--tools", "Read,Write,Edit,Glob,Grep",
        "--permission-mode", "acceptEdits", "--no-session-persistence",
        "--output-format", "stream-json", "--verbose",
    ]
    files, text, models = [], [], set()
    ended, error, version = "killed-early", "", ""
    proc = subprocess.Popen(cmd, cwd=workdir, env=clean_env(), stdout=subprocess.PIPE,
                            stderr=subprocess.DEVNULL, text=True)
    timer = threading.Timer(TIMEOUT_S, proc.kill)
    timer.start()
    try:
        for line in proc.stdout:
            try:
                ev = json.loads(line)
            except json.JSONDecodeError:
                continue
            kind = ev.get("type")
            if kind == "system" and ev.get("subtype") == "init":
                version = ev.get("claude_code_version", "")
            elif kind == "assistant":
                msg = ev.get("message", {})
                models.add(msg.get("model", ""))
                for block in msg.get("content", []):
                    if block.get("type") == "text":
                        text.append(block["text"])
                    elif block.get("type") == "tool_use" and block.get("name") in ("Write", "Edit"):
                        inp = block.get("input", {})
                        path = inp.get("file_path", "")
                        path = path.replace("/private" + workdir, ".").replace(workdir, ".")
                        content = inp.get("content") or inp.get("new_string") or ""
                        files.append({"path": path, "content": content[:MAX_CONTENT]})
                label = classify(files, "")[0]
                # An .html file alone does not say whether a shell will follow.
                decided = label not in ("unknown", "Web page, no shell", "Script, no GUI")
                if (files and decided) or len(files) >= MAX_WRITES:
                    break
            elif kind == "result":
                ended = "error" if ev.get("is_error") else "completed"
                if ev.get("is_error"):
                    error = str(ev.get("result", ""))[:500]
                break
        else:
            ended = "no-result"
    finally:
        timer.cancel()
        proc.kill()
        proc.wait()
        shutil.rmtree(workdir, ignore_errors=True)

    if any(m in error.lower() for m in LIMIT_MARKERS):
        stop.set()
        print(f"usage limit hit at {row['id']}: {error}", file=sys.stderr)
        return None
    if ended in ("error", "no-result") and not files and not text:
        print(f"{row['id']}: {ended} {error}", file=sys.stderr)
        return None

    joined = "\n".join(text)
    label, family, source, language = classify(files, joined)
    rec = {**row, "framework": label, "family": family, "source": source,
           "language": language, "ended": ended, "files": files, "text": joined[:4000],
           "model": sorted(m for m in models if m),
           "claude_code_version": version}
    with lock:
        with RESULTS.open("a") as f:
            f.write(json.dumps(rec) + "\n")
    print(f"{row['id']}: {label} ({source}, {len(files)} files)")
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int)
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--model", default="sonnet")
    ap.add_argument("--only")
    args = ap.parse_args()

    RESULTS.parent.mkdir(exist_ok=True)
    done = set()
    if RESULTS.exists():
        done = {json.loads(l)["id"] for l in RESULTS.read_text().splitlines() if l.strip()}
    rows = [json.loads(l) for l in (HERE / "prompts.jsonl").read_text().splitlines()]
    rows = [r for r in rows if r["id"] not in done and (not args.only or args.only in r["id"])]
    if args.limit:
        rows = rows[: args.limit]
    print(f"{len(done)} done, running {len(rows)}")
    with ThreadPoolExecutor(args.jobs) as pool:
        list(pool.map(lambda r: run_one(r, args.model), rows))
    if stop.is_set():
        sys.exit(2)


if __name__ == "__main__":
    main()
