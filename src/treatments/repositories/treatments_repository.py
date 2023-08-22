import datetime
import json

import settings
from src.treatments.entities.treatment import Treatment
from src.staff.repositories.staff_repository import StaffFactory
from src.staff.entities.role import Role
from src.treatments.entities.filial import Filial
from src.treatments.entities.department import Department
from src.treatments.repositories.services_repository import ServicesRepository
from src.treatments.repositories.filials_repository import FilialsRepository

from db.infodent.db import Connector
from db.infodent.repository import Repository


class TreatmentRepository:
    @staticmethod
    def get_all_treatments(filial: Filial | str,
                           date_begin: datetime.date = None,
                           date_end: datetime.date = None) -> list[Treatment]:

        if not isinstance(filial, Filial):
            filial = FilialsRepository.get_by_name(filial)

        if settings.Config.DEBUG:
            with open('src/treatments/repositories/treatments.json', 'rb') as file:
                response = json.load(file)[:10]
        else:
            connector = Connector(
                name=filial.db_name,
                address=filial.db_address,
                port=filial.db_port,
                user=filial.db_user,
                password=filial.db_password
            )
            response = Repository(connector).get_treatments(date_begin, date_end)

        data = []

        for row in response:
            new_treatment = Treatment(
                client=row['CLIENTS_FULLNAME'],
                on_date=row['TREATDATE'],
                amount=row['AMOUNT'],
                cost_wo_discount=row['COST_WO_DISCOUNT'],
                discount=row['DISCOUNT'],
                service=ServicesRepository.get_by_code(row['KODOPER']),
                tooth=row['TOOTHCODE']
            )
            new_treatment.staff = StaffFactory.create_staff(
                name=row['DNAME'],
                staff_role=Role(
                    name=row['DOCTOR_STDTYPENAME']
                )
            )
            new_treatment.filial = filial
            new_treatment.department = Department(
                name=row['DEPNAME']
            )
            new_treatment.technician = StaffFactory.create_staff(
                name=row['MECHANIC'],
                staff_role=Role(
                    name='Техник'
                )
            ) if row['MECHANIC'] else None

            data.append(new_treatment)

        return data
