import pytest
from uuid import uuid4
from pydantic import ValidationError

from app.models.deliveryman import Deliveryman


def test_deliveryman_creation():
    id = uuid4()
    name = 'name'
    deliveryman = Deliveryman(id=id, name=name)

    assert dict(deliveryman) == {'id': id, 'name': name}


def test_deliveryman_name_required():
    with pytest.raises(ValidationError):
        Deliveryman(id=id)
