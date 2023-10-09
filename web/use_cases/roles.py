from app import app
from flask import render_template, request


from src.staff.repositories.roles_repository import RolesRepository


@app.route('/roles', methods=['GET', ])
def roles_list():
    return [r.serialize() for r in RolesRepository.get_all()], 200
