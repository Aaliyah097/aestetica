from app import app
from flask import render_template

from src.treatments.repositories.treatments_repository import TreatmentRepository


@app.route('/treatments')
def list_treatments():
    return render_template(
        'treatments.html',
        treatments=TreatmentRepository.get_all_treatments(filial='Барвиха')
    )
