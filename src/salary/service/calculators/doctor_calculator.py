from src.staff.entities.users.staff import Staff
from src.staff.entities.department import Department
from src.treatments.entities.treatment import Treatment
from src.salary.entities.salary import Salary
from src.salary.repositories.salary_repository import SalaryRepository
from src.staff.entities.filial import Filial

from itertools import chain


class DoctorSalaryCalculator:
    def __init__(self):
        self.salary_repo: SalaryRepository = SalaryRepository()

    def calc(self, doctor: Staff, treatments: dict[Department, list[Treatment]], filial: Filial) -> tuple[list[Salary], list[Treatment]]:
        union_treatments = list(chain.from_iterable(treatments.values()))

        union_treatments.sort(key=lambda t: t.on_date, reverse=True)

        salaries = {
            dep: self.salary_repo.get_salary(staff=doctor, department=dep, filial=filial)
                 or Salary(staff=doctor, department=dep, filial=filial)
            for dep in treatments
        }

        for treatment in union_treatments:
            volume = 0
            if treatment.markdown.is_history:
                continue

            # если прием является Сдачей работ, то у него будет предыдущий прием (сами работы)
            if treatment.markdown.prev_treatment:
                # объем нам нужен именно у самих работ, но под определенный процент, поэтому помечаем как is_submit=True
                # и передаем именно предыдущий прием
                prev_volume = self.get_volume(
                    treatment.markdown.prev_treatment,
                    False
                )
                volume = self.get_volume(
                    treatment.markdown.prev_treatment,
                    True,
                    withdraw=prev_volume
                )

                treatment.markdown.prev_treatment.markdown.volume = prev_volume
                salaries[treatment.markdown.prev_treatment.department].volume = volume
            else:
                # обычнй прием, который за 1 раз оказывается в полной мере,
                # только проверяем, что он в текущем отчетном периоде был выполнен
                if not treatment.markdown.is_history:
                    volume = self.get_volume(treatment)
                    salaries[treatment.department].volume = volume

            if treatment.markdown:
                treatment.markdown.volume = volume

        return list(salaries.values()), union_treatments

    @staticmethod
    def get_volume(treatment: Treatment, is_submit: bool = False, withdraw: float = 0) -> float:
        if treatment.department.name == 'Исправление прикуса':
            fp, sp = 0.5, 0.5
        else:
            fp, sp = 0.7, 0.3

        if treatment.cost_wo_discount == 0:
            volume = 0
        elif treatment.staff.name == "Колотова Анастасия Валентиновна":
            if (treatment.discount * 100 / treatment.cost_wo_discount) > 10:
                volume = treatment.cost_wo_discount - (treatment.cost_wo_discount * 0.1)
            else:
                volume = treatment.cost
        elif ((treatment.discount * 100 / treatment.cost_wo_discount) >= 50) and treatment.staff.reduce_discount:
            volume = treatment.cost_wo_discount - (treatment.cost_wo_discount * 0.2)
        else:
            volume = treatment.cost

        consumables_cost = (treatment.consumables.cost or 0) if treatment.consumables else 0
        consumables_cost_new = (treatment.consumables.cost_new or 0) if treatment.consumables else 0

        if treatment.staff.name == "Манукян Артавазд Генрикович":
            consumables_cost = 0
            consumables_cost_new = 0

        # volume -= withdraw

        if is_submit:
            volume = ( (volume - consumables_cost_new) * sp ) + ( (volume - consumables_cost_new) - (volume - consumables_cost) ) * fp
        else:
            # если техник не указан, то в полном объеме начисляем
            if treatment.technician:
                volume = (volume - consumables_cost) * fp
            else:
                volume = volume

        return volume
