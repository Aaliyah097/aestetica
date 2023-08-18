import datetime
import json

import settings
from src.treatments.entities.treatment import Treatment
from src.staff.repositories.staff_repository import StaffFactory
from src.staff.entities.role import Role
from src.staff.entities.filial import Filial
from src.staff.entities.department import Department


from db.infodent.db import Connector
from db.infodent.repository import Repository


class TreatmentRepository:
    @staticmethod
    def get_all_treatments(filial: Filial,
                           date_begin: datetime.date = None,
                           date_end: datetime.date = None) -> list[Treatment]:

        if settings.Config.DEBUG:
            with open('src/treatments/repositories/treatments.json', 'rb') as file:
                response = json.load(file)
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
                name=row['SCHNAME'],
                client=row['CLIENTS_FULLNAME'],
                on_date=row['TREATDATE'],
                amount=row['AMOUNT'],
                cost_wo_discount=row['COST_WO_DISCOUNT'],
                discount=row['DISCOUNT']
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

            data.append(new_treatment)

        return data
