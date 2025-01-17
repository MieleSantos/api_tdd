from uuid import UUID

import pymongo
from motor.motor_asyncio import AsyncIOMotorClient

from store.core.exceptions import NotFoundException
from store.db.mongo import db_client
from store.models.product import ProductModel
from store.schemas.product import ProductIn, ProductOut, ProductUpdate, ProductUpdateOut


class ProductUsecase:
    def __init__(self) -> None:
        self.client: AsyncIOMotorClient = db_client.get()
        self.database: AsyncIOMotorClient = self.client.get_database()
        self.collection = self.database.get_collection("products")

    async def create(self, body: ProductIn) -> ProductOut:
        product_model = ProductModel(**body.model_dump())
        await self.collection.insert_one(product_model.model_dump())

        return ProductOut(**product_model.model_dump())

    async def get(self, id: UUID) -> ProductOut:
        result = await self.collection.find_one({"id": id})

        if not result:
            raise NotFoundException(message=f"Product not found filter: {id}")
        return ProductOut(**result)

    async def get_filter(self) -> list[ProductOut]:

        result = self.collection.find({"price": {"$gte": 5000, "$lte": 8000}})

        if not result:
            raise NotFoundException(
                message=f"Products not found with price >= 5000 and price <=8000"
            )
        return [ProductOut(**item) async for item in result]

    async def query(self) -> list[ProductOut]:
        return [ProductOut(**item) async for item in self.collection.find()]

    async def update(self, id: UUID, body: ProductUpdate) -> ProductUpdateOut:
        result = await self.collection.find_one_and_update(
            filter={"id": id},
            update={
                "$set": body.model_dump(exclude_none=True, exclude="created_at"),
            },
            return_document=pymongo.ReturnDocument.AFTER,
        )

        return ProductUpdateOut(**result)

    async def delete(self, id: UUID) -> bool:
        product = await self.collection.find_one({"id": id})
        if not product:
            raise NotFoundException(message=f"Product not found filter: {id}")

        result = await self.collection.delete_one({"id": id})
        return True if result.deleted_count > 0 else False


product_use_case = ProductUsecase()
