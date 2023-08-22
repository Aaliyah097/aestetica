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
        if not other:
            return None
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

