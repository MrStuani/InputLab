from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class MeasurementSession(Base):
    __tablename__ = "measurement_session"

    id: Mapped[int] = mapped_column(primary_key=True)
    mouse_id: Mapped[int] = mapped_column(
        ForeignKey("mouse.id", ondelete="CASCADE"), index=True
    )
    measured_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    kind: Mapped[str] = mapped_column(String(20))            # "click" | "motion"
    unit: Mapped[str] = mapped_column(String(5), default="ms")  # "ms" | "us"
    reference_method: Mapped[str | None] = mapped_column(String(120))
    firmware_version: Mapped[str | None] = mapped_column(String(40))
    notes: Mapped[str | None] = mapped_column(Text)

    # estatísticas calculadas no backend
    sample_count: Mapped[int]
    mean: Mapped[float]
    min_value: Mapped[float]
    max_value: Mapped[float]
    std_dev: Mapped[float]
    p50: Mapped[float]
    p95: Mapped[float]
    p99: Mapped[float]

    samples: Mapped[list["Sample"]] = relationship(
        back_populates="session",
        cascade="all, delete-orphan",
        passive_deletes=True,
        order_by="Sample.position",
    )


class Sample(Base):
    __tablename__ = "sample"

    id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[int] = mapped_column(
        ForeignKey("measurement_session.id", ondelete="CASCADE"), index=True
    )
    position: Mapped[int]
    value: Mapped[float]

    session: Mapped[MeasurementSession] = relationship(back_populates="samples")