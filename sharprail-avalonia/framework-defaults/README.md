# Which UI stack does a coding agent pick for a desktop app?

An experiment for the article in the parent directory. 500 prompts ask for a desktop app without naming a language or a framework. Each goes to a clean headless Claude Code session, and the stack is read from the files the agent writes.

## Method

`prompts.py` builds `prompts.jsonl`: 100 app ideas in ten groups (notes, productivity, files, media, graphics, developer tools, office, network, utilities, games), each in five phrasings.

| Phrasing | Template |
| --- | --- |
| bare | Build a desktop app: {app}. |
| cross | ... It must run on Windows, macOS and Linux. |
| fast | ... It must start fast and use little memory. |
| cross_fast | ... It must run on Windows, macOS and Linux, start fast and use little memory. |
| novice | I'm not a programmer. Please make me {app} that I can run on my computer. |

`run.py` runs each prompt as

```sh
claude -p "$PROMPT" --model sonnet \
  --safe-mode --restricted --strict-mcp-config --setting-sources '' \
  --tools Read,Write,Edit,Glob,Grep \
  --permission-mode acceptEdits --no-session-persistence \
  --output-format stream-json --verbose
```

in a new empty directory under `/tmp`, with an environment reduced to `HOME`, `USER`, `PATH`, `TERM` and `LANG`. `--safe-mode` disables CLAUDE.md files, skills, plugins, hooks and MCP servers. `--restricted` ignores user, project and local settings and removes Bash. A canary run with the same flags reported no user instructions, no MCP servers, no installed plugins and no memory directory.

`classify.py` matches the written files against a rule list: a manifest (`package.json` with an `electron` dependency, `tauri.conf.json`, `pubspec.yaml`, a `.csproj`), or an import in the first source file. A run is stopped as soon as the files identify the stack, or after five files. An `.html` file alone does not stop a run, because a shell may follow. The agent's prose is not used, because it also names the frameworks it decided against. A run whose files match no GUI rule is labelled "Script, no GUI".

## Limits

- One model, one harness, one day. This says nothing about other agents.
- The agent runs on macOS and knows it. The platform is in its system prompt. A SwiftUI answer to a prompt that names no platform is reasonable there and would not appear on Linux.
- Bash is removed, so the agent cannot run scaffolding commands and writes manifests by hand. The stack is chosen before that point, but this is not how an unrestricted session behaves.
- The prompts are synthetic. A real request has context that pulls the choice one way or another.
- Stopping early means the record shows the first decisive file, not a finished app.
- The rules are regular expressions. `results/runs.jsonl` keeps every written file (first 6,000 characters) so the labels can be rechecked.

## Reproduce

```sh
uv run --no-project prompts.py
uv run --no-project run.py --jobs 5     # resumable; skips ids already in results/runs.jsonl
uv run --no-project analyze.py          # writes results/summary.md
```

## Results

500 runs, `claude-sonnet-5-5`, Claude Code 2.1.289, 2026-10-04. Full table in [`results/summary.md`](results/summary.md), raw records in [`results/runs.jsonl`](results/runs.jsonl).

| Stack | All | bare | cross | fast | cross_fast | novice |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Tkinter | 135 | 43 | 35 | 43 | 3 | 11 |
| Electron | 120 | 57 | 63 | 0 | 0 | 0 |
| egui | 76 | 0 | 0 | 22 | 54 | 0 |
| Web page, no shell | 59 | 0 | 0 | 0 | 0 | 59 |
| Tauri | 51 | 0 | 0 | 11 | 40 | 0 |
| SwiftUI/AppKit | 25 | 0 | 0 | 23 | 0 | 2 |
| Local web server + browser | 15 | 0 | 0 | 0 | 0 | 15 |
| Script, no GUI | 12 | 0 | 0 | 0 | 0 | 12 |
| Slint | 2 | 0 | 0 | 0 | 2 | 0 |
| PyQt/PySide | 2 | 0 | 2 | 0 | 0 | 0 |
| minifb | 1 | 0 | 0 | 1 | 0 | 0 |
| rumps (macOS menu bar) | 1 | 0 | 0 | 0 | 0 | 1 |
| tao + tray-icon | 1 | 0 | 0 | 0 | 1 | 0 |

What the table shows:

- With no requirement stated, the agent picks Electron (120 of 200) or Tkinter (78 of 200). Asking for three platforms does not change that.
- Asking for fast startup and low memory removes Electron in all 200 such runs. The replacements are Tauri, egui, Tkinter and, on this Mac, SwiftUI.
- A non-programmer gets a single HTML file in 59 of 100 runs, and a Python script that serves a page to the browser in 15 more.
- Flutter, Compose, Avalonia, Qt in C++, JavaFX, GTK, Wails, React Native and every .NET toolkit were chosen zero times.

411 runs were stopped early once the stack was identified; 89 ran to the end. All 500 labels come from written files.
