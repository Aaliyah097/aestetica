class Service:
    def __init__(self, name: str, 
        code: str, 
        is_submit: bool = False, 
        is_double: bool = False,
        fp: float = 0,
        sp: float = 0):
        self.name: str = name
        self.code: str = code
        self.is_submit: bool = is_submit
        self.is_double: bool = is_double
        self.fp: float = fp if fp is not None else 0
        self.sp: float = sp if sp is not None else 0

    def serialize(self) -> dict:
        return {
            'name': self.name,
            'code': self.code,
            'is_submit': self.is_submit,
            'is_double': self.is_double,
            'fp': self.fp,
            'sp': self.sp
        }

    def __repr__(self):
        return str(self.serialize())

    def __eq__(self, other):
        if not other:
            return None

        return self.code == other.code
