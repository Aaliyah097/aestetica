import datetime

from src.staff.entities.users.staff import Staff
from src.staff.repositories.staff_repository import StaffRepository
from src.salary.entities.bonus import Bonus
from db.aestetica.tables import Bonus as BonusTable
from db.aestetica.tables import (
    Base, select
)


class BonusRepository:
    @staticmethod
    def get_bonus(staff: Staff, date_begin: datetime.date, date_end: datetime.date) -> list[Bonus]:
        query = select(BonusTable).where(BonusTable.staff == staff.name,
                                         BonusTable.on_date >= date_begin,
                                         BonusTable.on_date <= date_end)

        with Base() as session:
            return [
                Bonus(
                    staff=staff,
                    on_date=b.on_date,
                    amount=b.amount,
                    _id=b.id
                )
                for b in session.scalars(query).all()
            ]

    @staticmethod
    def create(staff_name: str, amount: float, on_date: datetime.date) -> None:
        if not StaffRepository().get_staff_by_name(staff_name):
            return

        with Base() as session:
            session.add(
                BonusTable(
                    staff=staff_name,
                    amount=amount,
                    on_date=on_date
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
                    on_date=b.on_date,
                    _id=b.id
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
