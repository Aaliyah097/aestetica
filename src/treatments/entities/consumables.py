from src.treatments.entities.service import Service
from src.staff.entities.users.technician import Staff


class Consumables:
    def __init__(self, service: Service,
                 technician: Staff,
                 cost: float = 0,
                 pk: int | None = None):
        self.service = service
        self.technician = technician
        self.cost = cost if cost >= 0 else 0
        self.pk: int | None = pk

    def serialize(self) -> dict:
        return {
            'id': self.pk,
            'service': self.service.serialize() if self.service else None,
            'technician': self.technician.serialize() if self.technician else None,
            'cost': self.cost
        }

    def __repr__(self):
        return str(self.serialize())
