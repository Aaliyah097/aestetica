from src.staff.entities.users.staff import Staff
from src.staff.entities.department import Department
from src.treatments.entities.consumables import Consumables
from src.treatments.entities.service import Service
from src.treatments.entities.treatment import Treatment
from src.salary.entities.salary import Salary
from src.salary.repositories.salary_repository import SalaryRepository

from itertools import chain


class DoctorSalaryCalculator:
    def __init__(self):
        self.salary_repo: SalaryRepository = SalaryRepository()

    def calc(self, doctor: Staff, treatments: dict[Department, list[Treatment]]) -> list[Salary]:
        union_treatments = list(chain.from_iterable(treatments.values()))
        union_treatments.sort(key=lambda t: t.on_date, reverse=True)

        salaries = {
            dep: self.salary_repo.get_salary(staff=doctor, department=dep) or Salary(staff=doctor, department=dep)
            for dep in treatments
        }

        for treatment in union_treatments:
            if treatment.markdown and treatment.markdown.to_treatment_number:
                # TODO append toothcode
                prev_treatments = list(filter(
                    lambda t: t.markdown.number == treatment.markdown.number,
                    union_treatments
                ))
                if len(prev_treatments) > 0:
                    salaries[prev_treatments[-1].department].volume = self.get_volume(
                        prev_treatments[-1],
                        True
                    )
            else:
                if not treatment.markdown.is_history:
                    salaries[treatment.department].volume = self.get_volume(treatment)

        return list(salaries.values())

    def get_volume(self, treatment: Treatment, is_submit: bool = False) -> float:
        if treatment.cost_wo_discount == 0:
            volume = 0
        elif (treatment.discount * 100 / treatment.cost_wo_discount) < 50:
            volume = treatment.cost
        else:
            volume = treatment.cost_wo_discount - (treatment.cost_wo_discount * 0.2)

        consumables_cost = treatment.consumables.cost if treatment.consumables else 0

        if is_submit:
            volume = (volume - consumables_cost) * 0.3
        else:
            if consumables_cost != 0:
                volume = (volume - consumables_cost) * 0.7
            else:
                volume = volume

        return volume
