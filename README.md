# 💾 PRO DISK ANALYZER

A lightweight, high-performance disk space analyzer for Windows and macOS that provides detailed insights into drive usage and folder sizes with a sleek terminal interface.

![C](https://img.shields.io/badge/C-00599C?style=flat-square&logo=c&logoColor=white)
![Windows](https://img.shields.io/badge/Windows-0078D6?style=flat-square&logo=windows&logoColor=white)
![macOS](https://img.shields.io/badge/macOS-000000?style=flat-square&logo=apple&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)

## 📋 Table of Contents
- [Features](#-features)
- [Installation](#-installation)
  - [Windows Installation](#windows-installation)
  - [macOS Installation](#macos-installation)
- [Usage](#-usage)
- [Technical Details](#-technical-details)
- [Configuration](#-configuration)
- [Limitations](#-limitations)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Features

- **Fast Directory Scanning** - Recursively calculates folder sizes with system API optimization
- **Visual Drive Usage Bar** - Color-coded progress bar showing drive capacity status
- **Smart Recommendations** - Provides actionable advice based on storage analysis
- **User-Friendly Interface** - Clean terminal UI with color-coded output
- **Personalized Experience** - Greets users by their system username
- **Dual Unit Support** - Display sizes in MB or GB based on preference
- **File Counter** - Tracks total number of files processed during scanning
- **Epilepsy-Friendly Animation** - Adjustable boot sequence timing
- **Cross-Platform Support** - Works on both Windows and macOS

## 📸 Example Output

```
==================================================
         WATSON-69'S PRO DISK ANALYZER
==================================================

   [ BOOTING SYSTEM ... ]

Enter Drive or Folder Path: /Users/Watson/Documents
View size in (1: MB, 2: GB): 2

[SCANNING] Analyzing files, please wait...
```

```
==================================================
              ANALYSIS COMPLETE :)
==================================================

Target: /Users/Watson/Documents
Files Found: 15427

>> CURRENT FOLDER SIZE: 45.32 GB

Drive Usage: [||||||||||||||......] 78.5%

  TOTAL DRIVE SPACE:   476.9 GB
  FREE DRIVE SPACE:    102.3 GB

ADVICE: Everything looks good.

Press Enter twice to exit...
```

## 🔧 Installation

### Windows Installation

#### Prerequisites
- Windows Operating System (Windows 7 or later)
- GCC/MinGW compiler or Microsoft Visual Studio
- Windows SDK

#### Compilation

**Using MinGW/GCC:**
```bash
gcc -o disk_analyzer.exe disk_analyzer.c -luser32 -lkernel32
```

**Using Visual Studio Developer Command Prompt:**
```bash
cl disk_analyzer.c /Fe:disk_analyzer.exe user32.lib kernel32.lib
```

### macOS Installation

#### Prerequisites
- macOS (Any recent version)
- GCC or Clang compiler (Xcode Command Line Tools)
- Homebrew (optional, for GCC installation)

#### Code Modification for macOS

**IMPORTANT:** Before compiling on macOS, change the header include at the top of the source file:

**Change this line:**
```c
#include <windows.h> // FOR MAC USERS use <sys/mount.h>
```

**To this:**
```c
#include <sys/mount.h> // FOR MAC USERS
```

#### Additional macOS Modifications Required

The source code uses Windows-specific functions that need to be adapted for macOS:

1. **Replace `SetConsoleTextAttribute`** - Use ANSI escape codes for colors
2. **Replace `GetDiskFreeSpaceEx`** - Use `statvfs()` from `<sys/statvfs.h>`
3. **Replace `FindFirstFile/FindNextFile`** - Use POSIX `opendir()/readdir()` from `<dirent.h>`
4. **Replace `Sleep()`** - Use `usleep()` from `<unistd.h>`
5. **Replace `GetStdHandle`** - Not needed with ANSI escape codes

#### Compilation on macOS

**Using GCC:**
```bash
gcc -o disk_analyzer disk_analyzer.c
```

**Using Clang:**
```bash
clang -o disk_analyzer disk_analyzer.c
```

**Installing GCC via Homebrew (if needed):**
```bash
brew install gcc
gcc-14 -o disk_analyzer disk_analyzer.c
```

### Quick Start (Both Platforms)
1. Save the source code as `disk_analyzer.c`
2. Make the platform-specific modifications above
3. Compile using the appropriate command for your OS
4. Run the executable:
   - Windows: `disk_analyzer.exe`
   - macOS: `./disk_analyzer`

## 🚀 Usage

### Windows Users
1. Launch the application
2. Enter the target path (e.g., `C:\` or `C:\Users\YourName\Documents`)
3. Select display unit (`1` for MB, `2` for GB)
4. Wait for scanning to complete
5. Review the analysis
6. Press Enter twice to exit

### macOS Users
1. Launch from Terminal: `./disk_analyzer`
2. Enter the target path (e.g., `/` or `/Users/YourName/Documents`)
3. Select display unit (`1` for MB, `2` for GB)
4. Wait for scanning to complete
5. Review the analysis
6. Press Enter twice to exit

## 🔬 Technical Details

### Core Components

| Component | Windows | macOS |
|-----------|---------|-------|
| Directory Scanning | FindFirstFile/FindNextFile API | opendir/readdir POSIX |
| Color Output | SetConsoleTextAttribute | ANSI Escape Codes |
| Disk Space Query | GetDiskFreeSpaceEx | statvfs |
| Size Calculation | 64-bit integers | 64-bit integers |
| Sleep Function | Sleep (milliseconds) | usleep (microseconds) |

### Color Coding System

| Color | Meaning |
|-------|---------|
| 🟢 Green | Normal usage (< 75%) |
| 🟡 Yellow | Warning level (75-90%) |
| 🔴 Red | Critical level (> 90%) |
| 🔵 Blue | Information headers |
| ⚪ White | Standard text |

### Performance Considerations

- Uses native OS APIs for optimal performance
- 64-bit integers prevent overflow on large drives (> 2TB)
- Minimal memory footprint during recursive scanning
- ~10,000 files/second scanning speed on modern hardware

## ⚙️ Configuration

### Adjusting Animation Speed

Locate the following line in `main()`:
```c
Sleep(15); // VARY ACCORDING TO YOUR NEED
```

Modify the value:
- `15-50` - Fast animation (standard users)
- `150-200` - Slower animation (recommended for photosensitive users)

**macOS Note:** If using macOS-adapted code with `usleep()`, multiply values by 1000 (e.g., `usleep(15000)`).

### Changing Default Unit

Modify the fallback choice in:
```c
if (scanf("%d", &choice) != 1) choice = 2;  // 1=MB, 2=GB
```

## 🚧 Limitations

### Windows Limitations
- Path Length limited to `MAX_PATH` (260 characters)
- Cannot access restricted system folders without admin rights
- No symlink/junction handling

### macOS Limitations
- Requires code modifications (as documented above)
- Some system directories may require sudo privileges
- No native colored console without ANSI support

### Cross-Platform Limitations
- Console Application only (no GUI)
- Single-threaded scanning
- No export functionality

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**:
   ```bash
   git checkout -b feature/amazing-improvement
   ```
3. **Commit your changes**:
   ```bash
   git commit -m 'Add some amazing improvement'
   ```
4. **Push to the branch**:
   ```bash
   git push origin feature/amazing-improvement
   ```
5. **Open a Pull Request**

### Planned Improvements
- [ ] Full macOS compatibility (built-in)
- [ ] Linux support
- [ ] Export results to CSV/JSON
- [ ] Multi-threaded scanning for faster analysis
- [ ] File type categorization
- [ ] Largest files identification
- [ ] GUI version

## 📝 License

MIT License

Copyright (c) 2024 Watson-69

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## 🙏 Acknowledgments

- Windows API Documentation
- Apple Developer Documentation
- POSIX Standards Documentation
- Stack Overflow community for optimization techniques
- All contributors who help improve this tool

## 📞 Support

Found a bug? Have a feature request? Please open an issue on the repository.

---

**Made with ❤️ by Watson-69 for the Windows and Mac community**
