from fastapi import APIRouter, Depends, HTTPException, Query ,status
from sqlalchemy import or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.mouse import Mouse
from app.schemas.mouse import MouseCreate, MouseRead, MouseUpdate

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
def list_mice(
    q: str | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    stmt = select(Mouse).order_by(Mouse.brand, Mouse.model)
    if q:
        like = f"%{q}%"
        stmt = stmt.where(or_(Mouse.brand.ilike(like), Mouse.model.ilike(like)))
    return db.scalars(stmt.offset(skip).limit(limit)).all()

@router.get("/{mouse_id}", response_model=MouseRead)
def get_mouse(mouse_id: int, db: Session = Depends(get_db)):
    return get_mouse_or_404(db, mouse_id)

@router.patch("/{mouse_id}", response_model=MouseRead)
def update_mouse(mouse_id: int, data: MouseUpdate, db: Session = Depends(get_db)):
    mouse = get_mouse_or_404(db, mouse_id)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(mouse, field, value)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Já existe um mouse com essa marca e modelo")
    db.refresh(mouse)
    return mouse


@router.delete("/{mouse_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_mouse(mouse_id: int, db: Session = Depends(get_db)):
    mouse = get_mouse_or_404(db, mouse_id)
    db.delete(mouse)
    db.commit()