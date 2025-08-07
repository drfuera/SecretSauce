# SecretSauce - Advanced Password Generator & Validator

![SecretScreenshot](https://github.com/drfuera/SecretSauce/raw/main/screenshots/main-window.png)

SecretSauce is a professional-grade password generator and validator with comprehensive security analysis, built with Python and GTK3.

## Features

🔐 **Cryptographically Secure Generation**
- Uses Python's `secrets` module for true randomness
- Ensures all selected character classes are represented
- Configurable length (8-4096 characters) and character sets

📊 **Advanced Security Analysis**
- Powered by zxcvbn algorithm (used by Dropbox)
- Detailed strength scoring (0-4)
- Pattern detection (dictionary words, sequences, repeats)
- Personalized feedback and suggestions

⏱️ **Realistic Crack Time Estimates**
- Multiple attack scenarios (from single CPU to massive GPU arrays)
- Human-readable time estimates (seconds to millennia)
- Scientific notation for extremely large numbers

🖥️ **User-Friendly GUI**
- Clean GTK3 interface
- Password highlighting for easy reading
- Copy to clipboard functionality
- Cross-platform support

## Installation

### Prerequisites
- Python 3.6+
- GTK3 development libraries
- pip or system package manager

### Linux Installation

```bash
# Install dependencies (Ubuntu/Debian example)
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0 python3-zxcvbn

# Clone repository
git clone https://github.com/drfuera/SecretSauce.git
cd SecretSauce

# Run the application
python3 password.py
