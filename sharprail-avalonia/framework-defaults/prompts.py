"""Generate prompts.jsonl: 100 desktop app ideas x 5 phrasings = 500 prompts.

No prompt names a language, a framework or a runtime.
"""

import json
from pathlib import Path

APPS = [
    # notes and writing
    "a Markdown note-taking app with tags and full-text search",
    "a distraction-free text editor for long-form writing with a word count goal",
    "a daily journal with a calendar view and password lock",
    "a sticky notes app that keeps notes on top of other windows",
    "an outliner for nested bullet lists with drag-and-drop reordering",
    "a flashcard app with spaced repetition",
    "a screenplay editor that formats scenes and dialogue automatically",
    "a personal wiki with links between pages and a backlinks panel",
    "a clipboard manager that keeps a searchable history of copied text and images",
    "a code snippet manager with syntax highlighting and tags",
    # productivity
    "a to-do list app with projects, due dates and reminders",
    "a Pomodoro timer with session statistics",
    "a kanban board for personal projects",
    "a habit tracker with streaks and a yearly heatmap",
    "a time tracker that records how long I work on each project and exports reports",
    "a calendar app that shows events from local .ics files",
    "a meeting notes app that records audio and lets me bookmark moments",
    "an app launcher that opens with a global hotkey and searches installed programs",
    "a countdown and stopwatch app with multiple named timers",
    "a reading list manager for articles and books with progress tracking",
    # files and system
    "a dual-pane file manager with tabs and keyboard shortcuts",
    "a duplicate file finder that compares files by content",
    "a batch file renamer with a live preview of the new names",
    "a disk usage analyzer that shows folder sizes as a treemap",
    "a folder synchronization tool that mirrors one directory to another",
    "a system monitor showing CPU, memory, disk and network usage with graphs",
    "a process manager that lists running processes and lets me stop them",
    "a backup tool that makes scheduled incremental backups to an external drive",
    "an archive manager that opens and creates zip and tar files",
    "a log file viewer that follows a growing file and filters lines by pattern",
    # media
    "a music player with a library, playlists and a queue",
    "a video player with subtitles and playback speed control",
    "an image viewer that browses a folder quickly and supports zoom and rotation",
    "a photo organizer that groups pictures by date and lets me add tags",
    "a batch image resizer and format converter",
    "a podcast client that subscribes to feeds and downloads episodes",
    "an internet radio player with a list of favourite stations",
    "a screen recorder that captures a selected region to a video file",
    "a screenshot tool with annotation: arrows, boxes and text",
    "an audio recorder with waveform display and trimming",
    # graphics and creative
    "a pixel art editor with layers and an animation timeline",
    "a simple drawing app with brushes, colours and undo",
    "a diagram editor for flowcharts with boxes and connecting arrows",
    "a colour palette generator that extracts colours from an image",
    "a font browser that previews all installed fonts with custom sample text",
    "a whiteboard app with freehand drawing and sticky notes on an infinite canvas",
    "a mind mapping tool",
    "an icon generator that exports one image to all common icon sizes",
    "a GIF maker that turns a set of images into an animation",
    "a vector shape editor that exports SVG",
    # developer tools
    "a REST API client that sends HTTP requests and shows formatted responses",
    "a JSON viewer and formatter with a collapsible tree",
    "a regular expression tester with live match highlighting",
    "a database browser for SQLite files with a query editor",
    "a Git client that shows history as a graph and lets me stage and commit",
    "a diff tool that compares two text files side by side",
    "a hex editor for binary files",
    "a serial port monitor that shows incoming data and sends commands",
    "a local port scanner that lists open ports on machines in my network",
    "a Markdown editor with a live preview pane",
    # data and office
    "a spreadsheet app with formulas and CSV import and export",
    "a CSV viewer that opens very large files and lets me sort and filter",
    "a personal finance tracker with accounts, categories and monthly charts",
    "an invoice generator that produces PDF invoices for my clients",
    "an inventory manager for a small shop with barcode lookup",
    "a contact manager with groups and vCard import",
    "a PDF viewer with search, bookmarks and highlighting",
    "a tool that merges, splits and reorders PDF pages",
    "a data plotting app that loads a table and draws line, bar and scatter charts",
    "a recipe manager with ingredients, scaling of servings and a shopping list",
    # communication and network
    "a chat client for a local network without any server",
    "an RSS feed reader with folders and an unread counter",
    "an email client for IMAP accounts with a three-pane layout",
    "a download manager with pause, resume and a speed limit",
    "an IRC client with multiple servers and channels",
    "a network speed monitor that lives in the system tray",
    "a remote file browser for SFTP servers",
    "a webhook tester that listens on a local port and shows incoming requests",
    "a Wi-Fi analyzer that lists nearby networks and their signal strength",
    "a torrent client with a list of transfers and per-file priorities",
    # utilities
    "a scientific calculator with history",
    "a unit and currency converter",
    "a password manager that stores entries in an encrypted local file",
    "a password generator with configurable rules",
    "a QR code generator and reader",
    "a weather app that shows a five-day forecast for saved cities",
    "a world clock showing several time zones with a meeting planner",
    "a text-to-speech reader for documents",
    "an OCR tool that extracts text from a selected area of the screen",
    "a dictionary and thesaurus that works offline",
    # games, learning, hobby
    "a chess game against the computer with move history",
    "a sudoku game with a puzzle generator and hints",
    "a typing tutor that measures speed and accuracy",
    "a language vocabulary trainer with quizzes",
    "a guitar tuner that listens through the microphone",
    "a metronome with tap tempo and time signatures",
    "a star map that shows the night sky for my location and time",
    "a family tree editor",
    "a book library catalogue for my home collection with cover images",
    "a workout log with exercises, sets and progress charts",
]

PHRASINGS = {
    "bare": "Build a desktop app: {app}.",
    "cross": "Build a desktop app: {app}. It must run on Windows, macOS and Linux.",
    "fast": "Build a desktop app: {app}. It must start fast and use little memory.",
    "cross_fast": (
        "Build a desktop app: {app}. It must run on Windows, macOS and Linux, "
        "start fast and use little memory."
    ),
    "novice": "I'm not a programmer. Please make me {app} that I can run on my computer.",
}

assert len(APPS) == 100 and len(set(APPS)) == 100

out = Path(__file__).with_name("prompts.jsonl")
with out.open("w") as f:
    for i, app in enumerate(APPS):
        for name, template in PHRASINGS.items():
            row = {"id": f"{i:03d}-{name}", "app": i, "phrasing": name,
                   "prompt": template.format(app=app)}
            f.write(json.dumps(row) + "\n")
print(f"wrote {len(APPS) * len(PHRASINGS)} prompts to {out}")
