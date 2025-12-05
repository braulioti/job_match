# <div align="center"><a href="https://brau.io"><img src="docs/images/job_match_logo.png" alt="Job Match" width="50%"></a></div>

## Job Match v0.1.0

[![Twitter: @_brau_io](https://img.shields.io/badge/contact-@_brau_io-blue.svg?style=flat)](https://x.com/_brau_io)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/7121155e1f184c898f147ffdb7a85949)](https://app.codacy.com/gh/braulioti/job_match/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/)
[![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)](https://sqlite.org/)
[![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/en/stable/)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Swagger](https://img.shields.io/badge/-Swagger-%23Clojure?style=for-the-badge&logo=swagger&logoColor=white)](https://swagger.io/)

Serviço de avaliação de currículos para avaliar o grau de aderência do currículo com a vaga.

Job Match é criado e mantido por [Bráulio Figueiredo](http://braulioti.com.br).
Novas atualizações do projeto podem ser acompanhadas através do X:
[@_brau_io](https://x.com/_brau_io).

## Índice

- [Estrutura do Projeto](#estrutura-do-projeto)
  - [Aplicação Desktop](#aplicação-desktop)
  - [Projeto Backend API](#projeto-backend-api)
  - [Integração Contínua](#integração-contínua)
- [Tencnologias](#tencnologias)
- [Instalação](#instalação)
- [Versão Desktop](#versão-desktop)
  - [Build da versão](#build-da-versão)
  - [Arquivos e pastas que precisam ser distribuídos](#arquivos-e-pastas-que-precisam-ser-distribuídos)
  - [Configurações do arquivo servers](#configurações-do-arquivo-servers)
- [Projeto Backend API](#projeto-backend-api-1)
  - [Health Check Endpoint](#health-check-endpoint)
  - [API v1](#api-v1)
  - [Documentação de API - Swagger](#documentação-de-api---swagger)
- [Versionamento](#versionamento)
- [Autor](#autor)

## Estrutura do Projeto

### Aplicação Desktop

```
desktop/
├── main.py                 # Ponto de entrada da aplicação
├── requirements.txt        # Dependências do projeto
├── build.spec             # Configuração do PyInstaller para compilação
├── build.py               # Script de build para Windows (Python)
├── servers                 # Arquivo com lista de servidores disponíveis
├── images/                # Imagens e ícones da aplicação
│   ├── favicon.ico        # Ícone da aplicação
│   ├── favicon.png        # Favicon em formato PNG
│   └── job_match_logo.png # Logo do Job Match
├── scripts/               # Scripts SQL de inicialização do banco
│   ├── 001-Create_Table_Project.sql      # Script de criação da tabela project
│   └── 002-Create_Table_Job_Vacancy.sql # Script de criação da tabela job_vacancy
└── src/                   # Código fonte
    ├── __init__.py
    ├── app.py             # Classe principal da aplicação
    ├── ui/                # Componentes de interface
    │   ├── __init__.py
    │   ├── main_window.py        # Janela principal com painéis divididos e barra de status
    │   ├── splash_screen.py     # Tela de splash com barra de progresso
    │   ├── new_project_dialog.py # Diálogo de cadastro de projeto
    │   ├── open_project_dialog.py # Diálogo para abrir projeto existente
    │   ├── new_vacancy_dialog.py # Diálogo de cadastro de vaga
    │   ├── about_dialog.py       # Diálogo sobre a aplicação
    │   ├── configuration_dialog.py # Diálogo de configurações
    │   └── builders/      # Builders de componentes UI
    │       ├── __init__.py
    │       └── main_menu.py       # Builder do menu principal
    ├── entities/          # Entidades de domínio
    │   ├── __init__.py
    │   ├── project.py    # Entidade Project com operações de banco
    │   └── job_vacancy.py # Entidade JobVacancy com operações de banco
    ├── database/          # Gerenciamento de banco de dados
    │   ├── __init__.py
    │   └── db.py          # Classe de gerenciamento do banco SQLite
    ├── manager/           # Gerenciadores de configuração e recursos
    │   ├── __init__.py
    │   ├── base_manager.py        # Classe base para managers
    │   ├── config_manager.py      # Gerenciador de configurações (config.ini)
    │   └── server_manager.py      # Gerenciador de servidores
    ├── interfaces/        # Interfaces e tipos de dados
    │   ├── __init__.py
    │   └── server.py      # Interface para estrutura de servidor
    ├── integration/       # Integrações com serviços externos
    │   ├── __init__.py
    │   └── server_integration.py  # Integração com servidores (health check)
    ├── utils/             # Funções utilitárias
    │   ├── __init__.py
    │   └── helpers.py
    └── config/            # Configurações
        ├── __init__.py
        └── settings.py
```

### Projeto Backend API

```
api/
├── app.py              # Aplicação principal Flask
├── wsgi.py             # Entry point WSGI para Gunicorn
├── Dockerfile          # Configuração Docker para a API
├── requirements.txt    # Dependências do projeto
├── README.md          # Documentação da API
├── config/            # Configurações
│   ├── __init__.py
│   └── settings.py
├── routes/           # Rotas da API
│   ├── __init__.py
│   ├── routes.py
│   └── swagger/      # Rotas de documentação Swagger
│       ├── __init__.py
│       └── swagger.py # Classe para renderizar Swagger UI
├── swagger/          # Documentação Swagger/OpenAPI
│   └── pt-BR.yaml    # Especificação OpenAPI em português brasileiro
├── models/           # Modelos de dados
│   ├── __init__.py
│   └── models.py
└── utils/            # Funções utilitárias
    ├── __init__.py
    └── helpers.py
```

### Integração Contínua

```
ci-cd/
└── docker/                  # Configurações Docker para a API
    ├── docker-compose.yml   # Arquivo de composição Docker
    └── .dockerignore        # Arquivos ignorados no build Docker
```

## Tencnologias

- Python 3.8 ou superior
- Tkinter (incluído com Python)
- SQLite (Aplicação Desktop)
- Flask 3.0.0 ou superior
- Docker Engine 20.10 ou superior
- Docker Compose 2.0 ou superior
- Swagger Open API 3.0

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

## Versão Desktop

### Build da versão

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

### Arquivos e pastas que precisam ser distribuídos

<div style="border-left: 4px solid #f44336; padding: 12px; margin: 16px 0;">
<strong style="color: #c62828;">⚠️ IMPORTANTE:</strong> Para que a aplicação funcione corretamente, alguns arquivos e pastas deverão ser distribuídos junto com o arquivo <code>JobMatch.exe</code>
</div>

É necessário copiar os seguintes arquivos/pastas para a pasta dist antes de iniciar o projeto
- images
- scripts
- servers

### Configurações do arquivo servers

Quando a aplicação for iniciada, o arquivo servers é carregado com a lista de servidores do projeto. Em tempo de desenvolvimento, você pode ajustar o arquivo da seguinte forma:
 ```
 Servidor Oficial do Projeto;https://job-match-api.brau.io
 Servidor Local;http://localhost:5000;default
 ```
Desta forma você terá dois servidores disponíveis para poder utilizar, o oficial do projeto e o seu localhost.
Caso queira subir a aplicação em um servidor dentro da sua empresa, basta adicionar outras linhas no arquivo servers

## Projeto Backend API

### Health Check Endpoint
- **GET** `/health`
    - Retorna o status da API

### API v1
- Todos os endpoints da API estão disponíveis em `/api/v1`

### Documentação de API - Swagger

A API possui documentação interativa usando Swagger/OpenAPI 3.0. A documentação está disponível em português brasileiro e pode ser acessada através dos seguintes endpoints:

- **Swagger UI**: `http://localhost:5000/docs`
  - Interface interativa para explorar e testar os endpoints da API
  - Permite visualizar todos os endpoints, parâmetros, respostas e exemplos
  - Possibilita testar os endpoints diretamente pela interface

- **Especificação YAML**: `http://localhost:5000/docs/swagger.yaml`
  - Arquivo YAML com a especificação completa da API em formato OpenAPI 3.0.3
  - Localizado em `api/swagger/pt-BR.yaml`

- **Especificação JSON**: `http://localhost:5000/docs/swagger.json`
  - Mesma especificação em formato JSON para integração com outras ferramentas

A documentação inclui:
- Descrição de todos os endpoints disponíveis
- Parâmetros de requisição e resposta
- Exemplos de uso
- Modelos de dados (schemas)
- Códigos de status HTTP
- Informações de autenticação (preparado para implementação futura)

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

