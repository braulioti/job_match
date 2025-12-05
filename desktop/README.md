# Job Match Desktop Application

Aplicação desktop para avaliação de currículos e correspondência com vagas.

## Estrutura do Projeto

```
desktop/
├── main.py                 # Ponto de entrada da aplicação
├── requirements.txt        # Dependências do projeto
├── build.spec             # Configuração do PyInstaller
├── build.bat              # Script de build para Windows (batch)
├── build.py               # Script de build para Windows (Python)
└── src/                   # Código fonte
    ├── __init__.py
    ├── app.py             # Classe principal da aplicação
    ├── ui/                # Componentes de interface
    │   ├── __init__.py
    │   └── main_window.py # Janela principal
    ├── utils/             # Funções utilitárias
    │   ├── __init__.py
    │   └── helpers.py
    └── config/            # Configurações
        ├── __init__.py
        └── settings.py
```

## Requisitos

- Python 3.8 ou superior
- Tkinter (incluído com Python)



2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Execução

Execute a aplicação com:

```bash
python main.py
```

## Compilação para Executável Windows

Para criar um executável Windows (.exe) da aplicação:

### Método 1: Usando o script batch (Windows)

```bash
build.bat
```

### Método 2: Usando o script Python

```bash
python build.py
```

### Método 3: Manualmente com PyInstaller

```bash
pyinstaller build.spec
```

### Resultado

Após a compilação, o executável estará em:
```
dist/JobMatch.exe
```

### Personalização do Build

Para personalizar o build, edite o arquivo `build.spec`:

- **name**: Nome do executável (padrão: `JobMatch`)
- **icon**: Caminho para um arquivo `.ico` para o ícone do executável
- **console**: `False` para aplicação GUI (sem console), `True` para mostrar console
- **upx**: `True` para comprimir o executável (requer UPX instalado)

### Adicionar Ícone

1. Crie ou obtenha um arquivo `.ico`
2. Coloque-o na pasta `desktop/`
3. Edite `build.spec` e altere:
   ```python
   icon=None,  # Para:
   icon='seu_icone.ico',
   ```

### Notas

- O primeiro build pode demorar alguns minutos
- O executável será criado na pasta `dist/`
- Arquivos temporários serão criados na pasta `build/`
- O executável é standalone e não requer Python instalado no sistema

## Desenvolvimento

A aplicação está estruturada de forma modular:

- **app.py**: Gerencia o ciclo de vida da aplicação
- **ui/**: Contém todos os componentes de interface do usuário
- **utils/**: Funções auxiliares e utilitários
- **config/**: Configurações e constantes da aplicação

## Troubleshooting

### Erro: "PyInstaller não encontrado"
```bash
pip install pyinstaller
```

### Executável muito grande
- O PyInstaller inclui todo o Python e dependências
- Para reduzir o tamanho, considere usar `--onefile` com UPX ou criar uma versão otimizada

### Executável não inicia
- Verifique se todas as dependências estão no `requirements.txt`
- Execute com `console=True` temporariamente para ver erros
- Verifique os logs do PyInstaller

