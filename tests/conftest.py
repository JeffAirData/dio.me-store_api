"""
Configuração de testes - Pytest fixtures
Seguindo padrão da professora Nayanna Nara - DIO.me Store API
"""
import asyncio
from typing import List
from uuid import UUID

import pytest
from httpx import AsyncClient

from store.db.mongo import connect_to_mongo, get_collection
from store.schemas.product import ProductIn, ProductUpdate
from store.usecases.product import product_usecase
from tests.factories import iphone_14_pro_max_data

pytest_plugins = ("pytest_asyncio",)


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


@pytest.fixture
async def mongo_client():
    """MongoDB client for tests"""
    await connect_to_mongo()
    return get_collection("products").database.client


@pytest.fixture(autouse=True)
async def setup_database():
    """Setup database connection and clean for each test"""
    await connect_to_mongo()

    # Clean products collection
    products_collection = get_collection("products")
    await products_collection.delete_many({})

    yield


# ============================================================================
# FIXTURES PARA TESTES DE INTEGRAÇÃO HTTP (Controllers)
# ============================================================================


@pytest.fixture
async def client():
    """
    HTTP Client para testes de integração
    Seguindo padrão da professora Nayanna Nara
    """
    # Garantir conexão MongoDB antes do client
    await connect_to_mongo()

    from httpx import ASGITransport

    from store.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def products_url() -> str:
    """URL base dos produtos"""
    return "/products/"


# ============================================================================
# FIXTURES DE DADOS
# ============================================================================


@pytest.fixture
def product_id() -> UUID:
    """UUID fixo para testes"""
    return UUID("fce6cc37-10b9-4a8e-a8b2-977df327001a")


@pytest.fixture
def product_in(product_id):
    """Product input data with fixed ID"""
    return ProductIn(**iphone_14_pro_max_data(), id=product_id)


@pytest.fixture
def product_update(product_id):
    """Product update data with fixed ID"""
    return ProductUpdate(id=product_id, price=7500.0)


@pytest.fixture
async def product_inserted(product_in):
    """Insert a product and return it"""
    return await product_usecase.create(body=product_in)


@pytest.fixture
def products_in():
    """Multiple products input data"""
    from tests.factories import all_products_data

    return [ProductIn(**product) for product in all_products_data()]


@pytest.fixture
async def products_inserted(products_in):
    """Insert multiple products and return them"""
    return [await product_usecase.create(body=product_in) for product_in in products_in]
