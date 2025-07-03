# MVP - Controle de Consumo de Água (Back-end)

Este repositório contém a API em Flask que serve de back-end para o MVP de controle de consumo de água, desenvolvido como parte do curso de Pós-Graduação em Full Stack Development da PUC-Rio.

## Tecnologias utilizadas

- Python
- Flask
- Flask-SQLAlchemy
- SQLite
- Flask-CORS
- Flasgger (Swagger)

## Funcionalidades

- Cadastro de consumo de água
- Listagem de todos os consumos
- Atualização de registro de consumo
- Exclusão de registro
- Busca de registro por ID (utilizado internamente)
- Documentação automática com Swagger

## Organização

- `app.py`: arquivo principal contendo as rotas, configuração do banco de dados e documentação
- `requirements.txt`: dependências do projeto

## Executando

1. Crie e ative um ambiente virtual:

python -m venv venv
venv\Scripts\activate

2. Instale as dependências:

pip install -r requirements.txt

3. Execute a aplicação:

python app.py

4. A API ficará disponível em:

http://127.0.0.1:5000

5. Acesse a documentação Swagger em:

http://127.0.0.1:5000/apidocs

## Observação

O banco de dados SQLite é gerado automaticamente na pasta `instance/` ao iniciar o app.