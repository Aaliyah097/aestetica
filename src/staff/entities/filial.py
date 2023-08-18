class Filial:
    names = ('Курская', "Барвиха")

    def __init__(self, name: str):
        if name not in self.names:
            raise NameError(f"{name} not in {self.names}")

        self.name = name
        self.db_address: str | None = None
        self.db_port: str | None = None
        self.db_name: str | None = None
        self.db_user: str | None = None
        self.db_password: str | None = None

    def serialize(self) -> dict:
        return {
            'name': self.name,
            'db_address': self.db_address,
            'db_port': self.db_port,
            'db_name': self.db_name,
            'db_user': self.db_user,
            'db_password': self.db_password
        }

    def __repr__(self):
        return str(self.serialize())
