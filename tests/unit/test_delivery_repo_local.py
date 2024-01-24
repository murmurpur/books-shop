import pytest
from uuid import uuid4
from datetime import datetime

from app.models.delivery import Delivery, DeliveryStatuses
from app.repositories.local_delivery_repo import DeliveryRepo
from app.repositories.local_deliveryman_repo import DeliverymenRepo


@pytest.fixture(scope='session')
def deliveryman_repo() -> DeliverymenRepo:
    return DeliverymenRepo()


@pytest.fixture(scope='session')
def first_delivery() -> Delivery:
    return Delivery(id=uuid4(), address='address', date=datetime.now(), status=DeliveryStatuses.CREATED)


@pytest.fixture(scope='session')
def second_delivery() -> Delivery:
    return Delivery(id=uuid4(), address='address1', date=datetime.now(), status=DeliveryStatuses.CREATED)


delivery_test_repo = DeliveryRepo()


def test_empty_list() -> None:
    assert delivery_test_repo.get_deliveries() == []


def test_add_first_delivery(first_delivery: Delivery) -> None:
    assert delivery_test_repo.create_delivery(first_delivery) == first_delivery


def test_add_first_delivery_repeat(first_delivery: Delivery) -> None:
    with pytest.raises(KeyError):
        delivery_test_repo.create_delivery(first_delivery)


def test_get_delivery_by_id(first_delivery: Delivery) -> None:
    assert delivery_test_repo.get_delivery_by_id(
        first_delivery.id) == first_delivery


def test_get_delivery_by_id_error() -> None:
    with pytest.raises(KeyError):
        delivery_test_repo.get_delivery_by_id(uuid4())


def test_add_second_delivery(first_delivery: Delivery, second_delivery: Delivery) -> None:
    assert delivery_test_repo.create_delivery(second_delivery) == second_delivery
    deliveries = delivery_test_repo.get_deliveries()
    assert len(deliveries) == 2
    assert deliveries[0] == first_delivery
    assert deliveries[1] == second_delivery


def test_set_status(first_delivery: Delivery) -> None:
    first_delivery.status = DeliveryStatuses.ACTIVATED
    assert delivery_test_repo.set_status(
        first_delivery).status == first_delivery.status

    first_delivery.status = DeliveryStatuses.CANCELED
    assert delivery_test_repo.set_status(
        first_delivery).status == first_delivery.status

    first_delivery.status = DeliveryStatuses.DONE
    assert delivery_test_repo.set_status(
        first_delivery).status == first_delivery.status

    first_delivery.status = DeliveryStatuses.CREATED
    assert delivery_test_repo.set_status(
        first_delivery).status == first_delivery.status


def test_set_deliveryman(first_delivery: Delivery, deliveryman_repo: DeliverymenRepo) -> None:
    first_delivery.deliveryman = deliveryman_repo.get_deliverymen()[0]
    assert delivery_test_repo.set_deliveryman(
        first_delivery).deliveryman == deliveryman_repo.get_deliverymen()[0]


def test_change_deliveryman(first_delivery: Delivery, deliveryman_repo: DeliverymenRepo) -> None:
    first_delivery.deliveryman = deliveryman_repo.get_deliverymen()[1]
    assert delivery_test_repo.set_deliveryman(
        first_delivery).deliveryman == deliveryman_repo.get_deliverymen()[1]
