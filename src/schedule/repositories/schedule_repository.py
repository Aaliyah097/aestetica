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
    @staticmethod
    def get_all_schedule(filial: Filial | str,
                         date_begin: datetime.date = None,
                         date_end: datetime.date = None) -> list[Schedule]:
        if not isinstance(filial, Filial):
            filial = FilialsRepository.get_by_name(filial)

        if settings.Config.DEBUG:
            with open('src/schedule/repositories/schedule.json', 'rb') as file:
                response = json.load(file)
        else:
            connector = Connector(
                name=filial.db_name,
                address=filial.db_address,
                port=filial.db_port,
                user=filial.db_user,
                password=filial.db_password
            )
            response = Repository(connector).get_schedule(date_begin, date_end)

        data = []

        for row in response:
            new_schedule = Schedule(
                on_date=row['WDATE'],
                staff=StaffFactory.create_staff(
                    name=row['DNAME'],
                    staff_role=Role(name=row['DOCTOR_STDTYPENAME'])
                ),
                filial=filial,
                department=Department(name=row['DEPNAME'])
            )
            data.append(new_schedule)

        return data
