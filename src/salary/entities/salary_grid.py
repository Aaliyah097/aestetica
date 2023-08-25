class SalaryGrid:
    def __init__(self, limit: float = 0, percent: float = 0):
        self.id: int | None = None
        self.limit: float = limit if limit >= 0 else 0
        self.percent: float = percent if percent >= 0 else 0

    def serialize(self) -> dict:
        return {
            'id': self.id,
            'limit': self.limit,
            'percent': self.percent
        }

    def __repr__(self):
        return str(self.serialize())
