import datetime
from src.staff.entities.users.staff import Staff
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
                    amount=b.amount
                )
                for b in session.scalars(query).all()
            ]
