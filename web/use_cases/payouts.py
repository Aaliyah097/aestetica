import datetime

from app import app
from flask import render_template, request


from src.salary.repositories.payout_repository import PayoutRepository


@app.route('/payouts', methods=['GET', ])
def get_payouts_on_staff():
    staff_name = request.args.get('staff', None)
    if not staff_name:
        return 'expected arg ?staff=', 500

    return [p.serialize() for p in PayoutRepository.get_by_staff(staff_name)], 200


@app.route('/payouts/create', methods=['POST', 'GET'])
def create_payout():
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

    PayoutRepository.create(staff_name, on_date, amount)

    return 'ok', 200


@app.route('/payouts/<int:pk>/delete', methods=['POST', ])
def delete_payout(pk: int):
    PayoutRepository.delete_by_id(pk)

    return 'ok', 200
