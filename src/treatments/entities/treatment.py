import datetime
from src.staff.entities.users.staff import Staff
from src.staff.entities.users.technician import Technician
from src.treatments.entities.filial import Filial
from src.treatments.entities.department import Department
from src.treatments.entities.service import Service


class Treatment:
    def __init__(self, client: str, on_date: datetime.datetime,
                 service: Service,
                 amount: int = 1, cost_wo_discount: float = 0,
                 discount: float = 0, tooth: int | None = None):
        self.client: str = client
        self.on_date: datetime.datetime = on_date
        self.service: Service | None = service
        self.amount: int = amount
        self.cost_wo_discount: float = cost_wo_discount or 0
        self.discount: float = discount or 0
        self.cost: float = self.cost_wo_discount - self.discount
        self.staff: Staff | None = None
        self.filial: Filial | None = None
        self.department: Department | None = None
        self.tooth: int | None = None if type(tooth) in [int, float] and tooth == 0 else tooth
        self.technician: Technician | None = None

    def serialize(self) -> dict:
        return {
            'client': self.client,
            'on_date': self.on_date,
            'service': self.service.serialize() if self.service else None,
            'amount': self.amount,
            'cost_wo_discount': self.cost_wo_discount,
            'discount': self.discount,
            'cost': self.cost,
            'staff': self.staff.serialize() if self.staff else None,
            'filial': self.filial.serialize() if self.filial else None,
            'department': self.department.serialize() if self.department else None,
            'tooth': self.tooth
        }

    def __repr__(self):
        return str(self.serialize())
