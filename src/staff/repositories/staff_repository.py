from src.staff.entities.users.staff import Staff
from src.staff.entities.users.doctor import Doctor
from src.staff.entities.users.assistant import Assistant
from src.staff.entities.users.technician import Technician
from src.staff.entities.role import Role


from db.aestetica.tables import Staff as StaffTable
from db.aestetica.tables import Base, select


class StaffFactory:
    @staticmethod
    def create_staff(name: str,
                     staff_role: Role) -> Staff:
        if staff_role.name == 'Рабочее место доктора':
            new_staff = Doctor(name=name)
        elif staff_role.name in ['Медсестра', "Ст. медсестра"]:
            new_staff = Assistant(name=name)
        elif staff_role.name == 'Техник':
            new_staff = Technician(name=name)
        else:
            new_staff = Staff(name=name)

        new_staff.role = staff_role

        return new_staff


class StaffRepository:
    @staticmethod
    def get_staff() -> list[Staff]:
        query = select(StaffTable)

        with Base() as session:
            return [
                StaffFactory.create_staff(
                    name=st.name,
                    staff_role=Role(
                        name=st.role
                    )
                )
                for st in session.scalars(query).all()
            ]
