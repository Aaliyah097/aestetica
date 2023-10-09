from app import app
from flask import render_template, request

from src.treatments.repositories.consumables_repository import ConsumablesRepository


@app.route('/consumables/create', methods=['POST', ])
def create_consumables():
    staff = request.form.get('staff', None)
    service = request.form.get('service', None)
    cost = request.form.get('cost', 0)
    cost_new = request.form.get('cost_new', 0)

    if staff == "":
        staff = None

    if not service:
        return 'expected data {staff: str, service: str, cost: float}', 500

    try:
        ConsumablesRepository().create(staff, service, cost, cost_new)
    except NameError as e:
        return str(e), 500

    return 'ok', 200


@app.route('/consumables/<int:pk>/delete', methods=['POST', ])
def delete_consumables(pk):
    ConsumablesRepository().delete(pk)
    return 'ok', 200


@app.route('/consumables/<int:pk>/update', methods=['POST', ])
def update_consumables(pk):
    cost = request.form.get('cost', 0)
    cost_new = request.form.get('cost_new', 0)

    ConsumablesRepository().update(pk, cost, cost_new)
    return 'ok', 200
