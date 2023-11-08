import datetime

from src.staff.entities.users.staff import Staff
from src.staff.entities.users.administrator import Administrator
from src.staff.entities.users.assistant import Assistant
from src.staff.entities.users.senior_assistant import SeniorAssistant
from src.staff.repositories.staff_repository import StaffRepository
from src.salary.entities.bonus import Bonus
from db.aestetica.tables import Bonus as BonusTable
from db.aestetica.tables import (
    Base, select
)


class BonusRepository:
    @staticmethod
    def get_bonus(staff: Staff, on_date: datetime.date) -> Bonus | None:
        query = select(BonusTable).where(BonusTable.staff.like(f"%{staff.name}%"),
                                         BonusTable.date_begin <= on_date,
                                         BonusTable.date_end >= on_date).limit(1)

        with Base() as session:
            bonus = session.scalar(query)

            return Bonus(
                staff=staff,
                date_begin=bonus.date_begin,
                date_end=bonus.date_end,
                amount=bonus.amount,
                _id=bonus.id,
                comment=bonus.comment
            ) if bonus else None

    @staticmethod
    def create(staff_name: str, amount: float, date_begin: datetime.date, date_end: datetime.date, comment: str = None) -> None:
        staff = StaffRepository().get_staff_by_name(staff_name)
        if not staff:
            return

        if not isinstance(staff, Assistant) and not isinstance(staff, Administrator) and not isinstance(staff, SeniorAssistant):
            raise Exception(f"Надбавки недоступны для должности {staff.role.name}")

        with Base() as session:
            session.add(
                BonusTable(
                    staff=staff_name,
                    amount=amount,
                    date_begin=date_begin,
                    date_end=date_end,
                    comment=comment
                )
            )
            session.commit()

    @staticmethod
    def get_by_staff(staff_name: str) -> list[Bonus]:
        query = select(BonusTable).where(BonusTable.staff.like(f"%{staff_name}%"))

        with Base() as session:
            return [
                Bonus(
                    staff=StaffRepository().get_staff_by_name(staff_name),
                    amount=b.amount,
                    date_begin=b.date_begin,
                    date_end=b.date_end,
                    _id=b.id,
                    comment=b.comment
                )
                for b in session.scalars(query).all()
            ]

    @staticmethod
    def delete(pk: int) -> None:
        with Base() as session:
            bonus = session.get(BonusTable, pk)
            if not bonus:
                return

            session.delete(bonus)
            session.commit()
