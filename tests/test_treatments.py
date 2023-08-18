from src.treatments.repositories.treatments_repository import TreatmentRepository
from src.staff.entities.role import Role
from src.staff.entities.filial import Filial


def test_treatments_list_from_source_db():
    repo = TreatmentRepository()
    filial = Filial('Барвиха')
    treatments = repo.get_all_treatments(filial)
    print(treatments)
