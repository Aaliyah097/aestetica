from src.staff.repositories.staff_repository import StaffRepository
from src.staff.service.staff_management_service import StaffManagementService
import json


def get_staff_from_repository():
    repo = StaffRepository()
    staff = repo.get_staff()
    print(staff)


def test_create_staff():
    service = StaffManagementService()

    with open('db/data/staff.json', 'r') as file:
        users = json.load(file)

        for user in users:
            if not user['DOCTOR_DNAME'] or not user['DOCTOR_STDTYPENAME']:
                continue

            service.create_staff(
                staff_name=user['DOCTOR_DNAME'],
                role_name=user['DOCTOR_STDTYPENAME']
            )