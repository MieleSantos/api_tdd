from typing import List
from uuid import UUID

import pytest

from store.core.exceptions import NotFoundException
from store.schemas.product import ProductOut, ProductUpdateOut
from store.usecases.product import product_use_case


async def test_usecases_shold_return_success(product_in):
    result = await product_use_case.create(body=product_in)

    assert isinstance(result, ProductOut)
    assert result.name == "Iphone 14 Pro Max"


async def test_usecases_get_shold_return_success(product_insert):
    result = await product_use_case.get(id=product_insert.id)

    assert isinstance(result, ProductOut)
    assert result.name == "Iphone 14 Pro Max"


async def test_usecases_get_shold_return_not_found():
    with pytest.raises(NotFoundException) as err:
        id = UUID("9f798ec2-32e4-4215-9806-24abf9451c7c")
        await product_use_case.get(id=id)

    assert err.value.message == f"Product not found filter: {id}"


@pytest.mark.usefixtures("products_insert")
async def test_usecases_query_should_return_success():
    result = await product_use_case.query()
    assert isinstance(result, List)
    assert len(result) > 1


async def test_usecases_update_should_return_success(product_up, product_insert):
    product_up.price = 7.500
    result = await product_use_case.update(id=product_insert.id, body=product_up)
    assert isinstance(result, ProductUpdateOut)


async def test_usecase_delete_should_return_success(product_insert):
    result = await product_use_case.delete(id=product_insert.id)
    assert result is True


async def test_usecase_delete_should_not_found():
    with pytest.raises(NotFoundException) as err:
        id = UUID("9f798ec2-32e4-4215-9806-24abf9451c7c")
        await product_use_case.delete(id=id)

    assert err.value.message == f"Product not found filter: {id}"
