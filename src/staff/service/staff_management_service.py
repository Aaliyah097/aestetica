from src.staff.entities.role import Role
from src.staff.repositories.staff_repository import StaffRepository, StaffFactory
from src.salary.repositories.salary_repository import SalaryRepository
from src.salary.service.salary_management_service import SalaryManagementService


class StaffManagementService:
    def __init__(self):
        self.staff_repo: StaffRepository = StaffRepository()
        self.salary_repo: SalaryRepository = SalaryRepository()
        self.salary_m_service: SalaryManagementService = SalaryManagementService()

    # TODO override in publish-subscriber form
    # because Salary depends on Staff
    # so Staff should not depends on Salary
    def create_staff(self, staff_name: str, role_name: str) -> None:
        if not staff_name and not role_name:
            return None

        new_staff = StaffFactory.create_staff(name=staff_name, staff_role=Role(name=role_name))
        new_staff = self.staff_repo.create_staff(new_staff)

        if new_staff:
            self.salary_m_service.create_salary_for_staff(new_staff)
