from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from Core.Analitics.session import get_anonymous_id
from db import get_db as get_session
from Models.Progress import Progress


router = APIRouter(
    prefix="/instructions",
    tags=["Analytics"],
)

@router.get("/{instruction_id}/analytics")
async def get_instruction_analytics(
    instruction_id: UUID,
    session: AsyncSession = Depends(get_session),
):
    """
    Возвращает аналитику по каждому шагу инструкции:
    - сколько пользователей начали шаг
    - сколько завершили
    - процент завершения
    - является ли шаг потенциально проблемным
    """

    stmt = (
        select(
            Progress.step_id,
            func.count().label("started"),
            func.count(Progress.completed_at).label("completed"),
        )
        .where(
            Progress.Instruction_id == instruction_id
        )
        .group_by(
            Progress.step_id
        )
    )

    result = await session.execute(stmt)
    rows = result.all()

    analytics = []

    for row in rows:

        completion_rate = (
            row.completed / row.started * 100
            if row.started > 0
            else 0
        )

        analytics.append({
            "step_id": str(row.step_id),
            "started": row.started,
            "completed": row.completed,
            "completion_rate": round(completion_rate, 2),

            # Можно изменить порог
            "problematic": completion_rate < 60,
        })

    return {
        "instruction_id": str(instruction_id),
        "steps": analytics,
    }

@router.post("/{instruction_id}/steps/{step_id}/start")
async def start_step(
    instruction_id: UUID,
    step_id: UUID,
    anonymous_id: UUID = Depends(get_anonymous_id),
    session: AsyncSession = Depends(get_session),
):
    """
    Создаёт запись о начале прохождения шага.

    Если пользователь уже начинал этот шаг,
    новая запись не создаётся.
    """

    stmt = select(Progress).where(
        Progress.Instruction_id == instruction_id,
        Progress.step_id == step_id,
        Progress.anonymous_id == anonymous_id,
    )

    result = await session.execute(stmt)

    progress = result.scalar_one_or_none()

    if progress is None:

        progress = Progress(
            instruction_id=instruction_id,
            step_id=step_id,
            anonymous_id=anonymous_id,
        )

        session.add(progress)

        await session.commit()

        return {
            "message": "Step started",
            "instruction_id": str(instruction_id),
            "step_id": str(step_id),
        }

    return {
        "message": "Step already started",
        "instruction_id": str(instruction_id),
        "step_id": str(step_id),
    }

@router.post("/{instruction_id}/steps/{step_id}/complete")
async def complete_step(
    instruction_id: UUID,
    step_id: UUID,
    anonymous_id: UUID = Depends(get_anonymous_id),
    session: AsyncSession = Depends(get_session),
):
    """
    Отмечает шаг как завершённый.
    """

    stmt = select(Progress).where(
        Progress.Instruction_id == instruction_id,
        Progress.step_id == step_id,
        Progress.anonymous_id == anonymous_id,
    )

    result = await session.execute(stmt)

    progress = result.scalar_one_or_none()

    if progress is None:
        raise HTTPException(
            status_code=404,
            detail="Step progress not found. Start the step first.",
        )

    if progress.completed_at is None:

        progress.completed_at = datetime.now(timezone.utc)

        await session.commit()

    return {
        "message": "Step completed",
        "instruction_id": str(instruction_id),
        "step_id": str(step_id),
    }