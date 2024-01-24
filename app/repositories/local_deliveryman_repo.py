# /app/repositories/local_deliveryman_repo.py

from uuid import UUID

from app.models.deliveryman import Deliveryman


deliverymen: list[Deliveryman] = [
    Deliveryman(id=UUID('85db966c-67f1-411e-95c0-f02edfa5464a'),
                name='Лаптев Иван Алексаендрович'),
    Deliveryman(id=UUID('31babbb3-5541-4a2a-8201-537cdff25fed'),
                name='Зуев Андрей Сергеевич'),
    Deliveryman(id=UUID('45309954-8e3c-4635-8066-b342f634252c'),
                name='Кудж Станислав Алексеевич')
]

class DeliverymenRepo():
    def get_deliverymen(self) -> list[Deliveryman]:
        return deliverymen

    def get_deliveryman_by_id(self, id: UUID) -> Deliveryman:
        for d in deliverymen:
            if d.id == id:
                return d

        raise KeyError
