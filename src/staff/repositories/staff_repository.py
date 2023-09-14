from src.staff.entities.users.staff import Staff
from src.staff.entities.users.doctor import Doctor
from src.staff.entities.users.assistant import Assistant
from src.staff.entities.users.technician import Technician
from src.staff.entities.users.senior_assistant import SeniorAssistant
from src.staff.entities.users.administrator import Administrator
from src.staff.entities.users.manager import Manager

from src.staff.entities.role import Role

from db.aestetica.tables import (
    Staff as StaffTable,
    Base, select
)


class StaffFactory:
    @staticmethod
    def create_staff(name: str,
                     staff_role: Role) -> Staff:
        if staff_role.name == 'Рабочее место доктора':
            new_staff = Doctor(name=name)
        elif staff_role.name in ['Медсестра', "Ассистент"]:
            new_staff = Assistant(name=name)
        elif staff_role.name == 'Техник':
            new_staff = Technician(name=name)
        elif staff_role.name == "Ст. медсестра":
            new_staff = SeniorAssistant(name=name)
        elif staff_role.name == "Администратор":
            new_staff = Administrator(name=name)
        elif staff_role.name == 'ADMIN':
            new_staff = Manager(name=name)
        else:
            new_staff = Staff(name=name)

        new_staff.role = staff_role

        return new_staff


class StaffRepository:
    def get_amount_by_role(self, staff_class: type) -> int:
        return len(list(filter(
            lambda st: isinstance(st, staff_class),
            self.get_staff())))

    @staticmethod
    def get_staff() -> list[Staff]:
        query = select(StaffTable)

        employees = []
        with Base() as session:
            for st in session.scalars(query).all():
                staff = StaffFactory.create_staff(
                    name=st.name,
                    staff_role=Role(
                        name=st.role
                    )
                )
                staff.is_new = st.is_new
                employees.append(staff)
        return employees

    @staticmethod
    def _get_staff_by_name(staff_name: str) -> StaffTable | None:
        with Base() as session:
            staff = session.scalars(select(StaffTable).where(
                StaffTable.name.like(f"%{staff_name}%"))
            ).first()
            session.expunge_all()
            return staff

    def get_staff_by_name(self, name: str) -> Staff:
        staff = self._get_staff_by_name(name)

        if staff:
            return StaffFactory.create_staff(
                name=staff.name,
                staff_role=Role(
                    name=staff.role
                )
            )

    def create_staff(self, staff: Staff) -> Staff | None:
        if self._get_staff_by_name(staff.name):
            return

        with Base() as session:
            session.add(
                StaffTable(
                    name=staff.name,
                    role=staff.role.name
                )
            )
            session.commit()

        return self.get_staff_by_name(staff.name)
