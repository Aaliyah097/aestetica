from src.staff.entities.role import Role
from src.staff.repositories.staff_repository import StaffRepository, StaffFactory
from src.staff.service.staff_management_service import StaffManagementService
from src.staff.entities.users.technician import Technician
from src.staff.entities.users.doctor import Doctor
import json


def get_staff_from_repository():
    repo = StaffRepository()
    staff = repo.get_staff()
    print(staff)


def create_staff():
    service = StaffManagementService()

    with open('db/data/staff.json', 'rb') as file:
        users = json.load(file)

        for user in users:
            if not user['DOCTOR_DNAME'] or not user['DOCTOR_STDTYPENAME']:
                continue

            service.create_staff(
                staff_name=user['DOCTOR_DNAME'],
                role_name=user['DOCTOR_STDTYPENAME']
            )


def get_staff_amount_by_role():
    amount = StaffRepository().get_amount_by_role(Doctor)
    assert amount != 0
    print(amount)


def delete_staff():
    repo = StaffRepository()
    staff = repo.get_staff()

    for st in staff:
        repo.delete_staff(st)


def delete_staff_by_name(name: str):
    repo = StaffRepository()
    staff = repo.get_staff_by_name(name)
    repo.delete_staff(staff)


def create_staff_by_name(name: str, role_name: str):
    role = Role(role_name)
    staff = StaffFactory.create_staff(name, role)
    service = StaffManagementService()
    service.create_staff(name, role_name)


def test():
    """"""
    # create_staff()
    # delete_staff()
    # delete_staff_by_name("Арашкович Кирилл Александрович")
    # create_staff_by_name("Стоноженко Юлия Васильевна", "Старший администратор")
