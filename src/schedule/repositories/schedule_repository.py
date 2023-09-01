import datetime
import json

import settings
from src.staff.repositories.staff_repository import StaffFactory
from src.staff.entities.department import Department
from src.staff.entities.role import Role
from src.schedule.entities.schedule import Schedule
from src.staff.entities.filial import Filial
from src.staff.repositories.filials_repository import FilialsRepository

from db.infodent.db import Connector
from db.infodent.repository import Repository


class ScheduleRepository:
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

    def _schedule_from_row(self, row: dict) -> Schedule:
        return Schedule(
            on_date=datetime.datetime.strptime(row['WDATE'], '%Y-%m-%d %H:%M:%S').date(),
            staff=StaffFactory.create_staff(
                name=row['DNAME'],
                staff_role=Role(name=row['DOCTOR_STDTYPENAME'])
            ),
            filial=self.filial,
            department=Department(name=row['DEPNAME']) if row['DEPNAME'] else None
        )

    def get_all_schedule(self,
                         date_begin: datetime.date = None,
                         date_end: datetime.date = None) -> list[Schedule]:
        if settings.Config.DEBUG:
            with open('src/schedule/repositories/schedule.json', 'rb') as file:
                response = json.load(file)
        else:
            response = Repository(self.connector).get_schedule(date_begin, date_end)

        data = []

        for row in response:
            data.append(self._schedule_from_row(row))

        return data
