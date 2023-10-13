import datetime
from collections import defaultdict
from dataclasses import dataclass
import calendar

from src.schedule.entities.schedule import Schedule

from src.staff.entities.users.assistant import Assistant
from src.staff.entities.users.householder import Householder
from src.staff.entities.users.anesthetist import Anesthetist
from src.staff.entities.users.doctor import Doctor
from src.staff.entities.users.staff import Staff
from src.staff.entities.users.technician import Technician
from src.staff.entities.users.senior_assistant import SeniorAssistant
from src.staff.entities.users.manager import Manager
from src.staff.entities.users.administrator import Administrator
from src.staff.entities.users.seller import Seller

from src.salary.entities.traffic import Traffic

from src.staff.entities.department import Department
from src.staff.entities.filial import Filial

from src.treatments.entities.service import Service
from src.treatments.entities.treatment import Treatment, MarkDown

from src.treatments.repositories.services_repository import ServicesRepository
from src.treatments.repositories.treatments_repository import TreatmentRepository
from src.schedule.repositories.schedule_repository import ScheduleRepository

from src.salary.repositories.bonus_repository import BonusRepository
from src.salary.repositories.salary_repository import SalaryRepository
from src.salary.repositories.payout_repository import PayoutRepository
from src.salary.repositories.traffic_repository import TrafficRepository

from src.staff.repositories.staff_repository import StaffRepository

from src.salary.service.calculators.doctor_calculator import DoctorSalaryCalculator
from src.salary.service.calculators.assistants_calculator import AssistantsSalaryCalculator
from src.salary.service.calculators.anesthetist_calculator import AnesthetistCalculator

from src.treatments.repositories.consumables_repository import ConsumablesRepository


@dataclass
class SalaryReport:
    staff: Staff
    income: float
    volume: float
    fix: float
    payout: float
    award: float


@dataclass
class DoctorsSalaryReport(SalaryReport):
    treatments: list[Treatment]


@dataclass
class AssistantSalaryReport(SalaryReport):
    schedule: list[Schedule]


@dataclass
class SellerSalaryReport(SalaryReport):
    traffic: list[Traffic]


class SalaryCalculationService:
    """Расчет ЗП по филиалу.
    В расчет попадает сразу два периода 1-15, 16-31 и сразу все роли в организации.
    Задача сервиса собрать расчеты по каждой роли в единый документ."""

    def __init__(self, filial: Filial | str,
                 date_begin: datetime.date = None,
                 date_end: datetime.date = None):
        self.filial = Filial(filial) if type(filial) == str else filial

        self.treatment_repo: TreatmentRepository = TreatmentRepository(filial)
        self.submit_services: list[Service] = ServicesRepository.get_submits()
        self.schedule_repo: ScheduleRepository = ScheduleRepository(filial)
        self.bonus_repository: BonusRepository = BonusRepository()
        self.consumables_repo: ConsumablesRepository = ConsumablesRepository()
        self.staff_repo: StaffRepository = StaffRepository()
        self.salary_repo: SalaryRepository = SalaryRepository()
        self.payout_repo: PayoutRepository = PayoutRepository()
        self.traffic_repo: TrafficRepository = TrafficRepository()

        self.date_begin = date_begin
        self.date_end = date_end

        month = date_begin.month
        year = date_begin.year
        first_day, last_day = calendar.monthrange(year, month)
        first_day = first_day if first_day else 1

        self.month_volume: float = self.treatment_repo.get_month_volume_payments(
            datetime.date(year, month, first_day), datetime.date(year, month, last_day)
        )

        roles = set([st.__class__ for st in self.staff_repo.get_staff()])
        self.team_members = defaultdict(int)
        for role in roles:
            self.team_members[role] += self.staff_repo.get_amount_by_role(role)

    def calc_payouts(self, staff: Staff) -> float:
        total = 0
        payouts = self.payout_repo.get_by_staff(staff.name)
        for pay in payouts:
            if self.date_begin <= pay.on_date <= self.date_end:
                total += pay.amount
        return total

    def calc_award(self, staff: Staff) -> float:
        award = 0
        if self.month_volume < 14_000_000:
            return award

        if self.date_begin.day < 15:
            return award

        if isinstance(staff, Administrator) or isinstance(staff, Assistant) or isinstance(staff, SeniorAssistant):
            members_count = self.team_members[Administrator] + \
                            self.team_members[Assistant] + \
                            self.team_members[SeniorAssistant]
            if members_count == 0:
                members_count = 1
            award += round((self.month_volume * 0.01) / members_count, 2)
        elif isinstance(staff, Manager):
            members_count = self.team_members[Manager]
            if members_count == 0:
                members_count = 1
            award += round((self.month_volume * 0.015) / members_count, 2)

        if staff.name == 'Сиразова Руфия Талгатовна':
            award += 10000

        return award

    # продажники
    def sellers_calc(self) -> list[SellerSalaryReport]:
        salary_reports = []
        for staff in self.staff_repo.get_staff():
            if not isinstance(staff, Seller):
                continue

            traffic = list(filter(lambda t: self.date_begin <= t.on_date <= self.date_end,
                                  self.traffic_repo.get_by_staff(staff.name)))
            volume = sum([t.amount for t in traffic])

            salary = self.salary_repo.get_salary(staff, Department('Прочее'), filial=self.filial)
            salary.volume = volume
            award = self.calc_award(staff)
            salary.add_award(award)
            payout = self.calc_payouts(staff)
            salary.add_payout(payout)

            salary_reports.append(
                SellerSalaryReport(
                    staff=staff,
                    income=salary.income,
                    award=award,
                    volume=volume,
                    fix=salary.fix,
                    payout=payout,
                    traffic=traffic
                )
            )
        return salary_reports

    # ассистенты
    def assistants_calc(self) -> list[AssistantSalaryReport]:
        schedules = self.schedule_repo.get_all_schedule(self.date_begin, self.date_end)
        salary_reports = []

        for staff, schedule in self._split_schedule(schedules).items():
            if not isinstance(staff, Assistant) and not isinstance(staff, SeniorAssistant) \
                    and not isinstance(staff, Administrator) and not isinstance(staff, Householder):
                continue
            salary = AssistantsSalaryCalculator().calc(staff, schedule, self.filial)
            award = self.calc_award(staff)
            salary.add_award(award)
            payout = self.calc_payouts(staff)
            salary.add_payout(payout)

            salary_reports.append(
                AssistantSalaryReport(
                    staff=staff,
                    income=salary.income,
                    volume=salary.volume,
                    fix=salary.fix,
                    schedule=schedule,
                    award=award,
                    payout=payout
                )
            )
        return salary_reports

    # прочие
    def other_staff_calc(self) -> list[SalaryReport]:
        salary_reports = []

        for staff in self.staff_repo.get_staff():
            if isinstance(staff, Doctor) or isinstance(staff, Assistant) or isinstance(staff, SeniorAssistant) \
                    or isinstance(staff, Technician) or isinstance(staff, Anesthetist) or isinstance(staff, Administrator) \
                    or isinstance(staff, Householder) or isinstance(staff, Seller):
                continue
            salary = self.salary_repo.get_salary(staff, Department("Прочее"), filial=self.filial)
            salary.volume = 1
            award = self.calc_award(staff)
            salary.add_award(award)
            payout = self.calc_payouts(staff)
            salary.add_payout(payout)

            salary_reports.append(
                SalaryReport(
                    staff=staff,
                    income=salary.income,
                    award=award,
                    volume=0,
                    fix=salary.fix,
                    payout=payout
                )
            )
        return salary_reports

    # анестезиологи
    def anesthetists_calc(self) -> list[DoctorsSalaryReport]:
        treatments = self.treatment_repo.get_all_treatments(
            date_begin=self.date_begin,
            date_end=self.date_end
        )

        treatments = list(filter(
            lambda t: isinstance(t.staff, Anesthetist),
            treatments
        ))

        salary_reports = []

        data = defaultdict(list)
        for t in treatments:
            data[t.staff].append(t)

        calculator = AnesthetistCalculator()
        for staff, treatments in data.items():
            salary = calculator.calc(staff, treatments, filial=self.filial)

            payout = self.calc_payouts(staff)
            salary.add_payout(payout)

            salary_reports.append(
                DoctorsSalaryReport(
                    staff=staff,
                    income=salary.income,
                    award=0,
                    volume=salary.volume,
                    fix=salary.fix,
                    treatments=treatments,
                    payout=payout
                )
            )

        return salary_reports

    # врачи
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
            salaries, marked_treatments = calculator.calc(doctor, departments, filial=self.filial)

            payout = self.calc_payouts(doctor)

            salary_report = DoctorsSalaryReport(
                staff=doctor,
                income=sum([salary.income for salary in salaries]) - payout,
                volume=sum([salary.volume for salary in salaries]),
                fix=0,
                treatments=marked_treatments,
                payout=payout,
                award=0
            )
            salary_reports.append(salary_report)
        return salary_reports

    def _split_schedule(self, schedule: list[Schedule]) -> dict[Staff, list[Schedule]]:
        data = defaultdict(list)

        for sch in schedule:
            # if sch.on_date < self.date_begin or sch.on_date > self.date_begin:
            #     continue
            bonus = self.bonus_repository.get_bonus(sch.staff, on_date=sch.on_date)
            if bonus:
                sch.bonus = bonus.amount
                sch.comment = bonus.comment

            data[sch.staff].append(sch)

        return data

    def _split_treatments(self, treatments: list[Treatment]) -> dict[Staff, dict[Department, list[Treatment]]]:
        result = defaultdict(lambda: defaultdict(list))

        for treatment in treatments:
            treatment.consumables = self.consumables_repo.get_by_technician_and_service(
                technician=treatment.technician,
                service=treatment.service
            )

            if not isinstance(treatment.staff, Doctor):
                continue

            if treatment.service in self.submit_services:
                history_treatments = sorted(list(filter(lambda t: t.on_date <= treatment.on_date and
                                                                  t.tooth == treatment.tooth and
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
