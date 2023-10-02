import re

from src.salary.entities.salary import Salary
from src.staff.entities.department import Department
from src.staff.entities.users.staff import Staff
from src.salary.repositories.salary_repository import SalaryRepository
from src.treatments.entities.treatment import Treatment


class AnesthetistCalculator:
    def __init__(self):
        self.salary_repo: SalaryRepository = SalaryRepository()

    def calc(self, anesthetist: Staff, treatments: list[Treatment]) -> Salary:
        department = Department('Прочее')

        salary = self.salary_repo.get_salary(
            staff=anesthetist, department=department
        ) or Salary(staff=anesthetist, department=department)

        for treatment in treatments:
            match = re.findall(r'\d+', treatment.service.name)
            if len(match) == 0:
                continue

            hours = int(match[-1])

            if hours == 30:
                hours = 0.5

            salary.volume = hours * treatment.amount

        return salary
