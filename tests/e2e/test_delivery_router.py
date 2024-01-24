# /tests/e2e/test_order_router.py

import time
import pytest
import requests
from uuid import UUID, uuid4
from datetime import datetime

from app.models.order import Order, OrderStatuses


time.sleep(5)
base_url = 'http://localhost:8000/api'


@pytest.fixture(scope='session')
def first_order_data() -> tuple[UUID, str, datetime]:
    return (uuid4(), 'address_1', datetime.now())


@pytest.fixture(scope='session')
def second_order_data() -> tuple[UUID, str, datetime]:
    return (uuid4(), 'address_2', datetime.now())


def test_get_orders_empty() -> None:
    assert requests.get(f'{base_url}/order').json() == []


def test_add_order_first_success(
    first_order_data: tuple[UUID, str, datetime]
) -> None:
    order_id, address, date = first_order_data
    order = Order.model_validate(requests.post(f'{base_url}/order', json={
        'order_id': order_id.hex,
        'date': str(date),
        'address': address
    }).json())
    assert order.id == order_id
    assert order.status == OrderStatuses.CREATED
    assert order.date == date
    assert order.address == address


def test_add_order_first_repeat_error(
    first_order_data: tuple[UUID, str, datetime]
) -> None:
    order_id, address, date = first_order_data
    result = requests.post(f'{base_url}/order', json={
        'order_id': order_id.hex,
        'date': str(date),
        'address': address
    })

    assert result.status_code == 400


def test_cancel_order_not_found() -> None:
    result = requests.post(f'{base_url}/order/{uuid4()}/cancel')

    assert result.status_code == 404


def test_finish_order_not_found() -> None:
    result = requests.post(f'{base_url}/order/{uuid4()}/finish')

    assert result.status_code == 404


def test_activate_order_not_found() -> None:
    result = requests.post(f'{base_url}/order/{uuid4()}/activate')

    assert result.status_code == 404


def test_cancel_order_success(
    first_order_data: tuple[UUID, str, datetime]
) -> None:
    order_id, address, date = first_order_data
    order = Order.model_validate_json(requests.post(
        f'{base_url}/order/{order_id}/cancel').text)

    assert order.id == order_id
    assert order.date == date
    assert order.address == address
    assert order.status == OrderStatuses.CANCELED


def test_finish_order_status_error(
    first_order_data: tuple[UUID, str, datetime]
) -> None:
    order_id = first_order_data[0]
    result = requests.post(f'{base_url}/order/{order_id}/finish')

    assert result.status_code == 400


def test_activate_order_status_error(
    first_order_data: tuple[UUID, str, datetime]
) -> None:
    order_id = first_order_data[0]
    result = requests.post(f'{base_url}/order/{order_id}/activate')

    assert result.status_code == 400


def test_add_order_second_success(
    second_order_data: tuple[UUID, str, datetime]
) -> None:
    order_id, address, date = second_order_data
    order = Order.model_validate(requests.post(f'{base_url}/order', json={
        'order_id': order_id.hex,
        'date': str(date),
        'address': address
    }).json())
    assert order.id == order_id
    assert order.status == OrderStatuses.CREATED
    assert order.date == date
    assert order.address == address


def test_get_orders_full(
    first_order_data: tuple[UUID, str, datetime],
    second_order_data: tuple[UUID, str, datetime]
) -> None:
    orders = [Order.model_validate(
        d) for d in requests.get(f'{base_url}/order').json()]
    assert len(orders) == 2
    assert orders[0].id == first_order_data[0]
    assert orders[1].id == second_order_data[0]


def test_set_storekeeper_order_not_found() -> None:
    result = requests.post(
        f'{base_url}/order/{uuid4()}/appoint', json={'storekeeper_id': uuid4().hex})

    assert result.status_code == 404


def test_set_storekeeper_storekeeper_not_found(
    first_order_data: tuple[UUID, str, datetime]
) -> None:
    order_id = first_order_data[0]
    result = requests.post(
        f'{base_url}/order/{order_id}/appoint', json={'storekeeper_id': uuid4().hex})

    assert result.status_code == 400


def test_set_storekeeper_status_error(
    first_order_data: tuple[UUID, str, datetime]
) -> None:
    order_id = first_order_data[0]
    result = requests.post(f'{base_url}/order/{order_id}/appoint',
                           json={'storekeeper_id': '45309954-8e3c-4635-8066-b342f634252c'})

    assert result.status_code == 400


def test_activate_order_success(
    second_order_data: tuple[UUID, str, datetime]
) -> None:
    order_id, address, date = second_order_data
    order = Order.model_validate_json(requests.post(
        f'{base_url}/order/{order_id}/activate').text)
    assert order.id == order_id
    assert order.status == OrderStatuses.ACTIVATED
    assert order.date == date
    assert order.address == address


def test_set_storekeeper_success(
    second_order_data: tuple[UUID, str, datetime]
) -> None:
    order_id, address, date = second_order_data
    order = Order.model_validate_json(requests.post(f'{base_url}/order/{order_id}/appoint',
                                                          json={'storekeeper_id': '45309954-8e3c-4635-8066-b342f634252c'}).text)

    assert order.id == order_id
    assert order.status == OrderStatuses.ACTIVATED
    assert order.date == date
    assert order.address == address


def test_finish_order_success(
    second_order_data: tuple[UUID, str, datetime]
) -> None:
    order_id, address, date = second_order_data
    order = Order.model_validate_json(requests.post(
        f'{base_url}/order/{order_id}/finish').text)
    assert order.id == order_id
    assert order.status == OrderStatuses.DONE
    assert order.date == date
    assert order.address == address


def test_cancel_order_status_error(
    second_order_data: tuple[UUID, str, datetime]
) -> None:
    order_id = second_order_data[0]
    result = requests.post(f'{base_url}/order/{order_id}/cancel')

    assert result.status_code == 400
