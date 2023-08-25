import datetime
from collections import defaultdict
from dataclasses import dataclass
from itertools import chain
from typing import Iterable

from src.salary.entities.salary import Salary
from src.staff.entities.users.doctor import Doctor
from src.staff.entities.users.staff import Staff
from src.treatments.entities.department import Department
from src.treatments.entities.filial import Filial
from src.treatments.entities.service import Service
from src.treatments.entities.treatment import Treatment
from src.treatments.repositories.filials_repository import FilialsRepository
from src.treatments.repositories.services_repository import ServicesRepository
from src.treatments.repositories.treatments_repository import TreatmentRepository

from src.salary.service.calculators.doctor_calculator import DoctorSalaryCalculator


@dataclass
class SalaryReport:
    staff: Staff
    income: float
    volume: float
    treatments: list[Treatment]


class SalaryCalculationService:
    """Расчет ЗП по филиалу.
    В расчет попадает сразу два периода 1-15, 16-31 и сразу все роли в организации.
    Задача сервиса собрать расчеты по каждой роли в единый документ."""

    def __init__(self, filial: Filial | str,
                 date_begin: datetime.date = None,
                 date_end: datetime.date = None):
        self.filial_repo: FilialsRepository = FilialsRepository()
        self.treatment_repo: TreatmentRepository = TreatmentRepository()

        if not isinstance(filial, Filial):
            self.filial = self.filial_repo.get_by_name(filial)
            if not filial:
                raise NameError(f"{filial} not in {Filial.names}")
        else:
            self.filial = filial

        self.date_begin = date_begin
        self.date_end = date_end

    def doctors_cals(self) -> list[SalaryReport]:
        treatments = self._split_treatments(
            self.treatment_repo.get_all_treatments(
                filial=self.filial,
                date_begin=self.date_begin,
                date_end=self.date_end
            )
        )

        salary_reports = []
        calculator = DoctorSalaryCalculator()

        for doctor, departments in treatments.items():
            salaries = calculator.calc(doctor, departments)
            salary_report = SalaryReport(
                staff=doctor,
                income=sum([salary.income for salary in salaries]),
                volume=sum([salary.volume for salary in salaries]),
                treatments=sorted(list(chain.from_iterable(departments.values())), key=lambda t: t.on_date)
            )
            salary_reports.append(salary_report)
        return salary_reports

    def total_calc(self):
        pass

    def calc_by_staff(self, doctor: Staff) -> tuple[Staff, list[Salary]]:
        pass

    @staticmethod
    def _split_treatments(treatments: list[Treatment]) -> dict[Staff, dict[Department, list[Treatment]]]:
        result = defaultdict(lambda: defaultdict(list))

        for treatment in treatments:
            if isinstance(treatment.staff, Doctor):
                result[treatment.staff][treatment.department].append(treatment)

        return result

    def get_history_treatment(self, treatment: Treatment) -> Treatment:
        pass
