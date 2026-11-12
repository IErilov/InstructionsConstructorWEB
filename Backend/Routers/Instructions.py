from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_db

from Models.Instruction import Instruction
from Models.Step import Step


router = APIRouter(
    prefix="/instructions",
    tags=["Instructions"],
)


@router.get("")
async def get_instructions(
    session: AsyncSession = Depends(get_db),
):
    """
    Получить список всех инструкций.
    """

    result = await session.execute(
        select(Instruction).order_by(Instruction.name)
    )

    instructions = result.scalars().all()

    return [
        {
            "id": str(instruction.id),
            "name": instruction.name,
        }
        for instruction in instructions
    ]


@router.get("/{instruction_id}")
async def get_instruction(
    instruction_id: UUID,
    session: AsyncSession = Depends(get_db),
):
    """
    Получить инструкцию и её шаги.
    """

    result = await session.execute(
        select(Instruction).where(
            Instruction.id == instruction_id
        )
    )

    instruction = result.scalar_one_or_none()

    if instruction is None:
        raise HTTPException(
            status_code=404,
            detail="Instruction not found",
        )

    result = await session.execute(
        select(Step)
        .where(
            Step.instruction_id == instruction_id
        )
        .order_by(Step.number)
    )

    steps = result.scalars().all()

    return {
        "id": str(instruction.id),
        "name": instruction.name,
        "steps": [
            {
                "id": str(step.id),
                "number": step.number,
                "title": step.title,
                "order": step.order,
            }
            for step in steps
        ],
    }