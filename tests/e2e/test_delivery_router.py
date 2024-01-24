# /tests/e2e/test_delivery_router.py

import time
import pytest
import requests
from uuid import UUID, uuid4
from datetime import datetime

from app.models.delivery import Delivery, DeliveryStatuses


time.sleep(5)
base_url = 'http://localhost:8000/api'


@pytest.fixture(scope='session')
def first_delivery_data() -> tuple[UUID, str, datetime]:
    return (uuid4(), 'address_1', datetime.now())


@pytest.fixture(scope='session')
def second_delivery_data() -> tuple[UUID, str, datetime]:
    return (uuid4(), 'address_2', datetime.now())


def test_get_deliveries_empty() -> None:
    assert requests.get(f'{base_url}/delivery').json() == []


def test_add_delivery_first_success(
    first_delivery_data: tuple[UUID, str, datetime]
) -> None:
    order_id, address, date = first_delivery_data
    delivery = Delivery.model_validate(requests.post(f'{base_url}/delivery', json={
        'order_id': order_id.hex,
        'date': str(date),
        'address': address
    }).json())
    assert delivery.id == order_id
    assert delivery.status == DeliveryStatuses.CREATED
    assert delivery.date == date
    assert delivery.address == address


def test_add_delivery_first_repeat_error(
    first_delivery_data: tuple[UUID, str, datetime]
) -> None:
    order_id, address, date = first_delivery_data
    result = requests.post(f'{base_url}/delivery', json={
        'order_id': order_id.hex,
        'date': str(date),
        'address': address
    })

    assert result.status_code == 400


def test_cancel_delivery_not_found() -> None:
    result = requests.post(f'{base_url}/delivery/{uuid4()}/cancel')

    assert result.status_code == 404


def test_finish_delivery_not_found() -> None:
    result = requests.post(f'{base_url}/delivery/{uuid4()}/finish')

    assert result.status_code == 404


def test_activate_delivery_not_found() -> None:
    result = requests.post(f'{base_url}/delivery/{uuid4()}/activate')

    assert result.status_code == 404


def test_cancel_delivery_success(
    first_delivery_data: tuple[UUID, str, datetime]
) -> None:
    order_id, address, date = first_delivery_data
    delivery = Delivery.model_validate_json(requests.post(
        f'{base_url}/delivery/{order_id}/cancel').text)

    assert delivery.id == order_id
    assert delivery.date == date
    assert delivery.address == address
    assert delivery.status == DeliveryStatuses.CANCELED


def test_finish_delivery_status_error(
    first_delivery_data: tuple[UUID, str, datetime]
) -> None:
    order_id = first_delivery_data[0]
    result = requests.post(f'{base_url}/delivery/{order_id}/finish')

    assert result.status_code == 400


def test_activate_delivery_status_error(
    first_delivery_data: tuple[UUID, str, datetime]
) -> None:
    order_id = first_delivery_data[0]
    result = requests.post(f'{base_url}/delivery/{order_id}/activate')

    assert result.status_code == 400


def test_add_delivery_second_success(
    second_delivery_data: tuple[UUID, str, datetime]
) -> None:
    order_id, address, date = second_delivery_data
    delivery = Delivery.model_validate(requests.post(f'{base_url}/delivery', json={
        'order_id': order_id.hex,
        'date': str(date),
        'address': address
    }).json())
    assert delivery.id == order_id
    assert delivery.status == DeliveryStatuses.CREATED
    assert delivery.date == date
    assert delivery.address == address


def test_get_deliveries_full(
    first_delivery_data: tuple[UUID, str, datetime],
    second_delivery_data: tuple[UUID, str, datetime]
) -> None:
    deliveries = [Delivery.model_validate(
        d) for d in requests.get(f'{base_url}/delivery').json()]
    assert len(deliveries) == 2
    assert deliveries[0].id == first_delivery_data[0]
    assert deliveries[1].id == second_delivery_data[0]


def test_set_deliveryman_delivery_not_found() -> None:
    result = requests.post(
        f'{base_url}/delivery/{uuid4()}/appoint', json={'deliveryman_id': uuid4().hex})

    assert result.status_code == 404


def test_set_deliveryman_deliveryman_not_found(
    first_delivery_data: tuple[UUID, str, datetime]
) -> None:
    order_id = first_delivery_data[0]
    result = requests.post(
        f'{base_url}/delivery/{order_id}/appoint', json={'deliveryman_id': uuid4().hex})

    assert result.status_code == 400


def test_set_deliveryman_status_error(
    first_delivery_data: tuple[UUID, str, datetime]
) -> None:
    order_id = first_delivery_data[0]
    result = requests.post(f'{base_url}/delivery/{order_id}/appoint',
                           json={'deliveryman_id': '45309954-8e3c-4635-8066-b342f634252c'})

    assert result.status_code == 400


def test_activate_delivery_success(
    second_delivery_data: tuple[UUID, str, datetime]
) -> None:
    order_id, address, date = second_delivery_data
    delivery = Delivery.model_validate_json(requests.post(
        f'{base_url}/delivery/{order_id}/activate').text)
    assert delivery.id == order_id
    assert delivery.status == DeliveryStatuses.ACTIVATED
    assert delivery.date == date
    assert delivery.address == address


def test_set_deliveryman_success(
    second_delivery_data: tuple[UUID, str, datetime]
) -> None:
    order_id, address, date = second_delivery_data
    delivery = Delivery.model_validate_json(requests.post(f'{base_url}/delivery/{order_id}/appoint',
                                                          json={'deliveryman_id': '45309954-8e3c-4635-8066-b342f634252c'}).text)

    assert delivery.id == order_id
    assert delivery.status == DeliveryStatuses.ACTIVATED
    assert delivery.date == date
    assert delivery.address == address


def test_finish_delivery_success(
    second_delivery_data: tuple[UUID, str, datetime]
) -> None:
    order_id, address, date = second_delivery_data
    delivery = Delivery.model_validate_json(requests.post(
        f'{base_url}/delivery/{order_id}/finish').text)
    assert delivery.id == order_id
    assert delivery.status == DeliveryStatuses.DONE
    assert delivery.date == date
    assert delivery.address == address


def test_cancel_delivery_status_error(
    second_delivery_data: tuple[UUID, str, datetime]
) -> None:
    order_id = second_delivery_data[0]
    result = requests.post(f'{base_url}/delivery/{order_id}/cancel')

    assert result.status_code == 400
