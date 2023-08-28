import json

from aestetica.tables import (
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


def update_assistants_fix():
    with Base() as session:
        query = select(StaffTable).where(or_(StaffTable.role == 'Ассистент',
                                             StaffTable.role == 'Ст. медсестра',
                                             StaffTable.role == 'Медсестра'))
        for staff in session.scalars(query).all():
            salary_query = select(SalaryTable).where(
                SalaryTable.staff == staff.name,
                SalaryTable.department == "Прочее"
            )
            for salary in session.scalars(salary_query).all():
                salary.fix = 5000
        session.commit()


if __name__ == '__main__':
    """sync"""
    # sync_services()
    # sync_roles()
    # sync_staff()
    # sync_departments()
    # sync_filials()
    update_assistants_fix()
