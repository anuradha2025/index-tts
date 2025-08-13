# IndexTTS Chrome Extension

A Chrome browser extension that provides offline text-to-speech functionality using the IndexTTS system. This extension can read web page content aloud using high-quality AI-generated speech.

## Features

- **Offline TTS**: Works completely offline using CPU/GPU
- **Web Page Reading**: Read selected text or entire web pages
- **High Quality**: Uses IndexTTS for natural-sounding speech
- **Configurable**: GUI application for easy settings management
- **Keyboard Shortcuts**: Quick access via keyboard shortcuts
- **Voice Cloning**: Use custom voice references for personalized speech

## System Requirements

- **OS**: Windows 11, macOS, or Linux
- **RAM**: 16GB recommended (minimum 8GB)
- **CPU**: Intel i3 11th gen or equivalent
- **Storage**: 2GB for models and dependencies
- **Browser**: Google Chrome or Chromium-based browsers

## Installation

### 1. Download Models

First, download the IndexTTS models (required for offline operation):

```bash
# Using huggingface-cli (recommended)
huggingface-cli download IndexTeam/IndexTTS-1.5 \
  config.yaml bigvgan_discriminator.pth bigvgan_generator.pth bpe.model dvae.pth gpt.pth unigram_12000.vocab \
  --local-dir checkpoints
```

### 2. Install Dependencies

```bash
# Install Python dependencies
pip install -e . --no-build-isolation
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu
```

### 3. Setup Extension

#### For Linux/macOS:
```bash
chmod +x setup.sh
./setup.sh
```

#### For Windows:
```cmd
setup.bat
```

### 4. Install Chrome Extension

1. Open Chrome and navigate to `chrome://extensions/`
2. Enable "Developer mode" (toggle in top right)
3. Click "Load unpacked" and select the `chrome-extension` folder
4. The extension should now appear in your extensions list

## Usage

### Basic Usage

1. **Read Selected Text**: 
   - Select text on any webpage
   - Press `Ctrl+Shift+R` or click the floating read button

2. **Read Entire Page**: 
   - Press `Ctrl+Shift+R` without selecting text
   - Or click the extension icon and select "Read Page"

3. **Stop Reading**: 
   - Press `Ctrl+Shift+S`
   - Or click "Stop" in the extension popup

### Settings Configuration

Launch the settings GUI application:

```bash
python gui-app/settings_gui.py
```

#### Available Settings:

- **Voice Settings**: Select custom voice reference files
- **Audio Settings**: Adjust speed, volume, and output format
- **Extension Settings**: Configure auto-play, text highlighting, and text limits
- **Model Settings**: Manage model installation and directory

### Voice Customization

1. Record a clean audio sample (WAV format, 10-30 seconds)
2. Open Settings GUI → Voice Settings
3. Browse and select your audio file
4. Test the voice using the "Test Voice" button

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Chrome        │    │   Native        │    │   IndexTTS      │
│   Extension     │◄──►│   Messaging     │◄──►│   Engine        │
│                 │    │   Host          │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         ▲                                               ▲
         │                                               │
         ▼                                               ▼
┌─────────────────┐                            ┌─────────────────┐
│   Web Page      │                            │   Settings GUI  │
│   Content       │                            │   (tkinter)     │
│                 │                            │                 │
└─────────────────┘                            └─────────────────┘
```

### Components:

1. **Chrome Extension**: 
   - Content scripts for text extraction
   - Background service worker for TTS requests
   - Popup interface for user controls

2. **Native Messaging Host**: 
   - Python application bridging extension and IndexTTS
   - Handles TTS generation and audio file management

3. **IndexTTS Engine**: 
   - Core TTS functionality
   - Model loading and inference

4. **Settings GUI**: 
   - tkinter-based configuration application
   - Model management and voice customization

## File Structure

```
index-tts/
├── chrome-extension/          # Chrome extension files
│   ├── manifest.json         # Extension manifest
│   ├── background.js         # Service worker
│   ├── content.js           # Content script
│   ├── popup.html           # Extension popup
│   ├── popup.js             # Popup logic
│   ├── icons/               # Extension icons
│   └── audio/               # Generated audio files
├── native-host/              # Native messaging host
│   ├── indextts_host.py     # Main host application
│   └── com.indextts.host.json # Manifest for native messaging
├── gui-app/                  # Settings GUI application
│   └── settings_gui.py      # tkinter GUI
├── checkpoints/              # Model files (downloaded separately)
├── indextts/                 # IndexTTS core library
├── setup.sh                 # Linux/macOS setup script
├── setup.bat                # Windows setup script
└── README_EXTENSION.md      # This file
```

## Troubleshooting

### Extension Not Working

1. **Check Native Messaging**: 
   - Ensure the native messaging manifest is installed correctly
   - Check Chrome's extension error console

2. **Model Issues**: 
   - Verify all model files are downloaded in `checkpoints/`
   - Run the settings GUI and check model status

3. **Permission Issues**: 
   - Ensure the extension has permission to access the current tab
   - Check that the native host script is executable

### Audio Issues

1. **No Audio Generated**: 
   - Check the native host logs in `~/.indextts/native_host.log`
   - Verify PyTorch and dependencies are installed correctly

2. **Poor Audio Quality**: 
   - Try using a different voice reference file
   - Adjust speed and volume settings in the GUI

### Performance Issues

1. **Slow Generation**: 
   - Use CPU mode for better compatibility
   - Reduce text length limits in settings
   - Ensure sufficient RAM is available

## Advanced Configuration

### Custom Voice Training

For best results with voice cloning:

1. **Audio Quality**: Use clean, noise-free recordings
2. **Duration**: 10-30 seconds of clear speech
3. **Format**: WAV format at 22050Hz or higher
4. **Content**: Natural speech with varied intonation

### Model Optimization

For better performance on lower-end hardware:

1. Use CPU mode (set in settings)
2. Reduce batch sizes in IndexTTS configuration
3. Limit maximum text length for processing

## Development

### Building from Source

```bash
# Clone repository
git clone https://github.com/anuradha2025/index-tts.git
cd index-tts

# Install development dependencies
pip install -e ".[dev]"

# Run tests
python -m pytest tests/
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the same license as IndexTTS. See LICENSE file for details.

## Support

For issues and questions:

1. Check the troubleshooting section above
2. Review the native host logs
3. Open an issue on GitHub with detailed error information

## Acknowledgments

- IndexTTS team for the core TTS technology
- Chrome Extensions API documentation
- Native Messaging API examples