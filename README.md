# Classifier

Serviço responsável por classificar transações em `FRAUDULENT` ou `GENUINE`.

## Requisitos

- Python3
- Pip3
- Python Virtualenv

### Como executar

```bash
# Crie um arquivo .env na raiz do repositório e altere as variáveis (se necessário)
cp .env.example .env

# Crie um ambiente virtual com virtualenv
python3 -m venv venv
source venv/bin/Activate

# Instale as dependências necessárias
pip3 install -r requirements.txt

# Execute o back-end em ambiente de desenvolvimento
uvicorn src.main:app --reload

# O back-end estará disponível em http://127.0.0.1:4000/docs
```
