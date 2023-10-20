from db.aestetica.tables import (
    Base,
    Role as RoleTable
)

from src.staff.entities.role import Role


class RolesRepository:
    @staticmethod
    def get_all() -> list[Role]:
        with Base() as session:
            return [
                Role(name=r.name)
                for r in session.query(RoleTable).all()
            ]
