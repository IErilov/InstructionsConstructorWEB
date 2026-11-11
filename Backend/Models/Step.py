import uuid

from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from db import Base

if TYPE_CHECKING:
    from Models.Instruction import Instruction


class Step(Base):
    __tablename__ = "Steps"

    number: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    order: Mapped[str] = mapped_column(String(200), nullable=False)

    instruction_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("Instruction.id"),
        nullable=False
    )

    instruction: Mapped["Instruction"] = relationship(
        "Instruction",
        back_populates="steps"
    )

    def __repr__(self):
        return f"Шаг {self.number}: {self.title}"