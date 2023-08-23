from src.treatments.entities.service import Service
from src.staff.entities.users.technician import Staff


class Consumables:
    def __init__(self, service: Service,
                 technician: Staff,
                 cost: float = 0):
        self.service = service
        self.technician = technician
        self.cost = cost if cost >= 0 else 0

    def serialize(self) -> dict:
        return {
            'service': self.service.serialize(),
            'technician': self.technician.serialize(),
            'cost': self.cost
        }

    def __repr__(self):
        return str(self.serialize())
