from src.treatments.repositories.treatments_repository import TreatmentRepository
from src.treatments.entities.filial import Filial


def test_treatments_list_from_source_db():
    repo = TreatmentRepository()
    filial = Filial('Барвиха')
    treatments = repo.get_all_treatments(filial)
    print(treatments)
