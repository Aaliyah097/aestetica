from dataclasses import dataclass

from src.staff.entities.users.staff import Staff
from src.staff.repositories.staff_repository import StaffRepository
from src.salary.repositories.salary_repository import SalaryRepository
from src.salary.entities.salary import Salary


@dataclass
class StaffView:
    staff: Staff
    salary: list[Salary]


class StaffManagementService:
    def __init__(self):
        self.staff_repo: StaffRepository = StaffRepository()
        self.salary_repo: SalaryRepository = SalaryRepository()

    def get_staff_view(self) -> list[StaffView]:
        employee = self.staff_repo.get_staff()

        staff_views = []

        for staff in employee:
            staff_view = StaffView(
                staff=staff,
                salary=self.salary_repo.get_salaries_by_staff(staff)
            )
            staff_views.append(staff_view)

        return staff_views


