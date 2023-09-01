import json

from db.aestetica.tables import (
    Base,
    select,
    or_,
    Service as ServiceTable,
    Role as RoleTable,
    Staff as StaffTable,
    Department as DepartmentTable,
    Filial as FilialTable,
    Salary as SalaryTable
)

from src.treatments.repositories.services_repository import ServicesRepository
from src.treatments.entities.service import Service

from src.staff.entities.filial import Filial
from src.staff.repositories.filials_repository import FilialsRepository


from src.staff.service.staff_management_service import StaffManagementService


def sync_services(file_path: str):
    repo = ServicesRepository()

    with open(file_path, 'r') as file:
        services = json.load(file)

    for service in services:
        if not service['SCHNAME'] or not service['KODOPER']:
            continue

        s = Service(
            name=service['SCHNAME'],
            code=service['KODOPER']
        )

        repo.create(s)


def sync_roles(file_path: str):
    with open(file_path, 'r') as file:
        roles = json.load(file)

    with Base() as session:
        for role in roles:
            if not role['STDTYPENAME']:
                continue

            if session.get(RoleTable, role['STDTYPENAME']):
                continue

            session.add(
                RoleTable(
                    name=role['STDTYPENAME']
                )
            )
        session.commit()


def sync_departments(file_path: str):
    with open(file_path, 'r') as file:
        departments = json.load(file)

    with Base() as session:
        for department in departments:
            if not department['DEPNAME']:
                continue

            if session.get(DepartmentTable, department['DEPNAME']):
                continue

            session.add(
                DepartmentTable(
                    name=department['DEPNAME']
                )
            )
        session.commit()


def sync_filials():
    names = ['Курская', "Барвиха"]
    repo = FilialsRepository()

    for name in names:
        repo.create(
            Filial(name)
        )


def sync_staff(file_path: str):
    service = StaffManagementService()

    with open(file_path, 'r') as file:
        staff = json.load(file)

    for st in staff:
        service.create_staff(
            staff_name=st['DOCTOR_DNAME'],
            role_name=st['DOCTOR_STDTYPENAME']
        )


def test_sync():
    """sync"""
    sync_services('db/data/services.json')
    sync_roles('db/data/roles.json')
    sync_departments('db/data/departments.json')
    sync_filials()
    sync_staff('db/data/staff.json')
