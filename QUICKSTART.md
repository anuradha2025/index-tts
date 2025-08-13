# IndexTTS Chrome Extension - Quick Start Guide

## Overview

This Chrome extension provides offline text-to-speech functionality using the IndexTTS system. It can read web page content aloud with high-quality AI-generated speech, works completely offline, and includes voice cloning capabilities.

## System Requirements

- **Operating System**: Windows 11, macOS, or Linux
- **Hardware**: Intel i3 11th gen (or equivalent), 16GB RAM, 8GB UHD Graphics
- **Browser**: Google Chrome or Chromium-based browsers
- **Storage**: ~2GB for models and dependencies

## Quick Installation (5 minutes)

### Step 1: Download Models
```bash
# Install huggingface-cli if not available
pip install huggingface_hub

# Download IndexTTS models (required for offline operation)
huggingface-cli download IndexTeam/IndexTTS-1.5 \
  config.yaml bigvgan_discriminator.pth bigvgan_generator.pth bpe.model dvae.pth gpt.pth unigram_12000.vocab \
  --local-dir checkpoints
```

### Step 2: Setup Environment
```bash
# For Linux/macOS
chmod +x setup.sh
./setup.sh

# For Windows
setup.bat
```

### Step 3: Install Chrome Extension
1. Open Chrome → `chrome://extensions/`
2. Enable "Developer mode" (toggle top-right)
3. Click "Load unpacked" → select `chrome-extension` folder
4. Extension icon should appear in toolbar

### Step 4: Test
- Visit any webpage
- Select text → Press `Ctrl+Shift+R`
- Or click extension icon → "Read Page"

## Key Features

### 🔊 **Text-to-Speech**
- Select any text on webpage → instant speech generation
- Full page reading with one click
- High-quality AI voices using IndexTTS models

### ⚡ **Offline Operation**
- No internet required after setup
- All processing on local CPU/GPU
- Privacy-focused (no data sent to servers)

### 🎚️ **Customizable**
- Adjustable speed (0.5x to 2.0x)
- Volume control
- Custom voice cloning with audio samples
- Text highlighting while reading

### ⌨️ **Keyboard Shortcuts**
- `Ctrl+Shift+R`: Read selected text or full page
- `Ctrl+Shift+S`: Stop reading

### 🔧 **Settings Management**
- GUI application for configuration
- Voice file selection and testing
- Model management
- Extension preferences

## File Structure

```
index-tts/
├── chrome-extension/          # Extension files
│   ├── manifest.json         # Extension config
│   ├── background.js         # Service worker
│   ├── content.js           # Text extraction
│   ├── popup.html/js        # UI controls
│   └── icons/               # Extension icons
├── native-host/              # Python bridge
│   ├── indextts_host.py     # Main host app
│   └── com.indextts.host.json # Native messaging config
├── gui-app/                  # Settings GUI
│   └── settings_gui.py      # tkinter interface
└── checkpoints/              # AI models (download separately)
```

## Usage Examples

### Basic Reading
```
1. Visit any webpage (news, articles, documentation)
2. Select interesting text
3. Press Ctrl+Shift+R
4. Listen to AI-generated speech
```

### Full Page Reading
```
1. Open any article or blog post
2. Click extension icon
3. Select "Read Entire Page"
4. Sit back and listen
```

### Voice Customization
```
1. Record 10-30 seconds of clear speech (WAV format)
2. Run: python gui-app/settings_gui.py
3. Voice Settings → Browse → select your audio file
4. Test voice → Save settings
5. Extension now uses your voice characteristics
```

## Troubleshooting

### Extension Not Working
- Check native messaging: extension error console
- Verify model files in `checkpoints/`
- Ensure Python dependencies installed

### No Audio Generated
- Check logs: `~/.indextts/native_host.log`
- Verify IndexTTS import: `python -c "from indextts.infer import IndexTTS"`
- Try CPU mode in settings

### Poor Performance
- Use CPU mode for stability
- Reduce text length limits
- Close other applications to free RAM

## Advanced Features

### Voice Cloning
Record high-quality audio samples (noise-free, 22050Hz) for best voice cloning results.

### Batch Processing
Select large text blocks - the system automatically chunks them for processing.

### Cross-Platform
Works on Windows 11, macOS, and Linux with the same setup process.

## Development

### Testing
```bash
python test_installation.py  # Verify setup
python demo.py              # Feature demonstration
```

### Configuration
Settings stored in `~/.indextts/settings.json`

### Logs
Native host logs: `~/.indextts/native_host.log`

## Support

1. Run installation test: `python test_installation.py`
2. Check native host logs for errors
3. Verify model files are complete
4. Test IndexTTS directly: `python script.py`

For hardware optimization on Intel i3 11th gen with 16GB RAM, the system is configured to use CPU processing for maximum compatibility and stability.