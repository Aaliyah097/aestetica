import datetime

from src.staff.entities.users.staff import Staff


class Payout:
    def __init__(self, staff: Staff, on_date: datetime.date, amount: float = 0, pk: int = None):
        self.pk: int | None = pk
        self.staff: Staff = staff
        self.on_date: datetime.date = on_date
        self.amount: float = amount

    def serialize(self) -> dict:
        return {
            'id': self.pk,
            'staff': self.staff.serialize() if self.staff else None,
            'on_date': str(self.on_date),
            'amount': self.amount
        }

    def __repr__(self):
        return str(self.serialize())
