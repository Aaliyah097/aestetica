import datetime

from src.staff.entities.users.staff import Staff
from src.staff.entities.users.assistant import Assistant


class Bonus:
    def __init__(self, staff: Staff,
                 on_date: datetime.date,
                 amount: float = 0):
        if not isinstance(staff, Assistant):
            raise Exception("bonus is provided only for Assistants")

        self.staff: Staff = staff
        self.on_date: datetime.date = on_date
        self.amount = amount or 0

    def serialize(self) -> dict:
        return {
            'staff': self.staff.serialize(),
            'on_date': self.on_date,
            'amount': self.amount
        }

    def __repr__(self):
        return str(self.serialize())
