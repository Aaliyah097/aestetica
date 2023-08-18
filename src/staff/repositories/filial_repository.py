from src.staff.entities.filial import Filial
from db.aestetica.tables import (
    Base,
    Filial as FilialTable
)


class FilialRepository:
    @staticmethod
    def get_by_name(name: str) -> Filial:
        with Base() as session:
            filial = session.get(FilialTable, name)

            new_filial = Filial(name=filial.name)
            new_filial.db_name = new_filial.db_name
            new_filial.db_port = new_filial.db_port
            new_filial.db_name = new_filial.db_name
            new_filial.db_user = new_filial.db_user
            new_filial.db_password = new_filial.db_password

            return new_filial
