import datetime

from src.staff.entities.users.staff import Staff


class Bonus:
    def __init__(self, staff: Staff,
                 on_date: datetime.date,
                 amount: float = 0,
                 _id: int = None):
        self.staff: Staff = staff
        self.on_date: datetime.date = on_date
        self.amount = amount or 0
        self.id: int | None = _id

    def serialize(self) -> dict:
        return {
            'id': self.id,
            'staff': self.staff.serialize(),
            'on_date': self.on_date,
            'amount': self.amount
        }

    def __repr__(self):
        return str(self.serialize())
