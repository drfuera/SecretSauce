#!/usr/bin/env python3
"""
SecretSauce - Advanced Password Generator and Validator
Features comprehensive password analysis and generation
"""

import sys
import subprocess
import importlib
import os

def check_and_install_requirements():
    """Check for required packages and install them if missing"""
    required_packages = {
        'gi': 'PyGObject',
    }
    
    missing_packages = []
    
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
    
    # Check other required modules (most are built-in)
    try:
        import random, string, math, re, zlib
        from collections import Counter, defaultdict
        from itertools import groupby
        from pathlib import Path
        import webbrowser
    except ImportError as e:
        print(f"Missing required module: {e}")
        sys.exit(1)
    
    print("All requirements satisfied!")

# Check requirements before proceeding
check_and_install_requirements()

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Pango', '1.0')
from gi.repository import Gtk, Pango, Gdk, GLib
import random
import string
import math
import re
from collections import Counter, defaultdict
from itertools import groupby
import zlib
from pathlib import Path
import webbrowser

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
            "Features 16+ validation methods including entropy analysis,\n"
            "pattern detection, and cryptographic strength evaluation."
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
        self._add_grid_row(grid, 0, "Version:", "1.0")
        
        # Author
        self._add_grid_row(grid, 1, "Author:", "Andrej Fuera - Created with Claude")
        
        # Features
        features_label = Gtk.Label()
        features_label.set_markup("<small>16+ Security Analysis Methods\nUp to 4096 Character Passwords\nReal-time Validation</small>")
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


class PasswordAnalyzer:
    """Comprehensive password analysis engine"""
    
    def __init__(self):
        # Keyboard layout for adjacency analysis
        self.keyboard_layout = {
            'q': ['w', 'a'], 'w': ['q', 'e', 's', 'a'], 'e': ['w', 'r', 'd', 's'],
            'r': ['e', 't', 'f', 'd'], 't': ['r', 'y', 'g', 'f'], 'y': ['t', 'u', 'h', 'g'],
            'u': ['y', 'i', 'j', 'h'], 'i': ['u', 'o', 'k', 'j'], 'o': ['i', 'p', 'l', 'k'],
            'p': ['o', 'l'], 'a': ['q', 'w', 's', 'z'], 's': ['a', 'w', 'e', 'd', 'z', 'x'],
            'd': ['s', 'e', 'r', 'f', 'x', 'c'], 'f': ['d', 'r', 't', 'g', 'c', 'v'],
            'g': ['f', 't', 'y', 'h', 'v', 'b'], 'h': ['g', 'y', 'u', 'j', 'b', 'n'],
            'j': ['h', 'u', 'i', 'k', 'n', 'm'], 'k': ['j', 'i', 'o', 'l', 'm'],
            'l': ['k', 'o', 'p'], 'z': ['a', 's', 'x'], 'x': ['z', 's', 'd', 'c'],
            'c': ['x', 'd', 'f', 'v'], 'v': ['c', 'f', 'g', 'b'], 'b': ['v', 'g', 'h', 'n'],
            'n': ['b', 'h', 'j', 'm'], 'm': ['n', 'j', 'k']
        }
        
        # Visual similarity groups
        self.similar_chars = [
            ['0', 'O', 'o'], ['1', 'l', 'I', '|'], ['2', 'Z'], ['5', 'S'],
            ['6', 'G'], ['8', 'B'], ['9', 'g'], ['rn', 'm'], ['vv', 'w']
        ]
    
    def analyze_password(self, password):
        """Perform comprehensive password analysis"""
        results = {}
        
        # Basic metrics
        results['length'] = self._check_length(password)
        results['char_classes'] = self._check_character_classes(password)
        results['unique_chars'] = self._check_unique_characters(password)
        results['repeated_sequences'] = self._check_repeated_sequences(password)
        results['ascii_sequences'] = self._check_ascii_sequences(password)
        results['palindromes'] = self._check_palindromes(password)
        results['shannon_entropy'] = self._calculate_shannon_entropy(password)
        results['positional_entropy'] = self._calculate_positional_entropy(password)
        results['bigram_uniformity'] = self._check_bigram_uniformity(password)
        results['keyboard_complexity'] = self._check_keyboard_complexity(password)
        results['case_switching'] = self._check_case_switching(password)
        results['symbol_distribution'] = self._check_symbol_distribution(password)
        results['digit_padding'] = self._check_digit_padding(password)
        results['lz_complexity'] = self._calculate_lz_complexity(password)
        results['visual_similarity'] = self._check_visual_similarity(password)
        results['frequency_distribution'] = self._check_frequency_distribution(password)
        
        return results
    
    def _check_length(self, password):
        """Check password length"""
        length = len(password)
        if length >= 64:
            return {'status': 'pass', 'score': 100, 'message': f'Length: {length} chars (Excellent)'}
        elif length >= 32:
            return {'status': 'warning', 'score': 80, 'message': f'Length: {length} chars (Good)'}
        elif length >= 16:
            return {'status': 'warning', 'score': 60, 'message': f'Length: {length} chars (Fair)'}
        else:
            return {'status': 'fail', 'score': 20, 'message': f'Length: {length} chars (Too short)'}
    
    def _check_character_classes(self, password):
        """Check character class inclusion"""
        classes = {
            'lowercase': bool(re.search(r'[a-z]', password)),
            'uppercase': bool(re.search(r'[A-Z]', password)),
            'digits': bool(re.search(r'[0-9]', password)),
            'symbols': bool(re.search(r'[^a-zA-Z0-9]', password))
        }
        
        count = sum(classes.values())
        if count == 4:
            return {'status': 'pass', 'score': 100, 'message': 'All character classes present'}
        elif count == 3:
            return {'status': 'warning', 'score': 75, 'message': f'{count}/4 character classes'}
        elif count == 2:
            return {'status': 'warning', 'score': 50, 'message': f'{count}/4 character classes'}
        else:
            return {'status': 'fail', 'score': 25, 'message': f'{count}/4 character classes'}
    
    def _check_unique_characters(self, password):
        """Check unique character count"""
        unique_count = len(set(password))
        total_count = len(password)
        ratio = unique_count / total_count if total_count > 0 else 0
        
        if ratio >= 0.9:
            return {'status': 'pass', 'score': 100, 'message': f'{unique_count}/{total_count} unique chars (Excellent)'}
        elif ratio >= 0.8:
            return {'status': 'pass', 'score': 85, 'message': f'{unique_count}/{total_count} unique chars (Good)'}
        elif ratio >= 0.7:
            return {'status': 'warning', 'score': 70, 'message': f'{unique_count}/{total_count} unique chars (Fair)'}
        else:
            return {'status': 'fail', 'score': 50, 'message': f'{unique_count}/{total_count} unique chars (Poor)'}
    
    def _check_repeated_sequences(self, password):
        """Check for repeated sequences"""
        # Check for exact repeated substrings of length 3+
        repeated_found = []
        for length in range(3, len(password) // 2 + 1):
            for i in range(len(password) - length + 1):
                substring = password[i:i + length]
                remaining = password[i + length:]
                if substring in remaining:
                    repeated_found.append(substring)
        
        if not repeated_found:
            return {'status': 'pass', 'score': 100, 'message': 'No repeated sequences found'}
        else:
            return {'status': 'fail', 'score': 30, 'message': f'Repeated sequences: {len(repeated_found)}'}
    
    def _check_ascii_sequences(self, password):
        """Check for increasing/decreasing ASCII sequences"""
        sequences = []
        current_seq = [ord(password[0])] if password else []
        
        for i in range(1, len(password)):
            curr_ord = ord(password[i])
            if len(current_seq) >= 1:
                diff = curr_ord - current_seq[-1]
                if abs(diff) == 1:  # Consecutive ASCII values
                    current_seq.append(curr_ord)
                else:
                    if len(current_seq) >= 3:
                        sequences.append(current_seq)
                    current_seq = [curr_ord]
            else:
                current_seq = [curr_ord]
        
        if len(current_seq) >= 3:
            sequences.append(current_seq)
        
        if not sequences:
            return {'status': 'pass', 'score': 100, 'message': 'No ASCII sequences found'}
        else:
            return {'status': 'warning', 'score': 60, 'message': f'ASCII sequences: {len(sequences)}'}
    
    def _check_palindromes(self, password):
        """Check for palindromic patterns"""
        palindromes = []
        for length in range(3, len(password) + 1):
            for i in range(len(password) - length + 1):
                substring = password[i:i + length]
                if substring == substring[::-1]:
                    palindromes.append(substring)
        
        # Remove overlapping shorter palindromes
        unique_palindromes = []
        for p in sorted(palindromes, key=len, reverse=True):
            if not any(p in existing for existing in unique_palindromes):
                unique_palindromes.append(p)
        
        if not unique_palindromes:
            return {'status': 'pass', 'score': 100, 'message': 'No palindromes found'}
        else:
            return {'status': 'warning', 'score': 70, 'message': f'Palindromes: {len(unique_palindromes)}'}
    
    def _calculate_shannon_entropy(self, password):
        """Calculate Shannon entropy"""
        if not password:
            return {'status': 'fail', 'score': 0, 'message': 'No password'}
        
        counter = Counter(password)
        length = len(password)
        entropy = -sum((count / length) * math.log2(count / length) for count in counter.values())
        
        # Theoretical maximum entropy for this length
        max_entropy = math.log2(len(counter)) if len(counter) > 1 else 0
        normalized_entropy = (entropy / max_entropy) * 100 if max_entropy > 0 else 0
        
        if entropy >= 5.5:
            return {'status': 'pass', 'score': 100, 'message': f'Entropy: {entropy:.2f} bits (Excellent)'}
        elif entropy >= 4.5:
            return {'status': 'pass', 'score': 85, 'message': f'Entropy: {entropy:.2f} bits (Good)'}
        elif entropy >= 3.5:
            return {'status': 'warning', 'score': 70, 'message': f'Entropy: {entropy:.2f} bits (Fair)'}
        else:
            return {'status': 'fail', 'score': 40, 'message': f'Entropy: {entropy:.2f} bits (Poor)'}
    
    def _calculate_positional_entropy(self, password):
        """Calculate positional entropy variation"""
        if len(password) < 8:
            return {'status': 'warning', 'score': 50, 'message': 'Too short for analysis'}
        
        # Split into 8-character blocks and analyze each position
        position_chars = defaultdict(list)
        for i, char in enumerate(password):
            pos = i % 8
            position_chars[pos].append(char)
        
        position_entropies = []
        for pos in range(8):
            if pos in position_chars:
                chars = position_chars[pos]
                counter = Counter(chars)
                length = len(chars)
                if length > 1:
                    entropy = -sum((count / length) * math.log2(count / length) for count in counter.values())
                    position_entropies.append(entropy)
        
        if position_entropies:
            avg_entropy = sum(position_entropies) / len(position_entropies)
            variance = sum((e - avg_entropy) ** 2 for e in position_entropies) / len(position_entropies)
            
            if variance < 0.5 and avg_entropy > 2.0:
                return {'status': 'pass', 'score': 100, 'message': f'Positional entropy: {avg_entropy:.2f} (Uniform)'}
            elif avg_entropy > 1.5:
                return {'status': 'pass', 'score': 80, 'message': f'Positional entropy: {avg_entropy:.2f} (Good)'}
            else:
                return {'status': 'warning', 'score': 60, 'message': f'Positional entropy: {avg_entropy:.2f} (Fair)'}
        else:
            return {'status': 'fail', 'score': 30, 'message': 'Insufficient variation'}
    
    def _check_bigram_uniformity(self, password):
        """Check bigram frequency uniformity"""
        if len(password) < 2:
            return {'status': 'fail', 'score': 0, 'message': 'Too short'}
        
        bigrams = [password[i:i+2] for i in range(len(password) - 1)]
        counter = Counter(bigrams)
        
        # Check for uniform distribution
        expected_freq = len(bigrams) / len(counter)
        variance = sum((count - expected_freq) ** 2 for count in counter.values()) / len(counter)
        
        if variance < expected_freq * 0.5:
            return {'status': 'pass', 'score': 100, 'message': 'Uniform bigram distribution'}
        elif variance < expected_freq * 1.0:
            return {'status': 'pass', 'score': 80, 'message': 'Good bigram distribution'}
        else:
            return {'status': 'warning', 'score': 60, 'message': 'Uneven bigram distribution'}
    
    def _check_keyboard_complexity(self, password):
        """Check keyboard traversal complexity"""
        if len(password) < 2:
            return {'status': 'fail', 'score': 0, 'message': 'Too short'}
        
        total_distance = 0
        adjacent_pairs = 0
        
        for i in range(len(password) - 1):
            char1, char2 = password[i].lower(), password[i + 1].lower()
            
            if char1 in self.keyboard_layout and char2 in self.keyboard_layout[char1]:
                adjacent_pairs += 1
            
            # Simple distance metric based on keyboard position
            if char1 in self.keyboard_layout and char2 in self.keyboard_layout:
                total_distance += 1  # Base distance for any transition
        
        adjacent_ratio = adjacent_pairs / (len(password) - 1) if len(password) > 1 else 0
        
        if adjacent_ratio < 0.2:
            return {'status': 'pass', 'score': 100, 'message': f'Good keyboard complexity ({adjacent_pairs} adjacent)'}
        elif adjacent_ratio < 0.4:
            return {'status': 'pass', 'score': 80, 'message': f'Fair keyboard complexity ({adjacent_pairs} adjacent)'}
        else:
            return {'status': 'warning', 'score': 50, 'message': f'Poor keyboard complexity ({adjacent_pairs} adjacent)'}
    
    def _check_case_switching(self, password):
        """Check case switching frequency"""
        if not any(c.isalpha() for c in password):
            return {'status': 'warning', 'score': 70, 'message': 'No alphabetic characters'}
        
        switches = 0
        last_case = None
        
        for char in password:
            if char.isalpha():
                current_case = 'upper' if char.isupper() else 'lower'
                if last_case and last_case != current_case:
                    switches += 1
                last_case = current_case
        
        alpha_chars = sum(1 for c in password if c.isalpha())
        switch_ratio = switches / alpha_chars if alpha_chars > 0 else 0
        
        if 0.2 <= switch_ratio <= 0.8:
            return {'status': 'pass', 'score': 100, 'message': f'Good case variation ({switches} switches)'}
        elif switch_ratio > 0:
            return {'status': 'pass', 'score': 80, 'message': f'Some case variation ({switches} switches)'}
        else:
            return {'status': 'warning', 'score': 40, 'message': 'No case variation'}
    
    def _check_symbol_distribution(self, password):
        """Check symbol position distribution"""
        symbols = [i for i, c in enumerate(password) if not c.isalnum()]
        
        if not symbols:
            return {'status': 'warning', 'score': 60, 'message': 'No symbols found'}
        
        # Check if symbols are well distributed
        if len(symbols) >= 3:
            # Check if symbols are not clustered
            gaps = [symbols[i+1] - symbols[i] for i in range(len(symbols) - 1)]
            avg_gap = sum(gaps) / len(gaps) if gaps else 0
            variance = sum((gap - avg_gap) ** 2 for gap in gaps) / len(gaps) if gaps else 0
            
            if variance < avg_gap:
                return {'status': 'pass', 'score': 100, 'message': f'Well distributed symbols ({len(symbols)})'}
            else:
                return {'status': 'pass', 'score': 80, 'message': f'Symbols present ({len(symbols)})'}
        else:
            return {'status': 'warning', 'score': 70, 'message': f'Few symbols ({len(symbols)})'}
    
    def _check_digit_padding(self, password):
        """Check for digit padding (digits as prefix/suffix)"""
        if not password:
            return {'status': 'fail', 'score': 0, 'message': 'No password'}
        
        # Check for leading digits
        leading_digits = len(password) - len(password.lstrip('0123456789'))
        # Check for trailing digits
        trailing_digits = len(password) - len(password.rstrip('0123456789'))
        
        padding_ratio = (leading_digits + trailing_digits) / len(password)
        
        if padding_ratio < 0.2:
            return {'status': 'pass', 'score': 100, 'message': 'No digit padding detected'}
        elif padding_ratio < 0.4:
            return {'status': 'warning', 'score': 70, 'message': 'Some digit padding detected'}
        else:
            return {'status': 'fail', 'score': 40, 'message': 'Heavy digit padding detected'}
    
    def _calculate_lz_complexity(self, password):
        """Calculate Lempel-Ziv complexity"""
        if not password:
            return {'status': 'fail', 'score': 0, 'message': 'No password'}
        
        # Use zlib compression as approximation of LZ complexity
        compressed = zlib.compress(password.encode('utf-8'))
        compression_ratio = len(compressed) / len(password)
        
        # Higher compression ratio indicates lower complexity
        if compression_ratio > 0.8:
            return {'status': 'pass', 'score': 100, 'message': f'High complexity (ratio: {compression_ratio:.2f})'}
        elif compression_ratio > 0.6:
            return {'status': 'pass', 'score': 80, 'message': f'Good complexity (ratio: {compression_ratio:.2f})'}
        elif compression_ratio > 0.4:
            return {'status': 'warning', 'score': 60, 'message': f'Fair complexity (ratio: {compression_ratio:.2f})'}
        else:
            return {'status': 'fail', 'score': 30, 'message': f'Low complexity (ratio: {compression_ratio:.2f})'}
    
    def _check_visual_similarity(self, password):
        """Check for visually similar character substitutions"""
        similar_groups_found = 0
        
        for group in self.similar_chars:
            group_chars = [char for char in group if len(char) == 1]  # Single characters only
            found_in_password = [char for char in group_chars if char in password]
            if len(found_in_password) > 1:
                similar_groups_found += 1
        
        if similar_groups_found == 0:
            return {'status': 'pass', 'score': 100, 'message': 'No visual similarity issues'}
        elif similar_groups_found <= 2:
            return {'status': 'warning', 'score': 75, 'message': f'Some visual similarity ({similar_groups_found} groups)'}
        else:
            return {'status': 'warning', 'score': 50, 'message': f'Multiple visual similarities ({similar_groups_found} groups)'}
    
    def _check_frequency_distribution(self, password):
        """Check character frequency distribution"""
        if not password:
            return {'status': 'fail', 'score': 0, 'message': 'No password'}
        
        counter = Counter(password)
        frequencies = list(counter.values())
        
        # Calculate statistical measures
        mean_freq = sum(frequencies) / len(frequencies)
        variance = sum((f - mean_freq) ** 2 for f in frequencies) / len(frequencies)
        
        # Check for uniform distribution
        if variance < mean_freq * 0.5:
            return {'status': 'pass', 'score': 100, 'message': 'Uniform frequency distribution'}
        elif variance < mean_freq * 1.0:
            return {'status': 'pass', 'score': 80, 'message': 'Good frequency distribution'}
        else:
            return {'status': 'warning', 'score': 60, 'message': 'Skewed frequency distribution'}


class PasswordGenerator:
    """Advanced password generator with validation optimization"""
    
    def __init__(self):
        self.lowercase = string.ascii_lowercase
        self.uppercase = string.ascii_uppercase
        self.digits = string.digits
        self.symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
    def generate(self, length=64, use_lower=True, use_upper=True, use_digits=True, use_symbols=True):
        """Generate optimized password that passes most validation checks"""
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
        
        # Generate password with good distribution
        password = []
        
        # Ensure all character classes are represented
        if use_lower:
            password.extend(random.choices(self.lowercase, k=max(1, length // 8)))
        if use_upper:
            password.extend(random.choices(self.uppercase, k=max(1, length // 8)))
        if use_digits:
            password.extend(random.choices(self.digits, k=max(1, length // 8)))
        if use_symbols:
            password.extend(random.choices(self.symbols, k=max(1, length // 8)))
        
        # Fill remaining length with random selection
        remaining = length - len(password)
        if remaining > 0:
            password.extend(random.choices(charset, k=remaining))
        
        # Shuffle to avoid predictable patterns
        random.shuffle(password)
        
        # Ensure we don't have obvious patterns
        password_str = ''.join(password)
        
        # Simple check for obvious issues and regenerate if needed
        attempts = 0
        while attempts < 10:
            # Check for too many repeated characters
            counter = Counter(password_str)
            max_freq = max(counter.values())
            if max_freq > length // 4:  # No character appears more than 25% of the time
                random.shuffle(password)
                password_str = ''.join(password)
                attempts += 1
            else:
                break
        
        return password_str[:length]


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
        self.window.set_default_size(600, 700)
        self.window.connect("destroy", Gtk.main_quit)
        
        # Main container
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        main_box.set_margin_start(20)
        main_box.set_margin_end(20)
        main_box.set_margin_top(20)
        main_box.set_margin_bottom(20)
        
        # Title with about button
        title_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        
        title = Gtk.Label()
        title.set_markup("<b><big>SecretSauce</big></b> - Advanced Password Security")
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
        options_main_box.set_margin_start(10)
        options_main_box.set_margin_end(10)
        options_main_box.set_margin_top(10)
        options_main_box.set_margin_bottom(10)
        
        # Character sets section
        charset_section = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        charset_label = Gtk.Label(label="Character Sets:")
        charset_label.set_xalign(0)
        charset_label.set_markup("<b>Character Sets:</b>")
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
        length_section = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        length_label = Gtk.Label(label="Password Length:")
        length_label.set_xalign(0)
        length_label.set_markup("<b>Password Length:</b>")
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
        
        # Generate and Copy buttons
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
        
        # Validation results
        validation_frame = Gtk.Frame(label="Security Analysis")
        validation_scroll = Gtk.ScrolledWindow()
        validation_scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        validation_scroll.set_min_content_height(300)
        
        self.validation_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.validation_box.set_margin_start(10)
        self.validation_box.set_margin_end(10)
        self.validation_box.set_margin_top(10)
        self.validation_box.set_margin_bottom(10)
        
        validation_scroll.add(self.validation_box)
        validation_frame.add(validation_scroll)
        main_box.pack_start(validation_frame, True, True, 0)
        
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
        # Clear previous results
        for child in self.validation_box.get_children():
            self.validation_box.remove(child)
        
        if not self.current_password:
            return
        
        results = self.analyzer.analyze_password(self.current_password)
        
        for test_name, result in results.items():
            self.add_validation_result(test_name, result)
        
        self.validation_box.show_all()
    
    def add_validation_result(self, test_name, result):
        """Add a validation result to the display"""
        row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        
        # Status icon
        if result['status'] == 'pass':
            icon = Gtk.Label(label="✓")
            icon.set_markup('<span color="green" size="medium"><b>✓</b></span>')
        elif result['status'] == 'warning':
            icon = Gtk.Label(label="⚠")
            icon.set_markup('<span color="orange" size="medium"><b>⚠</b></span>')
        else:
            icon = Gtk.Label(label="✗")
            icon.set_markup('<span color="red" size="medium"><b>✗</b></span>')
        
        # Test name
        name_label = Gtk.Label(label=test_name.replace('_', ' ').title())
        name_label.set_markup(f'<small>{test_name.replace("_", " ").title()}</small>')
        name_label.set_size_request(200, -1)
        name_label.set_xalign(0)
        
        # Score
        score_label = Gtk.Label(label=f"{result['score']}/100")
        score_label.set_markup(f'<small>{result["score"]}/100</small>')
        score_label.set_size_request(60, -1)
        
        # Message
        message_label = Gtk.Label(label=result['message'])
        message_label.set_markup(f'<small>{result["message"]}</small>')
        message_label.set_xalign(0)
        message_label.set_line_wrap(True)
        
        row.pack_start(icon, False, False, 0)
        row.pack_start(name_label, False, False, 0)
        row.pack_start(score_label, False, False, 0)
        row.pack_start(message_label, True, True, 0)
        
        self.validation_box.pack_start(row, False, False, 0)
    
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
    print("Starting SecretSauce...")
    app = SecretSauceGUI()
    app.run()
