#!/bin/bash
# Build script for Linux
# Creates standalone executable and optionally AppImage

set -e  # Exit on error

echo "========================================"
echo "Building My Personal Map for Linux"
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
echo "Building executable..."
pyinstaller build_config.spec --clean

# Check if build succeeded
if [ ! -d "dist/MyPersonalMap" ]; then
    echo "Build failed!"
    exit 1
fi

# Try to create AppImage if appimagetool is available
if command -v appimagetool &> /dev/null; then
    echo "Creating AppImage..."

    # Create AppDir structure
    mkdir -p dist/MyPersonalMap.AppDir/usr/bin
    cp -r dist/MyPersonalMap/* dist/MyPersonalMap.AppDir/usr/bin/

    # Desktop entry
    cat > dist/MyPersonalMap.AppDir/MyPersonalMap.desktop <<EOF
[Desktop Entry]
Type=Application
Name=My Personal Map
Exec=MyPersonalMap
Icon=mypersonalmap
Categories=Office;Geography;
Comment=Personal geographic markers management
EOF

    # Copy icon (or use placeholder)
    if [ -f "pymypersonalmap/gui/assets/icon.png" ]; then
        cp pymypersonalmap/gui/assets/icon.png dist/MyPersonalMap.AppDir/mypersonalmap.png
    else
        # Create placeholder icon
        echo "Warning: No icon found, using placeholder"
    fi

    # AppRun script
    cat > dist/MyPersonalMap.AppDir/AppRun <<EOF
#!/bin/bash
SELF=\$(readlink -f "\$0")
HERE=\${SELF%/*}
export PATH="\$HERE/usr/bin:\$PATH"
export LD_LIBRARY_PATH="\$HERE/usr/lib:\$LD_LIBRARY_PATH"
exec "\$HERE/usr/bin/MyPersonalMap" "\$@"
EOF
    chmod +x dist/MyPersonalMap.AppDir/AppRun

    # Build AppImage
    appimagetool dist/MyPersonalMap.AppDir dist/MyPersonalMap-Linux-x86_64.AppImage

    echo
    echo "========================================"
    echo "Build complete!"
    echo "========================================"
    echo
    echo "AppImage: dist/MyPersonalMap-Linux-x86_64.AppImage"
    echo
else
    # Fallback: create tar.gz
    echo "appimagetool not found, creating tar.gz instead..."
    echo "To install appimagetool: https://github.com/AppImage/AppImageKit/releases"

    cd dist
    tar -czf MyPersonalMap-Linux-x86_64.tar.gz MyPersonalMap/
    cd ..

    echo
    echo "========================================"
    echo "Build complete!"
    echo "========================================"
    echo
    echo "Directory: dist/MyPersonalMap/"
    echo "Archive: dist/MyPersonalMap-Linux-x86_64.tar.gz"
    echo
fi
