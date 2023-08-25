from dataclasses import dataclass

from src.staff.entities.users.staff import Staff
from src.staff.entities.role import Role
from src.staff.repositories.staff_repository import StaffRepository, StaffFactory
from src.salary.repositories.salary_repository import SalaryRepository
from src.salary.entities.salary import Salary
from src.salary.service.salary_management_service import SalaryManagementService


@dataclass
class StaffView:
    staff: Staff
    salary: list[Salary]


class StaffManagementService:
    def __init__(self):
        self.staff_repo: StaffRepository = StaffRepository()
        self.salary_repo: SalaryRepository = SalaryRepository()
        self.salary_m_service: SalaryManagementService = SalaryManagementService()

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

    def create_staff(self, staff_name: str, role_name: str) -> None:
        if not staff_name and not role_name:
            return None

        new_staff = StaffFactory.create_staff(name=staff_name, staff_role=Role(name=role_name))
        new_staff = self.staff_repo.create_staff(new_staff)

        if new_staff:
            self.salary_m_service.create_salary_for_staff(new_staff)
