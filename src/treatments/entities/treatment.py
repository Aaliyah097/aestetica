import datetime
from src.staff.entities.users.staff import Staff
from src.treatments.entities.filial import Filial
from src.treatments.entities.department import Department
from src.treatments.entities.service import Service


class Treatment:
    def __init__(self, name: str, client: str, on_date: datetime.datetime,
                 service: Service,
                 amount: int = 1, cost_wo_discount: float = 0,
                 discount: float = 0):
        self.name: str = name
        self.client: str = client
        self.on_date: datetime.datetime = on_date
        self.service: Service | None = service
        self.amount: int = amount
        self.cost_wo_discount: float = cost_wo_discount
        self.discount: float = discount
        self.cost: float = self.cost_wo_discount - self.discount
        self.staff: Staff | None = None
        self.filial: Filial | None = None
        self.department: Department | None = None

    def serialize(self) -> dict:
        return {
            'name': self.name,
            'client': self.client,
            'on_date': self.on_date,
            'service': self.service.serialize(),
            'amount': self.amount,
            'cost_wo_discount': self.cost_wo_discount,
            'discount': self.discount,
            'cost': self.cost,
            'staff': self.staff.__repr__() or None,
            'filial': self.filial.__repr__() or None,
            'department': self.department.__repr__() or None
        }

    def __repr__(self):
        return str(self.serialize())
