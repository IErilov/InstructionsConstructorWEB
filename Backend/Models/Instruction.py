from sqlalchemy import Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, TYPE_CHECKING

from db import Base

if TYPE_CHECKING:
    from Models.Step import Step

class Instruction(Base):
    __tablename__ = "Instruction"
 
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    order: Mapped[str] = mapped_column(String(200), default="NOT ORDER")

    steps: Mapped[List["Step"]] = relationship(
        "Step",
        back_populates="instruction",
        cascade="all, delete-orphan",
        order_by="Step.order"
    )

    def __repr__(self):
        return self.name