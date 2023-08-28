from src.salary.entities.salary import Salary
from src.salary.entities.salary_grid import SalaryGrid
from src.staff.entities.users.staff import Staff
from src.staff.entities.department import Department

from db.aestetica.tables import (
    Salary as SalaryTable,
    SalaryGrid as SalaryGridTable,
    Base, select
)


class SalaryRepository:
    @staticmethod
    def delete_by_id( _id: int) -> None:
        with Base() as session:
            salary = session.get(SalaryTable, _id)
            if salary:
                session.delete(SalaryTable, _id)
            session.commit()

    @staticmethod
    def _get_salary_by_id(salary_id: int) -> SalaryTable:
        with Base() as session:
            return session.get(SalaryTable, salary_id)

    @staticmethod
    def modify_salary(salary_id: int, fix, grid: list[SalaryGrid]) -> None:
        with Base() as session:
            ex_salary = session.get(SalaryTable, salary_id)
            if not ex_salary:
                return

            ex_salary.fix = fix

            query = select(SalaryGridTable).where(SalaryGridTable.salary == salary_id)

            for old_grid in session.scalars(query).all():
                session.delete(old_grid)

            for new_grid in grid:
                new_salary_grid = SalaryGridTable(
                    salary=salary_id,
                    limit=new_grid.limit,
                    percent=new_grid.percent
                )
                session.add(new_salary_grid)

            session.commit()

    def create_salary(self, staff: Staff, department: Department, fix: float = 0) -> Salary | None:
        with Base() as session:
            query = select(SalaryTable).where(SalaryTable.staff == staff.name,
                                              SalaryTable.department == department.name)
            if session.scalar(query):
                return

            salary = SalaryTable(
                staff=staff.name,
                department=department.name,
                fix=fix
            )
            session.add(salary)
            session.commit()

            return self.get_salary(staff, department)

    @staticmethod
    def create_grid(salary: Salary, grid: list[SalaryGrid]) -> None:
        with Base() as session:
            for grid_row in grid:
                query = select(SalaryGridTable).where(
                    SalaryGridTable.salary == salary.id,
                    SalaryGridTable.percent == grid_row.percent,
                    SalaryGridTable.limit == grid_row.limit
                )

                if session.scalar(query):
                    continue

                salary_grid = SalaryGridTable(
                    salary=salary.id,
                    limit=grid_row.limit,
                    percent=grid_row.percent
                )
                session.add(salary_grid)
            session.commit()

    def get_salary(self, staff: Staff, department: Department) -> Salary | None:
        salary_query = select(SalaryTable).where(
            (SalaryTable.staff == staff.name) &
            (SalaryTable.department == department.name)
        ).limit(1)

        with Base() as session:
            result = session.scalars(salary_query).first()
            if not result:
                return None

            salary = Salary(
                staff=staff,
                department=department,
                fix=result.fix
            )
            salary.id = result.id

            salary.grid = self.get_grid_by_salary_id(salary.id)

            return salary

    @staticmethod
    def get_grid_by_salary_id(salary_id: int) -> list[SalaryGrid]:
        grid_query = select(SalaryGridTable).where(SalaryGridTable.salary == salary_id)
        grid = []
        with Base() as session:
            for sg in session.scalars(grid_query).all():
                salary_grid = SalaryGrid(
                    limit=sg.limit,
                    percent=sg.percent
                )
                salary_grid.id = sg.id
                grid.append(salary_grid)

        return grid

    def get_salaries_by_staff(self, staff: Staff) -> list[Salary]:
        salary_query = select(SalaryTable).where((SalaryTable.staff == staff.name))
        salaries = []

        with Base() as session:
            for row in session.scalars(salary_query):
                salary = Salary(
                    staff=staff,
                    department=Department(name=row.department),
                    fix=row.fix
                )
                salary.id = row.id

                salary.grid = self.get_grid_by_salary_id(salary.id)

                salaries.append(salary)

        return salaries
