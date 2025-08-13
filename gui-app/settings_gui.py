#!/usr/bin/env python3
"""
IndexTTS Settings GUI Application
Provides a user interface for configuring the Chrome extension settings.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import os
import sys
from pathlib import Path
import threading
import subprocess

# Add parent directory to path for IndexTTS import
current_dir = Path(__file__).parent.parent
sys.path.insert(0, str(current_dir))

class IndexTTSSettingsGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("IndexTTS Settings")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Configuration file path
        self.config_dir = Path.home() / '.indextts'
        self.config_dir.mkdir(exist_ok=True)
        self.config_file = self.config_dir / 'settings.json'
        
        # Default settings
        self.settings = {
            'voice_file': '',
            'speed': 1.0,
            'volume': 1.0,
            'auto_play': True,
            'highlight_text': True,
            'model_dir': str(current_dir / 'checkpoints'),
            'output_format': 'wav',
            'max_text_length': 5000
        }
        
        self.load_settings()
        self.create_widgets()
        self.update_status()

    def load_settings(self):
        """Load settings from config file."""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    loaded_settings = json.load(f)
                    self.settings.update(loaded_settings)
        except Exception as e:
            print(f"Error loading settings: {e}")

    def save_settings(self):
        """Save settings to config file."""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.settings, f, indent=2)
            messagebox.showinfo("Success", "Settings saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {e}")

    def create_widgets(self):
        """Create the GUI widgets."""
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Voice Settings Tab
        self.create_voice_tab()
        
        # Audio Settings Tab
        self.create_audio_tab()
        
        # Extension Settings Tab
        self.create_extension_tab()
        
        # Model Settings Tab
        self.create_model_tab()
        
        # Create buttons frame
        self.create_buttons()

    def create_voice_tab(self):
        """Create voice settings tab."""
        voice_frame = ttk.Frame(self.notebook)
        self.notebook.add(voice_frame, text="Voice Settings")
        
        # Voice file selection
        ttk.Label(voice_frame, text="Reference Voice File:").pack(anchor=tk.W, pady=5)
        
        voice_file_frame = ttk.Frame(voice_frame)
        voice_file_frame.pack(fill=tk.X, pady=5)
        
        self.voice_file_var = tk.StringVar(value=self.settings['voice_file'])
        self.voice_file_entry = ttk.Entry(voice_file_frame, textvariable=self.voice_file_var, width=50)
        self.voice_file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Button(voice_file_frame, text="Browse", command=self.browse_voice_file).pack(side=tk.RIGHT, padx=(5,0))
        
        # Voice file info
        info_text = "Select a WAV audio file to use as voice reference. This will determine the voice characteristics for speech synthesis."
        ttk.Label(voice_frame, text=info_text, wraplength=500, font=('TkDefaultFont', 9)).pack(anchor=tk.W, pady=5)
        
        # Test voice button
        ttk.Button(voice_frame, text="Test Voice", command=self.test_voice).pack(anchor=tk.W, pady=10)

    def create_audio_tab(self):
        """Create audio settings tab."""
        audio_frame = ttk.Frame(self.notebook)
        self.notebook.add(audio_frame, text="Audio Settings")
        
        # Speed control
        ttk.Label(audio_frame, text="Speech Speed:").pack(anchor=tk.W, pady=(10,5))
        
        speed_frame = ttk.Frame(audio_frame)
        speed_frame.pack(fill=tk.X, pady=5)
        
        self.speed_var = tk.DoubleVar(value=self.settings['speed'])
        self.speed_scale = ttk.Scale(speed_frame, from_=0.5, to=2.0, variable=self.speed_var, orient=tk.HORIZONTAL)
        self.speed_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.speed_label = ttk.Label(speed_frame, text=f"{self.settings['speed']:.1f}x")
        self.speed_label.pack(side=tk.RIGHT, padx=(5,0))
        
        self.speed_scale.configure(command=self.update_speed_label)
        
        # Volume control
        ttk.Label(audio_frame, text="Volume:").pack(anchor=tk.W, pady=(10,5))
        
        volume_frame = ttk.Frame(audio_frame)
        volume_frame.pack(fill=tk.X, pady=5)
        
        self.volume_var = tk.DoubleVar(value=self.settings['volume'])
        self.volume_scale = ttk.Scale(volume_frame, from_=0.0, to=1.0, variable=self.volume_var, orient=tk.HORIZONTAL)
        self.volume_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.volume_label = ttk.Label(volume_frame, text=f"{int(self.settings['volume']*100)}%")
        self.volume_label.pack(side=tk.RIGHT, padx=(5,0))
        
        self.volume_scale.configure(command=self.update_volume_label)
        
        # Output format
        ttk.Label(audio_frame, text="Output Format:").pack(anchor=tk.W, pady=(10,5))
        
        self.format_var = tk.StringVar(value=self.settings['output_format'])
        format_combo = ttk.Combobox(audio_frame, textvariable=self.format_var, values=['wav', 'mp3'], state='readonly')
        format_combo.pack(anchor=tk.W, pady=5)

    def create_extension_tab(self):
        """Create extension settings tab."""
        ext_frame = ttk.Frame(self.notebook)
        self.notebook.add(ext_frame, text="Extension Settings")
        
        # Auto-play option
        self.auto_play_var = tk.BooleanVar(value=self.settings['auto_play'])
        ttk.Checkbutton(ext_frame, text="Auto-play generated speech", variable=self.auto_play_var).pack(anchor=tk.W, pady=5)
        
        # Highlight text option
        self.highlight_var = tk.BooleanVar(value=self.settings['highlight_text'])
        ttk.Checkbutton(ext_frame, text="Highlight text while reading", variable=self.highlight_var).pack(anchor=tk.W, pady=5)
        
        # Max text length
        ttk.Label(ext_frame, text="Maximum Text Length (characters):").pack(anchor=tk.W, pady=(10,5))
        
        self.max_length_var = tk.IntVar(value=self.settings['max_text_length'])
        max_length_spinbox = ttk.Spinbox(ext_frame, from_=100, to=10000, textvariable=self.max_length_var, increment=100)
        max_length_spinbox.pack(anchor=tk.W, pady=5)
        
        # Usage instructions
        instructions = """
Extension Usage:
• Click the extension icon or use Ctrl+Shift+R to read selected text or entire page
• Use Ctrl+Shift+S to stop reading
• Select text on any webpage and click the floating read button
• The extension works offline using your local IndexTTS installation
        """
        ttk.Label(ext_frame, text=instructions, justify=tk.LEFT, font=('TkDefaultFont', 9)).pack(anchor=tk.W, pady=10)

    def create_model_tab(self):
        """Create model settings tab."""
        model_frame = ttk.Frame(self.notebook)
        self.notebook.add(model_frame, text="Model Settings")
        
        # Model directory
        ttk.Label(model_frame, text="Model Directory:").pack(anchor=tk.W, pady=5)
        
        model_dir_frame = ttk.Frame(model_frame)
        model_dir_frame.pack(fill=tk.X, pady=5)
        
        self.model_dir_var = tk.StringVar(value=self.settings['model_dir'])
        self.model_dir_entry = ttk.Entry(model_dir_frame, textvariable=self.model_dir_var, width=50)
        self.model_dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Button(model_dir_frame, text="Browse", command=self.browse_model_dir).pack(side=tk.RIGHT, padx=(5,0))
        
        # Model status
        self.model_status_label = ttk.Label(model_frame, text="", font=('TkDefaultFont', 9))
        self.model_status_label.pack(anchor=tk.W, pady=5)
        
        # Check model button
        ttk.Button(model_frame, text="Check Model Installation", command=self.check_model).pack(anchor=tk.W, pady=10)
        
        # Download model button
        ttk.Button(model_frame, text="Download Model (requires internet)", command=self.download_model).pack(anchor=tk.W, pady=5)

    def create_buttons(self):
        """Create bottom button frame."""
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(button_frame, text="Save Settings", command=self.apply_settings).pack(side=tk.RIGHT, padx=(5,0))
        ttk.Button(button_frame, text="Test TTS", command=self.test_tts).pack(side=tk.RIGHT)
        ttk.Button(button_frame, text="Reset to Defaults", command=self.reset_settings).pack(side=tk.LEFT)

    def browse_voice_file(self):
        """Browse for voice reference file."""
        filename = filedialog.askopenfilename(
            title="Select Voice Reference File",
            filetypes=[("Audio files", "*.wav *.mp3 *.flac"), ("All files", "*.*")]
        )
        if filename:
            self.voice_file_var.set(filename)

    def browse_model_dir(self):
        """Browse for model directory."""
        dirname = filedialog.askdirectory(title="Select Model Directory")
        if dirname:
            self.model_dir_var.set(dirname)

    def update_speed_label(self, value):
        """Update speed label."""
        self.speed_label.config(text=f"{float(value):.1f}x")

    def update_volume_label(self, value):
        """Update volume label."""
        self.volume_label.config(text=f"{int(float(value)*100)}%")

    def test_voice(self):
        """Test the selected voice file."""
        voice_file = self.voice_file_var.get()
        if not voice_file or not os.path.exists(voice_file):
            messagebox.showwarning("Warning", "Please select a valid voice file first.")
            return
        
        messagebox.showinfo("Test Voice", f"Voice file selected: {os.path.basename(voice_file)}")

    def check_model(self):
        """Check if model files are present."""
        model_dir = Path(self.model_dir_var.get())
        required_files = ['config.yaml', 'gpt.pth', 'bigvgan_generator.pth', 'bpe.model']
        
        missing_files = []
        for file in required_files:
            if not (model_dir / file).exists():
                missing_files.append(file)
        
        if missing_files:
            self.model_status_label.config(text=f"Missing files: {', '.join(missing_files)}", foreground='red')
        else:
            self.model_status_label.config(text="Model installation complete ✓", foreground='green')

    def download_model(self):
        """Download model files."""
        def download():
            try:
                model_dir = Path(self.model_dir_var.get())
                model_dir.mkdir(exist_ok=True)
                
                # Use huggingface-cli to download
                cmd = [
                    'huggingface-cli', 'download', 'IndexTeam/IndexTTS-1.5',
                    'config.yaml', 'bigvgan_discriminator.pth', 'bigvgan_generator.pth',
                    'bpe.model', 'dvae.pth', 'gpt.pth', 'unigram_12000.vocab',
                    '--local-dir', str(model_dir)
                ]
                
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode == 0:
                    messagebox.showinfo("Success", "Model downloaded successfully!")
                    self.check_model()
                else:
                    messagebox.showerror("Error", f"Download failed: {result.stderr}")
            except Exception as e:
                messagebox.showerror("Error", f"Download failed: {e}")
        
        threading.Thread(target=download, daemon=True).start()
        messagebox.showinfo("Download", "Download started in background. This may take several minutes.")

    def test_tts(self):
        """Test TTS functionality."""
        def test():
            try:
                # Import and test IndexTTS
                from indextts.infer import IndexTTS
                
                model_dir = self.model_dir_var.get()
                config_path = os.path.join(model_dir, 'config.yaml')
                
                if not os.path.exists(config_path):
                    messagebox.showerror("Error", "Model not found. Please check model directory.")
                    return
                
                tts = IndexTTS(model_dir=model_dir, cfg_path=config_path, device='cpu')
                
                # Test with sample text
                test_text = "Hello, this is a test of the IndexTTS system."
                voice_file = self.voice_file_var.get() if os.path.exists(self.voice_file_var.get()) else None
                
                output_path = self.config_dir / 'test_output.wav'
                tts.infer(voice=voice_file, text=test_text, output_path=str(output_path))
                
                if output_path.exists():
                    messagebox.showinfo("Success", f"TTS test successful! Audio saved to: {output_path}")
                else:
                    messagebox.showerror("Error", "TTS test failed - no audio generated")
                    
            except Exception as e:
                messagebox.showerror("Error", f"TTS test failed: {e}")
        
        threading.Thread(target=test, daemon=True).start()

    def apply_settings(self):
        """Apply and save current settings."""
        self.settings.update({
            'voice_file': self.voice_file_var.get(),
            'speed': self.speed_var.get(),
            'volume': self.volume_var.get(),
            'auto_play': self.auto_play_var.get(),
            'highlight_text': self.highlight_var.get(),
            'model_dir': self.model_dir_var.get(),
            'output_format': self.format_var.get(),
            'max_text_length': self.max_length_var.get()
        })
        self.save_settings()

    def reset_settings(self):
        """Reset to default settings."""
        if messagebox.askyesno("Reset Settings", "Are you sure you want to reset all settings to defaults?"):
            self.settings = {
                'voice_file': '',
                'speed': 1.0,
                'volume': 1.0,
                'auto_play': True,
                'highlight_text': True,
                'model_dir': str(current_dir / 'checkpoints'),
                'output_format': 'wav',
                'max_text_length': 5000
            }
            self.update_gui_from_settings()

    def update_gui_from_settings(self):
        """Update GUI elements from current settings."""
        self.voice_file_var.set(self.settings['voice_file'])
        self.speed_var.set(self.settings['speed'])
        self.volume_var.set(self.settings['volume'])
        self.auto_play_var.set(self.settings['auto_play'])
        self.highlight_var.set(self.settings['highlight_text'])
        self.model_dir_var.set(self.settings['model_dir'])
        self.format_var.set(self.settings['output_format'])
        self.max_length_var.set(self.settings['max_text_length'])
        
        self.update_speed_label(self.settings['speed'])
        self.update_volume_label(self.settings['volume'])

    def update_status(self):
        """Update model status on startup."""
        self.root.after(1000, self.check_model)

    def run(self):
        """Run the GUI application."""
        self.root.mainloop()

if __name__ == '__main__':
    app = IndexTTSSettingsGUI()
    app.run()