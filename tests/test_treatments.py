from src.treatments.repositories.treatments_repository import TreatmentRepository
from src.staff.entities.filial import Filial
from src.treatments.entities.treatment import Treatment
from src.treatments.repositories.consumables_repository import ConsumablesRepository
from src.staff.repositories.staff_repository import StaffFactory
from src.staff.entities.users.technician import Technician
from src.treatments.entities.service import Service
from src.staff.entities.role import Role
from src.treatments.repositories.services_repository import ServicesRepository


def get_treatments_list_from_source_db():
    repo = TreatmentRepository()
    filial = Filial('Барвиха')
    treatments = repo.get_all_treatments(filial)
    assert isinstance(treatments[0], Treatment)


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


def test():
    # get_consumables()
    get_submitting_services()
    # get_treatments_list_from_source_db()
