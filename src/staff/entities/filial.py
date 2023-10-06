class Filial:
    def __init__(self, name: str,
                 db_address: str = None,
                 db_port: str = None,
                 db_name: str = None,
                 db_user: str = None,
                 db_password: str = None):
        self.name = name
        self.db_address: str | None = db_address
        self.db_port: str | None = db_port
        self.db_name: str | None = db_name
        self.db_user: str | None = db_user
        self.db_password: str | None = db_password

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
