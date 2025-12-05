# [Job Match v0.1.0](https://brau.io)
## Job Match

[![Twitter: @_brau_io](https://img.shields.io/badge/contact-@_brau_io-blue.svg?style=flat)](https://x.com/_brau_io)
[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/)
[![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)](https://sqlite.org/)

Serviço de avaliação de currículos para avaliar o grau de aderência do currículo com a vaga.

Job Match é criado e mantido por [Bráulio Figueiredo](http://braulioti.com.br).
Novas atualizações do projeto podem ser acompanhadas através do X:
[@_brau_io](https://x.com/_brau_io).

## Estrutura do Projeto

```
desktop/
├── main.py                 # Ponto de entrada da aplicação
├── requirements.txt        # Dependências do projeto
├── build.spec             # Configuração do PyInstaller para compilação
├── build.bat              # Script de build para Windows (batch)
├── build.py               # Script de build para Windows (Python)
├── README.md              # Documentação da aplicação desktop
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

