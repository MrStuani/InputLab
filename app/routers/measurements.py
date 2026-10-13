from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.measurement import MeasurementSession, Sample
from app.models.mouse import Mouse
from app.schemas.measurement import SessionCreate, SessionMeta, SessionRead
from app.services.stats import compute_stats

router = APIRouter(tags=["measurements"])


def build_session(db: Session, mouse_id: int, meta: SessionMeta, values: list[float]) -> MeasurementSession:
    if db.get(Mouse, mouse_id) is None:
        raise HTTPException(status_code=404, detail="Mouse não encontrado")
    stats = compute_stats(values)
    session = MeasurementSession(mouse_id=mouse_id, **meta.model_dump(), **stats)
    session.samples = [Sample(position=i, value=v) for i, v in enumerate(values)]
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


@router.post(
    "/mice/{mouse_id}/sessions",
    response_model=SessionRead,
    status_code=status.HTTP_201_CREATED,
)
def create_session(mouse_id: int, data: SessionCreate, db: Session = Depends(get_db)):
    meta = SessionMeta(**data.model_dump(exclude={"samples"}))
    return build_session(db, mouse_id, meta, data.samples)


@router.get("/mice/{mouse_id}/sessions", response_model=list[SessionRead])
def list_sessions(mouse_id: int, db: Session = Depends(get_db)):
    stmt = (
        select(MeasurementSession)
        .where(MeasurementSession.mouse_id == mouse_id)
        .order_by(MeasurementSession.measured_at.desc())
    )
    return db.scalars(stmt).all()


@router.get("/sessions/{session_id}", response_model=SessionRead)
def get_session(session_id: int, db: Session = Depends(get_db)):
    session = db.get(MeasurementSession, session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Sessão não encontrada")
    return session


@router.get("/sessions/{session_id}/samples", response_model=list[float])
def get_samples(session_id: int, db: Session = Depends(get_db)):
    session = db.get(MeasurementSession, session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Sessão não encontrada")
    return [s.value for s in session.samples]


@router.delete("/sessions/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_session(session_id: int, db: Session = Depends(get_db)):
    session = db.get(MeasurementSession, session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Sessão não encontrada")
    db.delete(session)
    db.commit()