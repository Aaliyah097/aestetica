from src.staff.repositories.staff_repository import StaffFactory
from src.staff.entities.role import Role
from src.treatments.entities.department import Department

from src.salary.repositories.salary_repository import SalaryRepository
from src.salary.service.salary_calculation_service import SalaryCalculationService


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


def test_salary_calculation():
    service = SalaryCalculationService(filial='Барвиха')
    for doctor, salaries in service.doctors_cals():
        print(doctor.name, [salary.income for salary in salaries])
