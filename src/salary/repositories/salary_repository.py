from src.salary.entities.salary import Salary
from src.salary.entities.salary_grid import SalaryGrid
from src.staff.entities.users.staff import Staff
from src.staff.entities.department import Department

from db.aestetica.tables import (
    Salary as SalaryTable,
    SalaryGrid as SalaryGridTable,
    Staff as StaffTable,
    Department as DepartmentTable,
    Base, select
)


class SalaryRepository:
    @staticmethod
    def get_salary(staff: Staff, department: Department) -> Salary | None:
        salary_query = select(SalaryTable).where(
            (StaffTable.name == staff.name) &
            (DepartmentTable.name == department.name)
        ).limit(1)

        with Base() as session:
            result = session.execute(salary_query).first()
            if not result:
                return None

            salary = Salary(
                _id=result[0].id,
                staff=staff,
                department=department,
                fix=result[0].fix
            )

            grid_query = select(SalaryGridTable).where(SalaryGridTable.salary == salary.id)
            salary.grid = [
                SalaryGrid(
                    _id=sg.id,
                    limit=sg.limit,
                    percent=sg.percent
                )
                for sg in session.scalars(grid_query).all()
            ]

            return salary
