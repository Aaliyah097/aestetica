import json

from aestetica.tables import (
    Base,
    Service as ServiceTable,
    Role as RoleTable,
    Staff as StaffTable,
    Department as DepartmentTable,
    Filial as FilialTable
)


def sync_services():
    with open('db/data/services.json', 'r') as file:
        services = json.load(file)

    with Base() as session:
        for service in services:
            if not service['SCHNAME'] or not service['KODOPER']:
                continue

            if session.get(ServiceTable, service['KODOPER']):
                continue

            session.add(
                ServiceTable(
                    name=service['SCHNAME'],
                    code=service['KODOPER']
                )
            )
        session.commit()


def sync_roles():
    with open('db/data/roles.json', 'r') as file:
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


def sync_staff():
    with open('db/data/staff.json', 'r') as file:
        users = json.load(file)

    with Base() as session:
        for user in users:
            if not user['DOCTOR_DNAME'] or not user['DOCTOR_STDTYPENAME']:
                continue

            if session.get(StaffTable, user['DOCTOR_DNAME']):
                continue

            session.add(
                StaffTable(
                    name=user['DOCTOR_DNAME'],
                    role=user['DOCTOR_STDTYPENAME']
                )
            )
        session.commit()


def sync_departments():
    with open('db/data/departments.json', 'r') as file:
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
    with Base() as session:
        for name in names:
            if session.get(FilialTable, name):
                continue

            session.add(
                FilialTable(
                    name=name
                )
            )
        session.commit()


if __name__ == '__main__':
    """sync"""
    sync_services()
    sync_roles()
    sync_staff()
    sync_departments()
    sync_filials()
