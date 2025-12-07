# <div align="center"><a href="https://brau.io"><img src="docs/images/job_match_logo.png" alt="Job Match" width="70%"></a></div>

## Job Match v0.1.0

[![X: @_brau_io](https://img.shields.io/badge/contact-@_brau_io-blue.svg?style=flat)](https://x.com/_brau_io)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/7121155e1f184c898f147ffdb7a85949)](https://app.codacy.com/gh/braulioti/job_match/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/)
[![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)](https://sqlite.org/)
[![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/en/stable/)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Swagger](https://img.shields.io/badge/-Swagger-%23Clojure?style=for-the-badge&logo=swagger&logoColor=white)](https://swagger.io/)
[![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)

Serviço de avaliação de currículos para avaliar o grau de aderência do currículo com a vaga.

Job Match é criado e mantido por [Bráulio Figueiredo](http://braulioti.com.br).
Novas atualizações do projeto podem ser acompanhadas através do X:
[@_brau_io](https://x.com/_brau_io).

## Índice

- [Estrutura do Projeto](#estrutura-do-projeto)
- [Tecnologias](#tecnologias)
- [Instalação](#instalação)
- [Versão Desktop](#versão-desktop)
  - [Build da versão](#build-da-versão)
  - [Arquivos e pastas que precisam ser distribuídos](#arquivos-e-pastas-que-precisam-ser-distribuídos)
  - [Configurações do arquivo servers](#configurações-do-arquivo-servers)
- [Projeto Backend API](#projeto-backend-api)
  - [Health Check Endpoint](#health-check-endpoint)
  - [API v1](#api-v1)
  - [Configuração das variáveis de ambiente](#configuração-das-variáveis-de-ambiente)
  - [Troubleshooting - Docling no Windows](#troubleshooting---docling-no-windows)
  - [Documentação de API - Swagger](#documentação-de-api---swagger)
- [Versionamento](#versionamento)
- [Autor](#autor)

## Estrutura do Projeto

Para uma visão detalhada da estrutura do projeto, consulte o arquivo [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md).

## Tecnologias

- Python 3.11 ou superior (recomendado para suporte completo e contínuo às bibliotecas de IA do Google)
  - Python 3.10 também funciona, mas o suporte será descontinuado em 2026
- Tkinter (incluído com Python)
- SQLite (Aplicação Desktop)
- Flask 3.0.0 ou superior
- Docker Engine 20.10 ou superior
- Docker Compose 2.0 ou superior
- Swagger Open API 3.0
- PostgreSQL 13 ou superior
- Flask-Migrate (Alembic)
- Dockling

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

### Configuração das variáveis de ambiente

A API utiliza variáveis de ambiente para configuração. Copie o arquivo `api/env.example` para `api/.env` e ajuste as variáveis conforme necessário

### Troubleshooting - Docling no Windows

Se você receber um erro como:
```
[WinError 1314] O cliente não tem o privilégio necessário
```

Isso ocorre porque o Hugging Face Hub (usado pelo docling) está tentando criar symlinks no Windows sem permissões adequadas. Para isso ative as configurações de desenvolvedor no windows

1. Abra **Configurações** do Windows
2. Vá para **Atualização e Segurança** > **Para desenvolvedores**
3. Ative o **Modo de Desenvolvedor**
4. Reinicie o computador

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

