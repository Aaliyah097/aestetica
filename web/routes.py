import json
import datetime
from dataclasses import asdict

from app import app
from flask import render_template
from flask import request

from src.treatments.repositories.treatments_repository import TreatmentRepository
from src.salary.service.salary_calculation_service import SalaryCalculationService


@app.route('/treatments')
def list_treatments():
    return render_template(
        'treatments.html',
        treatments=TreatmentRepository.get_all_treatments(filial='Барвиха')
    )


@app.route('/salary')
def list_doctors_salary():
    filial_name = request.args.get('filial', None)
    date_begin = request.args.get('date_begin', None)
    date_end = request.args.get('date_end', None)

    if not all([filial_name, date_begin, date_end]):
        return 'Expected params are ?filial_name&date_begin&date_end', 500

    try:
        date_begin = datetime.datetime.strptime(date_begin, '%Y-%m-%d').date()
        date_end = datetime.datetime.strptime(date_end, '%Y-%m-%d').date()
    except (AttributeError, ValueError):
        return "Expected date format is %Y-%m-%d", 500

    try:
        service = SalaryCalculationService(filial_name, date_begin, date_end)
    except NameError as e:
        return str(e), 500

    try:
        salary_reports = service.doctors_cals()
    except Exception as e:
        return str(e), 500

    return render_template(
        'salary_table.html',
        report=salary_reports
    )


@app.route('/employees')
def new_page():
    return render_template(
        'employees.html'
    )
