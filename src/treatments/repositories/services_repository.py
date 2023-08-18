from db.aestetica.tables import (
    Service as ServiceTable,
    select,
    Base
)

from src.treatments.entities.service import Service


class ServicesRepository:
    def save(self, service: Service):
        if self.get_by_code(service.code):
            return

        with Base() as session:
            session.add(ServiceTable(
                name=service.name,
                code=service.code
            ))
            session.commit()

    @staticmethod
    def get_by_code(code: str) -> Service | None:
        with Base() as session:
            return session.get(ServiceTable, code)

    @staticmethod
    def get_all() -> list[Service]:
        query = select(ServiceTable)

        with Base() as session:
            return [
                Service(
                    name=s.name,
                    code=s.code
                )
                for s in session.scalars(query).all()
            ]
