from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from Core.Analitics.session import get_anonymous_id
from db import get_db as get_session
from Models.Progress import Progress
from Models.Step import Step


router = APIRouter(
    prefix="/instructions",
    tags=["Analytics"],
)


@router.get("/{instruction_id}/analytics")
async def get_instruction_analytics(
    instruction_id: UUID,
    session: AsyncSession = Depends(get_session),
):
    # Общее количество шагов в инструкции
    total_steps_stmt = (
        select(func.count())
        .select_from(Step)
        .where(Step.Instruction_id == instruction_id)
    )

    total_steps_result = await session.execute(total_steps_stmt)

    total_steps = total_steps_result.scalar() or 0


    # Статистика по каждому шагу
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
            "problematic": completion_rate < 60,
        })


    # Сколько пользователей начали инструкцию
    users_stmt = (
        select(
            func.count(
                func.distinct(Progress.anonymous_id)
            )
        )
        .where(
            Progress.Instruction_id == instruction_id
        )
    )

    users_result = await session.execute(users_stmt)

    total_users = users_result.scalar() or 0


    # Пользователи, завершившие ВСЕ шаги
    completed_users = 0

    if total_steps > 0:

        completed_stmt = (
            select(
                Progress.anonymous_id
            )
            .where(
                Progress.Instruction_id == instruction_id,
                Progress.completed_at.is_not(None),
            )
            .group_by(
                Progress.anonymous_id
            )
            .having(
                func.count(
                    func.distinct(Progress.step_id)
                ) >= total_steps
            )
        )

        completed_result = await session.execute(completed_stmt)

        completed_users = len(
            completed_result.scalars().all()
        )


    # Процент пользователей, прошедших инструкцию полностью
    instruction_completion_percent = (
        completed_users / total_users * 100
        if total_users > 0
        else 0
    )


    return {
        "instruction_id": str(instruction_id),

        "total_steps": total_steps,

        "total_users": total_users,

        "completed_users": completed_users,

        "instruction_completion_percent": round(
            instruction_completion_percent,
            2,
        ),

        "steps": analytics,
    }

@router.post("/{instruction_id}/steps/{step_id}/start")
async def start_step(
    instruction_id: UUID,
    step_id: UUID,
    anonymous_id: UUID = Depends(get_anonymous_id),
    session: AsyncSession = Depends(get_session),
):
    stmt = select(Progress).where(
        Progress.Instruction_id == instruction_id,
        Progress.step_id == step_id,
        Progress.anonymous_id == anonymous_id,
    )

    result = await session.execute(stmt)
    progress = result.scalar_one_or_none()

    if progress is None:
        progress = Progress(
            Instruction_id=instruction_id,
            step_id=step_id,
            anonymous_id=anonymous_id,
        )

        session.add(progress)
        await session.commit()

    return {
        "message": "Step started" if progress is not None else "Step already started",
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