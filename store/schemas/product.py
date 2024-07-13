from datetime import datetime
from decimal import Decimal
from typing import Annotated, Optional

from bson import Decimal128
from pydantic import UUID4, AfterValidator, BaseModel, Field, model_validator

from store.schemas.base import BaseSchemaMixin


class ProductBase(BaseModel):
    name: str = Field(description="Product name")
    quantity: int = Field(description="Product quantity")
    price: Decimal = Field(
        description="Product price",
    )
    status: bool = Field(description="Product status")


#    @model_validator(mode="before")
#    def set_price(cls, price):
#        if price["price"] >= 5000 and price["price"] <= 8000:
#            return price["price"]
#        else:
#            raise ValueError(f"Price  {price['price']}  not => 5000 and <= 8000")


class ProductIn(ProductBase, BaseSchemaMixin): ...


class ProductOut(ProductIn):
    id: UUID4 = Field()
    created_at: datetime = Field()
    updated_at: datetime = Field()

    @model_validator(mode="before")
    def set_schema(cls, data):
        for key, value in data.items():
            if isinstance(value, Decimal128):
                data[key] = Decimal(str(value))
        return data


def convert_decimal_128(v):
    return Decimal128(str(v))


Decimal_ = Annotated[Decimal, AfterValidator(convert_decimal_128)]


class ProductUpdate(BaseSchemaMixin):
    quantity: Optional[int] = Field(None, description="Product quantity")
    price: Optional[Decimal_] = Field(None, description="Product price")
    status: Optional[bool] = Field(None, description="Product status")


class ProductUpdateOut(ProductOut): ...
