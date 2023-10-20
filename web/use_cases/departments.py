from app import app
from flask import render_template, request

from src.staff.repositories.departments_repository import DepartmentsRepository


@app.route('/departments', methods=['GET', ])
def departments_list():
    return [d.serialize() for d in DepartmentsRepository().get_all()], 200
