# /tests/unit/test_order_model.py

import pytest
from uuid import uuid4
from datetime import datetime
from pydantic import ValidationError

from app.models.storekeeper import Storekeeper
from app.models.order import Order, OrderStatuses


@pytest.fixture()
def any_storekeeper() -> Storekeeper:
    return Storekeeper(id=uuid4(), name='delliveryman')


def test_order_creation(any_storekeeper: Storekeeper):
    id = uuid4()
    address = 'address'
    date = datetime.now()
    status = OrderStatuses.DONE
    order = Order(id=id, address=address, date=date,
                        status=status, storekeeper=any_storekeeper)

    assert dict(order) == {'id': id, 'address': address, 'status': status,
                              'storekeeper': any_storekeeper, 'date': date}


def test_order_address_required(any_storekeeper: Storekeeper):
    with pytest.raises(ValidationError):
        Order(id=uuid4(), date=datetime.now(),
                 status=OrderStatuses.ACTIVATED, storekeeper=any_storekeeper)


def test_order_date_required(any_storekeeper: Storekeeper):
    with pytest.raises(ValidationError):
        Order(id=uuid4(), address='str',
                 status=OrderStatuses.ACTIVATED, storekeeper=any_storekeeper)


def test_order_status_required(any_storekeeper: Storekeeper):
    with pytest.raises(ValidationError):
        Order(id=uuid4(), date=datetime.now(),
                 address='str', storekeeper=any_storekeeper)
