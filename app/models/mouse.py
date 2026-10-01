from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Numeric, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Mouse(Base):
    __tablename__ = "mouse"
    __table_args__ = (
        UniqueConstraint("brand", "model", name="uq_mouse_brand_model"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    brand: Mapped[str] = mapped_column(String(80))
    model: Mapped[str] = mapped_column(String(120))
    sensor: Mapped[str | None] = mapped_column(String(80))
    weight_g: Mapped[int | None]
    connection: Mapped[str] = mapped_column(String(20), default="wired")
    polling_rate_hz: Mapped[int | None]
    switch_type: Mapped[str | None] = mapped_column(String(80))
    price: Mapped[Decimal | None] = mapped_column(Numeric(10, 2))
    notes: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )