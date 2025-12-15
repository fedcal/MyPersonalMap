@echo off
REM Build script for Windows
REM Creates standalone executable for Windows

echo ========================================
echo Building My Personal Map for Windows
echo ========================================

REM Check if venv exists
if not exist "venv\" (
    echo Error: Virtual environment not found!
    echo Please run: python -m venv venv
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Install/upgrade PyInstaller
echo Installing PyInstaller...
pip install --upgrade pyinstaller

REM Clean previous builds
echo Cleaning previous builds...
if exist "build\" rmdir /s /q build
if exist "dist\" rmdir /s /q dist

REM Build with PyInstaller
echo Building executable...
pyinstaller build_config.spec --clean

REM Check if build succeeded
if not exist "dist\MyPersonalMap\" (
    echo Build failed!
    pause
    exit /b 1
)

REM Create ZIP package
echo Creating ZIP package...
cd dist
powershell -Command "Compress-Archive -Path MyPersonalMap -DestinationPath MyPersonalMap-Windows-x64.zip -Force"
cd ..

echo.
echo ========================================
echo Build complete!
echo ========================================
echo.
echo Executable: dist\MyPersonalMap\MyPersonalMap.exe
echo Package: dist\MyPersonalMap-Windows-x64.zip
echo.
pause
