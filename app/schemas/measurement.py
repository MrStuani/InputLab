from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

Kind = Literal["click", "motion"]
Unit = Literal["ms", "us"]


class SessionMeta(BaseModel):
    kind: Kind
    unit: Unit = "ms"
    reference_method: str | None = Field(default=None, max_length=120)
    firmware_version: str | None = Field(default=None, max_length=40)
    notes: str | None = None


class SessionCreate(SessionMeta):
    samples: list[float] = Field(min_length=1, max_length=200_000)


class SessionRead(SessionMeta):
    model_config = ConfigDict(from_attributes=True)

    id: int
    mouse_id: int
    measured_at: datetime
    sample_count: int
    mean: float
    min_value: float
    max_value: float
    std_dev: float
    p50: float
    p95: float
    p99: float