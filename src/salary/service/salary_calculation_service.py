import datetime
from collections import defaultdict
from dataclasses import dataclass

from src.schedule.entities.schedule import Schedule

from src.staff.entities.users.assistant import Assistant
from src.staff.entities.users.doctor import Doctor
from src.staff.entities.users.staff import Staff
from src.staff.entities.users.technician import Technician
from src.staff.entities.users.senior_assistant import SeniorAssistant
from src.staff.entities.users.manager import Manager
from src.staff.entities.users.administrator import Administrator

from src.staff.entities.department import Department
from src.staff.entities.filial import Filial

from src.treatments.entities.consumables import Consumables
from src.treatments.entities.service import Service
from src.treatments.entities.treatment import Treatment, MarkDown

from src.treatments.repositories.services_repository import ServicesRepository
from src.treatments.repositories.treatments_repository import TreatmentRepository
from src.schedule.repositories.schedule_repository import ScheduleRepository

from src.salary.repositories.bonus_repository import BonusRepository
from src.staff.repositories.staff_repository import StaffRepository
from src.salary.entities.salary import Salary

from src.salary.service.calculators.doctor_calculator import DoctorSalaryCalculator
from src.salary.service.calculators.assistants_calculator import AssistantsSalaryCalculator
from src.treatments.repositories.consumables_repository import ConsumablesRepository


@dataclass
class SalaryReport:
    staff: Staff
    income: float
    volume: float
    fix: float


@dataclass
class DoctorsSalaryReport(SalaryReport):
    treatments: list[Treatment]
    award: float = 0


@dataclass
class AssistantSalaryReport(SalaryReport):
    schedule: list[Schedule]
    award: float = 0


@dataclass
class OtherSalaryReport(SalaryReport):
    award: float = 0


class SalaryCalculationService:
    """Расчет ЗП по филиалу.
    В расчет попадает сразу два периода 1-15, 16-31 и сразу все роли в организации.
    Задача сервиса собрать расчеты по каждой роли в единый документ."""

    def __init__(self, filial: Filial | str,
                 date_begin: datetime.date = None,
                 date_end: datetime.date = None):
        self.treatment_repo: TreatmentRepository = TreatmentRepository(filial)
        self.submit_services: list[Service] = ServicesRepository.get_submits()
        self.schedule_repo: ScheduleRepository = ScheduleRepository(filial)
        self.bonus_repository: BonusRepository = BonusRepository()
        self.consumables_repo: ConsumablesRepository = ConsumablesRepository()
        self.staff_repo: StaffRepository = StaffRepository()

        self.date_begin = date_begin
        self.date_end = date_end

        self.month_volume: float = self.treatment_repo.get_month_volume(
            date_begin.month, date_begin.year
        )

        roles = set([st.__class__ for st in self.staff_repo.get_staff()])
        self.team_members = defaultdict(int)
        for role in roles:
            self.team_members[role] += self.staff_repo.get_amount_by_role(role)

    def calc_award(self, staff: Staff) -> float:
        award = 0
        if self.month_volume < 14_000_000:
            return award

        if isinstance(staff, Administrator) or isinstance(staff, Assistant) or isinstance(staff, SeniorAssistant):
            members_count = self.team_members[Administrator] + \
                            self.team_members[Assistant] + \
                            self.team_members[SeniorAssistant]
            award += round((self.month_volume * 0.01) / members_count, 2)
        elif isinstance(staff, Manager):
            members_count = self.team_members[Manager]
            award += round((self.month_volume * 0.015) / members_count, 2)

        if staff.name == 'Сиразова Руфия Талгатовна':
            award += 10000

        return award

    # TODO применить премии ко всем ЗП
    # TODO Расчитать ЗП для всего прочего персонала
    # TODO Вывести ЗП для всего прочего персонала в таблицу
    # TODO Добавить поле Премия в таблицу

    # Считаться должно так:
    """
    Берем ставку фиксы,
    Прибавляем за период бонусы к ставке
    (Ставку и бонус) умножаем на количество дней в периоде отработанным
    И перенести это все в калькулятор по ассистентам
    """
    def assistants_calc(self) -> list[AssistantSalaryReport]:
        schedules = self.schedule_repo.get_all_schedule()

        salary_reports = []

        for staff, schedule in self._split_schedule(schedules).items():
            salary = AssistantsSalaryCalculator().calc(staff, schedule)
            award = self.calc_award(staff)
            salary.add_award(award)

            salary_reports.append(
                AssistantSalaryReport(
                    staff=staff,
                    income=salary.income,
                    volume=salary.volume,
                    fix=salary.fix,
                    schedule=schedule,
                    award=award
                )
            )
        return salary_reports

    def other_staff_calc(self) -> list[OtherSalaryReport]:
        salary_reports = []

        for staff in self.staff_repo.get_staff():
            if isinstance(staff, Doctor) or isinstance(staff, Assistant) or isinstance(staff, SeniorAssistant) or isinstance(staff, Technician):
                continue
            salary = Salary(staff, Department("Прочее"))
            award = self.calc_award(staff)
            salary.add_award(award)

            salary_reports.append(
                OtherSalaryReport(
                    staff=staff,
                    income=salary.income,
                    award=award,
                    volume=0,
                    fix=salary.fix
                )
            )
        return salary_reports

    def doctors_cals(self) -> list[DoctorsSalaryReport]:
        treatments = self._split_treatments(
            self.treatment_repo.get_all_treatments(
                date_begin=self.date_begin,
                date_end=self.date_end
            )
        )

        salary_reports = []
        calculator = DoctorSalaryCalculator()

        for doctor, departments in treatments.items():
            salaries, marked_treatments = calculator.calc(doctor, departments)
            salary_report = DoctorsSalaryReport(
                staff=doctor,
                income=sum([salary.income for salary in salaries]),
                volume=sum([salary.volume for salary in salaries]),
                fix=0,
                treatments=marked_treatments
            )
            salary_reports.append(salary_report)
        return salary_reports

    def _split_schedule(self, schedule: list[Schedule]) -> dict[Staff, list[Schedule]]:
        data = defaultdict(list)

        for sch in schedule:
            if not isinstance(sch.staff, Assistant) and not isinstance(sch.staff, SeniorAssistant):
                continue

            bonus = self.bonus_repository.get_bonus(sch.staff, on_date=sch.on_date)
            if bonus:
                sch.bonus = bonus.amount

            data[sch.staff].append(sch)

        return data

    def get_consumables(self, treatment: Treatment) -> Consumables | None:
        return self.consumables_repo.get_by_technician_and_service(
            technician=treatment.technician,
            service=treatment.service
        )

    def _split_treatments(self, treatments: list[Treatment]) -> dict[Staff, dict[Department, list[Treatment]]]:
        result = defaultdict(lambda: defaultdict(list))

        for treatment in treatments:
            treatment.consumables = self.get_consumables(treatment)

            if not isinstance(treatment.staff, Doctor):
                continue

            if treatment.service in self.submit_services:
                # TODO добавить код зуба в фильтр
                history_treatments = sorted(list(filter(lambda t: t.on_date <= treatment.on_date and
                                                                  t.staff.name == treatment.staff.name and
                                                                  t.service not in self.submit_services and
                                                                  t.client == treatment.client and
                                                                  t.cost != 0,
                                                        treatments)), key=lambda t: t.on_date, reverse=True)

                history_treatment = history_treatments[-1] if len(history_treatments) > 0 else None

                if not history_treatment:
                    history_treatment = self.treatment_repo.get_history_treatment(
                        lt_date=treatment.on_date,
                        tooth_code=treatment.tooth,
                        doctor_name=treatment.staff.name,
                        block_services_codes=tuple([service.code for service in self.submit_services]),
                        client=treatment.client
                    )

                if history_treatment:
                    treatment.markdown = MarkDown(
                        is_history=False,
                        prev_treatment=history_treatment
                    )

                    if history_treatment.on_date.date() <= self.date_begin:
                        history_treatment.markdown = MarkDown(
                            is_history=True
                        )
                        result[treatment.staff][treatment.department].append(history_treatment)

            result[treatment.staff][treatment.department].append(treatment)

        return result
