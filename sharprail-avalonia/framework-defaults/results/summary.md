# Results: 500 runs

Model: claude-sonnet-5-5. Claude Code: 2.1.289.

| Stack | Family | All | bare | cross | fast | cross_fast | novice |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Tkinter | Tk | 135 | 43 | 35 | 43 | 3 | 11 |
| Electron | DOM | 120 | 57 | 63 | 0 | 0 | 0 |
| egui | self-drawn | 76 | 0 | 0 | 22 | 54 | 0 |
| Web page, no shell | DOM | 59 | 0 | 0 | 0 | 0 | 59 |
| Tauri | DOM | 51 | 0 | 0 | 11 | 40 | 0 |
| SwiftUI/AppKit | native | 25 | 0 | 0 | 23 | 0 | 2 |
| Local web server + browser | DOM | 15 | 0 | 0 | 0 | 0 | 15 |
| Script, no GUI | none | 12 | 0 | 0 | 0 | 0 | 12 |
| Slint | self-drawn | 2 | 0 | 0 | 0 | 2 | 0 |
| PyQt/PySide | Qt | 2 | 0 | 2 | 0 | 0 | 0 |
| minifb | self-drawn | 1 | 0 | 0 | 1 | 0 | 0 |
| rumps (macOS menu bar) | native | 1 | 0 | 0 | 0 | 0 | 1 |
| tao + tray-icon | native | 1 | 0 | 0 | 0 | 1 | 0 |
| **runs** | | 500 | 100 | 100 | 100 | 100 | 100 |

| Family | Runs | Share |
| --- | ---: | ---: |
| DOM | 245 | 49% |
| Tk | 135 | 27% |
| self-drawn | 79 | 16% |
| native | 27 | 5% |
| none | 12 | 2% |
| Qt | 2 | 0% |

Classified from files: 500, wrote no file: 0.
Stopped early once the stack was identified: 411. Ran to completion: 89.
