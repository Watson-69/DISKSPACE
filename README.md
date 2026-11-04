<div align="center">

# 📊 DriveMetric

**Native-speed storage insight • Zero dependencies • Consumer-friendly**

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/UI-CustomTkinter-00599C?style=for-the-badge)
![Engine](https://img.shields.io/badge/Engine-Pure%20C-00599C?style=for-the-badge&logo=c&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS-lightgrey?style=for-the-badge)

DriveMetric is an eye-friendly desktop storage analyzer combining raw C filesystem traversal speed with a modern Dark Slate GUI.

</div>

---

## 📁 Repository File Structure

```text
DISKSPACEPROJECT/
├── drive_metric.py       # Primary Python GUI (Tkinter) — animated storage tree, themes, table
├── WINDOWS.c             # C source for Windows (FindFirstFile / GetDiskFreeSpaceEx)
├── MAC.c                 # C source for macOS (opendir / statfs)
├── WINDOWS.exe           # Precompiled Windows binary
├── SOURCECODE.exe        # Precompiled binary bundle
├── main7.exe             # Precompiled binary
├── README.md             # Project documentation
└── LICENSE               # MIT License
```

---

## 🎯 Key Features

- **🌳 Animated Storage Tree:** Visualizes drive breakdown (*Total Drive → Used vs Free → Subfolder Distribution*) with smooth node rendering.
- **📊 Multi-View Top Items:** Dynamically switch between **Top Files**, **Top Directories**, or **Combined** views.
- **📁 File Explorer Integration:** Double-click or right-click any scanned item to open its parent folder directly in File Explorer / Finder.
- **🎨 Refined Dark Slate UI:** High-contrast palette (`#0F172A`, `#1E293B`) optimized for zero visual glitches or eye strain.

---

## 🚀 Quick Start

```bash
# Clone repository
git clone https://github.com/your-username/drive-metric.git
cd drive-metric

# Run the GUI (Python 3.9+)
python drive_metric.py
```

### Compile the C engine (optional)

**Windows (MinGW/GCC):**
```bash
gcc -o DriveMetric.exe WINDOWS.c -luser32 -lkernel32
```

**Windows (MSVC):**
```bash
cl WINDOWS.c /Fe:DriveMetric.exe user32.lib kernel32.lib
```

**macOS:**
```bash
clang -o DriveMetric MAC.c
```

---

## 🧭 Usage

1. Launch the application (`python drive_metric.py`).
2. Enter a target path (e.g. `C:\`, `/Users/you/Documents`).
3. Choose a unit (`MB` or `GB`).
4. Pick a theme from the sidebar dropdown.
5. Press **Scan Now** and review the animated storage tree, top folders, file types, and top items table.
6. Double-click or right-click any row in the Top Items table to open its parent folder in File Explorer.

---

## 🏗 Architecture

- **GUI:** Python + Tkinter (CustomTkinter-compatible styling, no heavy dependencies).
- **Scanning Engine:** Native filesystem traversal (`os.walk`) with 64-bit size accumulation; optional raw C engine (`WINDOWS.c` / `MAC.c`).
- **Visualization:** Canvas-based animated tree, horizontal bar breakdowns, and type distribution bars.
- **Theming:** Centralized theme dictionary with runtime switching.

---

## 🎨 Customization

Colors, node colors, bar thresholds, and animation timing are centralized in `drive_metric.py`. Adjust the `THEMES` dictionary and tree node parameters to taste.

---

## 🚧 Limitations

- GUI application only (no web interface).
- Single-threaded scanning (multi-threaded scanning planned).
- Windows File Explorer integration is Windows-first; macOS/Linux use native open commands.

---

## 🤝 Contributing

Contributions are welcome. Fork the repo, create a feature branch, commit your changes, and open a Pull Request.

---

## 📄 License

Released under the [MIT License](./LICENSE).

---

<div align="center">

**Made with ❤️ by the DriveMetric community**

</div>
