"""
Script de build para compilar a aplicação Job Match Desktop
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path


def clean_build_dirs():
    """Remove diretórios de build anteriores"""
    dirs_to_remove = ['build', 'dist', '__pycache__']
    
    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            print(f"Removendo {dir_name}...")
            shutil.rmtree(dir_name)
    
    # Remove __pycache__ recursivamente
    for root, dirs, files in os.walk('src'):
        if '__pycache__' in dirs:
            pycache_path = os.path.join(root, '__pycache__')
            print(f"Removendo {pycache_path}...")
            shutil.rmtree(pycache_path)


def check_pyinstaller():
    """Verifica se PyInstaller está instalado"""
    try:
        import PyInstaller
        return True
    except ImportError:
        return False


def build():
    """Compila a aplicação"""
    print("=" * 50)
    print("Job Match Desktop - Build Script")
    print("=" * 50)
    print()
    
    # Verificar PyInstaller
    if not check_pyinstaller():
        print("[ERRO] PyInstaller não está instalado.")
        print("Execute: pip install -r requirements.txt")
        sys.exit(1)
    
    # Limpar builds anteriores
    print("Limpando builds anteriores...")
    clean_build_dirs()
    print()
    
    # Compilar
    print("Compilando aplicação...")
    result = subprocess.run(
        ['pyinstaller', 'build.spec'],
        cwd=Path(__file__).parent
    )
    
    if result.returncode == 0:
        print()
        print("=" * 50)
        print("Build concluído com sucesso!")
        print("=" * 50)
        print()
        print("Executável criado em: dist/JobMatch.exe")
        print()
    else:
        print()
        print("=" * 50)
        print("Erro durante a compilação!")
        print("=" * 50)
        print()
        sys.exit(1)


if __name__ == '__main__':
    build()

