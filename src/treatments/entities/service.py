class Service:
    def __init__(self, name: str, code: str):
        self.name: str = name
        self.code: str = code

    def serialize(self) -> dict:
        return {
            'name': self.name,
            'code': self.code
        }

    def __repr__(self):
        return str(self.serialize())
