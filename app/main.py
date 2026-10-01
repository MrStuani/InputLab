from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.routers import mice

app = FastAPI(title="Input Lab")


@app.get("/")
def root():
    return {"message": "Input Lab API"}


@app.get("/health")
def health(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"status": "ok", "database": "up"}




app.include_router(mice.router)