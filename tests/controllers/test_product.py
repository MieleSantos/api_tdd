from fastapi import status

from tests.factories import product_data_sucess


async def test_controller_post_should_return_sucess(client, products_url):
    response = await client.post(products_url, json=product_data_sucess())
    content = response.json()

    del content["created_at"]
    del content["updated_at"]
    del content["id"]

    assert response.status_code == status.HTTP_201_CREATED

    assert content == {
        "name": "Iphone 14 Pro Max",
        "quantity": 10,
        "price": "8.500",
        "status": True,
    }


async def test_controller_get_should_return_sucess(
    client, products_url, product_insert
):
    response = await client.get(f"{products_url}{product_insert.id}")
    assert response.status_code == status.HTTP_200_OK


async def test_controller_query_should_return_sucess(client, products_url):
    response = await client.get(products_url)
    assert response.status_code == status.HTTP_200_OK


async def test_controller_patch_should_return_sucess(
    client, products_url, product_insert
):
    response = await client.patch(
        f"{products_url}{product_insert.id}", json={"price": "1000"}
    )
    assert response.status_code == status.HTTP_200_OK


async def test_controller_delete_should_return_sucess(
    client, products_url, product_insert
):
    response = await client.delete(f"{products_url}{product_insert.id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
