import pytest
from uuid import UUID, uuid4

from app.models.storekeeper import Storekeeper
from app.repositories.local_storekeeper_repo import Storekeeper1Repo


@pytest.fixture()
def delivryman_list() -> list[Storekeeper]:
    return [
        Storekeeper(id=UUID('85db966c-67f1-411e-95c0-f02edfa5464a'),
                    name='Лаптев Иван Алексаендрович'),
        Storekeeper(id=UUID('31babbb3-5541-4a2a-8201-537cdff25fed'),
                    name='Зуев Андрей Сергеевич'),
        Storekeeper(id=UUID('45309954-8e3c-4635-8066-b342f634252c'),
                    name='Кудж Станислав Алексеевич')
    ]


@pytest.fixture()
def storekeeper_repo() -> Storekeeper1Repo:
    return Storekeeper1Repo()


def test_delivryman_list(delivryman_list: list[Storekeeper], storekeeper_repo: Storekeeper1Repo):
    assert storekeeper_repo.get_storekeeper1() == delivryman_list


def test_get_storekeeper_by_id(delivryman_list: list[Storekeeper], storekeeper_repo: Storekeeper1Repo):
    assert storekeeper_repo.get_storekeeper_by_id(
        delivryman_list[0].id) == delivryman_list[0]


def test_get_storekeeper_by_id_error(storekeeper_repo: Storekeeper1Repo):
    with pytest.raises(KeyError):
        storekeeper_repo.get_storekeeper_by_id(uuid4())
