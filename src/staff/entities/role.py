from src.utils import remove_spaces


class Role:
    def __init__(self, name: str):
        name = remove_spaces(name)

        self.name = name

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def serialize(self) -> dict:
        return {
            'name': self.name
        }

    def __repr__(self):
        return str(self.serialize())
