# /app/repositories/local_storekeeper_repo.py

from uuid import UUID

from app.models.storekeeper import Storekeeper


storekeeper1: list[Storekeeper] = [
    Storekeeper(id=UUID('85db966c-67f1-411e-95c0-f02edfa5464a'),
                name='Лаптев Иван Алексаендрович'),
    Storekeeper(id=UUID('31babbb3-5541-4a2a-8201-537cdff25fed'),
                name='Зуев Андрей Сергеевич'),
    Storekeeper(id=UUID('45309954-8e3c-4635-8066-b342f634252c'),
                name='Кудж Станислав Алексеевич')
]

class Storekeeper1Repo():
    def get_storekeeper1(self) -> list[Storekeeper]:
        return storekeeper1

    def get_storekeeper_by_id(self, id: UUID) -> Storekeeper:
        for d in storekeeper1:
            if d.id == id:
                return d

        raise KeyError
