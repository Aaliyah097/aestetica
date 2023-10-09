class Service:
    def __init__(self, name: str, code: str, is_submit: bool = False):
        self.name: str = name
        self.code: str = code
        self.is_submit: bool = is_submit

    def serialize(self) -> dict:
        return {
            'name': self.name,
            'code': self.code,
            'is_submit' : self.is_submit,
        }

    def __repr__(self):
        return str(self.serialize())

    def __eq__(self, other):
        if not other:
            return None

        return self.code == other.code
