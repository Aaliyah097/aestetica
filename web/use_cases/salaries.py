import datetime
from collections import defaultdict

from flask import request, render_template
from app import app

from src.salary.repositories.salary_repository import SalaryRepository
from src.salary.service.salary_calculation_service import SalaryCalculationService
from src.staff.repositories.staff_repository import StaffRepository
from src.salary.service.salary_management_service import SalaryManagementService


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


@app.route('/salary', methods=['GET', ])
def list_salary():
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
    other_salary_reports = service.other_staff_calc()
    anesthetists_salary_report = service.anesthetists_calc()
    sellers_salary_report = service.sellers_calc()

    groups = defaultdict(list)
    assistants_groups = defaultdict(list)

    for salary in other_salary_reports:
        groups[salary.staff.role.name].append(salary)

    for salary in assistants_salary_report:
        assistants_groups[salary.staff.role.name].append(salary)

    return render_template(
        'salary_table.html',
        doctors_report=doctors_salary_reports,
        assistants_report=assistants_salary_report,
        assistants_reports_groups=assistants_groups,
        anesthetists_report=anesthetists_salary_report,
        sellers_report=sellers_salary_report,
        other_reports=groups,
        total_income=sum([salary.income for salary in doctors_salary_reports]) +
                     sum([salary.income for salary in assistants_salary_report]) +
                     sum([salary.income for salary in other_salary_reports]) +
                     sum([salary.income for salary in anesthetists_salary_report])+
                     sum([salary.income for salary in sellers_salary_report]),
        month_volume=service.month_volume,
        date_begin=date_begin,
        date_end=date_end
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


@app.route('/salary/export', methods=['POST', ])
def export_salary_report():
    table = request.json.get('table')
    SalaryManagementService.export_salary(table)

    return 'ok', 200
