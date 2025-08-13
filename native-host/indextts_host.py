#!/usr/bin/env python3
"""
Native messaging host for IndexTTS Chrome extension.
Handles communication between the extension and IndexTTS.
"""

import sys
import json
import struct
import logging
import os
import subprocess
import threading
import base64
from pathlib import Path

# Setup logging
log_dir = Path.home() / '.indextts'
log_dir.mkdir(exist_ok=True)
logging.basicConfig(
    filename=log_dir / 'native_host.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Add current directory to path for IndexTTS import
current_dir = Path(__file__).parent.parent
sys.path.insert(0, str(current_dir))

try:
    from indextts.infer import IndexTTS
    logging.info("IndexTTS imported successfully")
except ImportError as e:
    logging.error(f"Failed to import IndexTTS: {e}")
    sys.exit(1)

class IndexTTSNativeHost:
    def __init__(self):
        self.tts = None
        self.audio_dir = current_dir / 'chrome-extension' / 'audio'
        self.audio_dir.mkdir(exist_ok=True)
        self.settings_app_path = current_dir / 'gui-app' / 'settings_gui.py'
        self.initialize_tts()

    def initialize_tts(self):
        """Initialize IndexTTS with model checkpoints."""
        try:
            model_dir = current_dir / 'checkpoints'
            config_path = model_dir / 'config.yaml'
            
            if not model_dir.exists() or not config_path.exists():
                logging.error(f"Model directory or config not found: {model_dir}")
                return False
                
            self.tts = IndexTTS(
                model_dir=str(model_dir),
                cfg_path=str(config_path),
                device='cpu'  # Use CPU for better compatibility
            )
            logging.info("IndexTTS initialized successfully")
            return True
        except Exception as e:
            logging.error(f"Failed to initialize IndexTTS: {e}")
            return False

    def read_message(self):
        """Read message from Chrome extension."""
        try:
            # Read message length (4 bytes)
            raw_length = sys.stdin.buffer.read(4)
            if not raw_length:
                return None
            
            message_length = struct.unpack('=I', raw_length)[0]
            
            # Read message
            message = sys.stdin.buffer.read(message_length).decode('utf-8')
            return json.loads(message)
        except Exception as e:
            logging.error(f"Error reading message: {e}")
            return None

    def send_message(self, message):
        """Send message to Chrome extension."""
        try:
            message_json = json.dumps(message)
            message_bytes = message_json.encode('utf-8')
            
            # Send message length
            sys.stdout.buffer.write(struct.pack('=I', len(message_bytes)))
            
            # Send message
            sys.stdout.buffer.write(message_bytes)
            sys.stdout.buffer.flush()
            
            logging.debug(f"Sent message: {message}")
        except Exception as e:
            logging.error(f"Error sending message: {e}")

    def synthesize_speech(self, text, settings):
        """Generate speech from text using IndexTTS."""
        if not self.tts:
            return {'success': False, 'error': 'TTS engine not initialized'}

        try:
            # Create temporary audio file
            import tempfile
            import time
            
            timestamp = int(time.time())
            audio_filename = f"tts_output_{timestamp}.wav"
            audio_path = self.audio_dir / audio_filename
            
            # Use default voice file if exists, otherwise create a simple prompt
            voice_file = current_dir / 'test_data' / 'input.wav'
            if not voice_file.exists():
                # Create a minimal voice file or use a default
                logging.warning("No voice reference file found, using default")
                voice_file = None

            # Generate speech
            if voice_file:
                self.tts.infer(
                    voice=str(voice_file),
                    text=text,
                    output_path=str(audio_path)
                )
            else:
                # Use default inference without voice reference
                self.tts.infer(
                    voice=None,
                    text=text,
                    output_path=str(audio_path)
                )

            if audio_path.exists():
                # Convert audio to base64 for transmission
                with open(audio_path, 'rb') as f:
                    audio_data = base64.b64encode(f.read()).decode('utf-8')
                
                return {
                    'success': True,
                    'audioData': f"data:audio/wav;base64,{audio_data}",
                    'audioUrl': audio_filename
                }
            else:
                return {'success': False, 'error': 'Audio generation failed'}

        except Exception as e:
            logging.error(f"Speech synthesis error: {e}")
            return {'success': False, 'error': str(e)}

    def open_settings(self):
        """Open the settings GUI application."""
        try:
            if self.settings_app_path.exists():
                subprocess.Popen([sys.executable, str(self.settings_app_path)])
                return {'success': True}
            else:
                return {'success': False, 'error': 'Settings app not found'}
        except Exception as e:
            logging.error(f"Error opening settings: {e}")
            return {'success': False, 'error': str(e)}

    def handle_message(self, message):
        """Handle incoming message from extension."""
        if not message:
            return

        action = message.get('action')
        logging.debug(f"Received action: {action}")

        if action == 'synthesize':
            text = message.get('text', '')
            settings = message.get('settings', {})
            response = self.synthesize_speech(text, settings)
            self.send_message(response)

        elif action == 'openSettings':
            response = self.open_settings()
            self.send_message(response)

        elif action == 'ping':
            self.send_message({'success': True, 'pong': True})

        else:
            self.send_message({'success': False, 'error': f'Unknown action: {action}'})

    def run(self):
        """Main loop for the native messaging host."""
        logging.info("IndexTTS Native Host started")
        
        try:
            while True:
                message = self.read_message()
                if message is None:
                    break
                
                # Handle message in a separate thread to avoid blocking
                thread = threading.Thread(target=self.handle_message, args=(message,))
                thread.daemon = True
                thread.start()
                
        except KeyboardInterrupt:
            logging.info("Native host interrupted by user")
        except Exception as e:
            logging.error(f"Unexpected error in main loop: {e}")
        finally:
            logging.info("IndexTTS Native Host stopped")

if __name__ == '__main__':
    host = IndexTTSNativeHost()
    host.run()