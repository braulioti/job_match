"""
Script de build para compilar a aplicação Job Match Desktop
"""

import os
import shutil
import subprocess
import sys
import stat
import time
from pathlib import Path


def kill_process_by_name(process_name):
    """Tenta encerrar processos pelo nome"""
    try:
        if sys.platform == 'win32':
            # Windows
            result = subprocess.run(
                ['taskkill', '/F', '/IM', process_name],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print(f"  Processo {process_name} encerrado.")
                time.sleep(1)  # Aguardar um pouco para o sistema liberar o arquivo
                return True
        return False
    except Exception:
        return False


def clean_build_dirs():
    """Remove diretórios de build anteriores"""
    def remove_readonly(func, path, exc_info):
        """Callback para remover arquivos somente leitura"""
        try:
            os.chmod(path, stat.S_IWRITE)
            func(path)
        except Exception as e:
            print(f"  Aviso: Não foi possível remover {path}: {e}")
    
    # Verificar se o executável está em execução
    exe_path = Path('dist/JobMatch.exe')
    if exe_path.exists():
        print("  Encontrado JobMatch.exe existente...")
        try:
            # Tentar remover o arquivo diretamente primeiro
            os.chmod(str(exe_path), stat.S_IWRITE)
            exe_path.unlink()
            print("  JobMatch.exe removido com sucesso.")
        except PermissionError:
            print("  JobMatch.exe está bloqueado. Tentando encerrar processo...")
            if kill_process_by_name('JobMatch.exe'):
                # Tentar novamente após encerrar o processo
                time.sleep(2)
                try:
                    os.chmod(str(exe_path), stat.S_IWRITE)
                    exe_path.unlink()
                    print("  JobMatch.exe removido após encerrar processo.")
                except Exception as e:
                    print(f"  Aviso: Ainda não foi possível remover JobMatch.exe: {e}")
                    print("  Feche manualmente o executável e tente novamente.")
                    return False
            else:
                print("  Não foi possível encerrar o processo automaticamente.")
                print("  Feche manualmente o executável JobMatch.exe e tente novamente.")
                return False
        except Exception as e:
            print(f"  Aviso: Erro ao remover JobMatch.exe: {e}")
            return False
    
    # Remover diretórios (build primeiro, depois dist)
    dirs_to_remove = ['build', '__pycache__']
    
    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            print(f"Removendo {dir_name}...")
            try:
                shutil.rmtree(dir_name, onerror=remove_readonly)
            except PermissionError as e:
                print(f"  Aviso: Alguns arquivos em {dir_name} estão em uso: {e}")
            except Exception as e:
                print(f"  Aviso: Erro ao remover {dir_name}: {e}")
    
    # Remover dist por último (já removemos o executável acima)
    if os.path.exists('dist'):
        print("Removendo dist...")
        try:
            shutil.rmtree('dist', onerror=remove_readonly)
        except PermissionError as e:
            print(f"  Aviso: Alguns arquivos em dist estão em uso: {e}")
            print(f"  Feche o executável JobMatch.exe se estiver em execução e tente novamente.")
            return False
        except Exception as e:
            print(f"  Aviso: Erro ao remover dist: {e}")
    
    # Remove __pycache__ recursivamente
    for root, dirs, files in os.walk('src'):
        if '__pycache__' in dirs:
            pycache_path = os.path.join(root, '__pycache__')
            print(f"Removendo {pycache_path}...")
            try:
                shutil.rmtree(pycache_path, onerror=remove_readonly)
            except Exception as e:
                print(f"  Aviso: Erro ao remover {pycache_path}: {e}")
    
    return True


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
    if not clean_build_dirs():
        print()
        print("=" * 50)
        print("Não foi possível limpar builds anteriores.")
        print("Feche o executável JobMatch.exe se estiver em execução e tente novamente.")
        print("=" * 50)
        print()
        sys.exit(1)
    
    # Verificação final: garantir que o executável não existe
    exe_path = Path('dist/JobMatch.exe')
    if exe_path.exists():
        print("  Aviso: JobMatch.exe ainda existe após limpeza.")
        print("  Tentando remover novamente...")
        try:
            os.chmod(str(exe_path), stat.S_IWRITE)
            exe_path.unlink()
        except Exception as e:
            print(f"  Erro: Não foi possível remover {exe_path}: {e}")
            print("  Feche o executável manualmente e tente novamente.")
            sys.exit(1)
    
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

