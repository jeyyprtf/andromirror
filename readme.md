# AndroMirror by Juan v1.0

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

**AndroMirror** is a modern, cross-platform GUI frontend for [scrcpy](https://github.com/Genymobile/scrcpy) that provides an elegant interface for Android device screen mirroring and control. Built with Python and CustomTkinter, it offers a clean, minimalist design inspired by macOS Sequoia with comprehensive device management features.

## 🚀 Features

### 📱 Device Connection
- **USB Connection**: Automatic detection of USB-connected Android devices
- **Wireless Connection**: TCP/IP connection support with custom IP and port
- **Real-time Device List**: Auto-refresh connected devices with status indicators
- **Connection Management**: Smart connect/disconnect with progress feedback

### 🎥 Video & Audio Settings
- **Resolution Options**: SD (540p), HD (720p), FHD (1080p), 4K
- **Frame Rate Control**: 30fps, 60fps, 120fps options
- **Video Codec**: H264 and H265 support
- **Bitrate Control**: 4M, 8M, 16M, 30M bitrate options
- **Audio Support**: Enable/disable with quality control (Low, Medium, High)

### ⚙️ Advanced Configuration
- **Power Management**: Stay awake and screen-off options
- **Input Methods**: UHID and SDK modes for keyboard/mouse
- **Theme Support**: Light, Dark, and System theme modes
- **Cross-platform**: Native look and feel on Windows, Linux, and macOS

### 🎨 Modern UI/UX
- **Clean Interface**: Minimalist design inspired by macOS Sequoia
- **Responsive Layout**: Adaptive UI that works on different screen sizes
- **Tabbed Interface**: Organized sections for connection, settings, and about
- **Real-time Feedback**: Progress bars and status indicators

## 📋 Prerequisites

Before installing AndroMirror, ensure you have the following installed on your system:

### Required Software
1. **Python 3.8 or higher**
   - Download from [python.org](https://www.python.org/downloads/)
   - Make sure to add Python to your system PATH

2. **Android Debug Bridge (ADB)**
   - Install [Android SDK Platform Tools](https://developer.android.com/studio/releases/platform-tools)
   - Add ADB to your system PATH
   - Verify installation: `adb --version`

3. **scrcpy v3.2 or higher**
   - Download from [scrcpy releases](https://github.com/Genymobile/scrcpy/releases)
   - Add scrcpy to your system PATH
   - Verify installation: `scrcpy --version`

### Android Device Setup
1. Enable **Developer Options** on your Android device
2. Enable **USB Debugging** in Developer Options
3. For wireless connection: Enable **Wireless ADB debugging** (Android 11+)

## 🔧 Installation

### Option 1: Install from Source

1. **Clone the repository**
   ```bash
   git clone https://github.com/jeyyprtf/andromirror.git
   cd andromirror
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

### Option 2: Install via pip (if published)

```bash
pip install andromirror
andromirror
```

## 🏗️ Building Executable

To create a standalone executable that can run without Python installed:

### Using builder build.py

1. **Run build.py**
   ```bash
   python3 build.py
   ```

### Using PyInstaller

1. **Install PyInstaller**
   ```bash
   pip install pyinstaller
   ```

2. **Build executable**
   ```bash
   # For Windows
   pyinstaller --onefile --windowed --name "AndroMirror" main.py
   
   # For Linux/macOS
   pyinstaller --onefile --windowed --name "AndroMirror" main.py
   ```

3. **Find executable**
   - Windows: `dist/AndroMirror.exe`
   - Linux/macOS: `dist/AndroMirror`

### Using Nuitka (Alternative)

1. **Install Nuitka**
   ```bash
   pip install nuitka
   ```

2. **Build executable**
   ```bash
   python -m nuitka --standalone --onefile --enable-plugin=tk-inter --windows-disable-console main.py
   ```

## 📁 Project Structure

```
andromirror/
├── main.py              # Main application file
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── LICENSE             # MIT License
└── assets/             # Application assets (if any)
    └── icons/          # Application icons
```

## 🖥️ Usage

### Basic Usage

1. **Launch the application**
   ```bash
   python main.py
   ```

2. **Connect your Android device**
   - Via USB: Connect device and enable USB debugging
   - Via Wireless: Enter IP address and port in the wireless section

3. **Configure settings**
   - Navigate to the "Settings" tab
   - Adjust video quality, audio settings, and other preferences

4. **Start mirroring**
   - Select your device from the list
   - Click "Connect" to start screen mirroring

### Advanced Features

- **Wireless Connection**: Use the wireless connection tab to connect via TCP/IP
- **Custom Settings**: Fine-tune video quality, input methods, and power settings
- **Theme Switching**: Toggle between Light, Dark, and System themes
- **Multi-device Support**: Connect to multiple devices (one at a time)

### Keyboard Shortcuts

When scrcpy window is active:
- `Ctrl+C`: Copy device clipboard to computer
- `Ctrl+V`: Paste computer clipboard to device
- `Ctrl+Shift+V`: Inject computer clipboard as text events
- `Ctrl+S`: Save screenshot
- `Ctrl+O`: Turn device screen off/on
- `Ctrl+Shift+O`: Turn device screen on
- `Ctrl+R`: Rotate device screen
- `Ctrl+N`: Expand notification panel

## 🐛 Troubleshooting

### Common Issues

1. **"ADB not found" error**
   - Ensure Android SDK Platform Tools are installed
   - Add ADB to your system PATH
   - Restart the application

2. **"scrcpy not found" error**
   - Install scrcpy from official releases
   - Add scrcpy to your system PATH
   - Verify with `scrcpy --version`

3. **Device not detected**
   - Enable USB Debugging on your Android device
   - Check USB cable connection
   - Try different USB ports
   - Refresh device list

4. **Wireless connection fails**
   - Ensure device and computer are on the same network
   - Check if wireless ADB is enabled on the device
   - Try connecting via USB first, then switch to wireless

5. **Application won't start**
   - Check Python version (3.8+ required)
   - Install dependencies: `pip install -r requirements.txt`
   - Check for error messages in terminal

### Performance Issues

- Lower resolution and FPS for better performance
- Reduce video bitrate for slower connections
- Close other applications using the device
- Use USB connection for best performance

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit your changes**
   ```bash
   git commit -m 'Add some amazing feature'
   ```
4. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open a Pull Request**

### Development Setup

1. Clone the repository
2. Install development dependencies
3. Make your changes
4. Test thoroughly on different platforms
5. Submit a pull request

## 📞 Developer Contact

**Juan Madhy**

- 📧 **Email**: [juanmadhy425@gmail.com](mailto:juanmadhy425@gmail.com)
- 📱 **WhatsApp**: [+62 888-0538-5353](https://wa.me/+6288805385353)
- 📷 **Instagram**: [@jeyy_prtf](https://instagram.com/jeyy_prtf)
- 💼 **LinkedIn**: [linkedin.com/in/inijuan](https://www.linkedin.com/in/inijuan/)
- 🎵 **TikTok**: [@jeyy_prtf](https://tiktok.com/@jeyy_prtf)

## 📝 Changelog

### v1.0 (2025-05-31)
- Initial release
- USB and wireless device connection
- Comprehensive video/audio settings
- Modern UI with theme support
- Cross-platform compatibility
- Built-in device management

## 🔗 Related Projects

- [scrcpy](https://github.com/Genymobile/scrcpy) - The underlying screen mirroring tool
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) - Modern UI library for Python

## ⭐ Support

If you find this project helpful, please consider:
- Giving it a star on GitHub
- Sharing it with others
- Contributing to the project
- Reporting bugs or suggesting features

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2025 Juan Madhy

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
```

---

<div align="center">
Made with ❤️ by <a href="https://github.com/jeyyprtf">Juan Madhy</a>
</div>
