from src.staff.entities.users.staff import Staff
from src.treatments.entities.department import Department
from src.treatments.entities.service import Service
from src.treatments.entities.treatment import Treatment
from src.salary.entities.salary import Salary
from src.treatments.repositories.consumables_repository import ConsumablesRepository
from src.treatments.repositories.services_repository import ServicesRepository
from src.salary.repositories.salary_repository import SalaryRepository

from itertools import chain


class DoctorSalaryCalculator:
    def __init__(self):
        self.consumables_repo: ConsumablesRepository = ConsumablesRepository()
        self.submit_services: list[Service] = ServicesRepository.get_submits()
        self.salary_repo: SalaryRepository = SalaryRepository()

    def calc(self, doctor: Staff, treatments: dict[Department, list[Treatment]]) -> list[Salary]:
        union_treatments = list(chain.from_iterable(treatments.values()))
        union_treatments.sort(key=lambda t: t.on_date, reverse=True)

        salaries = {
            dep: self.salary_repo.get_salary(staff=doctor, department=dep) or Salary(staff=doctor, department=dep)
            for dep in treatments
        }

        for treatment in union_treatments:
            if treatment.service not in self.submit_services:
                salaries[treatment.department].volume = self.get_volume(treatment)
            else:
                prev_treatments = list(filter(
                    lambda t: t.on_date <= treatment.on_date and
                              t.client == treatment.client and
                              t.cost != 0 and
                              t.service not in self.submit_services,
                    union_treatments
                ))
                if len(prev_treatments) > 0:
                    salaries[prev_treatments[-1].department].volume = self.get_volume(prev_treatments[-1], True)

        return list(salaries.values())

    def get_volume(self, treatment: Treatment, is_submit: bool = False) -> float:
        if treatment.cost_wo_discount == 0:
            volume = 0
        elif (treatment.discount * 100 / treatment.cost_wo_discount) < 50:
            volume = treatment.cost
        else:
            volume = treatment.cost_wo_discount - (treatment.cost_wo_discount * 0.2)

        if treatment.technician:
            consumables = self.consumables_repo.get_by_technician_and_service(
                technician=treatment.technician,
                service=treatment.service
            )
            consumables_cost = consumables.cost if consumables else 0
        else:
            consumables_cost = 0

        if is_submit:
            volume = (volume - consumables_cost) * 0.3
        else:
            if consumables_cost != 0:
                volume = (volume - consumables_cost) * 0.7
            else:
                volume = volume

        return volume
