from src.salary.entities.salary import Salary
from src.salary.entities.salary_grid import SalaryGrid
from src.staff.entities.users.staff import Staff
from src.treatments.entities.department import Department

from db.aestetica.tables import (
    Salary as SalaryTable,
    SalaryGrid as SalaryGridTable,
    Base, select, delete
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
    def get_salary(staff: Staff, department: Department) -> Salary | None:
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

            grid_query = select(SalaryGridTable).where(SalaryGridTable.salary == result.id)
            salary.grid = [
                SalaryGrid(
                    _id=sg.id,
                    limit=sg.limit,
                    percent=sg.percent
                )
                for sg in session.scalars(grid_query).all()
            ]

            return salary

    @staticmethod
    def get_salaries_by_staff(staff: Staff) -> list[Salary]:
        salary_query = select(SalaryTable).where((SalaryTable.staff == staff.name))
        salaries = []

        with Base() as session:
            for row in session.scalars(salary_query):
                salary = Salary(
                    staff=staff,
                    department=Department(name=row.department),
                    fix=row.fix
                )

                grid_query = select(SalaryGridTable).where(SalaryGridTable.salary == row.id)

                salary.grid = [
                    SalaryGrid(
                        _id=sg.id,
                        limit=sg.limit,
                        percent=sg.percent
                    )
                    for sg in session.scalars(grid_query).all()
                ]

                salaries.append(salary)

        return salaries
