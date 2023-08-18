import datetime

from src.salary.repositories.salary_repository import SalaryRepository
from src.treatments.repositories.treatments_repository import TreatmentRepository
from src.staff.repositories.staff_repository import StaffRepository
from src.staff.repositories.filial_repository import FilialRepository

from src.staff.entities.filial import Filial
from src.salary.entities.salary import Salary
from src.staff.entities.users.doctor import Doctor
from src.staff.entities.department import Department


class SalaryCalculationService:
    def __init__(self):
        self.filial_repo: FilialRepository = FilialRepository()

    def calc(self, filial_name: str,
             date_begin: datetime.date = None,
             date_end: datetime.date = None):
        filial = self.filial_repo.get_by_name(filial_name)

        calc_d = CalcDoctorSalary()
        doctors_salaries = calc_d.calc(
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
        self.volumes: list[tuple[Doctor, Department, float]] = []

    def calc(self, filial: Filial,
             date_begin: datetime.date = None,
             date_end: datetime.date = None
             ) -> list[Salary]:
        return self._get_salaries(
            self._get_volume(
                filial=filial,
                date_begin=date_begin,
                date_end=date_end
            )
        )

    def _get_salaries(self, doctors_volumes: list[tuple[Doctor, Department, float]]) -> list[Salary]:
        salaries = []
        for doctor, department, volume in doctors_volumes:
            salary = self.salary_repo.get_salary(
                staff=doctor,
                department=department,
            )
            salary.volume = volume
            salaries.append(salary)
        return salaries

    def _get_volume(self, filial: Filial,
                    date_begin: datetime.date = None,
                    date_end: datetime.date = None) -> list[tuple[Doctor, Department, float]]:

        treatments = self.treatment_repo.get_all_treatments(
            filial=filial,
            date_begin=date_begin,
            date_end=date_end
        )
        for threat in treatments:
            if not isinstance(threat.staff, Doctor):
                continue
            self._set_doctor_volume(
                doctor=threat.staff,
                department=threat.department,
                volume=threat.cost if (threat.discount * 100 / threat.cost_wo_discount) < 50
                else (threat.cost_wo_discount * 0.2)
            )

        return self.volumes

    def _set_doctor_volume(self, doctor: Doctor, department: Department, volume: float) -> None:
        for idx, (doc, dep, vol) in enumerate(self.volumes):
            if doc == doctor and dep == department:
                self.volumes[idx] = (doc, dep, vol + volume)
                return
        else:
            self.volumes.append(
                (doctor, department, volume)
            )


class CalcAssistantSalary:
    def __init__(self):
        pass

    def get_volume(self, filial: Filial,
                   date_begin: datetime.date = None,
                   date_end: datetime.date = None):
        pass
