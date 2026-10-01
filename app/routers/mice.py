from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.mouse import Mouse
from app.schemas.mouse import MouseCreate, MouseRead

router = APIRouter(prefix="/mice", tags=["mice"])


def get_mouse_or_404(db: Session, mouse_id: int) -> Mouse:
    mouse = db.get(Mouse, mouse_id)
    if mouse is None:
        raise HTTPException(status_code=404, detail="Mouse não encontrado")
    return mouse


@router.post("", response_model=MouseRead, status_code=status.HTTP_201_CREATED)
def create_mouse(data: MouseCreate, db: Session = Depends(get_db)):
    mouse = Mouse(**data.model_dump())
    db.add(mouse)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Mouse já cadastrado (marca + modelo)")
    db.refresh(mouse)
    return mouse


@router.get("", response_model=list[MouseRead])
def list_mice(db: Session = Depends(get_db)):
    stmt = select(Mouse).order_by(Mouse.brand, Mouse.model)
    return db.scalars(stmt).all()


@router.get("/{mouse_id}", response_model=MouseRead)
def get_mouse(mouse_id: int, db: Session = Depends(get_db)):
    return get_mouse_or_404(db, mouse_id)