# /tests/unit/test_delivery_model.py

import pytest
from uuid import uuid4
from datetime import datetime
from pydantic import ValidationError

from app.models.deliveryman import Deliveryman
from app.models.delivery import Delivery, DeliveryStatuses


@pytest.fixture()
def any_deliveryman() -> Deliveryman:
    return Deliveryman(id=uuid4(), name='delliveryman')


def test_delivery_creation(any_deliveryman: Deliveryman):
    id = uuid4()
    address = 'address'
    date = datetime.now()
    status = DeliveryStatuses.DONE
    delivery = Delivery(id=id, address=address, date=date,
                        status=status, deliveryman=any_deliveryman)

    assert dict(delivery) == {'id': id, 'address': address, 'status': status,
                              'deliveryman': any_deliveryman, 'date': date}


def test_delivery_address_required(any_deliveryman: Deliveryman):
    with pytest.raises(ValidationError):
        Delivery(id=uuid4(), date=datetime.now(),
                 status=DeliveryStatuses.ACTIVATED, deliveryman=any_deliveryman)


def test_delivery_date_required(any_deliveryman: Deliveryman):
    with pytest.raises(ValidationError):
        Delivery(id=uuid4(), address='str',
                 status=DeliveryStatuses.ACTIVATED, deliveryman=any_deliveryman)


def test_delivery_status_required(any_deliveryman: Deliveryman):
    with pytest.raises(ValidationError):
        Delivery(id=uuid4(), date=datetime.now(),
                 address='str', deliveryman=any_deliveryman)
