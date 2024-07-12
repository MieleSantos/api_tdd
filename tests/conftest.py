import asyncio
from uuid import UUID

import pytest
from httpx import AsyncClient

from store.db.mongo import db_client
from store.schemas.product import ProductIn, ProductUpdate
from store.usecases.product import product_use_case
from tests.factories import product_data_sucess, products_data_sucess


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture()
def mongo_client():
    return db_client.get()


@pytest.fixture(autouse=True)
async def clear_collections(mongo_client):
    yield
    collection_names = await mongo_client.get_database().list_collection_names()
    for collection_name in collection_names:
        if collection_name.startswith("system"):
            continue

    await mongo_client.get_database()[collection_name].delete_many({})


@pytest.fixture()
async def client() -> AsyncClient:  # type: ignore
    from store.main import app

    async with AsyncClient(app=app, base_url="htpp://test") as ac:
        yield ac


@pytest.fixture()
def products_url() -> str:
    return "/products/"


@pytest.fixture()
def product_id():
    return UUID("e2658700-6540-4720-a9ce-4bca2c848630")


@pytest.fixture()
def product_in():
    return ProductIn(**product_data_sucess())


@pytest.fixture()
def product_up():
    return ProductUpdate(**product_data_sucess())


@pytest.fixture()
async def product_insert(product_in):
    return await product_use_case.create(body=product_in)


@pytest.fixture()
def products_in():
    return [ProductIn(**product) for product in products_data_sucess()]


@pytest.fixture()
async def products_insert(products_in):
    return [
        await product_use_case.create(body=product_in) for product_in in products_in
    ]
