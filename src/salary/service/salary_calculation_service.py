import datetime
from collections import defaultdict

from src.salary.entities.salary import Salary
from src.salary.repositories.salary_repository import SalaryRepository
from src.staff.entities.users.doctor import Doctor
from src.staff.entities.users.staff import Staff
from src.treatments.entities.department import Department
from src.treatments.entities.filial import Filial
from src.treatments.entities.service import Service
from src.treatments.entities.treatment import Treatment
from src.treatments.repositories.consumables_repository import ConsumablesRepository
from src.treatments.repositories.filials_repository import FilialsRepository
from src.treatments.repositories.services_repository import ServicesRepository
from src.treatments.repositories.treatments_repository import TreatmentRepository

from src.salary.service.calculators.doctor_calculator import DoctorSalaryCalculator


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
        else:
            self.filial = filial

        self.date_begin = date_begin
        self.date_end = date_end

    def doctors_cals(self):
        treatments = self._split_treatments(
            self.treatment_repo.get_all_treatments(
                filial=self.filial,
                date_begin=self.date_begin,
                date_end=self.date_end
            )
        )

        calculator = DoctorSalaryCalculator()

        for doctor, departments in treatments.items():
            for department, treats in departments.items():
                salary = calculator.calc(
                    doctor=doctor,
                    department=department,
                    treatments=treats
                )
                print(doctor.name, '->', department.name, '->', salary.income)

    def total_calc(self):
        pass

    def calc_by_staff(self):
        pass

    @staticmethod
    def _split_treatments(treatments: list[Treatment]) -> dict[Staff, dict[Department, list[Treatment]]]:
        result = defaultdict(lambda: defaultdict(list))

        for treatment in treatments:
            if isinstance(treatment.staff, Doctor):
                result[treatment.staff][treatment.department].append(treatment)

        return result


class CalcDoctorSalary:
    def __init__(self):
        self.treatment_repo: TreatmentRepository = TreatmentRepository()
        self.salary_repo: SalaryRepository = SalaryRepository()
        self.consumables_repo: ConsumablesRepository = ConsumablesRepository()

        self.volumes: list[tuple[Staff, Department, float]] = []
        self.submit_services: list[Service] = ServicesRepository.get_submits()

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

        treatments = sorted(self.treatment_repo.get_all_treatments(
            filial=filial,
            date_begin=date_begin,
            date_end=date_end
        ), key=lambda t: t.on_date)
        treatments.reverse()

        for treatment in treatments:
            # rule 1 Doctors only
            if not isinstance(treatment.staff, Doctor):
                continue

            if treatment.service in self.submit_services:
                prev_treatments = list(filter(
                    lambda t: t.on_date <= treatment.on_date and
                              t.client == treatment.client and
                              t.staff == treatment.staff and
                              t.cost != 0 and
                              t.service not in self.submit_services,
                    treatments
                ))
                if len(prev_treatments) > 0:
                    print(prev_treatments[-1], '\n', treatment)
                    print('\n\n')

            self._set_doctor_volume(
                treatment=treatment
            )

    def _set_doctor_volume(self, treatment: Treatment) -> None:
        # rule 2 Discounts
        if treatment.cost_wo_discount == 0:
            volume = treatment.cost_wo_discount
        elif (treatment.discount * 100 / treatment.cost_wo_discount) < 50:
            volume = treatment.cost
        else:
            volume = treatment.cost_wo_discount * 0.2

        # rule 3 Consumables
        if treatment.technician:
            consumables = self.consumables_repo.get_by_technician_and_service(
                technician=treatment.technician,
                service=treatment.service
            )
            if consumables:
                volume = volume - consumables.cost

        # # rule 4 Submitting services
        # if treatment.service in self.submit_services:
        #     volume = volume * 0.3
        # else:
        #     volume = volume * 0.7

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
