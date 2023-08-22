import datetime

from src.salary.repositories.salary_repository import SalaryRepository
from src.treatments.repositories.treatments_repository import TreatmentRepository
from src.treatments.entities.treatment import Treatment
from src.staff.repositories.filial_repository import FilialRepository

from src.treatments.entities.filial import Filial
from src.salary.entities.salary import Salary
from src.staff.entities.users.doctor import Doctor
from src.staff.entities.users.staff import Staff
from src.treatments.entities.department import Department


class SalaryCalculationService:
    """Расчет ЗП по филиалу.
    В расчет попадает сразу два периода 1-5, 16-31 и сразу все роли в организации.
    Задача сервиса собрать расчеты по каждой роли в единый документ."""

    def __init__(self):
        self.filial_repo: FilialRepository = FilialRepository()

    def calc(self, filial_name: str,
             date_begin: datetime.date = None,
             date_end: datetime.date = None):
        filial = self.filial_repo.get_by_name(filial_name)

        doctors_salaries = CalcDoctorSalary().calc(
            filial=filial,
            date_begin=date_begin,
            date_end=date_end
        )
        for s in doctors_salaries:
            print(s)


class CalcDoctorSalary:
    def __init__(self):
        self.treatment_repo: TreatmentRepository = TreatmentRepository()
        self.salary_repo: SalaryRepository = SalaryRepository()
        self.volumes: list[tuple[Staff, Department, float]] = []

    def calc(self, filial: Filial,
             date_begin: datetime.date = None,
             date_end: datetime.date = None
             ) -> list[Salary]:
        self._get_volume(
            filial=filial,
            date_begin=date_begin,
            date_end=date_end
        )
        return self._get_salaries()

    def _get_salaries(self) -> list[Salary]:
        salaries = []
        for doctor, department, volume in self.volumes:
            salary = self.salary_repo.get_salary(
                staff=doctor,
                department=department,
            )
            salary.volume = volume
            salaries.append(salary)
        return salaries

    def _get_volume(self, filial: Filial,
                    date_begin: datetime.date = None,
                    date_end: datetime.date = None):
        self.volumes = []

        treatments = self.treatment_repo.get_all_treatments(
            filial=filial,
            date_begin=date_begin,
            date_end=date_end
        )
        for treatment in treatments:
            # rule 1
            if not isinstance(treatment.staff, Doctor):
                continue

            self._set_doctor_volume(
                treatment=treatment
            )

    def _set_doctor_volume(self, treatment: Treatment) -> None:
        # rule 2
        if (treatment.discount * 100 / treatment.cost_wo_discount) < 50:
            volume = treatment.cost
        else:
            volume = treatment.cost_wo_discount * 0.2

        # rule 3
        if treatment.technician:
            pass  # TODO Consumables repository

        for idx, (doc, dep, vol) in enumerate(self.volumes):
            if doc == treatment.staff and dep == treatment.department:
                self.volumes[idx] = (doc, dep, vol + volume)
                return
        else:
            self.volumes.append(
                (treatment.staff, treatment.department, volume)
            )


class CalcAssistantSalary:
    def __init__(self):
        pass

    def get_volume(self, filial: Filial,
                   date_begin: datetime.date = None,
                   date_end: datetime.date = None):
        pass
