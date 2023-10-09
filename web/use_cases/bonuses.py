import datetime

from flask import render_template, request
from app import app


from src.salary.repositories.bonus_repository import BonusRepository


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
    comment = request.form.get('comment', None)

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
        date_end=date_end,
        comment=comment
    )

    return 'ok', 200
