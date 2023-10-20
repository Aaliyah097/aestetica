import datetime

from src.salary.entities.payout import Payout
from db.aestetica.tables import (
    Base,
    Payouts as PayoutsTable
)
from src.staff.repositories.staff_repository import StaffRepository


class PayoutRepository:
    @staticmethod
    def get_by_staff(staff_name: str) -> list[Payout]:
        staff = StaffRepository().get_staff_by_name(staff_name)
        if not staff:
            return []

        with Base() as session:
            return [
                Payout(
                    pk=p.id,
                    staff=staff,
                    on_date=p.on_date,
                    amount=p.amount
                )
                for p in session.query(PayoutsTable).filter(PayoutsTable.staff == staff.name).all()
            ]

    @staticmethod
    def delete_by_id(pk: int) -> None:
        with Base() as session:
            payout = session.query(PayoutsTable).get(pk)
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
            payout = PayoutsTable(
                staff=staff_name,
                on_date=on_date,
                amount=amount
            )
            session.add(payout)
            session.commit()
