from sqladmin import ModelView

from Models.Instruction import Instruction
from Models.Step import Step


class InstructionAdmin(ModelView, model=Instruction):
    name = "Инструкция"
    name_plural = "Инструкции"
    icon = "fa-solid fa-book"

    column_list = [
        Instruction.id,
        Instruction.name,
        Instruction.order,
    ]

    column_details_list = [
        Instruction.id,
        Instruction.name,
        Instruction.order,
        Instruction.steps,
    ]

    column_searchable_list = [
        Instruction.name,
    ]

    form_columns = [
        Instruction.name,
        Instruction.order,
    ]


class StepAdmin(ModelView, model=Step):
    name = "Шаг"
    name_plural = "Шаги"

    can_create = False
    can_delete = False

    column_list = [
        Step.id,
        Step.number,
        Step.title,
        Step.order,
        Step.instruction
    ]

    column_details_list = column_list

    column_sortable_list = [Step.number]

    form_columns = [
        Step.title,
        Step.order
    ]