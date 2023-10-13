import datetime

from src.salary.entities.traffic import Traffic
from db.aestetica.tables import (
    Base,
    Traffic as TrafficTable
)
from src.staff.repositories.staff_repository import StaffRepository


class TrafficRepository:
    @staticmethod
    def get_by_staff(staff_name: str) -> list[Traffic]:
        staff = StaffRepository().get_staff_by_name(staff_name)
        if not staff:
            return []

        with Base() as session:
            return [
                Traffic(
                    pk=p.id,
                    staff=staff,
                    on_date=p.on_date,
                    amount=p.amount
                )
                for p in session.query(TrafficTable).filter(TrafficTable.staff == staff.name).all()
            ]

    @staticmethod
    def delete_by_id(pk: int) -> None:
        with Base() as session:
            payout = session.query(TrafficTable).get(pk)
            if not payout:
                return

            session.delete(payout)
            session.commit()

    @staticmethod
    def create(staff_name: str, on_date: datetime.date, amount: float = 0) -> None:
        staff = StaffRepository().get_staff_by_name(staff_name)
        if not staff:
            return

        with Base() as session:
            payout = TrafficTable(
                staff=staff_name,
                on_date=on_date,
                amount=amount
            )
            session.add(payout)
            session.commit()
