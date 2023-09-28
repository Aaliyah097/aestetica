from src.staff.entities.users.staff import Staff
from src.staff.entities.users.assistant import Assistant
from src.staff.entities.users.anesthetist import Anesthetist
from src.staff.entities.department import Department
from src.salary.entities.salary_grid import SalaryGrid


class Salary:
    def __init__(self,
                 staff: Staff,
                 department: Department,
                 fix: float = 0):
        self.id: int | None = None
        self.staff: Staff = staff
        self.department: Department = department
        self.fix: float = fix if fix >= 0 else 0
        self._grid: list[SalaryGrid] = []
        self._volume: float = 0
        self._income: float = 0
        self._bonuses: list[float] = []

    def add_bonus(self, value: float) -> None:
        try:
            float(value)
        except ValueError:
            return

        self._bonuses.append(value)

    def add_award(self, value: float) -> None:
        try:
            float(value)
        except ValueError:
            return

        self._income += value

    @property
    def income(self) -> float:
        for bonus in self._bonuses:
            self._income += bonus

        return round(self._income, 2)

    @property
    def volume(self) -> float:
        return round(self._volume, 2)

    @volume.setter
    def volume(self, value: float):
        self._volume += value

        if len(self._grid) == 0:
            if isinstance(self.staff, Assistant) or isinstance(self.staff, Anesthetist):
                self._income = self.fix * self._volume
            else:
                self._income = self.fix
            return

        total = 0

        if self._grid[0].limit > self._volume:
            total = round(self._volume * self._grid[0].percent / 100, 2)
        else:
            for idx, dimension in enumerate(self._grid):
                prev_limit = self._grid[idx - 1].limit if idx > 0 else 0
                if dimension.limit <= self._volume:
                    total += round((dimension.limit - prev_limit) * dimension.percent / 100, 2)
                else:
                    total += round((self._volume - prev_limit) * dimension.percent / 100, 2)
                    break

        self._income = total

    @property
    def grid(self):
        return self._grid

    @grid.setter
    def grid(self, value: list[SalaryGrid]):
        value = sorted(value, key=lambda x: x.limit)
        self._grid = value

    def serialize(self) -> dict:
        return {
            'id': self.id,
            'staff': self.staff.serialize(),
            'department': self.department.serialize(),
            'fix': self.fix,
            'grid': [
                grid.serialize() for grid in self._grid
            ],
            'volume': self._volume,
            'income': self._income
        }

    def __repr__(self):
        return str(self.serialize())
