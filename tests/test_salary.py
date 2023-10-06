from src.staff.repositories.staff_repository import StaffFactory, StaffRepository
from src.staff.entities.role import Role
from src.staff.entities.users.doctor import Doctor
from src.staff.entities.department import Department

from src.salary.repositories.salary_repository import SalaryRepository
from src.salary.service.salary_calculation_service import SalaryCalculationService
from src.salary.service.salary_management_service import SalaryManagementService


def salary_by_staff():
    staff = StaffFactory.create_staff(
        name='Манукян Артавазд Генрикович',
        staff_role=Role(
            'Рабочее место доктора'
        )
    )
    department = Department(name='Стоматология')
    salary = SalaryRepository.get_salary(
        staff=staff,
        department=department
    )


def delete_salary_by_id(_id: int):
    SalaryRepository.delete_by_id(_id)


def salary_calculation():
    service = SalaryCalculationService(filial='Барвиха')
    for doctor, salaries in service.doctors_cals():
        print(doctor.name, [salary.income for salary in salaries])


def create_salary():
    staff = StaffFactory.create_staff(
        name='Манукян Артавазд Генрикович',
        staff_role=Role(
            'Рабочее место доктора'
        )
    )
    department = Department(name='Стоматология')
    SalaryRepository().create_salary(staff, department)


def modify_salary():
    salary_id = 78
    fix = 0
    grid = [
        {
            'percent': 25,
            'limit': 1500000
        },
        {
            'percent': 30,
            'limit': 2500000
        },
    ]

    service = SalaryManagementService()
    service.modify_salary(salary_id, fix, grid)


def change_salaries_defaults():
    staff = StaffRepository().get_staff()
    service = SalaryManagementService()

    for st in staff:
        if not isinstance(st, Doctor):
            continue
        salaries = SalaryRepository().get_salaries_by_staff(st)
        for sal in salaries:
            grid = [
                {
                    'percent': 20,
                    'limit': 1_500_000
                },
                {
                    'percent': 25,
                    'limit': 2_500_000
                },
                {
                    'percent': 30,
                    'limit': 3_500_000
                },
            ]
            fix = 0

            if sal.department.name == "Лечение кариеса и каналов":
                grid = [
                    {
                        'percent': 25,
                        'limit': 1_800_000
                    },
                    {
                        'percent': 30,
                        'limit': 3_000_000
                    },
                    {
                        'percent': 35,
                        'limit': 100_000_000
                    },
                ]
            elif sal.department.name == "Детство":
                grid = [
                    {
                        'percent': 20,
                        'limit': 500_000
                    },
                    {
                        'percent': 25,
                        'limit': 700_000
                    },
                    {
                        'percent': 30,
                        'limit': 100_000_000
                    },
                ]
            elif sal.department.name == "Виниры и коронки":
                grid = [
                    {
                        'percent': 20,
                        'limit': 3_500_000
                    },
                    {
                        'percent': 25,
                        'limit': 7_000_000
                    },
                    {
                        'percent': 30,
                        'limit': 100_000_000
                    },
                ]
            elif sal.department.name == "Имплантация":
                grid = [
                    {
                        'percent': 25,
                        'limit': 1_800_000
                    },
                    {
                        'percent': 30,
                        'limit': 2_800_000
                    },
                    {
                        'percent': 35,
                        'limit': 100_000_000
                    },
                ]
            elif sal.department.name == "Исправление прикуса":
                grid = [
                    {
                        'percent': 35,
                        'limit': 2_500_000
                    },
                    {
                        'percent': 40,
                        'limit': 5_000_000
                    },
                    {
                        'percent': 45,
                        'limit': 100_000_000
                    },
                ]
            elif sal.department.name == "Профессиональная гигиена и отбеливание":
                grid = [
                    {
                        'percent': 25,
                        'limit': 600_000
                    },
                    {
                        'percent': 30,
                        'limit': 900_000
                    },
                    {
                        'percent': 35,
                        'limit': 100_000_000
                    },
                ]

            service.modify_salary(sal.id, fix, grid)


def test():
    """"""
    # change_salaries_defaults()

