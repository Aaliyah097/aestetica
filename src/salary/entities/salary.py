from src.staff.entities.users.staff import Staff
from src.staff.entities.users.assistant import Assistant
from src.staff.entities.department import Department
from src.salary.entities.salary_grid import SalaryGrid


class Salary:
    def __init__(self, _id: int,
                 staff: Staff,
                 department: Department,
                 fix: float = 0,):
        self.id: int = _id
        self.staff: Staff = staff
        self.department: Department = department
        self.fix: float = fix if fix >= 0 else 0
        self._grid: list[SalaryGrid] = []
        self._volume: float = 0
        self._income: float = 0

    @property
    def income(self) -> float:
        return self.income

    @property
    def volume(self) -> float:
        return self.volume

    @volume.setter
    def volume(self, value: float):
        self._volume = value

        if len(self._grid) == 0:
            if isinstance(self.staff, Assistant):
                self._income = self.fix * value
            else:
                self._income = self.fix

            return

        total = 0
        for idx, dimension in enumerate(self._grid):
            if self._grid[0].limit > value:
                total = round(value * self._grid[0].percent / 100, 2)
                break

            prev_limit = self._grid[idx - 1].limit if idx > 0 else 0
            if dimension.limit <= value:
                total += round((dimension.limit - prev_limit) * dimension.percent / 100, 2)
            else:
                total += round((value - prev_limit) * dimension.percent / 100)

        self._income = total

    @property
    def grid(self):
        return self.grid

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
