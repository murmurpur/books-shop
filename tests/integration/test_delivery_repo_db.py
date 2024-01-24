# /tests/integration/test_delivery_repo_db.py

import pytest
from uuid import uuid4
from time import sleep
from datetime import datetime

from app.models.delivery import Delivery, DeliveryStatuses
from app.repositories.db_delivery_repo import DeliveryRepo
from app.repositories.local_deliveryman_repo import DeliverymenRepo

sleep(5)


@pytest.fixture()
def delivery_repo() -> DeliverymenRepo:
    repo = DeliveryRepo()
    return repo


@pytest.fixture(scope='session')
def deliveryman_repo() -> DeliverymenRepo:
    return DeliverymenRepo()


@pytest.fixture(scope='session')
def first_delivery() -> Delivery:
    return Delivery(id=uuid4(), address='address', date=datetime.now(), status=DeliveryStatuses.CREATED)


@pytest.fixture(scope='session')
def second_delivery() -> Delivery:
    return Delivery(id=uuid4(), address='address1', date=datetime.now(), status=DeliveryStatuses.CREATED)


def test_empty_list(delivery_repo: DeliverymenRepo) -> None:
    assert delivery_repo.get_deliveries() == []


def test_add_first_delivery(first_delivery: Delivery, delivery_repo: DeliverymenRepo) -> None:
    assert delivery_repo.create_delivery(first_delivery) == first_delivery


def test_add_first_delivery_repeat(first_delivery: Delivery, delivery_repo: DeliverymenRepo) -> None:
    with pytest.raises(KeyError):
        delivery_repo.create_delivery(first_delivery)


def test_get_delivery_by_id(first_delivery: Delivery, delivery_repo: DeliverymenRepo) -> None:
    assert delivery_repo.get_delivery_by_id(
        first_delivery.id) == first_delivery


def test_get_delivery_by_id_error(delivery_repo: DeliverymenRepo) -> None:
    with pytest.raises(KeyError):
        delivery_repo.get_delivery_by_id(uuid4())


def test_add_second_delivery(first_delivery: Delivery, second_delivery: Delivery, delivery_repo: DeliverymenRepo) -> None:
    assert delivery_repo.create_delivery(second_delivery) == second_delivery
    deliveries = delivery_repo.get_deliveries()
    assert len(deliveries) == 2
    assert deliveries[0] == first_delivery
    assert deliveries[1] == second_delivery


def test_set_status(first_delivery: Delivery, delivery_repo: DeliverymenRepo) -> None:
    first_delivery.status = DeliveryStatuses.ACTIVATED
    assert delivery_repo.set_status(
        first_delivery).status == first_delivery.status

    first_delivery.status = DeliveryStatuses.CANCELED
    assert delivery_repo.set_status(
        first_delivery).status == first_delivery.status

    first_delivery.status = DeliveryStatuses.DONE
    assert delivery_repo.set_status(
        first_delivery).status == first_delivery.status

    first_delivery.status = DeliveryStatuses.CREATED
    assert delivery_repo.set_status(
        first_delivery).status == first_delivery.status


def test_set_deliveryman(first_delivery: Delivery, deliveryman_repo: DeliverymenRepo, delivery_repo: DeliverymenRepo) -> None:
    first_delivery.deliveryman = deliveryman_repo.get_deliverymen()[0]
    assert delivery_repo.set_deliveryman(
        first_delivery).deliveryman == deliveryman_repo.get_deliverymen()[0]


def test_change_deliveryman(first_delivery: Delivery, deliveryman_repo: DeliverymenRepo, delivery_repo: DeliverymenRepo) -> None:
    first_delivery.deliveryman = deliveryman_repo.get_deliverymen()[1]
    assert delivery_repo.set_deliveryman(
        first_delivery).deliveryman == deliveryman_repo.get_deliverymen()[1]
