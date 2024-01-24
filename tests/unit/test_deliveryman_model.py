import pytest
from uuid import uuid4
from pydantic import ValidationError

from app.models.storekeeper import Storekeeper


def test_storekeeper_creation():
    id = uuid4()
    name = 'name'
    storekeeper = Storekeeper(id=id, name=name)

    assert dict(storekeeper) == {'id': id, 'name': name}


def test_storekeeper_name_required():
    with pytest.raises(ValidationError):
        Storekeeper(id=id)
