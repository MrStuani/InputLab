# InputLab

API e site para cadastrar mouses e guardar as medições de latência
feitas com o gamer-latency-meter. Projeto em desenvolvimento.

## Stack

- Python 3.12 e FastAPI
- PostgreSQL (via Docker)
- SQLAlchemy e Alembic (migrations)
- pytest (testes)

## Como rodar

Pré-requisitos: Python 3.12+, Git e Docker Desktop.

```powershell
git clone https://github.com/MrStuani/InputLab.git
cd InputLab
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
docker compose up -d
alembic upgrade head
python -m uvicorn app.main:app --reload
```

- Documentação da API: http://127.0.0.1:8000/docs
- Teste de conexão com o banco: http://127.0.0.1:8000/health

## Testes

```powershell
docker compose exec db psql -U inputlab -d inputlab -c "CREATE DATABASE inputlab_test;"
pytest -q
```

## Rotas atuais

| Método | Rota | O que faz |
|---|---|---|
| POST | `/mice` | Cadastra um mouse |
| GET | `/mice` | Lista com busca (`q`) e paginação (`skip`, `limit`) |
| GET | `/mice/{id}` | Detalhe de um mouse |
| PATCH | `/mice/{id}` | Atualiza campos enviados |
| DELETE | `/mice/{id}` | Remove um mouse |

## Status

Em desenvolvimento. Semana 1 concluída: CRUD de mouses com testes.
Próximo: sessões de medição e importação de CSV/JSON.