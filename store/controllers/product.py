from fastapi import APIRouter, Body, Depends, Path, status
from pydantic import UUID4

from store.schemas.product import ProductIn, ProductOut, ProductUpdate
from store.usecases.product import ProductUsecase

router = APIRouter()


@router.post(path="/", status_code=status.HTTP_201_CREATED)
async def postin(
    body: ProductIn = Body(...),
    use_case: ProductUsecase = Depends(),  # type: ignore
) -> ProductOut:
    return await use_case.create(body=body)


@router.get(path="/{id}", status_code=status.HTTP_200_OK)
async def get(
    id: UUID4 = Path(alias="id"),
    use_case: ProductUsecase = Depends(),  # type: ignore
) -> ProductOut:
    return await use_case.get(id=id)


@router.get(path="/", status_code=status.HTTP_200_OK)
async def get(use_case: ProductUsecase = Depends()) -> list[ProductOut]:  # type: ignore
    return await use_case.query()


@router.patch(path="/{id}", status_code=status.HTTP_200_OK)
async def patch(
    id: UUID4 = Path(alias="id"),
    body: ProductUpdate = Body(...),
    use_case: ProductUsecase = Depends(),  # type: ignore
) -> ProductOut:
    return await use_case.update(id=id, body=body)


@router.delete(path="/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    id: UUID4 = Path(alias="id"),
    use_case: ProductUsecase = Depends(),  # type: ignore
):
    return await use_case.delete(id=id)
