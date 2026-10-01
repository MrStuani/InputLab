from datetime import datetime
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class Connection(str, Enum):
    wired = "wired"
    wireless_2_4 = "wireless_2_4"
    bluetooth = "bluetooth"


class MouseBase(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    brand: str = Field(min_length=1, max_length=80)
    model: str = Field(min_length=1, max_length=120)
    sensor: str | None = Field(default=None, max_length=80)
    weight_g: int | None = Field(default=None, gt=0, le=300)
    connection: Connection = Connection.wired
    polling_rate_hz: int | None = Field(default=None, gt=0)
    switch_type: str | None = Field(default=None, max_length=80)
    price: Decimal | None = Field(default=None, ge=0)
    notes: str | None = None


class MouseCreate(MouseBase):
    pass


class MouseRead(MouseBase):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    id: int
    created_at: datetime
    updated_at: datetime