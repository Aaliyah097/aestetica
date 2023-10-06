import json

from settings import Config
from src.staff.repositories.filials_repository import FilialsRepository
from src.treatments.repositories.services_repository import ServicesRepository
from db.infodent.repository import Repository, Connector

from src.treatments.entities.service import Service


def sync_services():
    service_repository = ServicesRepository()

    services = {}

    if Config.DEBUG:
        with open('db/data/services.json', 'r', encoding='utf-8') as file:
            for d in sorted(json.loads(file.read()), key=lambda x: x['SCHID'], reverse=True):
                if d['KODOPER'] in services or d['KODOPER'] == None or d['KODOPER'] == "":
                    continue
                services[d['KODOPER']] = d
    else:
        filials = FilialsRepository().get_all()
        for filial in filials:
            connector = Connector(
                address=filial.db_address,
                port=filial.db_port,
                name=filial.db_name,
                user=filial.db_user,
                password=filial.db_password
            )
            for d in sorted(Repository(connector=connector).get_services(), key=lambda x: x['SCHID'], reverse=True):
                if d['KODOPER'] in services or d['KODOPER'] == None or d['KODOPER'] == "":
                    continue
                services[d['KODOPER']] = d

    for service_code, service in services.items():
        if service_repository.get_by_code(service['KODOPER']):
            service_repository.update(service['KODOPER'], service['SCHNAME'])
        else:
            service_repository.create(
                Service(name=service['SCHNAME'], code=service['KODOPER'], is_submit=False)
            )


if __name__ == '__main__':
    sync_services()
