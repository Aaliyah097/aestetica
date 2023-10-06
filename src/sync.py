import json

from settings import Config

from db.infodent.repository import Repository, Connector

from src.treatments.entities.service import Service

from src.staff.repositories.filials_repository import FilialsRepository
from src.treatments.repositories.services_repository import ServicesRepository
from src.salary.repositories.salary_repository import SalaryRepository

from db.aestetica.tables import (
    Base,
    Salary as SalaryTable,
    and_
)


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


def sync_staff():
    salary_repository = SalaryRepository()
    with Base() as session:
        salaries = session.query(SalaryTable).all()
        for salary in salaries:
            grid = salary_repository.get_grid_by_salary_id(salary.id)
            new_salary = SalaryTable(
                staff=salary.staff,
                department=salary.department,
                fix=salary.fix,
                filial='Барвиха'
            )
            session.add(new_salary)
            session.commit()

            new_salary = session.query(SalaryTable).filter(
                and_(
                    SalaryTable.staff == salary.staff,
                    SalaryTable.department == salary.department,
                    SalaryTable.filial == 'Барвиха'
                )
            ).first()

            salary_repository.create_grid_(new_salary.id, grid)
        session.commit()


def test():
    sync_staff()


if __name__ == '__main__':
    sync_staff()
