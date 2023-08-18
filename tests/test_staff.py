from src.staff.repositories.staff_repository import StaffRepository


def test_get_staff_from_repository():
    repo = StaffRepository()
    staff = repo.get_staff()
    print(staff)
