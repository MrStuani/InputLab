# InputLab
 
API e site para cadastrar mouses e guardar as medições de latência
feitas com o gamer-latency-meter. Projeto em desenvolvimento.
 
## Stack
 
- Python 3.12 e FastAPI
- PostgreSQL (via Docker)
- SQLAlchemy
 
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
python -m uvicorn app.main:app --reload
