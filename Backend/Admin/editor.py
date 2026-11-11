import uuid

from fastapi import Request
from starlette.responses import RedirectResponse
from sqlalchemy import select, func

from sqladmin import BaseView, expose

from Models.Instruction import Instruction
from Models.Step import Step


class InstructionEditor(BaseView):
    name = "Редактор"
    icon = "fa-solid fa-pen-to-square"

    @expose("/instruction-editor", methods=["GET", "POST"])
    async def editor(self, request: Request):
        session_maker = self._admin_ref.session_maker

        instruction_id = request.query_params.get("instruction_id")
        error = None

        async with session_maker() as session:

            # POST: действия с шагами
            if request.method == "POST":
                form = await request.form()

                action = form.get("action")
                selected_id = form.get("instruction_id")

                try:
                    selected_uuid = uuid.UUID(str(selected_id))

                    instruction = await session.get(
                        Instruction,
                        selected_uuid
                    )

                    if instruction is None:
                        raise ValueError("Инструкция не найдена")

                    if action == "create":
                        title = str(form.get("title", "")).strip()
                        order = str(form.get("order", "")).strip()

                        if not title or not order:
                            raise ValueError("Заполни название и описание шага")

                        # Блокируем строку инструкции,
                        # чтобы параллельное создание не дало одинаковые номера.
                        await session.execute(
                            select(Instruction)
                            .where(Instruction.id == selected_uuid)
                            .with_for_update()
                        )

                        max_number = await session.scalar(
                            select(func.max(Step.number))
                            .where(Step.instruction_id == selected_uuid)
                        )

                        new_step = Step(
                            number=(max_number or 0) + 1,
                            title=title,
                            order=order,
                            instruction_id=selected_uuid
                        )

                        session.add(new_step)

                    elif action == "edit":
                        step_id = uuid.UUID(str(form.get("step_id")))

                        step = await session.get(Step, step_id)

                        if step is None or step.instruction_id != selected_uuid:
                            raise ValueError("Шаг не найден")

                        title = str(form.get("title", "")).strip()
                        order = str(form.get("order", "")).strip()

                        if not title or not order:
                            raise ValueError("Заполни название и описание шага")

                        step.title = title
                        step.order = order

                    elif action == "delete":
                        step_id = uuid.UUID(str(form.get("step_id")))

                        step = await session.get(Step, step_id)

                        if step is None or step.instruction_id != selected_uuid:
                            raise ValueError("Шаг не найден")

                        await session.delete(step)

                    else:
                        raise ValueError("Неизвестное действие")

                    await session.commit()

                    return RedirectResponse(
                        url=f"{request.url.path}?instruction_id={selected_uuid}",
                        status_code=303
                    )

                except (ValueError, TypeError) as exc:
                    await session.rollback()
                    error = str(exc)

            # Получаем все инструкции для выбора
            instructions_result = await session.scalars(
                select(Instruction).order_by(Instruction.name)
            )
            instructions = list(instructions_result)

            selected_instruction = None
            steps = []

            if instruction_id:
                try:
                    selected_uuid = uuid.UUID(instruction_id)

                    selected_instruction = await session.get(
                        Instruction,
                        selected_uuid
                    )

                    if selected_instruction:
                        steps_result = await session.scalars(
                            select(Step)
                            .where(Step.instruction_id == selected_uuid)
                            .order_by(Step.number)
                        )
                        steps = list(steps_result)

                except ValueError:
                    error = "Некорректный ID инструкции"

            return await self.templates.TemplateResponse(
                request,
                "editor.html",
                {
                    "instructions": instructions,
                    "selected_instruction": selected_instruction,
                    "steps": steps,
                    "error": error
                }
            )