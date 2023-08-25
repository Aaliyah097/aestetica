from src.staff.entities.users.staff import Staff
from src.staff.entities.users.doctor import Doctor
from src.treatments.entities.department import Department
from src.salary.repositories.salary_repository import SalaryRepository
from src.salary.entities.salary_grid import SalaryGrid


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
        if isinstance(staff, Doctor):
            for dep_name in filter(lambda d: d != 'Прочее', Department.names):
                department = Department(name=dep_name)

                salary = self.salary_repo.create_salary(
                    staff=staff,
                    department=department,
                    fix=0
                )

                if not salary:
                    continue

                default_grids = {
                    1500000: 25,
                    2500000: 30
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
            self.salary_repo.create_salary(
                staff=staff,
                department=department,
                fix=0
            )
