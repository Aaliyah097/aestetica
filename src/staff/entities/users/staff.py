from src.staff.entities.role import Role


class Staff:
    def __init__(self, name: str):
        self.name: str = name
        self.role: Role | None = None

    def serialize(self) -> dict:
        return {
            'name': self.name,
            'role': self.role.serialize() or None
        }

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name

