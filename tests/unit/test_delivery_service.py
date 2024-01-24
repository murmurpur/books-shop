# /tests/unit/test_delivery_service.py

import pytest
from uuid import uuid4, UUID
from datetime import datetime

from app.services.delivery_service import DeliveryService
from app.models.delivery import DeliveryStatuses
from app.repositories.local_delivery_repo import DeliveryRepo
from app.repositories.local_deliveryman_repo import DeliverymenRepo


@pytest.fixture(scope='session')
def delivery_service() -> DeliveryService:
    return DeliveryService(DeliveryRepo(clear=True))


@pytest.fixture()
def deliveryman_repo() -> DeliverymenRepo:
    return DeliverymenRepo()


@pytest.fixture(scope='session')
def first_delivery_data() -> tuple[UUID, str, datetime]:
    return (uuid4(), 'address_1', datetime.now())


@pytest.fixture(scope='session')
def second_delivery_data() -> tuple[UUID, str, datetime]:
    return (uuid4(), 'address_2', datetime.now())


def test_empty_deliveries(delivery_service: DeliveryService) -> None:
    assert delivery_service.get_deliveries() == []


def test_create_first_delivery(
    first_delivery_data: tuple[UUID, str, datetime],
    delivery_service: DeliveryService
) -> None:
    order_id, address, date = first_delivery_data
    delivery = delivery_service.create_delivery(order_id, date, address)
    assert delivery.id == order_id
    assert delivery.address == address
    assert delivery.date == date
    assert delivery.status == DeliveryStatuses.CREATED
    assert delivery.deliveryman == None


def test_create_first_delivery_repeat(
    first_delivery_data: tuple[UUID, str, datetime],
    delivery_service: DeliveryService
) -> None:
    order_id, address, date = first_delivery_data
    with pytest.raises(KeyError):
        delivery_service.create_delivery(order_id, date, address)


def test_create_second_delivery(
    second_delivery_data: tuple[UUID, str, datetime],
    delivery_service: DeliveryService
) -> None:
    order_id, address, date = second_delivery_data
    delivery = delivery_service.create_delivery(order_id, date, address)
    assert delivery.id == order_id
    assert delivery.address == address
    assert delivery.date == date
    assert delivery.status == DeliveryStatuses.CREATED
    assert delivery.deliveryman == None


def test_get_deliveries_full(
    first_delivery_data: tuple[UUID, str, datetime],
    second_delivery_data: tuple[UUID, str, datetime],
    delivery_service: DeliveryService
) -> None:
    deliveries = delivery_service.get_deliveries()
    assert len(deliveries) == 2
    assert deliveries[0].id == first_delivery_data[0]
    assert deliveries[1].id == second_delivery_data[0]


def test_set_deliveryman_status_error(
    first_delivery_data: tuple[UUID, str, datetime],
    delivery_service: DeliveryService,
    deliveryman_repo: DeliverymenRepo
) -> None:
    with pytest.raises(ValueError):
        delivery_service.set_deliveryman(
            first_delivery_data[0], deliveryman_repo.get_deliverymen()[0].id)


def test_set_deliveryman_delivery_error(
    delivery_service: DeliveryService,
    deliveryman_repo: DeliverymenRepo
) -> None:
    with pytest.raises(KeyError):
        delivery_service.set_deliveryman(
            uuid4(), deliveryman_repo.get_deliverymen()[0].id)


def test_set_deliveryman_deliveryman_error(
    first_delivery_data: tuple[UUID, str, datetime],
    delivery_service: DeliveryService
) -> None:
    with pytest.raises(ValueError):
        delivery_service.set_deliveryman(first_delivery_data[0], uuid4())


def test_finish_delivery_status_error(
    first_delivery_data: tuple[UUID, str, datetime],
    delivery_service: DeliveryService
) -> None:
    with pytest.raises(ValueError):
        delivery_service.finish_delivery(first_delivery_data[0])


def test_finish_delivery_not_found(
    delivery_service: DeliveryService
) -> None:
    with pytest.raises(KeyError):
        delivery_service.finish_delivery(uuid4())


def test_cancel_delivery(
    second_delivery_data: tuple[UUID, str, datetime],
    delivery_service: DeliveryService
) -> None:
    delivery = delivery_service.cancel_delivery(second_delivery_data[0])
    assert delivery.status == DeliveryStatuses.CANCELED
    assert delivery.id == second_delivery_data[0]


def test_activate_delivery_status_error(
    second_delivery_data: tuple[UUID, str, datetime],
    delivery_service: DeliveryService
) -> None:
    with pytest.raises(ValueError):
        delivery_service.activate_delivery(second_delivery_data[0])


def test_activate_delivery_not_found(
    delivery_service: DeliveryService
) -> None:
    with pytest.raises(KeyError):
        delivery_service.activate_delivery(uuid4())


def test_activate_delivery(
    first_delivery_data: tuple[UUID, str, datetime],
    delivery_service: DeliveryService
) -> None:
    delivery = delivery_service.activate_delivery(first_delivery_data[0])
    assert delivery.status == DeliveryStatuses.ACTIVATED
    assert delivery.id == first_delivery_data[0]


def test_set_deliveryman(
    first_delivery_data: tuple[UUID, str, datetime],
    delivery_service: DeliveryService,
    deliveryman_repo: DeliverymenRepo
) -> None:
    deliveryman = deliveryman_repo.get_deliverymen()[0]
    delivery = delivery_service.set_deliveryman(
        first_delivery_data[0], deliveryman.id)
    assert delivery.status == DeliveryStatuses.ACTIVATED
    assert delivery.id == first_delivery_data[0]
    assert delivery.deliveryman.id == deliveryman.id
    assert delivery.deliveryman.name == deliveryman.name


def test_change_deliveryman(
    first_delivery_data: tuple[UUID, str, datetime],
    delivery_service: DeliveryService,
    deliveryman_repo: DeliverymenRepo
) -> None:
    deliveryman = deliveryman_repo.get_deliverymen()[1]
    delivery = delivery_service.set_deliveryman(
        first_delivery_data[0], deliveryman.id)
    assert delivery.status == DeliveryStatuses.ACTIVATED
    assert delivery.id == first_delivery_data[0]
    assert delivery.deliveryman.id == deliveryman.id
    assert delivery.deliveryman.name == deliveryman.name


def test_finish_delivery(
    first_delivery_data: tuple[UUID, str, datetime],
    delivery_service: DeliveryService
) -> None:
    delivery = delivery_service.finish_delivery(first_delivery_data[0])
    assert delivery.status == DeliveryStatuses.DONE
    assert delivery.id == first_delivery_data[0]


def test_cancel_delivery_status_error(
    first_delivery_data: tuple[UUID, str, datetime],
    delivery_service: DeliveryService
) -> None:
    with pytest.raises(ValueError):
        delivery_service.cancel_delivery(first_delivery_data[0])


def test_cancel_delivery_not_found(
    delivery_service: DeliveryService
) -> None:
    with pytest.raises(KeyError):
        delivery_service.cancel_delivery(uuid4())
