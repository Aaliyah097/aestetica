from src.staff.entities.users.staff import Staff
from src.staff.entities.users.doctor import Doctor
from src.staff.entities.users.seller import Seller
from src.staff.entities.users.assistant import Assistant
from src.staff.entities.department import Department
from src.salary.repositories.salary_repository import SalaryRepository
from src.salary.entities.salary_grid import SalaryGrid
from src.staff.repositories.filials_repository import FilialsRepository
from src.staff.repositories.departments_repository import DepartmentsRepository

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
                        1_500_000: 20,
                        2_500_000: 25,
                        100_000_000: 30
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
        elif isinstance(staff, Seller):
            for filial in FilialsRepository.get_all():
                salary = self.salary_repo.create_salary(
                    staff=staff,
                    department=Department(name='Прочее'),
                    fix=25000,
                    filial=filial
                )

                if not salary:
                    continue

                default_grids = {
                    5_000_000: 2,
                    10_000_000: 2.5,
                    100_000_000: 3
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
            for filial in FilialsRepository.get_all():
                self.salary_repo.create_salary(
                    staff=staff,
                    department=Department(name='Прочее'),
                    fix=5000 if isinstance(staff, Assistant) else 0,
                    filial=filial
                )

    @staticmethod
    def export_salary(table_html: str) -> None:
        table = bs4.BeautifulSoup(table_html, "html.parser")
        df = pandas.read_html(table_html)[0]
        df.to_excel("data.xlsx")
