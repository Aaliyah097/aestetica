from app import app
from flask import render_template, request

from src.staff.repositories.staff_repository import StaffRepository
from src.treatments.repositories.consumables_repository import ConsumablesRepository
from src.treatments.repositories.services_repository import ServicesRepository
from src.staff.entities.users.technician import Technician
from src.staff.service.staff_management_service import StaffManagementService

from src.utils import remove_spaces


@app.route('/staff', methods=['GET', ])
def list_staff():
    return render_template(
        'staff.html',
        staff=StaffRepository.get_staff(),
        services=ServicesRepository.get_all(),
        consumables=ConsumablesRepository().get_all(),
        technicians=list(filter(lambda st: isinstance(st, Technician), StaffRepository.get_staff()))
    )


@app.route('/staff/create', methods=['POST', ])
def create_staff():
    staff_name = request.form.get('name', None)
    role_name = request.form.get('role', None)

    if not staff_name or not role_name:
        return "expected form-data is 'name': str, 'role': str", 500

    service = StaffManagementService()
    service.create_staff(remove_spaces(staff_name), remove_spaces(role_name))

    return "ok", 200


@app.route('/staff/delete', methods=['POST', ])
def delete_staff():
    staff_name = request.args.get('staff', None)

    if not staff_name:
        return 'expected argument ?staff='

    StaffRepository().delete_staff_by_name(staff_name)

    return 'ok', 200


@app.route('/staff/update', methods=['POST', ])
def update_staff():
    staff_name = request.args.get('staff', None)

    if not staff_name:
        return 'expected argument ?staff='

    reduce_discount = request.json.get('reduce_discount', None)
    is_new = request.json.get('is_new', None)

    StaffRepository().update_staff_by_name(staff_name, is_new, reduce_discount)

    return 'ok', 200
