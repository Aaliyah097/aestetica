from db.aestetica.tables import (
    Base,
    Filial as FilialTable
)
from src.staff.entities.filial import Filial


class FilialsRepository:
    @staticmethod
    def get_by_name(name: str) -> Filial | None:
        if not name:
            return None

        with Base() as session:
            filial = session.get(FilialTable, name)
            if not filial:
                return None

            new_filial = Filial(name=filial.name)
            new_filial.db_name = filial.db_name
            new_filial.db_port = filial.db_port
            new_filial.db_name = filial.db_name
            new_filial.db_user = filial.db_user
            new_filial.db_password = filial.db_password
            return new_filial
