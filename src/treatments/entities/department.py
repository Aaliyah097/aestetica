class Department:
    names = (
        "Виниры и коронки",
        "Детство",
        "Стоматология",
        "Лечение кариеса и каналов",
        "Имплантация",
        "Исправление прикуса",
        "Профессиональная гигиена и отбеливание",
    )

    def __init__(self, name: str):
        if name not in self.names:
            raise NameError(f"{name} not in {self.names}")

        self.name = name

    def serialize(self) -> dict:
        return {
            'name': self.name
        }

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)
