import datetime
from collections import defaultdict
from dataclasses import dataclass
from itertools import chain

from src.salary.entities.salary import Salary
from src.staff.entities.users.doctor import Doctor
from src.staff.entities.users.staff import Staff
from src.staff.entities.department import Department
from src.staff.entities.filial import Filial
from src.treatments.entities.service import Service
from src.treatments.entities.treatment import Treatment, MarkDown
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
        self.treatment_repo: TreatmentRepository = TreatmentRepository(filial)
        self.submit_services: list[Service] = ServicesRepository.get_submits()

        self.date_begin = date_begin
        self.date_end = date_end

    def doctors_cals(self) -> list[SalaryReport]:
        treatments = self._split_treatments(
            self.treatment_repo.get_all_treatments(
                date_begin=self.date_begin,
                date_end=self.date_end
            )[:50]
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

    def _split_treatments(self, treatments: list[Treatment]) -> dict[Staff, dict[Department, list[Treatment]]]:
        result = defaultdict(lambda: defaultdict(list))

        treatment_number = 1

        for treatment in treatments:
            to_treatment_number = None

            if not isinstance(treatment.staff, Doctor):
                continue

            if treatment.service in self.submit_services:
                history_treatment = self.treatment_repo.get_history_treatment(
                    lt_date=treatment.on_date,
                    tooth_code=treatment.tooth,
                    doctor_name=treatment.staff.name,
                    block_services_codes=tuple([service.code for service in self.submit_services]),
                    client=treatment.client
                )
                if history_treatment:
                    to_treatment_number = treatment_number

                    history_markdown = MarkDown(
                        number=treatment_number,
                        to_treatment_number=None,
                        is_history=True
                    )

                    history_treatment.markdown = history_markdown
                    result[treatment.staff][treatment.department].append(history_treatment)

                    treatment_number += 1

            markdown = MarkDown(number=treatment_number,
                                is_history=False,
                                to_treatment_number=to_treatment_number)

            treatment.markdown = markdown

            result[treatment.staff][treatment.department].append(treatment)

            treatment_number += 1

        return result
