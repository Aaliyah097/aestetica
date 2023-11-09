from src.utils import remove_spaces


class Department:
    def __init__(self, name: str):
        name = remove_spaces(name)

        if name == "None":
            name = 'Стоматология'
        self.name = name or 'Стоматология'

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
