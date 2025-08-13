@echo off
REM IndexTTS Chrome Extension Setup Script for Windows

echo ==========================================
echo IndexTTS Chrome Extension Setup
echo ==========================================

set PROJECT_DIR=%~dp0
set PROJECT_DIR=%PROJECT_DIR:~0,-1%

echo Project directory: %PROJECT_DIR%

REM Install Python dependencies
echo Installing Python dependencies...
pip install -e . --no-build-isolation
pip install tkinter pillow

REM Create directories
echo Creating necessary directories...
if not exist "%USERPROFILE%\.indextts" mkdir "%USERPROFILE%\.indextts"
if not exist "%PROJECT_DIR%\chrome-extension\audio" mkdir "%PROJECT_DIR%\chrome-extension\audio"

REM Setup native messaging manifest
echo Setting up native messaging...
set MANIFEST_FILE=%PROJECT_DIR%\native-host\com.indextts.host.json
set NATIVE_HOST_SCRIPT=%PROJECT_DIR%\native-host\indextts_host.py

REM Update manifest with correct path (Windows style)
powershell -Command "(Get-Content '%MANIFEST_FILE%') -replace 'REPLACE_WITH_ACTUAL_PATH', '%PROJECT_DIR%' | Set-Content '%MANIFEST_FILE%'"

REM Install native messaging manifest for Chrome
set CHROME_NATIVE_DIR=%LOCALAPPDATA%\Google\Chrome\User Data\NativeMessagingHosts
if not exist "%CHROME_NATIVE_DIR%" mkdir "%CHROME_NATIVE_DIR%"
copy "%MANIFEST_FILE%" "%CHROME_NATIVE_DIR%\"
echo Native messaging manifest installed for Windows Chrome

REM Check if model files exist
echo Checking for model files...
if not exist "%PROJECT_DIR%\checkpoints\config.yaml" (
    echo Model files not found. Please download them using:
    echo huggingface-cli download IndexTeam/IndexTTS-1.5 ^
    echo   config.yaml bigvgan_discriminator.pth bigvgan_generator.pth bpe.model dvae.pth gpt.pth unigram_12000.vocab ^
    echo   --local-dir checkpoints
    echo.
    echo Or use the Settings GUI to download automatically.
) else (
    echo Model files found ✓
)

REM Test the setup
echo Testing setup...
python -c "
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

echo.
echo ==========================================
echo Setup completed!
echo ==========================================
echo.
echo Next steps:
echo 1. Open Chrome and go to chrome://extensions/
echo 2. Enable 'Developer mode' (toggle in top right)
echo 3. Click 'Load unpacked' and select: %PROJECT_DIR%\chrome-extension
echo 4. The extension should now be installed and ready to use
echo.
echo To configure settings, run: python %PROJECT_DIR%\gui-app\settings_gui.py
echo.
echo Usage:
echo - Click the extension icon or use Ctrl+Shift+R to read text
echo - Use Ctrl+Shift+S to stop reading
echo - Select text on any webpage for quick reading

pause