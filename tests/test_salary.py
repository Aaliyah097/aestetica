from src.staff.repositories.staff_repository import StaffFactory
from src.staff.entities.role import Role
from src.treatments.entities.department import Department

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


def test_modify_salary():
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

