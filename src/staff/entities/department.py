from src.utils import remove_spaces


class Department:
    names = (
        "Виниры и коронки",
        "Детство",
        "Стоматология",
        "Лечение кариеса и каналов",
        "Имплантация",
        "Исправление прикуса",
        "Профессиональная гигиена и отбеливание",
        "Прочее",
    )

    def __init__(self, name: str):
        name = remove_spaces(name)

        if name not in self.names:
            name = "Стоматология"

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
