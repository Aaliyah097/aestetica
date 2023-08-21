from db.aestetica.tables import (
    Base,
    Filial as FilialTable
)
from src.treatments.entities.filial import Filial


class FilialsRepository:
    @staticmethod
    def get_by_name(name: str) -> Filial | None:
        if not name:
            return None

        with Base() as session:
            filial = session.get(FilialTable, name)
            return Filial(
                name=filial.name
            ) if filial else None
