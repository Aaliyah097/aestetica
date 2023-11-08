import datetime
from src.staff.entities.users.staff import Staff
from src.staff.entities.users.technician import Technician
from src.staff.entities.filial import Filial
from src.staff.entities.department import Department
from src.treatments.entities.consumables import Consumables
from src.treatments.entities.service import Service

from hashlib import sha256


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
        self.consumables: Consumables | None = None
        self.markdown: MarkDown = MarkDown()

    def __hash__(self):
        data = (self.client, self.on_date,
                self.staff.name if self.staff else "",
                self.department.name if self.department else "",
                self.service.code if self.service else "",
                self.tooth if self.tooth else "")
        return hash(data)

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
            'tooth': self.tooth,
            'markdown': self.markdown.serialize() if self.markdown else None,
            'consumables': self.consumables.serialize() if self.consumables else None
        }

    def __repr__(self):
        return str(self.serialize())


class MarkDown:
    def __init__(self, is_history: bool = False, prev_treatment: Treatment | None = None, number: int | None = None):
        self.is_history = is_history
        self.volume: float = 0
        self.prev_treatment: Treatment | None = prev_treatment
        self.number: int | None = number

    def serialize(self) -> dict:
        return {
            'is_history': self.is_history,
            'prev_treatment': self.prev_treatment.serialize() if self.prev_treatment else None,
            'volume': self.volume,
            'number': self.number
        }

    def __repr__(self):
        return str(self.serialize())
