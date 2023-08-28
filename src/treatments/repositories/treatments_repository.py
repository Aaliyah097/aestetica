import datetime
import json

import settings
from src.treatments.entities.treatment import Treatment
from src.staff.repositories.staff_repository import StaffFactory
from src.staff.entities.role import Role
from src.staff.entities.filial import Filial
from src.staff.entities.department import Department
from src.treatments.repositories.services_repository import ServicesRepository
from src.staff.repositories.filials_repository import FilialsRepository

from db.infodent.db import Connector
from db.infodent.repository import Repository


class TreatmentRepository:
    def __init__(self, filial: Filial | str):
        if not isinstance(filial, Filial):
            filial = FilialsRepository.get_by_name(filial)
        self.filial = filial
        self.connector = Connector(
            name=filial.db_name,
            address=filial.db_address,
            port=filial.db_port,
            user=filial.db_user,
            password=filial.db_password
        )

    def get_history_treatment(self, lt_date: datetime.date,
                              tooth_code: int, doctor_name: str,
                              block_services_codes: tuple[str],
                              client: str
                              ) -> Treatment | None:
        if settings.Config.DEBUG:
            with open('src/treatments/repositories/treatments.json', 'rb') as file:
                treatments = [self.convert_treatment(row) for row in json.load(file)]

                treatments.sort(key=lambda t: t.on_date, reverse=True)

                history_treatment = list(filter(
                    lambda t: t.on_date <= lt_date and
                    t.client == client and
                    t.cost != 0 and
                    t.service.code not in block_services_codes and
                    t.staff.name == doctor_name,
                    treatments
                ))
                return history_treatment[-1] if len(history_treatment) > 0 else None
        else:
            response = Repository(self.connector).get_history_treatment(
                lt_date=lt_date,
                tooth_code=tooth_code,
                doctor_name=doctor_name,
                block_services_codes=block_services_codes,
                client=client
            )

        if response:
            return self.convert_treatment(response)
        else:
            return None

    def convert_treatment(self, row: dict) -> Treatment:
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
        new_treatment.filial = self.filial
        new_treatment.department = Department(
            name=row['DEPNAME']
        )
        new_treatment.technician = StaffFactory.create_staff(
            name=row['MECHANIC'],
            staff_role=Role(
                name='Техник'
            )
        ) if row['MECHANIC'] else None

        return new_treatment

    def get_all_treatments(self,
                           date_begin: datetime.date = None,
                           date_end: datetime.date = None) -> list[Treatment]:
        if settings.Config.DEBUG:
            with open('src/treatments/repositories/treatments.json', 'rb') as file:
                response = json.load(file)
        else:
            response = Repository(self.connector).get_treatments(date_begin, date_end)

        data = []

        for row in response:
            new_treatment = self.convert_treatment(
                row=row
            )
            data.append(new_treatment)

        return data
