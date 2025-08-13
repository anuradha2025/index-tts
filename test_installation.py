#!/usr/bin/env python3
"""
Test script for IndexTTS Chrome Extension components
"""

import sys
import os
import json
from pathlib import Path

def test_imports():
    """Test if required modules can be imported."""
    print("Testing imports...")
    
    try:
        import torch
        print("✓ PyTorch imported successfully")
    except ImportError:
        print("✗ PyTorch not available")
        return False
    
    try:
        import tkinter
        print("✓ tkinter imported successfully")
    except ImportError:
        print("✗ tkinter not available")
        return False
    
    try:
        from indextts.infer import IndexTTS
        print("✓ IndexTTS imported successfully")
    except ImportError as e:
        print(f"✗ IndexTTS import failed: {e}")
        return False
    
    return True

def test_file_structure():
    """Test if all required files are present."""
    print("\nTesting file structure...")
    
    current_dir = Path(__file__).parent
    required_files = [
        'chrome-extension/manifest.json',
        'chrome-extension/background.js',
        'chrome-extension/content.js',
        'chrome-extension/popup.html',
        'chrome-extension/popup.js',
        'native-host/indextts_host.py',
        'native-host/com.indextts.host.json',
        'gui-app/settings_gui.py',
        'setup.sh',
        'setup.bat'
    ]
    
    missing_files = []
    for file_path in required_files:
        full_path = current_dir / file_path
        if full_path.exists():
            print(f"✓ {file_path}")
        else:
            print(f"✗ {file_path}")
            missing_files.append(file_path)
    
    return len(missing_files) == 0

def test_extension_manifest():
    """Test Chrome extension manifest validity."""
    print("\nTesting extension manifest...")
    
    current_dir = Path(__file__).parent
    manifest_path = current_dir / 'chrome-extension' / 'manifest.json'
    
    try:
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)
        
        required_keys = ['manifest_version', 'name', 'version', 'permissions', 'background', 'content_scripts']
        missing_keys = [key for key in required_keys if key not in manifest]
        
        if missing_keys:
            print(f"✗ Missing manifest keys: {missing_keys}")
            return False
        
        if manifest['manifest_version'] != 3:
            print("✗ Manifest version should be 3")
            return False
        
        print("✓ Extension manifest is valid")
        return True
        
    except Exception as e:
        print(f"✗ Manifest validation failed: {e}")
        return False

def test_native_messaging_manifest():
    """Test native messaging manifest validity."""
    print("\nTesting native messaging manifest...")
    
    current_dir = Path(__file__).parent
    manifest_path = current_dir / 'native-host' / 'com.indextts.host.json'
    
    try:
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)
        
        required_keys = ['name', 'description', 'path', 'type', 'allowed_origins']
        missing_keys = [key for key in required_keys if key not in manifest]
        
        if missing_keys:
            print(f"✗ Missing manifest keys: {missing_keys}")
            return False
        
        if manifest['type'] != 'stdio':
            print("✗ Native messaging type should be 'stdio'")
            return False
        
        print("✓ Native messaging manifest is valid")
        return True
        
    except Exception as e:
        print(f"✗ Native messaging manifest validation failed: {e}")
        return False

def test_model_directory():
    """Test if model directory exists and has required files."""
    print("\nTesting model directory...")
    
    current_dir = Path(__file__).parent
    model_dir = current_dir / 'checkpoints'
    
    if not model_dir.exists():
        print("✗ Model directory 'checkpoints' not found")
        print("  Please download models using:")
        print("  huggingface-cli download IndexTeam/IndexTTS-1.5 \\")
        print("    config.yaml bigvgan_discriminator.pth bigvgan_generator.pth bpe.model dvae.pth gpt.pth unigram_12000.vocab \\")
        print("    --local-dir checkpoints")
        return False
    
    required_files = ['config.yaml', 'gpt.pth', 'bigvgan_generator.pth', 'bpe.model']
    missing_files = []
    
    for file_name in required_files:
        file_path = model_dir / file_name
        if file_path.exists():
            print(f"✓ {file_name}")
        else:
            print(f"✗ {file_name}")
            missing_files.append(file_name)
    
    if missing_files:
        print(f"✗ Missing model files: {missing_files}")
        return False
    
    print("✓ All required model files found")
    return True

def main():
    """Run all tests."""
    print("IndexTTS Chrome Extension Test Suite")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_file_structure,
        test_extension_manifest,
        test_native_messaging_manifest,
        test_model_directory
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✓ All tests passed! Extension should work correctly.")
    else:
        print("✗ Some tests failed. Please fix the issues above.")
        
    print("\nNext steps:")
    print("1. If models are missing, run the setup script to download them")
    print("2. Install the Chrome extension by loading the 'chrome-extension' folder")
    print("3. Test the extension on a webpage")
    
    return passed == total

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)