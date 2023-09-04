import datetime
import time 

from app import app
from flask import render_template
from flask import request

from src.salary.service.salary_calculation_service import SalaryCalculationService
from src.salary.service.salary_management_service import SalaryManagementService
from src.staff.repositories.staff_repository import StaffRepository
from src.salary.repositories.salary_repository import SalaryRepository
from src.salary.repositories.bonus_repository import BonusRepository
from src.treatments.repositories.consumables_repository import ConsumablesRepository
from src.treatments.repositories.services_repository import ServicesRepository
from src.staff.entities.users.technician import Technician


@app.route('/consumables/create', methods=['POST', ])
def create_consumables():
    staff = request.args.get('staff', None)
    service = request.args.get('service', None)
    cost = request.args.get('cost', 0)

    if not all([staff, service]):
        return 'expected data {staff: str, service: str, cost: float}', 500

    try:
        ConsumablesRepository().create(staff, service, cost)
    except NameError as e:
        return str(e), 500

    return 'ok', 200


@app.route('/consumables/<int:pk>/delete')
def delete_consumables(pk):
    ConsumablesRepository().delete(pk)
    return 'ok', 200


@app.route('/bonus-by-staff')
def bonus_by_staff():
    staff = request.args.get('staff', None)
    if not staff:
        return "expected param 'staff'"

    return render_template(
        'bonus.html',
        bonuses=BonusRepository.get_by_staff(staff)
    )


@app.route('/bonus/<int:pk>/delete/', methods=['POST', ])
def delete_bonus(pk):
    BonusRepository.delete(pk)
    return 'ok', 200


@app.route('/bonus', methods=['POST', ])
def create_bonus():
    staff = request.form.get('staff', None)
    amount = request.form.get('amount', None)
    date_begin = request.form.get('date_begin', None)
    date_end = request.form.get('date_end', None)

    if not all([staff, amount, date_begin, date_end]):
        return 'expected params ?staff=&amount=&date_begin=&date_end=', 500

    try:
        date_begin = datetime.datetime.strptime(date_begin, '%Y-%m-%d').date()
        date_end = datetime.datetime.strptime(date_end, '%Y-%m-%d').date()
    except (AttributeError, ValueError):
        return "Expected date format is %Y-%m-%d", 500

    try:
        amount = float(amount)
    except ValueError:
        return "amount should be a number", 500

    BonusRepository.create(
        staff_name=staff,
        amount=amount,
        date_begin=date_begin,
        date_end=date_end
    )

    return 'ok', 200


@app.route('/staff', methods=['GET', ])
def list_staff():
    return render_template(
        'staff.html',
        staff=StaffRepository.get_staff(),
        services=ServicesRepository.get_all(),
        consumables=ConsumablesRepository().get_all(),
        technicians=list(filter(lambda st: isinstance(st, Technician), StaffRepository.get_staff()))
    )


@app.route('/staff/salary', methods=['GET', ])
def get_salary_by_staff():
    staff_name = request.args.get('staff', None)
    if not staff_name:
        return "expected param 'staff'", 500

    staff = StaffRepository().get_staff_by_name(staff_name)
    return render_template(
        'salary.html',
        salaries=SalaryRepository().get_salaries_by_staff(staff)
    )


@app.route('/salary/update/<int:pk>', methods=['POST', ])
def modify_salary(pk: int):
    fix = request.json.get('fix', 0)
    salary_grid = request.json.get('grid', [])

    if salary_grid == [] and fix == 0:
        return "expected params 'fix: int' and 'salary_grid: list[dict]'"

    for grid in salary_grid:
        if type(grid) != dict or 'limit' not in grid or 'percent' not in grid:
            return "param 'grid' should be as list[dict[str, int]]: grid=[{limit: int, percent: int}, ]"

    service = SalaryManagementService()
    service.modify_salary(salary_id=pk, fix=fix or 0, grid=salary_grid or [])

    return 'ok', 200


@app.route('/salary', methods=['GET', ])
def list_salary():
    time.sleep(2)
    filial_name = request.args.get('filial', None)
    date_begin = request.args.get('date_begin', None)
    date_end = request.args.get('date_end', None)

    if not all([filial_name, date_begin, date_end]):
        return 'Expected params are ?filial&date_begin&date_end', 500

    try:
        date_begin = datetime.datetime.strptime(date_begin, '%Y-%m-%d').date()
        date_end = datetime.datetime.strptime(date_end, '%Y-%m-%d').date()
    except (AttributeError, ValueError):
        return "Expected date format is %Y-%m-%d", 500

    service = SalaryCalculationService(filial_name, date_begin, date_end)

    doctors_salary_reports = service.doctors_cals()
    assistants_salary_report = service.assistants_calc()

    return render_template(
        'salary_table.html',
        doctors_report=doctors_salary_reports,
        assistants_report=assistants_salary_report,
        total_income=sum([salary.income for salary in doctors_salary_reports]) +
                     sum([salary.income for salary in assistants_salary_report]),
        date_begin=date_begin,
        date_end=date_end
    )


@app.route('/', methods=['GET', ])
def new_page():
    return render_template(
        'index.html'
    )
