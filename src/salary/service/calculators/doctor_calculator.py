from src.staff.entities.users.staff import Staff
from src.treatments.entities.department import Department
from src.treatments.entities.service import Service
from src.treatments.entities.treatment import Treatment
from src.salary.entities.salary import Salary
from src.treatments.repositories.consumables_repository import ConsumablesRepository
from src.treatments.repositories.services_repository import ServicesRepository
from src.salary.repositories.salary_repository import SalaryRepository


class DoctorSalaryCalculator:
    def __init__(self):
        self.consumables_repo: ConsumablesRepository = ConsumablesRepository()
        self.submit_services: list[Service] = ServicesRepository.get_submits()
        self.salary_repo: SalaryRepository = SalaryRepository()

    def calc(self, doctor: Staff, department: Department, treatments: list[Treatment]) -> Salary:
        treatments.sort(key=lambda t: t.on_date, reverse=True)

        salary = self.salary_repo.get_salary(
            staff=doctor,
            department=department,
        ) or Salary(
            staff=doctor,
            department=department,
        )
        volume = 0
        for treatment in treatments:
            if treatment.service not in self.submit_services:
                volume += self.get_volume(treatment)
            else:
                prev_treatments = list(filter(
                    lambda t: t.on_date <= treatment.on_date and
                    t.client == treatment.client and
                    t.cost != 0 and
                    t.service not in self.submit_services,
                    treatments
                ))

        salary.volume = volume

        return salary

    def get_volume(self, treatment: Treatment) -> float:
        is_submit = treatment.service in self.submit_services
        if is_submit:
            """request prev treatment"""

        # 1
        if treatment.cost_wo_discount == 0:
            volume = treatment.cost_wo_discount
        elif (treatment.discount * 100 / treatment.cost_wo_discount) < 50:
            volume = treatment.cost
        else:
            volume = treatment.cost_wo_discount - (treatment.cost_wo_discount * 0.2)

        if treatment.technician:
            consumables = self.consumables_repo.get_by_technician_and_service(
                technician=treatment.technician,
                service=treatment.service
            )
            if consumables:
                volume = (volume - consumables.cost) * 0.7

        return volume

