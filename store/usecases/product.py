import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo.errors import DuplicateKeyError, PyMongoError

from store.db.mongo import get_collection
from store.exceptions.base import (DatabaseConnectionError, InvalidProductId,
                                   ProductInsertionError, ProductNotFound,
                                   ProductUpdateError)
from store.models.product import ProductModel
from store.schemas.product import (ProductIn, ProductOut, ProductUpdate,
                                   ProductUpdateOut)


class ProductUsecase:
    def __init__(self) -> None:
        self._collection = None

    @property
    def collection(self) -> AsyncIOMotorCollection:
        if self._collection is None:
            self._collection = get_collection("products")
        return self._collection

    async def create(self, body: ProductIn) -> ProductOut:
        """
        Create a new product using ProductModel
        Seguindo padrão da professora Nayanna Nara - DIO.me Store API
        """
        try:
            # Usar ProductModel para criação (inclui id, created_at, updated_at automaticamente)
            product_model = ProductModel(**body.model_dump())

            # Inserir no MongoDB usando serialização do model
            await self.collection.insert_one(product_model.model_dump())

            # Retornar ProductOut com os dados do model criado
            return ProductOut(**product_model.model_dump())

        except DuplicateKeyError as e:
            raise ProductInsertionError(f"Product already exists: {str(e)}")
        except PyMongoError as e:
            raise DatabaseConnectionError(
                f"Database error during product creation: {str(e)}"
            )
        except Exception as e:
            raise ProductInsertionError(f"Unexpected error creating product: {str(e)}")

    async def get(self, id: str) -> ProductOut:
        """Get product by ID"""
        try:
            # Validar se é UUID válido
            uuid.UUID(id)
        except ValueError:
            raise InvalidProductId(id)

        try:
            # Buscar pelo campo id (UUID) em vez de _id (ObjectId)
            # Converter string para UUID para busca no MongoDB
            uuid_obj = uuid.UUID(id)
            result = await self.collection.find_one({"id": uuid_obj})
            if not result:
                raise ProductNotFound(id)

            return ProductOut(**result)
        except PyMongoError as e:
            raise DatabaseConnectionError(
                f"Database error retrieving product: {str(e)}"
            )

    async def query(self, filters: Optional[Dict[str, Any]] = None) -> List[ProductOut]:
        """Get all products with optional filters"""
        try:
            query_filter = filters or {}
            products = []
            async for product in self.collection.find(query_filter):
                products.append(ProductOut(**product))
            return products
        except PyMongoError as e:
            raise DatabaseConnectionError(f"Database error querying products: {str(e)}")

    async def query_by_price_range(
        self, min_price: float, max_price: float
    ) -> List[ProductOut]:
        """Get products within price range"""
        price_filter = {"price": {"$gte": min_price, "$lte": max_price}}
        return await self.query(filters=price_filter)

    async def query_by_category_and_price(
        self,
        category: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
    ) -> List[ProductOut]:
        """Get products by category and/or price range"""
        filters = {}

        if category:
            # Busca por nome que contenha a categoria
            filters["name"] = {"$regex": category, "$options": "i"}

        if min_price is not None or max_price is not None:
            price_filter = {}
            if min_price is not None:
                price_filter["$gte"] = min_price
            if max_price is not None:
                price_filter["$lte"] = max_price
            filters["price"] = price_filter

        return await self.query(filters=filters)

    async def get_luxury_products(self) -> List[ProductOut]:
        """Get luxury products (price > 5000)"""
        return await self.query_by_price_range(min_price=5000, max_price=float("inf"))

    async def get_affordable_products(self) -> List[ProductOut]:
        """Get affordable products (price < 500)"""
        return await self.query_by_price_range(min_price=0, max_price=500)

    async def search_products(self, search_term: str) -> List[ProductOut]:
        """Search products by name"""
        search_filter = {"name": {"$regex": search_term, "$options": "i"}}
        return await self.query(filters=search_filter)

    async def update(self, id: str, body: ProductUpdate) -> ProductUpdateOut:
        """Update product"""
        update_data = body.model_dump(exclude_unset=True)
        if not update_data:
            raise ProductUpdateError("No fields to update")

        try:
            # Validar se é UUID válido
            uuid.UUID(id)
        except ValueError:
            raise InvalidProductId(id)

        try:
            # Converter string para UUID para busca no MongoDB
            uuid_obj = uuid.UUID(id)

            # Verificar se produto existe antes de atualizar
            existing = await self.collection.find_one({"id": uuid_obj})
            if not existing:
                raise ProductNotFound(id)

            # Add/update timestamp (allow manual override)
            if "updated_at" not in update_data:
                update_data["updated_at"] = datetime.now()

            result = await self.collection.update_one(
                {"id": uuid_obj}, {"$set": update_data}
            )

            if result.matched_count == 0:
                raise ProductNotFound(id)

            return await self.get(id)

        except ProductNotFound:
            raise
        except PyMongoError as e:
            raise DatabaseConnectionError(f"Database error updating product: {str(e)}")
        except Exception as e:
            raise ProductUpdateError(f"Unexpected error updating product: {str(e)}")

    async def delete(self, id: str) -> bool:
        """Delete product"""
        try:
            # Validar se é UUID válido
            uuid.UUID(id)
        except ValueError:
            raise InvalidProductId(id)

        try:
            # Converter string para UUID para busca no MongoDB
            uuid_obj = uuid.UUID(id)

            # Verificar se produto existe antes de deletar
            existing = await self.collection.find_one({"id": uuid_obj})
            if not existing:
                raise ProductNotFound(id)

            result = await self.collection.delete_one({"id": uuid_obj})
            return result.deleted_count > 0

        except ProductNotFound:
            raise
        except PyMongoError as e:
            raise DatabaseConnectionError(f"Database error deleting product: {str(e)}")


product_usecase = ProductUsecase()
