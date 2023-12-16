class Service:
    def __init__(self, name: str, code: str, is_submit: bool = False, is_double: bool = False):
        self.name: str = name
        self.code: str = code
        self.is_submit: bool = is_submit
        self.is_double: bool = is_double

    def serialize(self) -> dict:
        return {
            'name': self.name,
            'code': self.code,
            'is_submit': self.is_submit,
            'is_double': self.is_double

        }

    def __repr__(self):
        return str(self.serialize())

    def __eq__(self, other):
        if not other:
            return None

        return self.code == other.code
