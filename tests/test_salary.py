from src.staff.repositories.staff_repository import StaffFactory
from src.staff.entities.role import Role
from src.staff.entities.department import Department

from src.salary.repositories.salary_repository import SalaryRepository
from src.salary.service.salary_calculation_service import SalaryCalculationService


def test_salary_by_staff():
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


def test_salary_calculation():
    service = SalaryCalculationService()
    service.calc(
        filial_name='Барвиха'
    )
