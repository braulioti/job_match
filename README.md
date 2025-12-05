# <div align="center"><a href="https://brau.io"><img src="docs/images/job_match_logo.png" alt="Job Match" width="50%"></a></div>

## Job Match v0.1.0

[![Twitter: @_brau_io](https://img.shields.io/badge/contact-@_brau_io-blue.svg?style=flat)](https://x.com/_brau_io)
[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/)
[![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)](https://sqlite.org/)

Serviço de avaliação de currículos para avaliar o grau de aderência do currículo com a vaga.

Job Match é criado e mantido por [Bráulio Figueiredo](http://braulioti.com.br).
Novas atualizações do projeto podem ser acompanhadas através do X:
[@_brau_io](https://x.com/_brau_io).

## Índice

- [Estrutura do Projeto](#estrutura-do-projeto)
- [Requisitos](#requisitos)
- [Instalação](#instalação)
- [Build da Versão Desktop](#build-da-versão-desktop)
- [Versionamento](#versionamento)
- [Autor](#autor)

## Estrutura do Projeto

```
desktop/
├── main.py                 # Ponto de entrada da aplicação
├── requirements.txt        # Dependências do projeto
├── build.spec             # Configuração do PyInstaller para compilação
├── build.bat              # Script de build para Windows (batch)
├── build.py               # Script de build para Windows (Python)
├── README.md              # Documentação da aplicação desktop
├── images/                # Imagens e ícones da aplicação
│   ├── favicon.ico        # Ícone da aplicação
│   ├── favicon.png        # Favicon em formato PNG
│   └── job_match_logo.png # Logo do Job Match
├── scripts/               # Scripts SQL de inicialização do banco
│   └── 001-Create_Table_Project.sql  # Script de criação da tabela project
└── src/                   # Código fonte
    ├── __init__.py
    ├── app.py             # Classe principal da aplicação
    ├── ui/                # Componentes de interface
    │   ├── __init__.py
    │   ├── main_window.py        # Janela principal
    │   ├── new_project_dialog.py # Diálogo de cadastro de projeto
    │   └── about_dialog.py       # Diálogo sobre a aplicação
    ├── database/          # Gerenciamento de banco de dados
    │   ├── __init__.py
    │   └── db.py          # Classe de gerenciamento do banco SQLite
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
- SQLite

## Instalação

1. Ative o ambiente virtual (se estiver usando):
```bash
# Windows PowerShell
.\venv\Scripts\Activate.ps1

# Windows CMD
.\venv\Scripts\activate.bat
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Build da Versão Desktop

Para compilar a aplicação em um executável standalone, execute o script de build:

```bash
cd desktop
python build.py
```

O script irá:
- Limpar builds anteriores (pasta `build` e `dist`)
- Compilar a aplicação usando PyInstaller
- Gerar o executável `JobMatch.exe` na pasta `dist`

O executável será criado em: `desktop/dist/JobMatch.exe`

<div style="border-left: 4px solid #f44336; padding: 12px; margin: 16px 0;">
<strong style="color: #c62828;">⚠️ IMPORTANTE:</strong> Para que a aplicação funcione corretamente, as pastas <code>images</code> e <code>scripts</code> devem ser distribuídas junto com o executável. Certifique-se de copiar as pastas <code>images</code> e <code>scripts</code> para o mesmo diretório onde está o <code>JobMatch.exe</code>.
</div>

## Versionamento

Job Match utiliza as diretrizes do "Semantic Versioning" sempre que possível.
As atualizações são numeradas da seguinte forma:

`<maior>.<menor>.<correção>`

Construído sobre as seguintes diretrizes:

* Quebra de compatibilidade com a versão anterior será atualizado em "maior"
* Novas implementações e funcionalidades em "menor"
* Correção de erros em "correção"

Para mais informações sobre o SemVer, por favor visite http://semver.org.

## Autor
- Email: braulio@braulioti.com.br
- X: https://x.com/_brau_io
- GitHub: https://github.com/braulioti
- Website: http://brau.io

