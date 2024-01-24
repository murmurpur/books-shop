import pytest
from uuid import UUID, uuid4

from app.models.deliveryman import Deliveryman
from app.repositories.local_deliveryman_repo import DeliverymenRepo


@pytest.fixture()
def delivryman_list() -> list[Deliveryman]:
    return [
        Deliveryman(id=UUID('85db966c-67f1-411e-95c0-f02edfa5464a'),
                    name='Лаптев Иван Алексаендрович'),
        Deliveryman(id=UUID('31babbb3-5541-4a2a-8201-537cdff25fed'),
                    name='Зуев Андрей Сергеевич'),
        Deliveryman(id=UUID('45309954-8e3c-4635-8066-b342f634252c'),
                    name='Кудж Станислав Алексеевич')
    ]


@pytest.fixture()
def deliveryman_repo() -> DeliverymenRepo:
    return DeliverymenRepo()


def test_delivryman_list(delivryman_list: list[Deliveryman], deliveryman_repo: DeliverymenRepo):
    assert deliveryman_repo.get_deliverymen() == delivryman_list


def test_get_deliveryman_by_id(delivryman_list: list[Deliveryman], deliveryman_repo: DeliverymenRepo):
    assert deliveryman_repo.get_deliveryman_by_id(
        delivryman_list[0].id) == delivryman_list[0]


def test_get_deliveryman_by_id_error(deliveryman_repo: DeliverymenRepo):
    with pytest.raises(KeyError):
        deliveryman_repo.get_deliveryman_by_id(uuid4())
