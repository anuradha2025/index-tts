#!/bin/bash
# IndexTTS Chrome Extension Setup Script

set -e

echo "=========================================="
echo "IndexTTS Chrome Extension Setup"
echo "=========================================="

# Get the absolute path of the script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "Project directory: $PROJECT_DIR"

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -e . --no-build-isolation

# Install additional dependencies
pip install tkinter pillow

# Create directories
echo "Creating necessary directories..."
mkdir -p "$HOME/.indextts"
mkdir -p "$PROJECT_DIR/chrome-extension/audio"

# Setup native messaging manifest
echo "Setting up native messaging..."
MANIFEST_FILE="$PROJECT_DIR/native-host/com.indextts.host.json"
NATIVE_HOST_SCRIPT="$PROJECT_DIR/native-host/indextts_host.py"

# Make the native host script executable
chmod +x "$NATIVE_HOST_SCRIPT"

# Update manifest with correct path
sed -i "s|REPLACE_WITH_ACTUAL_PATH|$PROJECT_DIR|g" "$MANIFEST_FILE"

# Install native messaging manifest for Chrome
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    CHROME_NATIVE_DIR="$HOME/.config/google-chrome/NativeMessagingHosts"
    mkdir -p "$CHROME_NATIVE_DIR"
    cp "$MANIFEST_FILE" "$CHROME_NATIVE_DIR/"
    echo "Native messaging manifest installed for Linux Chrome"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    CHROME_NATIVE_DIR="$HOME/Library/Application Support/Google/Chrome/NativeMessagingHosts"
    mkdir -p "$CHROME_NATIVE_DIR"
    cp "$MANIFEST_FILE" "$CHROME_NATIVE_DIR/"
    echo "Native messaging manifest installed for macOS Chrome"
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    echo "For Windows, please manually copy $MANIFEST_FILE to:"
    echo "C:\\Users\\%USERNAME%\\AppData\\Local\\Google\\Chrome\\User Data\\NativeMessagingHosts\\"
fi

# Check if model files exist
echo "Checking for model files..."
MODEL_DIR="$PROJECT_DIR/checkpoints"
if [ ! -f "$MODEL_DIR/config.yaml" ] || [ ! -f "$MODEL_DIR/gpt.pth" ]; then
    echo "Model files not found. Please download them using:"
    echo "huggingface-cli download IndexTeam/IndexTTS-1.5 \\"
    echo "  config.yaml bigvgan_discriminator.pth bigvgan_generator.pth bpe.model dvae.pth gpt.pth unigram_12000.vocab \\"
    echo "  --local-dir checkpoints"
    echo ""
    echo "Or use the Settings GUI to download automatically."
else
    echo "Model files found ✓"
fi

# Test the setup
echo "Testing setup..."
python3 -c "
try:
    from indextts.infer import IndexTTS
    print('✓ IndexTTS import successful')
except Exception as e:
    print(f'✗ IndexTTS import failed: {e}')

try:
    import tkinter
    print('✓ tkinter available')
except Exception as e:
    print(f'✗ tkinter not available: {e}')
"

echo ""
echo "=========================================="
echo "Setup completed!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Open Chrome and go to chrome://extensions/"
echo "2. Enable 'Developer mode' (toggle in top right)"
echo "3. Click 'Load unpacked' and select: $PROJECT_DIR/chrome-extension"
echo "4. The extension should now be installed and ready to use"
echo ""
echo "To configure settings, run: python3 $PROJECT_DIR/gui-app/settings_gui.py"
echo ""
echo "Usage:"
echo "- Click the extension icon or use Ctrl+Shift+R to read text"
echo "- Use Ctrl+Shift+S to stop reading"
echo "- Select text on any webpage for quick reading"