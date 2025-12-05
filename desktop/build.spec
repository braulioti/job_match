# -*- mode: python ; coding: utf-8 -*-
import os
from pathlib import Path
from PyInstaller.utils.hooks import collect_all, collect_submodules

block_cipher = None

# Caminho do ícone
icon_path = Path('images/favicon.ico')
if not icon_path.exists():
    icon_path = None
else:
    icon_path = str(icon_path)

# Coletar platformdirs primeiro (pkg_resources depende dele)
try:
    platformdirs_datas, platformdirs_binaries, platformdirs_hiddenimports = collect_all('platformdirs')
    # Adicionar todos os submódulos explicitamente
    platformdirs_submodules = list(collect_submodules('platformdirs'))
    platformdirs_hiddenimports = list(set(platformdirs_hiddenimports + platformdirs_submodules))
except Exception as e:
    print(f"Aviso ao coletar platformdirs: {e}")
    platformdirs_datas, platformdirs_binaries = [], []
    platformdirs_hiddenimports = ['platformdirs', 'platformdirs.api', 'platformdirs.windows', 'platformdirs.unix', 'platformdirs.macos']

# Coletar pkg_resources (que depende de platformdirs)
try:
    pkg_resources_datas, pkg_resources_binaries, pkg_resources_hiddenimports = collect_all('pkg_resources')
except Exception as e:
    print(f"Aviso ao coletar pkg_resources: {e}")
    pkg_resources_datas, pkg_resources_binaries = [], []
    pkg_resources_hiddenimports = ['pkg_resources', 'pkg_resources.py2_warn']

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=platformdirs_binaries + pkg_resources_binaries,
    datas=[
        ('images', 'images'),  # Incluir pasta images
        ('scripts', 'scripts'),  # Incluir scripts SQL
    ] + platformdirs_datas + pkg_resources_datas,
    hiddenimports=[
        'tkinter',
        'tkinter.ttk',
        'sqlite3',
        'PIL',
        'PIL.Image',
        'PIL.ImageTk',
        'PIL._tkinter_finder',
        # platformdirs DEVE vir antes de pkg_resources
        'platformdirs',
        'platformdirs.api',
        'platformdirs.windows',
        'platformdirs.unix',
        'platformdirs.macos',
        'pkg_resources',
        'pkg_resources.py2_warn',
        'jaraco',
        'jaraco.text',
        'jaraco.functools',
        'jaraco.context',
        'more_itertools',
        'src',
        'src.app',
        'src.ui',
        'src.ui.main_window',
        'src.ui.new_project_dialog',
        'src.ui.about_dialog',
        'src.utils',
        'src.utils.helpers',
        'src.config',
        'src.config.settings',
        'src.database',
        'src.database.db',
    ] + platformdirs_hiddenimports + pkg_resources_hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='JobMatch',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Não mostrar console (GUI application)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_path,  # Ícone do executável
)

