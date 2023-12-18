from db.aestetica.tables import (
    Base,
    select,
    Consumables as ConsumablesTable
)

from src.treatments.entities.consumables import Consumables
from src.treatments.entities.service import Service
from src.staff.entities.users.staff import Staff
from src.staff.repositories.staff_repository import StaffRepository
from src.treatments.repositories.services_repository import ServicesRepository


class ConsumablesRepository:
    @staticmethod
    def get_all() -> list[Consumables]:
        with Base() as session:
            return [
                Consumables(
                    technician=StaffRepository().get_staff_by_name(c.staff),
                    service=ServicesRepository().get_by_code(c.service),
                    cost=c.cost,
                    pk=c.id,
                    cost_new=c.cost_new
                )
                for c in session.scalars(select(ConsumablesTable)).all()
            ]

    @staticmethod
    def get_by_technician_and_service(technician: Staff | None, service: Service, amount: float = 1) -> Consumables:
        if not service:
            return None

        if technician:
            query = select(ConsumablesTable).where(
                ConsumablesTable.staff == technician.name,
                ConsumablesTable.service == service.code
            ).limit(1)
        else:
            query = select(ConsumablesTable).where(
                ConsumablesTable.staff.is_(None),
                ConsumablesTable.service == service.code
            ).limit(1)

        with Base() as session:
            consumables = session.scalars(query).first()

            return Consumables(
                service=service,
                technician=technician,
                cost=consumables.cost * amount,
                cost_new=consumables.cost_new * amount
            ) if consumables else Consumables(
                service=service,
                technician=technician,
                cost=0,
                cost_new=0
            )

    def create(self, technician_name: str, service_code: str, cost: float = 0, cost_new: float = 0) -> None:
        if technician_name:
            staff = StaffRepository().get_staff_by_name(technician_name)
            if not staff:
                raise NameError(f"Сотрудник с именем '{technician_name}' не существует")
        else:
            staff = None

        service = ServicesRepository().get_by_code(service_code)
        if not service:
            raise NameError(f"Услуга с кодом '{service_code}' не существует")

        print(self.get_by_technician_and_service(staff, service), technician_name)
        if self.get_by_technician_and_service(staff, service):
            return None

        with Base() as session:
            session.add(
                ConsumablesTable(
                    service=service_code,
                    staff=technician_name,
                    cost=cost,
                    cost_new=cost_new
                )
            )
            session.commit()

    @staticmethod
    def delete(pk: int) -> None:
        with Base() as session:
            consumables = session.get(ConsumablesTable, pk)
            if not consumables:
                return
            session.delete(consumables)
            session.commit()

    @staticmethod
    def update(pk: int, cost: float = 0, cost_new: float = 0) -> None:
        with Base() as session:
            consumables = session.get(ConsumablesTable, pk)
            if not consumables:
                return
            consumables.cost = cost
            consumables.cost_new = cost_new
            session.commit()
