from src.staff.entities.role import Role
from src.utils import remove_spaces


class Staff:
    def __init__(self, name: str):
        self.name: str = remove_spaces(name)
        self.role: Role | None = None
        self.is_new: bool = False
        self.reduce_discount: bool = True

    def serialize(self) -> dict:
        return {
            'name': self.name,
            'role': self.role.serialize() or None,
            'is_new': self.is_new,
            'reduce_discount': self.reduce_discount
        }

    def __repr__(self):
        return f"{self.role} {self.name}"

    def __eq__(self, other):
        if not other:
            return None
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

