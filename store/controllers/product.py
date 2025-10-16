"""
Controllers FastAPI para produtos
Seguindo padrão da professora Nayanna Nara - DIO.me Store API
"""
from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException, Path, status
from pydantic import UUID4

from store.exceptions.base import (InvalidProductId, ProductInsertionError,
                                   ProductNotFound)
from store.schemas.product import (ProductIn, ProductOut, ProductUpdate,
                                   ProductUpdateOut)
from store.usecases.product import product_usecase

router = APIRouter(tags=["products"])


def get_product_usecase():
    """Dependency injection do usecase"""
    return product_usecase


@router.post(path="/", status_code=status.HTTP_201_CREATED)
async def post(
    body: ProductIn = Body(...), usecase=Depends(get_product_usecase)
) -> ProductOut:
    """
    CREATE - Criar novo produto

    **Desafio 1**: Capturar exceções de inserção na controller
    """
    try:
        return await usecase.create(body=body)
    except ProductInsertionError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Erro na inserção do produto: {exc.message}",
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor durante a criação do produto",
        )


@router.get(path="/{id}", status_code=status.HTTP_200_OK)
async def get(
    id: str = Path(alias="id"), usecase=Depends(get_product_usecase)
) -> ProductOut:
    """GET - Buscar produto por ID"""
    try:
        return await usecase.get(id=id)
    except ProductNotFound as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message)
    except InvalidProductId as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=exc.message)


@router.get(path="/", status_code=status.HTTP_200_OK)
async def query(usecase=Depends(get_product_usecase)) -> List[ProductOut]:
    """QUERY - Listar todos os produtos"""
    return await usecase.query()


@router.patch(path="/{id}", status_code=status.HTTP_200_OK)
async def patch(
    id: str = Path(alias="id"),
    body: ProductUpdate = Body(...),
    usecase=Depends(get_product_usecase),
) -> ProductOut:
    """
    UPDATE - Atualizar produto (PATCH)

    **Desafio 2**: Exceção Not Found tratada na controller
    **Desafio 2**: updated_at atualizado automaticamente
    """
    try:
        return await usecase.update(id=id, body=body)
    except ProductNotFound as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Produto não encontrado para atualização: {exc.message}",
        )
    except InvalidProductId as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=exc.message)


@router.delete(path="/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    id: str = Path(alias="id"), usecase=Depends(get_product_usecase)
) -> None:
    """DELETE - Remover produto"""
    try:
        await usecase.delete(id=id)
    except ProductNotFound as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message)
    except InvalidProductId as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=exc.message)


# ============================================================================
# ENDPOINTS EXTRAS - DESAFIO 3: FILTROS
# ============================================================================


@router.get(path="/filter/price-range/", status_code=status.HTTP_200_OK)
async def filter_by_price_range(
    min_price: float = 5000,
    max_price: float = 8000,
    usecase=Depends(get_product_usecase),
) -> List[ProductOut]:
    """
    **Desafio 3**: Filtro de preço (price > 5000 and price < 8000)

    Query Parameters:
    - min_price: Preço mínimo (default: 5000)
    - max_price: Preço máximo (default: 8000)
    """
    return await usecase.query_by_price_range(min_price, max_price)


@router.get(path="/filter/luxury/", status_code=status.HTTP_200_OK)
async def get_luxury_products(usecase=Depends(get_product_usecase)) -> List[ProductOut]:
    """Filtro: Produtos de luxo (> R$ 5.000)"""
    return await usecase.get_luxury_products()


@router.get(path="/filter/affordable/", status_code=status.HTTP_200_OK)
async def get_affordable_products(
    usecase=Depends(get_product_usecase),
) -> List[ProductOut]:
    """Filtro: Produtos acessíveis (< R$ 500)"""
    return await usecase.get_affordable_products()


@router.get(path="/search/", status_code=status.HTTP_200_OK)
async def search_products(
    q: str, usecase=Depends(get_product_usecase)
) -> List[ProductOut]:
    """
    Busca de produtos por nome

    Query Parameters:
    - q: Termo de busca
    """
    return await usecase.search_products(q)
