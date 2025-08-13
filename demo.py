#!/usr/bin/env python3
"""
Demo script showing IndexTTS Chrome Extension functionality
This demonstrates the key components without requiring model files or GUI
"""

import json
import sys
from pathlib import Path

def demo_extension_features():
    """Demonstrate extension components"""
    print("=" * 60)
    print("IndexTTS Chrome Extension Demo")
    print("=" * 60)
    
    # Check extension manifest
    print("\n1. Chrome Extension Manifest:")
    print("-" * 30)
    
    manifest_path = Path('chrome-extension/manifest.json')
    if manifest_path.exists():
        with open(manifest_path) as f:
            manifest = json.load(f)
        
        print(f"Extension Name: {manifest['name']}")
        print(f"Version: {manifest['version']}")
        print(f"Manifest Version: {manifest['manifest_version']}")
        print(f"Permissions: {', '.join(manifest['permissions'])}")
        print("✓ Extension manifest valid")
    else:
        print("✗ Extension manifest not found")
    
    # Check native messaging setup
    print("\n2. Native Messaging Configuration:")
    print("-" * 30)
    
    native_manifest_path = Path('native-host/com.indextts.host.json')
    if native_manifest_path.exists():
        with open(native_manifest_path) as f:
            native_manifest = json.load(f)
        
        print(f"Host Name: {native_manifest['name']}")
        print(f"Description: {native_manifest['description']}")
        print(f"Type: {native_manifest['type']}")
        print("✓ Native messaging configured")
    else:
        print("✗ Native messaging manifest not found")
    
    # Check file structure
    print("\n3. File Structure:")
    print("-" * 30)
    
    files_to_check = [
        'chrome-extension/background.js',
        'chrome-extension/content.js', 
        'chrome-extension/popup.html',
        'native-host/indextts_host.py',
        'gui-app/settings_gui.py'
    ]
    
    for file_path in files_to_check:
        if Path(file_path).exists():
            size = Path(file_path).stat().st_size
            print(f"✓ {file_path} ({size} bytes)")
        else:
            print(f"✗ {file_path}")
    
    # Demo native messaging protocol
    print("\n4. Native Messaging Protocol Demo:")
    print("-" * 30)
    
    sample_messages = [
        {
            "action": "synthesize",
            "text": "Hello, this is a test message",
            "settings": {
                "speed": 1.0,
                "volume": 1.0,
                "voice": "default"
            }
        },
        {
            "action": "openSettings"
        },
        {
            "action": "ping"
        }
    ]
    
    for msg in sample_messages:
        print(f"Sample message: {json.dumps(msg, indent=2)}")
        print()
    
    # Demo extension features
    print("5. Extension Features:")
    print("-" * 30)
    
    features = [
        "✓ Text selection and extraction from web pages",
        "✓ Full page content reading",
        "✓ Keyboard shortcuts (Ctrl+Shift+R, Ctrl+Shift+S)",
        "✓ Floating controls overlay",
        "✓ Audio generation using IndexTTS",
        "✓ Offline operation (no internet required)",
        "✓ Voice cloning with custom reference files",
        "✓ Configurable speed, volume, and settings",
        "✓ Native messaging for secure communication",
        "✓ Cross-platform support (Windows, macOS, Linux)"
    ]
    
    for feature in features:
        print(feature)
    
    # Installation steps
    print("\n6. Installation Steps:")
    print("-" * 30)
    
    steps = [
        "1. Download IndexTTS models to 'checkpoints/' directory",
        "2. Run setup script: ./setup.sh (Linux/macOS) or setup.bat (Windows)",
        "3. Open Chrome → chrome://extensions/",
        "4. Enable 'Developer mode'",
        "5. Click 'Load unpacked' → select 'chrome-extension' folder",
        "6. Extension ready to use!"
    ]
    
    for step in steps:
        print(step)
    
    print("\n7. Usage Examples:")
    print("-" * 30)
    
    usage = [
        "• Select text on any webpage → Press Ctrl+Shift+R to read",
        "• Click extension icon → 'Read Page' for full page reading", 
        "• Press Ctrl+Shift+S to stop reading",
        "• Run settings GUI: python gui-app/settings_gui.py",
        "• Configure voice files, speed, volume in settings",
        "• Works offline with local IndexTTS models"
    ]
    
    for use_case in usage:
        print(use_case)
    
    print("\n" + "=" * 60)
    print("Demo completed! Extension is ready for installation.")
    print("=" * 60)

if __name__ == '__main__':
    # Change to script directory
    script_dir = Path(__file__).parent
    import os
    os.chdir(script_dir)
    
    demo_extension_features()