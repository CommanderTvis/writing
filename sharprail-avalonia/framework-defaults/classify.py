"""Decide which UI stack a run chose, from the files it wrote.

Rules look at file names and file contents only. The assistant's prose is
not used: it also names the frameworks it decided against.
"""

import re

# (label, family, pattern) checked in order against "path\ncontent" of each file.
FILE_RULES = [
    ("Tauri", "DOM", r"tauri\.conf\.json|@tauri-apps/|^\s*tauri(-build)?\s*=|\btauri::"),
    ("Electron", "DOM", r"\"electron\"\s*:|require\(['\"]electron['\"]\)|from ['\"]electron['\"]|electron-builder|electron-forge"),
    ("Wails", "DOM", r"wailsapp/wails|wails\.json"),
    ("Neutralino", "DOM", r"neutralino\.config\.json|@neutralinojs"),
    ("NW.js", "DOM", r"\"nw\"\s*:|nw-builder"),
    ("pywebview", "DOM", r"^\s*import webview|^\s*from webview "),
    ("Flet", "self-drawn", r"^\s*import flet|^\s*from flet "),
    ("Flutter", "self-drawn", r"pubspec\.yaml|package:flutter/"),
    ("Avalonia", "self-drawn", r"Avalonia"),
    ("Compose Desktop", "self-drawn", r"org\.jetbrains\.compose|androidx\.compose"),
    ("Slint", "self-drawn", r"\bslint\b\s*=|slint::|\.slint\b"),
    ("egui", "self-drawn", r"\beframe\b|\begui\b"),
    ("iced", "self-drawn", r"^\s*iced\s*=|\biced::"),
    ("Dear ImGui", "self-drawn", r"imgui\.h|\bimgui\b|dearpygui"),
    ("Kivy", "self-drawn", r"^\s*(import|from) kivy"),
    ("pygame", "self-drawn", r"^\s*import pygame"),
    ("Fyne", "self-drawn", r"fyne\.io/fyne"),
    ("PyQt/PySide", "Qt", r"^\s*(from|import) (PyQt[56]|PySide[26])"),
    ("Qt (C++/QML)", "Qt", r"find_package\(Qt|#include <Q[A-Z]|QT \+=|import QtQuick"),
    ("CustomTkinter", "Tk", r"^\s*import customtkinter|^\s*from customtkinter"),
    ("Tkinter", "Tk", r"^\s*import tkinter|^\s*from tkinter"),
    ("wxPython/wxWidgets", "native", r"^\s*import wx\b|wx/wx\.h"),
    ("GTK", "native", r"gi\.require_version\(['\"]Gtk|gtk4|gtk-rs|<gtk/gtk\.h>|gtkmm"),
    ("WPF", "native", r"<UseWPF>true|PresentationFramework|xmlns=\"http://schemas\.microsoft\.com/winfx/2006/xaml/presentation\""),
    ("WinForms", "native", r"<UseWindowsForms>true|System\.Windows\.Forms"),
    ("WinUI", "native", r"Microsoft\.WindowsAppSDK|Microsoft\.UI\.Xaml"),
    (".NET MAUI", "native", r"<UseMaui>true|Microsoft\.Maui"),
    ("SwiftUI/AppKit", "native", r"^\s*import (SwiftUI|AppKit|Cocoa)"),
    ("JavaFX", "self-drawn", r"javafx\."),
    ("Swing", "self-drawn", r"javax\.swing"),
    ("React Native", "native", r"react-native-(macos|windows)"),
    ("minifb", "self-drawn", r"\bminifb\b"),
    ("tao + tray-icon", "native", r"\btray-icon\b"),
    ("rumps (macOS menu bar)", "native", r"^\s*import rumps"),
    ("Local web server + browser", "DOM",
     r"http\.server|BaseHTTPRequestHandler|^\s*import webbrowser|^\s*(from|import) flask"),
    ("Web page, no shell", "DOM", r"\.html\n|<!doctype html|<html"),
]

LANG_BY_EXT = {
    ".py": "Python", ".js": "JavaScript", ".mjs": "JavaScript", ".cjs": "JavaScript",
    ".jsx": "JavaScript", ".ts": "TypeScript", ".tsx": "TypeScript", ".rs": "Rust",
    ".cs": "C#", ".dart": "Dart", ".swift": "Swift", ".go": "Go", ".kt": "Kotlin",
    ".java": "Java", ".cpp": "C++", ".cc": "C++", ".cxx": "C++", ".c": "C",
}


def classify(files, text):
    """files: list of {path, content}. Returns (label, family, source, language)."""
    blobs = [f"{f['path']}\n{f.get('content') or ''}" for f in files]
    language = ""
    for f in files:
        ext = "." + f["path"].rsplit(".", 1)[-1].lower() if "." in f["path"] else ""
        if ext in LANG_BY_EXT:
            language = LANG_BY_EXT[ext]
            break
    for label, family, pattern in FILE_RULES:
        rx = re.compile(pattern, re.M | re.I if label == "Web page, no shell" else re.M)
        if any(rx.search(b) for b in blobs):
            return label, family, "files", language
    if files:
        return "Script, no GUI", "none", "files", language
    return "unknown", "", "none", language
