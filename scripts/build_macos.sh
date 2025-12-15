#!/bin/bash
# Build script for macOS
# Creates standalone .app bundle and optionally DMG

set -e  # Exit on error

echo "========================================"
echo "Building My Personal Map for macOS"
echo "========================================"

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Error: Virtual environment not found!"
    echo "Please run: python3 -m venv venv"
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install/upgrade PyInstaller
echo "Installing PyInstaller..."
pip install --upgrade pyinstaller

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf build dist

# Build with PyInstaller
echo "Building .app bundle..."
pyinstaller build_config.spec --clean

# Check if build succeeded
if [ ! -d "dist/MyPersonalMap.app" ]; then
    echo "Build failed!"
    exit 1
fi

# Try to create DMG if create-dmg is available
if command -v create-dmg &> /dev/null; then
    echo "Creating DMG..."

    # Remove old DMG if exists
    rm -f dist/MyPersonalMap-macOS.dmg

    # Create DMG
    create-dmg \
        --volname "My Personal Map" \
        --volicon "pymypersonalmap/gui/assets/icon.icns" \
        --window-pos 200 120 \
        --window-size 800 400 \
        --icon-size 100 \
        --icon "MyPersonalMap.app" 200 190 \
        --hide-extension "MyPersonalMap.app" \
        --app-drop-link 600 185 \
        "dist/MyPersonalMap-macOS.dmg" \
        "dist/MyPersonalMap.app" || true  # Don't fail if create-dmg has issues

    if [ -f "dist/MyPersonalMap-macOS.dmg" ]; then
        echo
        echo "========================================"
        echo "Build complete!"
        echo "========================================"
        echo
        echo "App Bundle: dist/MyPersonalMap.app"
        echo "DMG: dist/MyPersonalMap-macOS.dmg"
        echo
    else
        echo
        echo "========================================"
        echo "Build complete!"
        echo "========================================"
        echo
        echo "App Bundle: dist/MyPersonalMap.app"
        echo "DMG creation failed - app bundle still available"
        echo
    fi
else
    echo "create-dmg not found, skipping DMG creation"
    echo "To install: brew install create-dmg"

    echo
    echo "========================================"
    echo "Build complete!"
    echo "========================================"
    echo
    echo "App Bundle: dist/MyPersonalMap.app"
    echo
    echo "To create DMG manually, install create-dmg:"
    echo "  brew install create-dmg"
    echo
fi

echo "Note: On first run, users may need to bypass Gatekeeper:"
echo "  System Settings → Privacy & Security → Open Anyway"
echo "Or run: xattr -cr dist/MyPersonalMap.app"
