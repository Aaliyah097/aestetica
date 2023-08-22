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
    def get_submits() -> list[Service]:
        query = select(ServiceTable).where(ServiceTable.is_submit == True)
        with Base() as session:
            return [
                Service(
                    name=s.name,
                    code=s.code,
                    is_submit=s.is_submit
                )
                for s in session.scalars(query).all()
            ]

    @staticmethod
    def get_by_code(code: str) -> Service | None:
        if not code:
            return None

        with Base() as session:
            service = session.get(ServiceTable, code)
            return Service(
                name=service.name,
                code=service.code
            )

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
