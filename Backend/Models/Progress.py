import uuid
from sqlalchemy import Uuid, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from typing import TYPE_CHECKING

from db import Base

if TYPE_CHECKING:
    from Models.Instruction import Instruction


class Progress(Base):
    __tablename__ = "Progress"

    Instruction_id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    step_id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    anonymous_id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    completed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        pass