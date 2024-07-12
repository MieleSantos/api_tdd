from uuid import UUID

import pytest
from pydantic import ValidationError

from store.schemas.product import ProductIn
from tests.factories import product_data_raises, product_data_sucess


def test_schemas_return_sucess():
    # product = ProductIn(**data)
    product = ProductIn.model_validate(product_data_sucess())

    assert product.name == "Iphone 14 Pro Max"
    assert isinstance(product.quantity, int)
    # assert isinstance(product.price, float)
    assert isinstance(product.status, bool)
    assert isinstance(product.id, UUID)


def test_schemas_return_raise():
    with pytest.raises(ValidationError) as err:
        ProductIn.model_validate(product_data_raises())

    assert err.value.errors()[0] == {
        "type": "missing",
        "loc": ("status",),
        "msg": "Field required",
        "input": {"name": "Iphone 14 Pro Max", "quantity": 10, "price": "8.500"},
        "url": "https://errors.pydantic.dev/2.8/v/missing",
    }
