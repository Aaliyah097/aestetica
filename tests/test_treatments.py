from src.treatments.repositories.consumables_repository import ConsumablesRepository
from src.staff.repositories.staff_repository import StaffFactory
from src.staff.entities.users.technician import Technician
from src.treatments.entities.service import Service
from src.staff.entities.role import Role
from src.treatments.repositories.services_repository import ServicesRepository


def get_consumables():
    repo = ConsumablesRepository()
    technician = StaffFactory.create_staff(
        name='Лаборатория Денто-Эль',
        staff_role=Role(
            name='Техник'
        )
    )
    assert isinstance(technician, Technician)
    service = Service(
        name='',
        code='4.6.1'
    )
    consumables = repo.get_by_technician_and_service(
        technician=technician,
        service=service
    )
    print(consumables)


def get_submitting_services():
    repo = ServicesRepository()
    print(repo.get_submits())


def create_consumables():
    service_code = "6.2"
    tech = None
    cost = 2000

    repo = ConsumablesRepository()
    repo.create(technician_name=tech, service_code=service_code, cost=cost)


def update_consumables():
    pk = 1
    cost = 200

    repo = ConsumablesRepository()
    repo.update(pk, cost)


def test():
    update_consumables()
    # create_consumables()
    # get_consumables()
    # get_submitting_services()
    # get_treatments_list_from_source_db()
