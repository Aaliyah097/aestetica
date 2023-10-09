from src.salary.entities.salary import Salary
from src.salary.repositories.salary_repository import SalaryRepository
from src.schedule.entities.schedule import Schedule
from src.staff.entities.users.staff import Staff
from src.staff.entities.department import Department
from src.staff.entities.filial import Filial


class AssistantsSalaryCalculator:
    def __init__(self):
        self.salary_repo: SalaryRepository = SalaryRepository()

    def calc(self, assistant: Staff, schedule: list[Schedule], filial: Filial) -> Salary:
        on_date_set = set()
        department = Department('Прочее')

        salary = self.salary_repo.get_salary(
            staff=assistant, department=department, filial=filial
        ) or Salary(staff=assistant, department=department, filial=filial)

        for sch in schedule:
            if sch.on_date in on_date_set:
                continue

            salary.volume = 1

            if sch.bonus:
                salary.add_bonus(sch.bonus)

            on_date_set.add(sch.on_date)

        return salary
