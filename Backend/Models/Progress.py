
import uuid

from sqlalchemy import Uuid, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from typing import Optional, TYPE_CHECKING

from db import Base


if TYPE_CHECKING:
    from Models.Instruction import Instruction


class Progress(Base):
    __tablename__ = "Progress"

    Instruction_id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    step_id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    anonymous_id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True, default=None)

    def __repr__(self):
        return (
            f"Progress(Instruction_id={self.Instruction_id}, "
            f"step_id={self.step_id}, "
            f"anonymous_id={self.anonymous_id}, "
            f"completed_at={self.completed_at})"
        )
