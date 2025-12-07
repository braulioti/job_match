# Estrutura do Projeto Job Match

## Visão Geral

Este documento descreve a estrutura completa do projeto Job Match, que consiste em duas partes principais:
- **Aplicação Desktop**: Interface gráfica para gerenciar projetos e vagas
- **Backend API**: API REST para processamento de análise de currículos com IA

---

## Aplicação Desktop

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

## Projeto Backend API

```
api/
├── app.py              # Aplicação principal Flask
├── wsgi.py             # Entry point WSGI para Gunicorn
├── Dockerfile          # Configuração Docker para a API
├── requirements.txt    # Dependências do projeto
├── env.example         # Arquivo de exemplo para variáveis de ambiente
├── config/             # Configurações
│   ├── __init__.py
│   └── settings.py     # Configurações da aplicação (Flask, DB, etc)
├── database/           # Configuração do banco de dados
│   ├── __init__.py
│   └── database.py     # Setup do SQLAlchemy e gerenciamento de sessão
├── models/             # Modelos de dados (SQLAlchemy)
│   ├── __init__.py
│   ├── models.py       # Importa todos os models para registro
│   ├── base_model.py   # Modelo base com campos comuns (id, created_at, updated_at)
│   └── file.py         # Modelo File para armazenar metadados de arquivos
├── migrations/         # Migrations do banco de dados (Flask-Migrate/Alembic)
│   ├── __init__.py
│   ├── alembic.ini     # Configuração do Alembic
│   ├── env.py          # Configuração do ambiente de migrations
│   ├── script.py.mako  # Template para criação de migrations
│   └── versions/       # Arquivos de migration
│       └── 001_create_file_table.py  # Migration inicial da tabela file
├── dto/                # Data Transfer Objects
│   ├── __init__.py
│   ├── job_analysis_dto.py  # DTO para requisições de análise de vagas
│   └── file_data_dto.py     # DTO para dados de arquivos validados
├── controller/         # Controladores (camada de controle)
│   ├── __init__.py
│   ├── ia_controller.py    # Controller para processamento de IA
│   └── file_controller.py  # Controller para operações de upload de arquivos
├── services/           # Serviços (lógica de negócio)
│   ├── __init__.py
│   ├── ia_service.py   # Serviço de processamento de IA
│   └── file_service.py # Serviço para validação e processamento de arquivos (conversão DOC/PDF para texto)
├── integration/        # Integrações com serviços externos
│   ├── __init__.py
│   └── provider/       # Provedores de IA
│       ├── __init__.py
│       ├── base_provider.py    # Classe base abstrata para providers
│       ├── ollama_provider.py  # Provider para integração com Ollama
│       └── gemini_provider.py  # Provider para integração com Google Gemini
├── routes/             # Rotas da API
│   ├── __init__.py
│   ├── routes.py       # Definição das rotas principais
│   └── swagger.py      # Rotas de documentação Swagger
├── swagger/            # Documentação Swagger/OpenAPI
│   └── pt-BR.yaml      # Especificação OpenAPI em português brasileiro
├── prompts/            # Arquivos de prompt para modelos de IA
│   └── job_vacancy_analysis.txt  # Template de prompt para análise de vagas
└── utils/              # Funções utilitárias
    ├── __init__.py
    └── helpers.py
```


## Integração Contínua

```
ci-cd/
└── docker/                  # Configurações Docker para a API
    ├── docker-compose.yml   # Arquivo de composição Docker
    └── .dockerignore        # Arquivos ignorados no build Docker
```

## Estrutura de Arquivos na Raiz

```
.
├── README.md              # Documentação principal do projeto
├── PROJECT_STRUCTURE.md   # Este arquivo - estrutura detalhada do projeto
├── CHANGELOG.md           # Histórico de mudanças
├── CONTRIBUTING.md        # Guia de contribuição
├── .gitignore             # Arquivos ignorados pelo Git
├── api/                   # Diretório da API Backend
├── desktop/               # Diretório da aplicação Desktop
├── ci-cd/                 # Configurações de CI/CD
└── docs/                  # Documentação adicional
    └── images/            # Imagens para documentação
```

## Banco de Dados

### Desktop (SQLite)
- Tabela `project`: Projetos criados pelo usuário
- Tabela `job_vacancy`: Vagas cadastradas

### API (PostgreSQL)
- Tabela `file`: Metadados e conteúdo de arquivos processados

