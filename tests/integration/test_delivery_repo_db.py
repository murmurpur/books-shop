# /tests/integration/test_order_repo_db.py

import pytest
from uuid import uuid4
from time import sleep
from datetime import datetime

from app.models.order import Order, OrderStatuses
from app.repositories.db_order_repo import OrderRepo
from app.repositories.local_storekeeper_repo import Storekeeper1Repo

sleep(5)


@pytest.fixture()
def order_repo() -> Storekeeper1Repo:
    repo = OrderRepo()
    return repo


@pytest.fixture(scope='session')
def storekeeper_repo() -> Storekeeper1Repo:
    return Storekeeper1Repo()


@pytest.fixture(scope='session')
def first_order() -> Order:
    return Order(id=uuid4(), address='address', date=datetime.now(), status=OrderStatuses.CREATED)


@pytest.fixture(scope='session')
def second_order() -> Order:
    return Order(id=uuid4(), address='address1', date=datetime.now(), status=OrderStatuses.CREATED)


def test_empty_list(order_repo: Storekeeper1Repo) -> None:
    assert order_repo.get_orders() == []


def test_add_first_order(first_order: Order, order_repo: Storekeeper1Repo) -> None:
    assert order_repo.create_order(first_order) == first_order


def test_add_first_order_repeat(first_order: Order, order_repo: Storekeeper1Repo) -> None:
    with pytest.raises(KeyError):
        order_repo.create_order(first_order)


def test_get_order_by_id(first_order: Order, order_repo: Storekeeper1Repo) -> None:
    assert order_repo.get_order_by_id(
        first_order.id) == first_order


def test_get_order_by_id_error(order_repo: Storekeeper1Repo) -> None:
    with pytest.raises(KeyError):
        order_repo.get_order_by_id(uuid4())


def test_add_second_order(first_order: Order, second_order: Order, order_repo: Storekeeper1Repo) -> None:
    assert order_repo.create_order(second_order) == second_order
    orders = order_repo.get_orders()
    assert len(orders) == 2
    assert orders[0] == first_order
    assert orders[1] == second_order


def test_set_status(first_order: Order, order_repo: Storekeeper1Repo) -> None:
    first_order.status = OrderStatuses.ACTIVATED
    assert order_repo.set_status(
        first_order).status == first_order.status

    first_order.status = OrderStatuses.CANCELED
    assert order_repo.set_status(
        first_order).status == first_order.status

    first_order.status = OrderStatuses.DONE
    assert order_repo.set_status(
        first_order).status == first_order.status

    first_order.status = OrderStatuses.CREATED
    assert order_repo.set_status(
        first_order).status == first_order.status


def test_set_storekeeper(first_order: Order, storekeeper_repo: Storekeeper1Repo, order_repo: Storekeeper1Repo) -> None:
    first_order.storekeeper = storekeeper_repo.get_storekeeper1()[0]
    assert order_repo.set_storekeeper(
        first_order).storekeeper == storekeeper_repo.get_storekeeper1()[0]


def test_change_storekeeper(first_order: Order, storekeeper_repo: Storekeeper1Repo, order_repo: Storekeeper1Repo) -> None:
    first_order.storekeeper = storekeeper_repo.get_storekeeper1()[1]
    assert order_repo.set_storekeeper(
        first_order).storekeeper == storekeeper_repo.get_storekeeper1()[1]
