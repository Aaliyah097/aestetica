import datetime
from src.staff.entities.users.staff import Staff
from src.staff.entities.filial import Filial
from src.staff.entities.department import Department


class Schedule:
    def __init__(self, on_date: datetime.date,
                 staff: Staff,
                 filial: Filial,
                 department: Department):
        self.on_date: datetime.date = on_date
        self.staff: Staff = staff
        self.filial: Filial = filial
        self.department: Department = department or Department("Прочее")
        self.bonus: float = 0

    def serialize(self) -> dict:
        return {
            'on_date': self.on_date,
            'staff': self.staff.serialize() if self.staff else None,
            'filial': self.filial.serialize() if self.filial else None,
            'department': self.department.serialize() if self.department else None,
            'bonus': self.bonus
        }

    def __repr__(self):
        return str(self.serialize())
