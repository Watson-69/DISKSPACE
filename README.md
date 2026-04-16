# 💾 PRO DISK ANALYZER

A lightweight, high-performance disk space analyzer for Windows and macOS that provides detailed insights into drive usage and folder sizes with a sleek terminal interface.

![C](https://img.shields.io/badge/C-00599C?style=flat-square&logo=c&logoColor=white)
![Windows](https://img.shields.io/badge/Windows-0078D6?style=flat-square&logo=windows&logoColor=white)
![macOS](https://img.shields.io/badge/macOS-000000?style=flat-square&logo=apple&logoColor=white)
[![License](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](https://github.com/Watson-69/DISKSPACE?tab=MIT-1-ov-file#readme)

## 📋 Table of Contents
- [Features](#-features)
- [Installation](#-installation)
  - [Windows Installation](#windows-installation)
  - [macOS Installation](#macos-installation)
- [Usage](#-usage)
- [Customization](#-customization)
  - [Changing Colors](#changing-colors)
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
- **Customizable Colors** - Easily modify console colors to your preference

## 📸 Example Output

```
==================================================
         WATSON-69'S PRO DISK ANALYZER
==================================================

   [ BOOTING SYSTEM ... ]

Enter Drive or Folder Path: C:\Users\Watson\Documents
View size in (1: MB, 2: GB): 2

[SCANNING] Analyzing files, please wait...
```

```
==================================================
              ANALYSIS COMPLETE :)
==================================================

Target: C:\Users\Watson\Documents
Files Found: 15427

>> CURRENT FOLDER SIZE: 45.32 GB

Drive Usage: [||||||||||||||......] 78.5%

  TOTAL DRIVE SPACE:   476.9 GB
  FREE DRIVE SPACE:    102.3 GB

ADVICE: Everything looks good.

Press Enter twice to exit... (FOR MAC USERS (Press Enter to exit...)
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

#### macOS Compatibility

This project includes a separate macOS-compatible source file. Instead of modifying the Windows version, simply use the provided alternate file.

**Alternate macOS File:** `MAC.c`

The `MAC.c` file contains all necessary modifications for macOS, including:
- ANSI escape codes for colors
- `statvfs()` for disk space queries
- POSIX `opendir()`/`readdir()` for directory scanning
- `usleep()` for animation timing

#### Compilation on macOS

**Using the alternate MAC.c file:**
```bash
gcc -o disk_analyzer MAC.c
```

**Using Clang:**
```bash
clang -o disk_analyzer MAC.c
```

### Quick Start
1. Save the source code:
   - Windows: `disk_analyzer.c`
   - macOS: `MAC.c`
2. Compile using the appropriate command for your OS
3. Run the executable:
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

## 🎨 Customization

### Changing Colors

You can easily customize the colors used throughout the application by modifying the color codes in the source file.

#### Windows Color Codes

Windows uses numeric values (0-15) for colors in `SetConsoleTextAttribute()`:

| Code | Color | Code | Bright Color |
|------|-------|------|--------------|
| 0 | Black | 8 | Gray |
| 1 | Blue | 9 | Bright Blue |
| 2 | Green | 10 | Bright Green |
| 3 | Cyan | 11 | Bright Cyan |
| 4 | Red | 12 | Bright Red |
| 5 | Magenta | 13 | Bright Magenta |
| 6 | Yellow | 14 | Bright Yellow |
| 7 | White | 15 | Bright White |

**Where to change colors in the code:**

```c
// BOOT ANIMATION COLORS
set_color(i % 2 == 0 ? 9 : 15);  // Change 9 and 15 to your preferred colors
// Example: set_color(i % 2 == 0 ? 11 : 13);  // Cyan and Magenta

// INPUT PROMPT COLOR
set_color(7);  // White - change to any color 0-15

// HEADER COLOR
set_color(11);  // Bright Cyan - change to any color 0-15

// FOLDER SIZE COLOR
set_color(14);  // Bright Yellow - change to any color 0-15

// DRIVE BAR COLORS
set_color(12);  // Bright Red (Critical >90%)
set_color(14);  // Bright Yellow (Warning 75-90%)
set_color(10);  // Bright Green (Normal <75%)
set_color(8);   // Gray (Empty space indicator)

// ADVICE COLORS
set_color(12);  // Bright Red (Critical warning)
set_color(14);  // Bright Yellow (Caution)
set_color(10);  // Bright Green (Good status)
```

**Example Windows Color Customization:**
```c
// ORIGINAL
set_color(i % 2 == 0 ? 9 : 15);  // Blue and White alternating

// CUSTOMIZED - Purple and Cyan theme
set_color(i % 2 == 0 ? 13 : 11);  // Magenta and Cyan alternating

// ORIGINAL HEADER
set_color(11);  // Bright Cyan

// CUSTOMIZED HEADER - Golden
set_color(6);   // Yellow (non-bright version)

// ORIGINAL DRIVE BAR
if (percent_used > 90) set_color(12);      // Red
else if (percent_used > 75) set_color(14); // Yellow
else set_color(10);                         // Green

// CUSTOMIZED DRIVE BAR - Purple theme
if (percent_used > 90) set_color(13);      // Magenta
else if (percent_used > 75) set_color(5);  // Dark Magenta
else set_color(3);                          // Cyan
```

#### macOS ANSI Color Codes (for MAC.c)

The `MAC.c` file uses ANSI escape codes for colors:

| Code | Color | Code | Bright Color |
|------|-------|------|--------------|
| \033[30m | Black | \033[90m | Bright Black |
| \033[31m | Red | \033[91m | Bright Red |
| \033[32m | Green | \033[92m | Bright Green |
| \033[33m | Yellow | \033[93m | Bright Yellow |
| \033[34m | Blue | \033[94m | Bright Blue |
| \033[35m | Magenta | \033[95m | Bright Magenta |
| \033[36m | Cyan | \033[96m | Bright Cyan |
| \033[37m | White | \033[97m | Bright White |
| \033[0m | Reset | | |

**Example ANSI Color Implementation in MAC.c:**
```c
void set_color(const char* color_code) {
    printf("%s", color_code);
}

// Usage examples:
set_color("\033[34m");  // Blue text
set_color("\033[91m");  // Bright Red text
set_color("\033[0m");   // Reset to default

// For animated boot sequence:
set_color(i % 2 == 0 ? "\033[94m" : "\033[97m");  // Bright Blue / Bright White

// For drive bar:
if (percent_used > 90) set_color("\033[91m");      // Bright Red
else if (percent_used > 75) set_color("\033[93m"); // Bright Yellow
else set_color("\033[92m");                        // Bright Green
```

### Color Scheme Examples

#### 🟢 Matrix Theme (Green/Black)
```c
set_color(i % 2 == 0 ? 10 : 2);  // Bright Green / Dark Green alternating
set_color(10);                    // Headers in Bright Green
set_color(10);                    // Folder size in Bright Green
// Drive Bar:
if (percent_used > 90) set_color(10);      // Bright Green
else if (percent_used > 75) set_color(2);  // Dark Green
else set_color(10);                         // Bright Green
```

#### 🔴 Neon Theme (Red/Yellow)
```c
set_color(i % 2 == 0 ? 12 : 14);  // Bright Red / Bright Yellow alternating
set_color(14);                     // Headers in Bright Yellow
set_color(12);                     // Folder size in Bright Red
// Drive Bar:
if (percent_used > 90) set_color(12);      // Bright Red
else if (percent_used > 75) set_color(6);  // Dark Yellow
else set_color(14);                         // Bright Yellow
```

#### 🔵 Ocean Theme (Blue/Cyan)
```c
set_color(i % 2 == 0 ? 9 : 11);  // Bright Blue / Bright Cyan alternating
set_color(11);                    // Headers in Bright Cyan
set_color(9);                     // Folder size in Bright Blue
// Drive Bar:
if (percent_used > 90) set_color(1);       // Dark Blue
else if (percent_used > 75) set_color(9);  // Bright Blue
else set_color(11);                         // Bright Cyan
```

#### 🟣 Sunset Theme (Purple/Magenta)
```c
set_color(i % 2 == 0 ? 13 : 12);  // Bright Magenta / Bright Red alternating
set_color(13);                     // Headers in Bright Magenta
set_color(5);                      // Folder size in Dark Magenta
// Drive Bar:
if (percent_used > 90) set_color(13);      // Bright Magenta
else if (percent_used > 75) set_color(12); // Bright Red
else set_color(5);                          // Dark Magenta
```

## 🔬 Technical Details

### Core Components

| Component | Windows | macOS |
|-----------|---------|-------|
| Directory Scanning | FindFirstFile/FindNextFile API | opendir/readdir POSIX |
| Color Output | SetConsoleTextAttribute | ANSI Escape Codes |
| Disk Space Query | GetDiskFreeSpaceEx | statvfs |
| Size Calculation | 64-bit integers | 64-bit integers |
| Sleep Function | Sleep (milliseconds) | usleep (microseconds) |

### Default Color Coding System

| Color | Meaning |
|-------|---------|
| 🟢 Green (10) | Normal usage (< 75%) |
| 🟡 Yellow (14) | Warning level (75-90%) |
| 🔴 Red (12) | Critical level (> 90%) |
| 🔵 Cyan (11) | Information headers |
| ⚪ White (7) | Standard text |
| 🔵 Blue/White (9/15) | Boot animation |

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

**macOS Note:** In `MAC.c`, the equivalent is `usleep()` with values multiplied by 1000 (e.g., `usleep(15000)`).

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
- Some system directories may require sudo privileges
- Terminal must support ANSI escape codes (most modern terminals do)

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
- [ ] Linux support
- [ ] Export results to CSV/JSON
- [ ] Multi-threaded scanning for faster analysis
- [ ] File type categorization
- [ ] Largest files identification
- [ ] GUI version
- [ ] Color theme presets

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
