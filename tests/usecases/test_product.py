from store.usecases.product import product_use_case


async def test_usecases_shold_return_sucess(product_in):
    result = await product_use_case.create(body=product_in)

    # assert isinstance(result, ProductOut)
    assert result is None
