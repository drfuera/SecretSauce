#!/usr/bin/env python3
"""
SecretSauce - Advanced Password Generator and Validator
Features comprehensive password analysis using zxcvbn and secure generation
"""

import sys
import subprocess
import importlib
import os

def check_and_install_requirements():
    """Check for required packages and install them if missing"""
    # Check GTK3 availability
    try:
        import gi
        gi.require_version('Gtk', '3.0')
        gi.require_version('Pango', '1.0')
        from gi.repository import Gtk, Pango, Gdk, GLib
    except (ImportError, ValueError) as e:
        print(f"GTK3 not available: {e}")
        print("Please install GTK3 development libraries:")
        print("Ubuntu/Debian: sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0")
        print("Fedora: sudo dnf install python3-gobject gtk3-devel")
        print("Arch: sudo pacman -S python-gobject gtk3")
        sys.exit(1)
    
    # Check zxcvbn
    try:
        import zxcvbn
        print("All requirements satisfied!")
        return
    except ImportError:
        pass
    
    print("zxcvbn not found. Attempting to install...")
    
    # Try different installation methods in order of preference
    install_methods = [
        # Method 1: Try system package manager (most reliable)
        {
            'name': 'system package manager',
            'commands': [
                ['apt', 'install', '-y', 'python3-zxcvbn'],  # Debian/Ubuntu
                ['dnf', 'install', '-y', 'python3-zxcvbn'],  # Fedora
                ['pacman', '-S', '--noconfirm', 'python-zxcvbn'],  # Arch
            ]
        },
        # Method 2: Try pipx (recommended for applications)
        {
            'name': 'pipx',
            'commands': [
                ['pipx', 'install', 'zxcvbn']
            ]
        },
        # Method 3: Try pip with user flag
        {
            'name': 'pip --user',
            'commands': [
                [sys.executable, '-m', 'pip', 'install', '--user', 'zxcvbn']
            ]
        }
    ]
    
    for method in install_methods:
        for cmd in method['commands']:
            try:
                print(f"Trying {method['name']}: {' '.join(cmd)}")
                subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                
                # Test if installation worked
                try:
                    import zxcvbn
                    print(f"zxcvbn installed successfully via {method['name']}!")
                    return
                except ImportError:
                    continue
                    
            except (subprocess.CalledProcessError, FileNotFoundError):
                continue
    
    # If all methods failed, provide clear instructions
    print("\n" + "="*60)
    print("❌ INSTALLATION FAILED")
    print("="*60)
    print("SecretSauce requires the 'zxcvbn' package, but automatic installation failed.")
    print("Please install it manually using ONE of these methods:")
    print()
    print("🔸 METHOD 1 - System Package Manager (Recommended):")
    print("   Ubuntu/Debian: sudo apt install python3-zxcvbn")
    print("   Fedora:        sudo dnf install python3-zxcvbn") 
    print("   Arch:          sudo pacman -S python-zxcvbn")
    print()
    print("🔸 METHOD 2 - Virtual Environment:")
    print("   python3 -m venv secretsauce-env")
    print("   source secretsauce-env/bin/activate")
    print("   pip install zxcvbn")
    print("   python password.py")
    print()
    print("🔸 METHOD 3 - pipx (if available):")
    print("   pipx install zxcvbn")
    print()
    print("🔸 METHOD 4 - User install:")
    print("   python3 -m pip install --user zxcvbn")
    print()
    print("🔸 METHOD 5 - Override system protection (NOT recommended):")
    print("   python3 -m pip install --break-system-packages zxcvbn")
    print()
    print("After installation, run: python3 password.py")
    print("="*60)
    sys.exit(1)

# Check requirements before proceeding
check_and_install_requirements()

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Pango', '1.0')
from gi.repository import Gtk, Pango, Gdk, GLib
import secrets
import string
import math
import time
from pathlib import Path
import webbrowser
from zxcvbn import zxcvbn

class AboutDialog(Gtk.Dialog):
    """About dialog for SecretSauce"""
    
    def __init__(self, parent):
        super().__init__(title="About SecretSauce", parent=parent, modal=True)
        self.set_default_size(500, 400)
        self.set_resizable(False)
        
        # Add close button
        self.add_button("Close", Gtk.ResponseType.CLOSE)
        
        # Main content area
        content_area = self.get_content_area()
        content_area.set_border_width(20)
        
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        content_area.add(main_box)
        
        # Title section
        header_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=15)
        header_box.set_halign(Gtk.Align.CENTER)
        
        # Application title
        title_label = Gtk.Label()
        title_label.set_markup("<span size='x-large' weight='bold'>SecretSauce</span>")
        header_box.pack_start(title_label, False, False, 0)
        main_box.pack_start(header_box, False, False, 0)
        
        # Description
        desc_label = Gtk.Label()
        desc_label.set_markup(
            "<span size='medium'>Advanced Password Generator &amp; Security Validator</span>\n\n"
            "Generate ultra-secure passwords with comprehensive security analysis.\n"
            "Powered by zxcvbn for professional-grade password strength evaluation\n"
            "and cryptographically secure generation using Python's secrets module."
        )
        desc_label.set_line_wrap(True)
        desc_label.set_justify(Gtk.Justification.CENTER)
        main_box.pack_start(desc_label, False, False, 0)
        
        # Separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        main_box.pack_start(separator, False, False, 0)
        
        # Info grid
        grid = Gtk.Grid()
        grid.set_column_spacing(10)
        grid.set_row_spacing(8)
        grid.set_halign(Gtk.Align.CENTER)
        
        # Version
        self._add_grid_row(grid, 0, "Version:", "2.0")
        
        # Author
        self._add_grid_row(grid, 1, "Author:", "Andrej Fuera - Created with Claude")
        
        # Features
        features_label = Gtk.Label()
        features_label.set_markup("<small>zxcvbn Password Analysis\nCryptographically Secure Generation\nCrack Time Estimation</small>")
        features_label.set_justify(Gtk.Justification.LEFT)
        self._add_grid_custom_widget(grid, 2, "Features:", features_label)
        
        # GitHub link
        github_label = Gtk.Label()
        github_label.set_markup("<a href='https://github.com/drfuera/SecretSauce'>https://github.com/drfuera/SecretSauce</a>")
        github_label.connect("activate-link", self._on_github_clicked)
        self._add_grid_custom_widget(grid, 3, "GitHub:", github_label)
        
        main_box.pack_start(grid, False, False, 0)
        
        # License
        license_label = Gtk.Label()
        license_label.set_markup(
            "<span size='small'>© 2024 Andrej Fuera - Licensed under CC BY (Creative Commons Attribution)</span>"
        )
        license_label.set_margin_top(15)
        main_box.pack_start(license_label, False, False, 0)
        
        self.show_all()
    
    def _add_grid_row(self, grid, row, label_text, value_text):
        label = Gtk.Label(label=label_text)
        label.set_halign(Gtk.Align.END)
        label.set_markup(f"<b>{label_text}</b>")
        grid.attach(label, 0, row, 1, 1)
        
        value_label = Gtk.Label(label=value_text)
        value_label.set_halign(Gtk.Align.START)
        value_label.set_xalign(0)
        grid.attach(value_label, 1, row, 1, 1)
        return value_label
    
    def _add_grid_custom_widget(self, grid, row, label_text, widget):
        label = Gtk.Label()
        label.set_markup(f"<b>{label_text}</b>")
        label.set_halign(Gtk.Align.END)
        label.set_valign(Gtk.Align.START)
        grid.attach(label, 0, row, 1, 1)
        
        widget.set_halign(Gtk.Align.START)
        widget.set_xalign(0)
        grid.attach(widget, 1, row, 1, 1)
        return widget
    
    def _on_github_clicked(self, label, uri):
        webbrowser.open(uri)
        return True


class PasswordGenerator:
    """Cryptographically secure password generator"""
    
    def __init__(self):
        self.lowercase = string.ascii_lowercase
        self.uppercase = string.ascii_uppercase
        self.digits = string.digits
        self.symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
    def generate(self, length=64, use_lower=True, use_upper=True, use_digits=True, use_symbols=True):
        """Generate cryptographically secure password"""
        charset = ""
        if use_lower:
            charset += self.lowercase
        if use_upper:
            charset += self.uppercase
        if use_digits:
            charset += self.digits
        if use_symbols:
            charset += self.symbols
        
        if not charset:
            return "Error: No character sets selected"
        
        # Use secrets for cryptographically secure generation
        password = ''.join(secrets.choice(charset) for _ in range(length))
        
        # Ensure all selected character classes are represented
        classes_needed = []
        if use_lower and not any(c in self.lowercase for c in password):
            classes_needed.append(self.lowercase)
        if use_upper and not any(c in self.uppercase for c in password):
            classes_needed.append(self.uppercase)
        if use_digits and not any(c in self.digits for c in password):
            classes_needed.append(self.digits)
        if use_symbols and not any(c in self.symbols for c in password):
            classes_needed.append(self.symbols)
        
        # If any classes are missing, replace random characters
        if classes_needed:
            password_list = list(password)
            for char_class in classes_needed:
                if len(password_list) > 0:
                    # Replace a random position with a character from the missing class
                    pos = secrets.randbelow(len(password_list))
                    password_list[pos] = secrets.choice(char_class)
            password = ''.join(password_list)
        
        return password


class PasswordAnalyzer:
    """Password analyzer using zxcvbn"""
    
    def __init__(self):
        pass
    
    def analyze_password(self, password):
        """Analyze password using zxcvbn"""
        if not password:
            return {
                'score': 0,
                'guesses': 0,
                'crack_times_seconds': {},
                'feedback': {'warning': 'No password provided', 'suggestions': []},
                'sequence': []
            }
        
        result = zxcvbn(password)
        return result
    
    def get_crack_time_estimates(self, analysis):
        """Get crack time estimates for different scenarios"""
        base_guesses = analysis.get('guesses', 0)
        if base_guesses == 0:
            return {}
        
        # Convert to float if it's a Decimal object
        try:
            base_guesses = float(base_guesses)
        except (TypeError, ValueError):
            base_guesses = 0
        
        if base_guesses == 0:
            return {}
        
        # More realistic attack scenarios (guesses per second) for modern hardware
        scenarios = {
            'Single CPU (Basic)': 1e5,           # 100K guesses/sec
            'Single CPU (Optimized)': 1e7,       # 10M guesses/sec  
            'Single GPU (RTX 4090)': 1e11,       # 100B guesses/sec
            'GPU Cluster (10 GPUs)': 1e12,       # 1T guesses/sec
            'GPU Cluster (100 GPUs)': 1e13,      # 10T guesses/sec
            'Massive GPU Array (1K GPUs)': 1e14, # 100T guesses/sec
            'Massive GPU Array (10K GPUs)': 1e15, # 1P guesses/sec
            'Massive GPU Array (100K GPUs)': 1e16, # 10P guesses/sec
        }
        
        estimates = {}
        for scenario, guesses_per_sec in scenarios.items():
            seconds = base_guesses / (2 * guesses_per_sec)  # Average case
            estimates[scenario] = self._format_time(seconds)
        
        return estimates
    
    def _format_time(self, seconds):
        """Format time in human readable format with millennia as the maximum unit"""
        if seconds < 1:
            return "< 1 second"
        elif seconds < 60:
            return f"{seconds:.1f} seconds"
        elif seconds < 3600:
            minutes = seconds / 60
            return f"{minutes:.1f} minutes"
        elif seconds < 86400:
            hours = seconds / 3600
            return f"{hours:.1f} hours"
        elif seconds < 2629746:  # 1 month
            days = seconds / 86400
            return f"{days:.1f} days"
        elif seconds < 31556952:  # 1 year
            months = seconds / 2629746
            return f"{months:.1f} months"
        elif seconds < 3155695200:  # 100 years
            years = seconds / 31556952
            return f"{years:.1f} years"
        elif seconds < 31556952000:  # 1000 years  
            centuries = seconds / 3155695200
            return f"{centuries:.1f} centuries"
        else:
            # Everything beyond 1000 years uses millennia as the unit
            millennia = seconds / 31556952000
            
            if millennia < 1000:
                # Simple millennia count for reasonable numbers
                return f"{millennia:.1f} millennia"
            else:
                # Scientific notation in millennia for very large numbers
                try:
                    exponent = int(math.log10(millennia))
                    mantissa = millennia / (10 ** exponent)
                    return f"{mantissa:.1f} × 10^{exponent} millennia"
                except (ValueError, OverflowError):
                    return "∞ millennia"


class SecretSauceGUI:
    """Main GTK3 GUI application for SecretSauce"""
    
    def __init__(self):
        self.generator = PasswordGenerator()
        self.analyzer = PasswordAnalyzer()
        self.current_password = ""
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the GTK3 user interface"""
        # Main window
        self.window = Gtk.Window()
        self.window.set_title("SecretSauce - Password Generator & Validator")
        self.window.set_default_size(600, 650)
        self.window.connect("destroy", Gtk.main_quit)
        
        # Main container
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        main_box.set_margin_start(20)
        main_box.set_margin_end(20)
        main_box.set_margin_top(20)
        main_box.set_margin_bottom(20)
        
        # Title with about button
        title_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        
        title = Gtk.Label()
        title.set_markup("<b><big>SecretSauce 2.0</big></b> - Advanced Password Security")
        title.set_halign(Gtk.Align.START)
        
        about_button = Gtk.Button(label="About")
        about_button.connect("clicked", self.on_about_clicked)
        about_button.set_halign(Gtk.Align.END)
        
        title_box.pack_start(title, True, True, 0)
        title_box.pack_start(about_button, False, False, 0)
        main_box.pack_start(title_box, False, False, 0)
        
        # Password generation options
        options_frame = Gtk.Frame(label="Password Generation Options")
        options_main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
        options_main_box.set_margin_start(15)
        options_main_box.set_margin_end(15)
        options_main_box.set_margin_top(15)
        options_main_box.set_margin_bottom(15)
        
        # Character sets section
        charset_section = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        charset_label = Gtk.Label()
        charset_label.set_markup("<b>Character Sets:</b>")
        charset_label.set_xalign(0)
        charset_section.pack_start(charset_label, False, False, 0)
        
        charset_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=15)
        
        self.lowercase_check = Gtk.CheckButton(label="a-z")
        self.lowercase_check.set_active(True)
        self.uppercase_check = Gtk.CheckButton(label="A-Z")
        self.uppercase_check.set_active(True)
        self.digits_check = Gtk.CheckButton(label="0-9")
        self.digits_check.set_active(True)
        self.symbols_check = Gtk.CheckButton(label="Symbols")
        self.symbols_check.set_active(True)
        
        charset_box.pack_start(self.lowercase_check, False, False, 0)
        charset_box.pack_start(self.uppercase_check, False, False, 0)
        charset_box.pack_start(self.digits_check, False, False, 0)
        charset_box.pack_start(self.symbols_check, False, False, 0)
        
        charset_section.pack_start(charset_box, False, False, 0)
        
        # Length setting section
        length_section = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        length_label = Gtk.Label()
        length_label.set_markup("<b>Password Length:</b>")
        length_label.set_xalign(0)
        length_section.pack_start(length_label, False, False, 0)
        
        length_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.length_spinbutton = Gtk.SpinButton()
        self.length_spinbutton.set_range(8, 4096)
        self.length_spinbutton.set_value(64)
        self.length_spinbutton.set_increments(1, 8)
        length_box.pack_start(self.length_spinbutton, False, False, 0)
        
        length_section.pack_start(length_box, False, False, 0)
        
        # Pack sections side by side
        options_main_box.pack_start(charset_section, True, True, 0)
        options_main_box.pack_start(length_section, False, False, 0)
        
        options_frame.add(options_main_box)
        main_box.pack_start(options_frame, False, False, 0)
        
        # Generate and Copy buttons (removed scan button)
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10, homogeneous=True)
        
        self.generate_button = Gtk.Button(label="Generate Password")
        self.generate_button.connect("clicked", self.on_generate_clicked)
        
        self.copy_button = Gtk.Button(label="Copy Password")
        self.copy_button.connect("clicked", self.on_copy_clicked)
        self.copy_button.set_sensitive(False)
        
        button_box.pack_start(self.generate_button, True, True, 0)
        button_box.pack_start(self.copy_button, True, True, 0)
        
        main_box.pack_start(button_box, False, False, 0)
        
        # Password display
        password_frame = Gtk.Frame(label="Generated Password")
        password_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        password_container.set_margin_start(10)
        password_container.set_margin_end(10)
        password_container.set_margin_top(10)
        password_container.set_margin_bottom(10)
        
        self.password_textview = Gtk.TextView()
        self.password_textview.set_editable(False)
        self.password_textview.set_wrap_mode(Gtk.WrapMode.CHAR)
        self.password_textview.set_cursor_visible(False)
        self.password_textview.set_justification(Gtk.Justification.CENTER)
        
        # Minimal styling - transparent background, good font, auto height
        style_context = self.password_textview.get_style_context()
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(b"""
        textview {
            font-family: 'Courier New', 'DejaVu Sans Mono', monospace;
            font-size: 14px;
            font-weight: bold;
            padding: 8px;
            background-color: transparent;
        }
        textview text {
            background-color: transparent;
        }
        """)
        style_context.add_provider(css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        
        # Set up text buffer for highlighting
        self.password_buffer = self.password_textview.get_buffer()
        self.highlight_tag = self.password_buffer.create_tag("highlight")
        self.highlight_tag.set_property("foreground", "#dc3545")  # Red text color
        self.highlight_tag.set_property("weight", Pango.Weight.BOLD)
        
        password_container.pack_start(self.password_textview, False, False, 0)
        
        password_frame.add(password_container)
        main_box.pack_start(password_frame, False, False, 0)
        
        # Security Analysis
        analysis_frame = Gtk.Frame(label="Security Analysis (zxcvbn)")
        analysis_scroll = Gtk.ScrolledWindow()
        analysis_scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        analysis_scroll.set_min_content_height(200)
        
        self.analysis_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.analysis_box.set_margin_start(15)
        self.analysis_box.set_margin_end(15)
        self.analysis_box.set_margin_top(15)
        self.analysis_box.set_margin_bottom(15)
        
        analysis_scroll.add(self.analysis_box)
        analysis_frame.add(analysis_scroll)
        main_box.pack_start(analysis_frame, True, True, 0)
        
        # Crack Time Estimates
        crack_time_frame = Gtk.Frame(label="Crack Time Estimates")
        crack_time_scroll = Gtk.ScrolledWindow()
        crack_time_scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        crack_time_scroll.set_min_content_height(200)
        
        self.crack_time_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.crack_time_box.set_margin_start(15)
        self.crack_time_box.set_margin_end(15)
        self.crack_time_box.set_margin_top(15)
        self.crack_time_box.set_margin_bottom(15)
        
        crack_time_scroll.add(self.crack_time_box)
        crack_time_frame.add(crack_time_scroll)
        main_box.pack_start(crack_time_frame, True, True, 0)
        
        self.window.add(main_box)
        self.window.show_all()
        
        # Auto-generate a password when the application starts
        self.on_generate_clicked(None)
    
    def on_about_clicked(self, button):
        """Show about dialog"""
        about_dialog = AboutDialog(self.window)
        about_dialog.run()
        about_dialog.destroy()
    
    def on_generate_clicked(self, button):
        """Handle generate button click"""
        length = int(self.length_spinbutton.get_value())
        use_lower = self.lowercase_check.get_active()
        use_upper = self.uppercase_check.get_active()
        use_digits = self.digits_check.get_active()
        use_symbols = self.symbols_check.get_active()
        
        self.current_password = self.generator.generate(
            length, use_lower, use_upper, use_digits, use_symbols
        )
        
        self.display_password()
        self.analyze_password()
        self.copy_button.set_sensitive(True)
    
    def display_password(self):
        """Display password with highlighting every 8th character"""
        self.password_buffer.set_text("")
        
        if not self.current_password:
            return
        
        # Insert text with highlighting
        for i, char in enumerate(self.current_password):
            iter_pos = self.password_buffer.get_end_iter()
            if (i + 1) % 8 == 0:  # Every 8th character
                self.password_buffer.insert_with_tags(iter_pos, char, self.highlight_tag)
            else:
                self.password_buffer.insert(iter_pos, char)
    
    def analyze_password(self):
        """Analyze current password and display results"""
        if not self.current_password:
            return
        
        analysis = self.analyzer.analyze_password(self.current_password)
        self.display_analysis(analysis)
    
    def display_analysis(self, analysis):
        """Display zxcvbn analysis results"""
        # Clear previous results
        for child in self.analysis_box.get_children():
            self.analysis_box.remove(child)
        
        for child in self.crack_time_box.get_children():
            self.crack_time_box.remove(child)
        
        if not analysis:
            return
        
        # Score display
        score = analysis.get('score', 0)
        score_colors = ['red', 'orange', 'orange', 'blue', 'green']
        score_labels = ['Very Weak', 'Weak', 'Fair', 'Good', 'Strong']
        
        score_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        score_label = Gtk.Label()
        score_label.set_markup(f'<span size="large"><b>Password Strength: </b></span>')
        score_value = Gtk.Label()
        score_value.set_markup(f'<span size="large" color="{score_colors[score]}"><b>{score}/4 - {score_labels[score]}</b></span>')
        
        score_box.pack_start(score_label, False, False, 0)
        score_box.pack_start(score_value, False, False, 0)
        self.analysis_box.pack_start(score_box, False, False, 0)
        
        # Guesses - format with scientific notation for large numbers
        guesses = analysis.get('guesses', 0)
        if guesses > 0:
            try:
                guesses_float = float(guesses)
                if guesses_float >= 1e6:  # Use scientific notation for numbers >= 1 million
                    exponent = int(math.log10(guesses_float))
                    mantissa = guesses_float / (10 ** exponent)
                    guesses_text = f"{mantissa:.1f} × 10^{exponent}"
                else:
                    guesses_text = f"{guesses_float:,.0f}"
            except (TypeError, ValueError, OverflowError):
                guesses_text = str(guesses)
        else:
            guesses_text = "0"
        
        guesses_label = Gtk.Label()
        guesses_label.set_markup(f'<b>Estimated Guesses:</b> {guesses_text}')
        guesses_label.set_xalign(0)
        self.analysis_box.pack_start(guesses_label, False, False, 0)
        
        # Feedback
        feedback = analysis.get('feedback', {})
        warning = feedback.get('warning', '')
        suggestions = feedback.get('suggestions', [])
        
        if warning:
            warning_label = Gtk.Label()
            warning_label.set_markup(f'<span color="red"><b>Warning:</b> {warning}</span>')
            warning_label.set_xalign(0)
            warning_label.set_line_wrap(True)
            self.analysis_box.pack_start(warning_label, False, False, 0)
        
        if suggestions:
            suggestions_label = Gtk.Label()
            suggestions_label.set_markup('<b>Suggestions:</b>')
            suggestions_label.set_xalign(0)
            self.analysis_box.pack_start(suggestions_label, False, False, 0)
            
            for suggestion in suggestions:
                suggestion_label = Gtk.Label()
                suggestion_label.set_markup(f'• {suggestion}')
                suggestion_label.set_xalign(0)
                suggestion_label.set_line_wrap(True)
                suggestion_label.set_margin_start(20)
                self.analysis_box.pack_start(suggestion_label, False, False, 0)
        
        # Sequence analysis
        sequence = analysis.get('sequence', [])
        if sequence:
            sequence_label = Gtk.Label()
            sequence_label.set_markup('<b>Pattern Analysis:</b>')
            sequence_label.set_xalign(0)
            self.analysis_box.pack_start(sequence_label, False, False, 0)
            
            # Add patterns sequentially right after the header
            for i, pattern in enumerate(sequence[:5]):  # Show first 5 patterns
                pattern_text = f"• {pattern.get('pattern', 'unknown')}: '{pattern.get('token', '')}'"
                if 'dictionary_name' in pattern:
                    pattern_text += f" (from {pattern['dictionary_name']})"
                
                pattern_label = Gtk.Label()
                pattern_label.set_markup(pattern_text)
                pattern_label.set_xalign(0)
                pattern_label.set_line_wrap(True)
                pattern_label.set_margin_start(20)
                self.analysis_box.pack_start(pattern_label, False, False, 0)
        
        # Crack time estimates
        crack_times = self.analyzer.get_crack_time_estimates(analysis)
        
        for scenario, time_estimate in crack_times.items():
            time_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            
            scenario_label = Gtk.Label()
            scenario_label.set_markup(f'<b>{scenario}:</b>')
            scenario_label.set_size_request(250, -1)
            scenario_label.set_xalign(0)
            
            time_label = Gtk.Label()
            time_label.set_markup(time_estimate)
            time_label.set_xalign(0)
            
            time_box.pack_start(scenario_label, False, False, 0)
            time_box.pack_start(time_label, True, True, 0)
            
            self.crack_time_box.pack_start(time_box, False, False, 0)
        
        self.analysis_box.show_all()
        self.crack_time_box.show_all()
    
    def on_copy_clicked(self, button):
        """Copy password to clipboard"""
        if self.current_password:
            clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
            clipboard.set_text(self.current_password, -1)
            
            # Show temporary notification
            button.set_label("Copied!")
            GLib.timeout_add(2000, lambda: button.set_label("Copy Password"))
    
    def run(self):
        """Start the application"""
        Gtk.main()


if __name__ == "__main__":
    print("Starting SecretSauce 2.0...")
    app = SecretSauceGUI()
    app.run()
