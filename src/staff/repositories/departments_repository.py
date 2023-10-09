from db.aestetica.tables import (
    Base,
    Department as DepartmentTable
)

from src.staff.entities.department import Department


class DepartmentsRepository:
    @staticmethod
    def get_all() -> list[Department]:
        with Base() as session:
            return [
                Department(name=d.name)
                for d in session.query(DepartmentTable).all()
            ]
