import datetime

from app import app
from flask import render_template, request


from src.salary.repositories.traffic_repository import TrafficRepository


@app.route('/traffic', methods=['GET', ])
def get_traffic_on_staff():
    staff_name = request.args.get('staff', None)
    if not staff_name:
        return 'expected arg ?staff=', 500

    return [t.serialize() for t in TrafficRepository.get_by_staff(staff_name)], 200


@app.route('/traffic/create', methods=['POST', 'GET'])
def create_traffic():
    staff_name = request.json.get('staff', None)
    on_date = request.json.get('on_date', datetime.date.today())
    amount = request.json.get('amount', 0)

    if not staff_name:
        return 'expected form-data: staff_name: str, on_date: %Y-%m-%d, amount: float', 500

    if type(on_date) == str:
        try:
            on_date = datetime.datetime.strptime(on_date, '%Y-%m-%d').date()
        except (AttributeError, ValueError):
            return "Expected date format is %Y-%m-%d", 500

    TrafficRepository.create(staff_name, on_date, amount)

    return 'ok', 200


@app.route('/traffic/<int:pk>/delete', methods=['POST', ])
def delete_traffic(pk: int):
    TrafficRepository.delete_by_id(pk)

    return 'ok', 200
