from flask import request
from app import app

from src.treatments.repositories.services_repository import ServicesRepository
from src.sync import sync_services


@app.route('/services/update', methods=['POST'])
def services_update():
    name = request.json.get('name', None)
    is_submit = request.json.get('is_submit', None)
    code = request.json.get('code', None)
    is_double = request.json.get("is_double", None)
    fp = request.json.get("fp", None)
    so = request.json.get("sp", None)

    if code == None:
        return "'code' is not defined", 500

    ServicesRepository().update(code=code, name=name, is_submit=is_submit, is_double=is_double, fp=fp, sp=sp)

    return 'ok', 200


@app.route('/sync/services', methods=['GET'])
def services_sync():
    sync_services()
    return 'ok', 200
