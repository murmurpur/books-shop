# /tests/unit/test_order_service.py

import pytest
from uuid import uuid4, UUID
from datetime import datetime

from app.services.order_service import OrderService
from app.models.order import OrderStatuses
from app.repositories.local_order_repo import OrderRepo
from app.repositories.local_storekeeper_repo import Storekeeper1Repo


@pytest.fixture(scope='session')
def order_service() -> OrderService:
    return OrderService(OrderRepo(clear=True))


@pytest.fixture()
def storekeeper_repo() -> Storekeeper1Repo:
    return Storekeeper1Repo()


@pytest.fixture(scope='session')
def first_order_data() -> tuple[UUID, str, datetime]:
    return (uuid4(), 'address_1', datetime.now())


@pytest.fixture(scope='session')
def second_order_data() -> tuple[UUID, str, datetime]:
    return (uuid4(), 'address_2', datetime.now())


def test_empty_orders(order_service: OrderService) -> None:
    assert order_service.get_orders() == []


def test_create_first_order(
    first_order_data: tuple[UUID, str, datetime],
    order_service: OrderService
) -> None:
    order_id, address, date = first_order_data
    order = order_service.create_order(order_id, date, address)
    assert order.id == order_id
    assert order.address == address
    assert order.date == date
    assert order.status == OrderStatuses.CREATED
    assert order.storekeeper == None


def test_create_first_order_repeat(
    first_order_data: tuple[UUID, str, datetime],
    order_service: OrderService
) -> None:
    order_id, address, date = first_order_data
    with pytest.raises(KeyError):
        order_service.create_order(order_id, date, address)


def test_create_second_order(
    second_order_data: tuple[UUID, str, datetime],
    order_service: OrderService
) -> None:
    order_id, address, date = second_order_data
    order = order_service.create_order(order_id, date, address)
    assert order.id == order_id
    assert order.address == address
    assert order.date == date
    assert order.status == OrderStatuses.CREATED
    assert order.storekeeper == None


def test_get_orders_full(
    first_order_data: tuple[UUID, str, datetime],
    second_order_data: tuple[UUID, str, datetime],
    order_service: OrderService
) -> None:
    orders = order_service.get_orders()
    assert len(orders) == 2
    assert orders[0].id == first_order_data[0]
    assert orders[1].id == second_order_data[0]


def test_set_storekeeper_status_error(
    first_order_data: tuple[UUID, str, datetime],
    order_service: OrderService,
    storekeeper_repo: Storekeeper1Repo
) -> None:
    with pytest.raises(ValueError):
        order_service.set_storekeeper(
            first_order_data[0], storekeeper_repo.get_storekeeper1()[0].id)


def test_set_storekeeper_order_error(
    order_service: OrderService,
    storekeeper_repo: Storekeeper1Repo
) -> None:
    with pytest.raises(KeyError):
        order_service.set_storekeeper(
            uuid4(), storekeeper_repo.get_storekeeper1()[0].id)


def test_set_storekeeper_storekeeper_error(
    first_order_data: tuple[UUID, str, datetime],
    order_service: OrderService
) -> None:
    with pytest.raises(ValueError):
        order_service.set_storekeeper(first_order_data[0], uuid4())


def test_finish_order_status_error(
    first_order_data: tuple[UUID, str, datetime],
    order_service: OrderService
) -> None:
    with pytest.raises(ValueError):
        order_service.finish_order(first_order_data[0])


def test_finish_order_not_found(
    order_service: OrderService
) -> None:
    with pytest.raises(KeyError):
        order_service.finish_order(uuid4())


def test_cancel_order(
    second_order_data: tuple[UUID, str, datetime],
    order_service: OrderService
) -> None:
    order = order_service.cancel_order(second_order_data[0])
    assert order.status == OrderStatuses.CANCELED
    assert order.id == second_order_data[0]


def test_activate_order_status_error(
    second_order_data: tuple[UUID, str, datetime],
    order_service: OrderService
) -> None:
    with pytest.raises(ValueError):
        order_service.activate_order(second_order_data[0])


def test_activate_order_not_found(
    order_service: OrderService
) -> None:
    with pytest.raises(KeyError):
        order_service.activate_order(uuid4())


def test_activate_order(
    first_order_data: tuple[UUID, str, datetime],
    order_service: OrderService
) -> None:
    order = order_service.activate_order(first_order_data[0])
    assert order.status == OrderStatuses.ACTIVATED
    assert order.id == first_order_data[0]


def test_set_storekeeper(
    first_order_data: tuple[UUID, str, datetime],
    order_service: OrderService,
    storekeeper_repo: Storekeeper1Repo
) -> None:
    storekeeper = storekeeper_repo.get_storekeeper1()[0]
    order = order_service.set_storekeeper(
        first_order_data[0], storekeeper.id)
    assert order.status == OrderStatuses.ACTIVATED
    assert order.id == first_order_data[0]
    assert order.storekeeper.id == storekeeper.id
    assert order.storekeeper.name == storekeeper.name


def test_change_storekeeper(
    first_order_data: tuple[UUID, str, datetime],
    order_service: OrderService,
    storekeeper_repo: Storekeeper1Repo
) -> None:
    storekeeper = storekeeper_repo.get_storekeeper1()[1]
    order = order_service.set_storekeeper(
        first_order_data[0], storekeeper.id)
    assert order.status == OrderStatuses.ACTIVATED
    assert order.id == first_order_data[0]
    assert order.storekeeper.id == storekeeper.id
    assert order.storekeeper.name == storekeeper.name


def test_finish_order(
    first_order_data: tuple[UUID, str, datetime],
    order_service: OrderService
) -> None:
    order = order_service.finish_order(first_order_data[0])
    assert order.status == OrderStatuses.DONE
    assert order.id == first_order_data[0]


def test_cancel_order_status_error(
    first_order_data: tuple[UUID, str, datetime],
    order_service: OrderService
) -> None:
    with pytest.raises(ValueError):
        order_service.cancel_order(first_order_data[0])


def test_cancel_order_not_found(
    order_service: OrderService
) -> None:
    with pytest.raises(KeyError):
        order_service.cancel_order(uuid4())
