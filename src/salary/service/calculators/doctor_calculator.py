from src.staff.entities.users.staff import Staff
from src.staff.entities.department import Department
from src.treatments.entities.treatment import Treatment
from src.salary.entities.salary import Salary
from src.salary.repositories.salary_repository import SalaryRepository

from itertools import chain


class DoctorSalaryCalculator:
    def __init__(self):
        self.salary_repo: SalaryRepository = SalaryRepository()

    def calc(self, doctor: Staff, treatments: dict[Department, list[Treatment]]) -> tuple[list[Salary], list[Treatment]]:
        union_treatments = list(chain.from_iterable(treatments.values()))

        union_treatments.sort(key=lambda t: t.on_date, reverse=True)

        salaries = {
            dep: self.salary_repo.get_salary(staff=doctor, department=dep) or Salary(staff=doctor, department=dep)
            for dep in treatments
        }

        for treatment in union_treatments:
            volume = 0
            if treatment.markdown.is_history:
                continue

            if treatment.markdown.prev_treatment:
                volume = self.get_volume(
                    treatment.markdown.prev_treatment,
                    True
                )
                salaries[treatment.markdown.prev_treatment.department].volume = volume
            else:
                if not treatment.markdown.is_history:
                    volume = self.get_volume(treatment)
                    salaries[treatment.department].volume = volume

            if treatment.markdown:
                treatment.markdown.volume = volume

        return list(salaries.values()), union_treatments

    @staticmethod
    def get_volume(treatment: Treatment, is_submit: bool = False) -> float:
        if treatment.cost_wo_discount == 0:
            volume = 0
        elif treatment.staff.name == "Колотова Анастасия Валентиновна":
            if (treatment.discount * 100 / treatment.cost_wo_discount) > 10:
                volume = treatment.cost_wo_discount - (treatment.cost_wo_discount * 0.1)
            else:
                volume = treatment.cost
        elif (treatment.discount * 100 / treatment.cost_wo_discount) > 50:
            volume = treatment.cost_wo_discount - (treatment.cost_wo_discount * 0.2)
        else:
            volume = treatment.cost

        consumables_cost = treatment.consumables.cost if treatment.consumables else 0

        if is_submit:
            volume = (volume - consumables_cost) * 0.3
        else:
            if consumables_cost != 0:
                volume = (volume - consumables_cost) * 0.7
            else:
                volume = volume

        return volume
