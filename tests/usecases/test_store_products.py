import pytest

from store.exceptions.base import (InvalidProductId, ProductInsertionError,
                                   ProductNotFound)
from store.schemas.product import ProductIn, ProductOut, ProductUpdate
from store.usecases.product import product_usecase
from tests.factories import (consumer_products_data, electronics_products_data,
                             products_by_price_range, sports_products_data)


class TestStoreVariedProducts:
    """Testes para produtos variados da loja"""

    @pytest.mark.asyncio
    async def test_create_electronics_products(self):
        """Test: Criar produtos eletrônicos"""
        electronics = electronics_products_data()[:3]  # Primeiros 3
        created_products = []

        for product_data in electronics:
            body = ProductIn(**product_data)
            result = await product_usecase.create(body=body)
            created_products.append(result)

        assert len(created_products) == 3
        assert created_products[0].name == "iPhone 15 Pro Max"
        assert created_products[1].price == 7500.00

    @pytest.mark.asyncio
    async def test_create_sports_products(self):
        """Test: Criar produtos esportivos"""
        sports = sports_products_data()[:2]  # Primeiros 2
        created_products = []

        for product_data in sports:
            body = ProductIn(**product_data)
            result = await product_usecase.create(body=body)
            created_products.append(result)

        assert len(created_products) == 2
        assert "Nike" in created_products[0].name
        assert created_products[1].price == 749.90

    @pytest.mark.asyncio
    async def test_price_filter_range_5000_to_8000(self):
        """Test: Filtro de preço entre R$ 5000 e R$ 8000"""
        # Criar alguns produtos primeiro
        test_products = [
            {"name": "Produto Barato", "price": 100.00, "quantity": 10, "status": True},
            {"name": "iPhone 13", "price": 5500.00, "quantity": 5, "status": True},
            {"name": "Dell XPS 13", "price": 6800.00, "quantity": 3, "status": True},
            {"name": "iPhone 14 Pro", "price": 7500.00, "quantity": 2, "status": True},
            {"name": "MacBook Pro", "price": 15000.00, "quantity": 1, "status": True},
        ]

        for product_data in test_products:
            body = ProductIn(**product_data)
            await product_usecase.create(body=body)

        # Filtrar produtos entre R$ 5000 e R$ 8000
        filtered_products = await product_usecase.query_by_price_range(
            min_price=5000, max_price=8000
        )

        assert len(filtered_products) == 3
        for product in filtered_products:
            assert 5000 <= product.price <= 8000

    @pytest.mark.asyncio
    async def test_luxury_products_filter(self):
        """Test: Filtro de produtos de luxo (> R$ 5000)"""
        # Criar produtos de diferentes faixas de preço
        luxury_data = [
            {
                "name": "iPhone 15 Pro Max",
                "price": 10500.00,
                "quantity": 2,
                "status": True,
            },
            {
                "name": "MacBook Pro M3",
                "price": 15000.00,
                "quantity": 1,
                "status": True,
            },
        ]

        regular_data = [
            {"name": "Camisa Nike", "price": 149.90, "quantity": 20, "status": True},
            {"name": "Tênis Adidas", "price": 450.00, "quantity": 10, "status": True},
        ]

        # Criar produtos
        for product_data in luxury_data + regular_data:
            body = ProductIn(**product_data)
            await product_usecase.create(body=body)

        # Buscar produtos de luxo
        luxury_products = await product_usecase.get_luxury_products()

        assert len(luxury_products) == 2
        for product in luxury_products:
            assert product.price > 5000

    @pytest.mark.asyncio
    async def test_search_products_by_name(self):
        """Test: Buscar produtos por nome"""
        # Criar produtos com nomes específicos
        products_data = [
            {
                "name": "iPhone 14 Pro Max",
                "price": 8500.00,
                "quantity": 5,
                "status": True,
            },
            {"name": "iPhone 13", "price": 5500.00, "quantity": 8, "status": True},
            {
                "name": "Samsung Galaxy S24",
                "price": 7200.00,
                "quantity": 3,
                "status": True,
            },
            {
                "name": "Nike Air Jordan",
                "price": 899.90,
                "quantity": 15,
                "status": True,
            },
        ]

        for product_data in products_data:
            body = ProductIn(**product_data)
            await product_usecase.create(body=body)

        # Buscar por "iPhone"
        iphone_products = await product_usecase.search_products("iPhone")
        assert len(iphone_products) == 2

        # Buscar por "Nike"
        nike_products = await product_usecase.search_products("Nike")
        assert len(nike_products) == 1
