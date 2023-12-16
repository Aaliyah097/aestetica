import datetime

from src.staff.entities.users.staff import Staff


class Bonus:
    def __init__(self, staff: Staff,
                 date_begin: datetime.date,
                 date_end: datetime.date,
                 amount: float = 0,
                 _id: int = None,
                 comment: str | None = None):
        self.staff: Staff = staff
        self.date_begin: datetime.date = date_begin
        self.date_end: datetime.date = date_end
        self.amount = amount or 0
        self.id: int | None = _id
        if comment:
            self.comment = f"{comment} ({self.amount} руб.)"
        else:
            self.comment = ""

    def serialize(self) -> dict:
        return {
            'id': self.id,
            'staff': self.staff.serialize(),
            'date_begin': self.date_begin,
            'date_end': self.date_end,
            'amount': self.amount,
            'comment': self.comment,
        }

    def __add__(self, other):
        if not other:
            return self

        self.amount += other.amount
        self.comment += f" + {other.comment}"
        if other.date_end > self.date_end:
            self.date_end = other.date_end
        if other.date_begin < self.date_begin:
            self.date_begin = other.date_begin
        return self

    def __repr__(self):
        return str(self.serialize())
