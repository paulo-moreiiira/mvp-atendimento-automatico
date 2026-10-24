
# MVP de Atendimento Automático

## Sobre o projeto

Este projeto é um Produto Mínimo Viável (MVP) desenvolvido para demonstrar como orientar interessados durante o primeiro contato com um serviço digital.

A aplicação apresenta um fluxo guiado para identificar o dispositivo utilizado pelo interessado e fornecer orientações iniciais conforme as informações selecionadas.

O objetivo é reduzir dúvidas repetitivas no atendimento inicial e tornar a experiência mais simples e organizada.

## Problema identificado

O atendimento inicial exige respostas manuais para perguntas frequentes, como o tipo de dispositivo utilizado, o sistema operacional e a marca da televisão.

O MVP propõe organizar essas informações por meio de um formulário interativo, apresentando orientações de acordo com as seleções do usuário.

## Funcionalidades

- Identificação do tipo de dispositivo.
- Orientações para celulares Android e iPhone (iOS).
- Orientações para Smart TVs conforme a marca selecionada.
- Orientações para TV Box conforme o sistema escolhido.
- Validação de seleções inválidas ou incompletas.
- Interface com mensagens claras para o usuário.

## Tecnologias utilizadas

- Python 3.14
- Flask
- HTML
- CSS
- JavaScript
- pytest
- Git e GitHub
- GitHub Actions

## Arquitetura

A aplicação utiliza uma estrutura web simples, com Flask responsável pelo processamento das requisições e pelas validações no servidor.

A interface é construída com HTML, CSS e JavaScript. Os arquivos HTML são armazenados em `templates/`, enquanto os estilos ficam em `static/`.

Os testes automatizados estão organizados no diretório `tests/`.

## Estrutura do projeto

```text
mvp-atendimento-automatico/
├── .github/
│   └── workflows/
│       └── testes.yml
├── static/
│   └── style.css
├── templates/
│   └── index.html
├── tests/
│   └── test_app.py
├── app.py
├── requirements.txt
└── README.md
```

## Requisitos

- Python 3.14 ou compatível com as dependências utilizadas.
- pip.
- Git, caso queira clonar o repositório.

## Como executar o projeto

### 1. Clonar o repositório

```bash
git clone https://github.com/paulo-moreiiira/mvp-atendimento-automatico.git
cd mvp-atendimento-automatico
```

### 2. Criar um ambiente virtual

No Windows:

```powershell
python -m venv .venv
```

### 3. Ativar o ambiente virtual

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Instalar as dependências

```powershell
python -m pip install -r requirements.txt
```

### 5. Iniciar a aplicação

```powershell
python app.py
```

Depois, abra no navegador o endereço local indicado pelo Flask, normalmente `http://127.0.0.1:5000`.

## Como executar os testes

Com o ambiente virtual ativado, execute:

```powershell
python -m pytest -v
```

Os testes verificam o carregamento da página e os principais fluxos de seleção e validação do formulário.

## Integração contínua

O GitHub Actions utiliza o arquivo `.github/workflows/testes.yml` para executar os testes automaticamente em eventos de envio de código (`push`) e criação ou atualização de Pull Requests.

## Limitações do MVP

- O fluxo é uma demonstração de atendimento guiado.
- Não existe integração real com o WhatsApp nesta versão.
- As orientações de compatibilidade são informativas e não confirmam a compatibilidade real de dispositivos ou aplicativos.
- O escopo não inclui o processamento de pagamentos ou a renovação de serviços.

## Objetivo acadêmico

O projeto aplica conceitos de desenvolvimento web, validação de dados, testes automatizados, controle de versão, integração contínua e melhoria da experiência do usuário.

## Licença

Nenhuma licença foi definida até o momento.
