from sqladmin import BaseView, expose
from sqlalchemy import select, func

from db import async_session
from Models.Progress import Progress


class AnalyticsView(BaseView):
    name = "Analytics"
    icon = "fa-solid fa-chart-line"

    @expose("/analytics", methods=["GET"])
    async def analytics(self, request):

        async with async_session() as session:

            stmt = (
                select(
                    Progress.Instruction_id,
                    Progress.step_id,
                    func.count().label("started"),
                    func.count(Progress.completed_at).label("completed"),
                )
                .group_by(
                    Progress.Instruction_id,
                    Progress.step_id,
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
                "instruction_id": str(row.Instruction_id),
                "step_id": str(row.step_id),
                "started": row.started,
                "completed": row.completed,
                "completion_rate": round(completion_rate, 2),
                "problematic": completion_rate < 60,
            })

        return await self.templates.TemplateResponse(
    request,
    "analytics.html",
    {
        "rows": analytics,
    },
)