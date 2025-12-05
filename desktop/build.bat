@echo off
REM Script de build para Windows
REM Compila a aplicação Job Match Desktop em um executável

echo ========================================
echo Job Match Desktop - Build Script
echo ========================================
echo.

REM Verificar se o venv está ativado
python -c "import sys; sys.exit(0 if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix) else 1)" 2>nul
if %errorlevel% neq 0 (
    echo [AVISO] Ambiente virtual não detectado.
    echo Recomendado: Ative o venv antes de executar este script.
    echo.
)

REM Verificar se PyInstaller está instalado
python -c "import PyInstaller" 2>nul
if %errorlevel% neq 0 (
    echo [ERRO] PyInstaller não está instalado.
    echo Execute: pip install -r requirements.txt
    pause
    exit /b 1
)

echo Limpando builds anteriores...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist __pycache__ rmdir /s /q __pycache__
if exist src\__pycache__ rmdir /s /q src\__pycache__
if exist src\config\__pycache__ rmdir /s /q src\config\__pycache__
if exist src\ui\__pycache__ rmdir /s /q src\ui\__pycache__
if exist src\utils\__pycache__ rmdir /s /q src\utils\__pycache__
echo.

echo Compilando aplicação...
pyinstaller build.spec

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo Build concluído com sucesso!
    echo ========================================
    echo.
    echo Executável criado em: dist\JobMatch.exe
    echo.
) else (
    echo.
    echo ========================================
    echo Erro durante a compilação!
    echo ========================================
    echo.
)

pause

