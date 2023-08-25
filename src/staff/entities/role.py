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
    )

    def __init__(self, name: str):
        name = remove_spaces(name)

        if not name or name not in self.names:
            raise NameError(f"{name} not in {self.names}")

        self.name = name

    def serialize(self) -> dict:
        return {
            'name': self.name
        }

    def __repr__(self):
        return str(self.serialize())
