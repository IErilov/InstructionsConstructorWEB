
from uuid import UUID

from sqladmin import BaseView, expose
from sqlalchemy import select, func

from db import async_session

from Models.Progress import Progress
from Models.Instruction import Instruction
from Models.Step import Step


class AnalyticsView(BaseView):
    name = "Analytics"
    icon = "fa-solid fa-chart-line"

    @expose("/analytics", methods=["GET"])
    async def analytics(self, request):

        instruction_id = request.query_params.get("instruction_id")

        async with async_session() as session:

            instructions_stmt = select(Instruction)

            instructions_result = await session.execute(
                instructions_stmt
            )

            instructions = instructions_result.scalars().all()

            # Данные по умолчанию
            context = {
                "instructions": instructions,
                "selected_instruction": None,
                "total_steps": 0,
                "total_users": 0,
                "completed_users": 0,
                "instruction_completion_percent": 0,
                "average_instruction_progress": 0,
                "steps": [],
            }

            if not instruction_id:
                return await self.templates.TemplateResponse(
                    request,
                    "analytics.html",
                    context,
                )

            try:
                instruction_uuid = UUID(instruction_id)
            except ValueError:
                return await self.templates.TemplateResponse(
                    request,
                    "analytics.html",
                    context,
                )

            instruction_stmt = select(Instruction).where(
                Instruction.id == instruction_uuid
            )

            instruction_result = await session.execute(
                instruction_stmt
            )

            selected_instruction = (
                instruction_result.scalar_one_or_none()
            )

            if selected_instruction is None:
                return await self.templates.TemplateResponse(
                    request,
                    "analytics.html",
                    context,
                )

            context["selected_instruction"] = selected_instruction


            total_steps_stmt = (
                select(func.count())
                .select_from(Step)
                .where(
                    Step.instruction_id == instruction_uuid
                )
            )

            total_steps_result = await session.execute(
                total_steps_stmt
            )

            total_steps = total_steps_result.scalar() or 0


            total_users_stmt = (
                select(
                    func.count(
                        func.distinct(Progress.anonymous_id)
                    )
                )
                .where(
                    Progress.Instruction_id == instruction_uuid
                )
            )

            total_users_result = await session.execute(
                total_users_stmt
            )

            total_users = total_users_result.scalar() or 0

            analytics_stmt = (
                select(
                    Progress.step_id,
                    func.count(
                        func.distinct(Progress.anonymous_id)
                    ).label("started"),
                    func.count(
                        func.distinct(Progress.anonymous_id)
                    ).filter(
                        Progress.completed_at.is_not(None)
                    ).label("completed"),
                )
                .join(
                    Step,
                    Step.id == Progress.step_id
                )
                .where(
                    Progress.Instruction_id == instruction_uuid,
                    Step.instruction_id == instruction_uuid,
                )
                .group_by(
                    Progress.step_id
                )
            )

            analytics_result = await session.execute(
                analytics_stmt
            )

            rows = analytics_result.all()

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
                    "completion_rate": round(
                        completion_rate, 2
                    ),
                    "problematic": completion_rate < 60,
                })

            completed_users = 0

            if total_steps > 0:

                completed_users_stmt = (
                    select(
                        Progress.anonymous_id
                    )
                    .join(
                        Step,
                        Step.id == Progress.step_id
                    )
                    .where(
                        Progress.Instruction_id == instruction_uuid,
                        Progress.completed_at.is_not(None),
                        Step.instruction_id == instruction_uuid,
                    )
                    .group_by(
                        Progress.anonymous_id
                    )
                    .having(
                        func.count(
                            func.distinct(Progress.step_id)
                        ) == total_steps
                    )
                )

                completed_users_result = await session.execute(
                    completed_users_stmt
                )

                completed_users = len(
                    completed_users_result.scalars().all()
                )

            # =====================================
            # ПРОЦЕНТ ПОЛНОГО ЗАВЕРШЕНИЯ
            # =====================================

            instruction_completion_percent = (
                completed_users / total_users * 100
                if total_users > 0
                else 0
            )

            # =====================================
            # СРЕДНИЙ ПРОГРЕСС ПОЛЬЗОВАТЕЛЕЙ
            # =====================================

            average_instruction_progress = 0

            if total_steps > 0 and total_users > 0:

                completed_steps_stmt = (
                    select(
                        Progress.anonymous_id,
                        func.count(
                            func.distinct(Progress.step_id)
                        ).label("completed_steps"),
                    )
                    .join(
                        Step,
                        Step.id == Progress.step_id
                    )
                    .where(
                        Progress.Instruction_id == instruction_uuid,
                        Progress.completed_at.is_not(None),
                        Step.instruction_id == instruction_uuid,
                    )
                    .group_by(
                        Progress.anonymous_id
                    )
                )

                completed_steps_result = await session.execute(
                    completed_steps_stmt
                )

                user_progress = completed_steps_result.all()

                if user_progress:
                    average_instruction_progress = (
                        sum(
                            min(row.completed_steps, total_steps)
                            / total_steps * 100
                            for row in user_progress
                        ) / total_users
                    )

            # =====================================
            # ПЕРЕДАЧА ДАННЫХ В ШАБЛОН
            # =====================================

            context.update({
                "total_steps": total_steps,
                "total_users": total_users,
                "completed_users": completed_users,

                "instruction_completion_percent": round(
                    instruction_completion_percent, 2
                ),

                "average_instruction_progress": round(
                    average_instruction_progress, 2
                ),

                "steps": analytics,
            })

        return await self.templates.TemplateResponse(
            request,
            "analytics.html",
            context,
        )
