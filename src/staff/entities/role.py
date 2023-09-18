from src.utils import remove_spaces


class Role:
    names = (
        "Бухгалтерия",
        "Не сотрудник",
        "Регистратура",
        "Завхоз",
        "Техник",
        "Медсестра",
        "Прочие",
        "Администратор_не исп",
        "Администратор",
        "Системный пользователь",
        "ADMIN",
        "Ст. медсестра",
        "Ассистент",
        "Рабочее место доктора",
        "Маркетинг",
        "Анестезиолог",
        "Рабочее место анестезиолога"
    )

    def __init__(self, name: str):
        name = remove_spaces(name)

        if not name or name not in self.names:
            name = "Не сотрудник"

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
