# SecretSauce 2.0 🔐

**Advanced Password Generator & Security Validator**

SecretSauce is a professional-grade password generator and security analyzer built with GTK3. It combines cryptographically secure password generation with industry-standard strength analysis using Dropbox's zxcvbn library.

## ✨ Features

### 🔒 **Cryptographically Secure Generation**
- Uses Python's `secrets` module for cryptographic randomness
- Customizable character sets (lowercase, uppercase, digits, symbols)
- Password lengths from 8 to 4096 characters
- Guaranteed character class representation

### 📊 **Professional Security Analysis**
- **zxcvbn integration** - Industry-standard password strength evaluation (0-4 scale)
- **Pattern detection** - Identifies common patterns, dictionary words, and sequences
- **Detailed feedback** - Specific warnings and improvement suggestions
- **Scientific notation** - Clean display of large numbers (guesses, time estimates)

### ⏱️ **Comprehensive Crack Time Estimates**
- **8 attack scenarios** from single CPU to massive GPU arrays
- **Realistic hardware performance** based on modern computing capabilities
- **Intuitive time formatting** with scientific notation in millennia for very large values
- **Range**: seconds to 10^40+ millennia

### 🎨 **Clean User Interface**
- **GTK3-based** native desktop application
- **Visual password highlighting** - Every 8th character highlighted for readability
- **Real-time analysis** - Instant feedback on password strength
- **Professional design** - Clean, intuitive layout

## 🖼️ Screenshots

*Screenshots showing the application interface with password generation, security analysis, and crack time estimates.*

## 🚀 Installation

### Prerequisites

**Ubuntu/Debian:**
```bash
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0
```

**Fedora:**
```bash
sudo dnf install python3-gobject gtk3-devel
```

**Arch Linux:**
```bash
sudo pacman -S python-gobject gtk3
```

### Install SecretSauce

1. **Clone the repository:**
```bash
git clone https://github.com/drfuera/SecretSauce.git
cd SecretSauce
```

2. **Run the application:**
```bash
python3 password.py
```

The application will automatically install the `zxcvbn` dependency if it's not already installed.

## 📖 Usage

### Basic Usage

1. **Select character sets** - Choose which types of characters to include
2. **Set password length** - Use the spinner to select desired length (8-4096)
3. **Generate password** - Click "Generate Password" for a new secure password
4. **Analyze strength** - View real-time security analysis and crack time estimates
5. **Copy password** - Click "Copy Password" to copy to clipboard

### Understanding the Analysis

#### Password Strength (0-4 Scale)
- **0**: Very Weak (red)
- **1**: Weak (orange) 
- **2**: Fair (orange)
- **3**: Good (blue)
- **4**: Strong (green)

#### Crack Time Scenarios
- **Single CPU (Basic)**: 100K guesses/sec
- **Single CPU (Optimized)**: 10M guesses/sec
- **Single GPU (RTX 4090)**: 100B guesses/sec
- **GPU Cluster (10 GPUs)**: 1T guesses/sec
- **GPU Cluster (100 GPUs)**: 10T guesses/sec
- **Massive GPU Array (1K GPUs)**: 100T guesses/sec
- **Massive GPU Array (10K GPUs)**: 1P guesses/sec
- **Massive GPU Array (100K GPUs)**: 10P guesses/sec

#### Time Units
Times progress naturally: seconds → minutes → hours → days → months → years → centuries → millennia

For very large times, scientific notation is used: `2.7 × 10^36 millennia`

## 🔧 Technical Details

### Dependencies
- **Python 3.6+**
- **GTK3** with GObject Introspection
- **zxcvbn** (automatically installed)

### Security Features
- **Cryptographic randomness** using `secrets.SystemRandom`
- **No predictable patterns** in generation
- **Industry-standard analysis** via zxcvbn
- **No data collection** - everything runs locally

### Performance
- **Instant generation** for passwords up to 4096 characters
- **Real-time analysis** with sub-second response times
- **Minimal memory footprint** 
- **Cross-platform compatibility** (Linux, macOS, Windows with GTK3)

## 🛠️ Development

### Project Structure
```
SecretSauce/
├── password.py          # Main application
├── README.md           # This file
└── LICENSE             # CC BY License
```

### Key Classes
- **`PasswordGenerator`** - Cryptographically secure password generation
- **`PasswordAnalyzer`** - zxcvbn integration and crack time calculations  
- **`SecretSauceGUI`** - GTK3 user interface
- **`AboutDialog`** - Application information dialog

## 📋 Requirements

**System Requirements:**
- Linux with GTK3 support
- Python 3.6 or higher
- 50MB disk space
- 64MB RAM

**Tested On:**
- Ubuntu 20.04+ 
- Fedora 35+
- Arch Linux
- Debian 11+

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test on multiple GTK3 environments
5. Submit a pull request

### Coding Standards
- Follow PEP 8 for Python code
- Add comments for complex algorithms
- Maintain GTK3 compatibility
- Test password generation security

## 📄 License

This project is licensed under the **Creative Commons Attribution (CC BY)** license.

You are free to:
- **Share** - Copy and redistribute in any medium or format
- **Adapt** - Remix, transform, and build upon the material
- **Commercial use** - Use for commercial purposes

Under the following terms:
- **Attribution** - You must give appropriate credit to Andrej Fuera

See the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Andrej Fuera**
- GitHub: [@drfuera](https://github.com/drfuera)
- Created with assistance from Claude (Anthropic)

## 🔗 Related Projects

- **[zxcvbn](https://github.com/dropbox/zxcvbn)** - Password strength estimation library by Dropbox
- **[Python Secrets](https://docs.python.org/3/library/secrets.html)** - Cryptographically secure random number generation

## 📚 References

- [NIST SP 800-63B](https://pages.nist.gov/800-63-3/sp800-63b.html) - Digital Identity Guidelines
- [OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
- [Dropbox zxcvbn Paper](https://www.usenix.org/conference/usenixsecurity16/technical-sessions/presentation/wheeler)

---

⭐ **Star this repository if you find SecretSauce useful!**

🔐 **Generate secure passwords. Stay safe online.**
