from src.staff.entities.users.staff import Staff
from src.staff.entities.users.doctor import Doctor
from src.staff.entities.users.assistant import Assistant
from src.staff.entities.department import Department
from src.salary.repositories.salary_repository import SalaryRepository
from src.salary.entities.salary_grid import SalaryGrid
from src.staff.repositories.filials_repository import FilialsRepository
from src.staff.repositories.departments_repository import DepartmentsRepository

from src.salary.service.salary_calculation_service import SalaryReport
import bs4
import pandas


class SalaryManagementService:
    def __init__(self):
        self.salary_repo: SalaryRepository = SalaryRepository()

    def modify_salary(self, salary_id: int, fix: 0, grid: list[dict]) -> None:
        if not fix or fix < 0:
            fix = 0

        if not grid:
            grid = []

        salary_grid = [
            SalaryGrid(
                limit=g['limit'],
                percent=g['percent']
            )
            for g in grid
        ]

        self.salary_repo.modify_salary(salary_id=salary_id, fix=fix, grid=salary_grid)

    def create_salary_for_staff(self, staff: Staff) -> None:
        departments = DepartmentsRepository.get_all()
        if isinstance(staff, Doctor):
            for filial in FilialsRepository.get_all():
                for department in filter(lambda d: d.name != 'Прочее', departments):
                    salary = self.salary_repo.create_salary(
                        staff=staff,
                        department=department,
                        fix=0,
                        filial=filial
                    )

                    if not salary:
                        continue

                    default_grids = {
                        1500000: 20,
                        2500000: 25,
                        3000000: 30
                    }

                    self.salary_repo.create_grid(
                        salary=salary,
                        grid=[
                            SalaryGrid(
                                limit=key,
                                percent=value
                            )
                            for key, value in default_grids.items()
                        ]
                    )
        else:
            department = Department(name='Прочее')
            for filial in FilialsRepository.get_all():
                self.salary_repo.create_salary(
                    staff=staff,
                    department=department,
                    fix=5000 if isinstance(staff, Assistant) else 0,
                    filial=filial
                )

    @staticmethod
    def export_salary(table_html: str) -> None:
        table = bs4.BeautifulSoup(table_html, "html.parser")
        df = pandas.read_html(table_html)[0]
        df.to_excel("data.xlsx")
