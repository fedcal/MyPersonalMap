# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller Configuration for My Personal Map

Builds standalone executable for Windows, macOS, and Linux.

Usage:
    pyinstaller build_config.spec --clean
"""

import sys
from pathlib import Path

# Project root
project_root = Path('.').resolve()

# Entry point
entry_point = project_root / 'pymypersonalmap' / 'gui' / 'app.py'

# Analysis: Find all dependencies
a = Analysis(
    [str(entry_point)],
    pathex=[str(project_root)],
    binaries=[],
    datas=[
        # Theme JSON
        (str(project_root / 'pymypersonalmap' / 'gui' / 'themes' / '*.json'), 'pymypersonalmap/gui/themes'),
        # Assets (icons, images) - if they exist
        # (str(project_root / 'pymypersonalmap' / 'gui' / 'assets' / '*'), 'pymypersonalmap/gui/assets'),
    ],
    # IMPORTANTE: Escludi cartelle cache, venv, etc.
    excludes=[
        # Development tools
        'pytest',
        'black',
        'mypy',
        'flake8',
        'pylint',

        # Large unused packages
        'matplotlib',
        'notebook',
        'IPython',
        'jupyter',
        'sphinx',
        'setuptools',
        'pip',
        'scipy',  # Non usata
        'statsmodels',  # Non usata
        'sympy',  # Non usata

        # Test modules
        'tkinter.test',
        'unittest',
        'test',
        'tests',

        # Cache e temp
        '__pycache__',
        'venv',
        'env',
        '.git',
        '.pytest_cache',
        '.mypy_cache',
        'node_modules',

        # GDAL drivers non usati (ottimizzazione build size)
        'osgeo.gdal_HDF4',
        'osgeo.gdal_HDF5',
        'osgeo.gdal_netCDF',
        'osgeo.gdal_GRIB',
        'osgeo.gdal_MEM',
        'osgeo.gdal_WCS',
        'osgeo.gdal_WMS',

        # Pandas components non usati
        'pandas.tests',
        'pandas.io.clipboard',
        'pandas.io.html',
        'pandas.io.sql',
        'pandas.io.excel',
        'pandas.plotting._matplotlib',

        # NumPy optimization
        'numpy.tests',
        'numpy.distutils',
        'numpy.f2py',

        # Unused web frameworks
        'flask',
        'django',
        'tornado',
        'aiohttp',

        # Unused documentation
        'pydoc',
        'doctest',
    ],
    hiddenimports=[
        # CustomTkinter
        'customtkinter',
        'PIL._tkinter_finder',

        # FastAPI + Uvicorn
        'uvicorn.logging',
        'uvicorn.loops',
        'uvicorn.loops.auto',
        'uvicorn.protocols',
        'uvicorn.protocols.http',
        'uvicorn.protocols.http.auto',
        'uvicorn.protocols.websockets',
        'uvicorn.protocols.websockets.auto',
        'uvicorn.lifespan',
        'uvicorn.lifespan.on',

        # SQLAlchemy + GeoAlchemy2
        'sqlalchemy.sql.default_comparator',
        'sqlalchemy.ext.baked',
        'geoalchemy2',

        # Geospatial libraries
        'shapely',
        'shapely.geometry',
        'fiona',
        'fiona.schema',
        'folium',
        'folium.plugins',
        'geopandas',

        # Database
        'pymysql',
        'pymysql.cursors',

        # Web/HTML
        'tkinterweb',

        # Other
        'requests',
        'dotenv',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    # Pathex excludes - NON raccogliere questi pattern
    pathex_excludes=[
        '*/__pycache__/*',
        '*/venv/*',
        '*/env/*',
        '*/.git/*',
        '*/.pytest_cache/*',
        '*/.mypy_cache/*',
        '*/node_modules/*',
        '*/build/*',
        '*/dist/*',
        '*/.vscode/*',
        '*/.idea/*',
        '*/tests/*',
        '*/test/*',
        '*/*.pyc',
        '*/*.pyo',
        '*/*.pyd',
        '*/frontend/*',  # Escludi frontend residuo
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

# Create PYZ archive
pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=None
)

# Create EXE
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='MyPersonalMap',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,  # Strip debug symbols to reduce size
    upx=True,  # UPX compression
    console=False,  # No console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=str(project_root / 'pymypersonalmap' / 'gui' / 'assets' / 'icon.ico') if (project_root / 'pymypersonalmap' / 'gui' / 'assets' / 'icon.ico').exists() else None,
)

# Collect all files
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=True,  # Strip debug symbols from binaries
    upx=True,  # UPX compression
    upx_exclude=[
        # Exclude problematic libraries from UPX compression
        'vcruntime*.dll',
        'python*.dll',
        'libgdal*.so*',
        'libproj*.so*',
    ],
    name='MyPersonalMap',
)

# macOS App Bundle
if sys.platform == 'darwin':
    app = BUNDLE(
        coll,
        name='MyPersonalMap.app',
        icon=str(project_root / 'pymypersonalmap' / 'gui' / 'assets' / 'icon.icns') if (project_root / 'pymypersonalmap' / 'gui' / 'assets' / 'icon.icns').exists() else None,
        bundle_identifier='com.mypersonalmap.app',
        info_plist={
            'CFBundleName': 'My Personal Map',
            'CFBundleDisplayName': 'My Personal Map',
            'CFBundleVersion': '1.0.0',
            'CFBundleShortVersionString': '1.0.0',
            'NSHighResolutionCapable': 'True',
            'NSRequiresAquaSystemAppearance': 'False',  # Support dark mode
        },
    )
