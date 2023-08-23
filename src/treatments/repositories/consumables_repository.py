from db.aestetica.tables import (
    Base,
    select,
    Consumables as ConsumablesTable
)

from src.treatments.entities.consumables import Consumables
from src.treatments.entities.service import Service
from src.staff.entities.users.staff import Staff


class ConsumablesRepository:
    @staticmethod
    def get_by_technician_and_service(technician: Staff, service: Service) -> Consumables | None:
        if not service or not technician:
            return None

        query = select(ConsumablesTable).where(
            ConsumablesTable.staff == technician.name,
            ConsumablesTable.service == service.code
        ).limit(1)
        with Base() as session:
            consumables = session.scalars(query).first()

            return Consumables(
                service=service,
                technician=technician,
                cost=consumables.cost
            ) if consumables else None
