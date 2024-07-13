from fastapi import APIRouter, Body, Depends, HTTPException, Path, status
from pydantic import UUID4

from store.core.exceptions import NotFoundException
from store.schemas.product import ProductIn, ProductOut, ProductUpdate
from store.usecases.product import ProductUsecase

router = APIRouter()


@router.post(
    path="/", status_code=status.HTTP_201_CREATED, description="Create product"
)
async def postin(
    body: ProductIn = Body(...),
    use_case: ProductUsecase = Depends(),  # type: ignore
) -> ProductOut:
    try:
        return await use_case.create(body=body)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error update products",
        )


@router.get(
    path="/{id}", status_code=status.HTTP_200_OK, description="Search for Id product"
)
async def get_id(
    id: UUID4 = Path(alias="id"),
    use_case: ProductUsecase = Depends(),  # type: ignore
) -> ProductOut:
    try:
        return await use_case.get(id=id)
    except NotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Products Not Found",
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    description="Search all products",
)
async def get(use_case: ProductUsecase = Depends()) -> list[ProductOut]:  # type: ignore
    try:
        return await use_case.query()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error search products",
        )


@router.get(
    path="/filter/",
    status_code=status.HTTP_200_OK,
    description="Search product with price >5000",
)
async def get_filter(use_case: ProductUsecase = Depends()) -> list[ProductOut]:  # type: ignore
    try:
        return await use_case.get_filter()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error search products",
        )


@router.patch(
    path="/{id}", status_code=status.HTTP_200_OK, description="Update product for Id"
)
async def patch(
    id: UUID4 = Path(alias="id"),
    body: ProductUpdate = Body(...),
    use_case: ProductUsecase = Depends(),  # type: ignore
) -> ProductOut:

    try:

        if await use_case.get(id=id):
            return await use_case.update(id=id, body=body)
    except NotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product Not Found",
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error update products",
        )


@router.delete(
    path="/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Delete product for Id",
)
async def delete(
    id: UUID4 = Path(alias="id"),
    use_case: ProductUsecase = Depends(),  # type: ignore
):

    try:
        if await use_case.get(id=id):
            return await use_case.delete(id=id)
    except NotFoundException:
        raise Exception(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product not found filter: {id}",
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error delete products",
        )
