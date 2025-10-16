import pytest

from store.schemas.product import ProductIn, ProductOut, ProductUpdate
from store.usecases.product import product_usecase
from tests.factories import product_data


class TestProductUsecase:
    @pytest.mark.asyncio
    async def test_create_product_should_return_success(self):
        """Test: Criar produto deve retornar sucesso"""
        body = ProductIn(**product_data())
        result = await product_usecase.create(body=body)

        assert isinstance(result, ProductOut)
        assert result.name == body.name
        assert result.price == body.price
        assert result.quantity == body.quantity
        assert result.status == body.status
        assert result.id is not None

    @pytest.mark.asyncio
    async def test_create_product_iphone_14_pro_max_success(self):
        """Test: Criar iPhone 14 Pro Max deve retornar sucesso"""
        iphone_data = {
            "name": "Iphone 14 pro Max",
            "price": 8500.00,
            "quantity": 10,
            "status": True,
        }
        body = ProductIn(**iphone_data)
        result = await product_usecase.create(body=body)

        assert isinstance(result, ProductOut)
        assert result.name == "Iphone 14 pro Max"
        assert result.price == 8500.00
        assert result.quantity == 10
        assert result.status is True
        assert result.id is not None

    @pytest.mark.asyncio
    async def test_get_product_should_return_success(self):
        """Test: Buscar produto deve retornar sucesso"""
        # Primeiro criar um produto
        body = ProductIn(**product_data())
        created_product = await product_usecase.create(body=body)

        # Depois buscar o produto
        result = await product_usecase.get(id=created_product.id)

        assert isinstance(result, ProductOut)
        assert result.id == created_product.id
        assert result.name == body.name

    @pytest.mark.asyncio
    async def test_get_product_should_return_not_found(self):
        """Test: Buscar produto inexistente deve retornar erro"""
        with pytest.raises(Exception) as exc_info:
            await product_usecase.get(
                id="507f1f77bcf86cd799439011"
            )  # ObjectId válido mas inexistente

        assert str(exc_info.value) == "Product not found"

    @pytest.mark.asyncio
    async def test_query_products_should_return_list(self):
        """Test: Listar produtos deve retornar lista"""
        result = await product_usecase.query()

        assert isinstance(result, list)

    @pytest.mark.asyncio
    async def test_update_product_should_return_success(self):
        """Test: Atualizar produto deve retornar sucesso"""
        # Primeiro criar um produto
        body = ProductIn(**product_data())
        created_product = await product_usecase.create(body=body)

        # Depois atualizar o produto
        update_data = ProductUpdate(name="Produto Atualizado", price=999.99)
        result = await product_usecase.update(id=created_product.id, body=update_data)

        assert isinstance(result, ProductOut)
        assert result.id == created_product.id
        assert result.name == "Produto Atualizado"
        assert result.price == 999.99

    @pytest.mark.asyncio
    async def test_update_iphone_14_pro_max_price(self):
        """Test: Atualizar preço do iPhone 14 Pro Max"""
        # Criar iPhone 14 Pro Max
        iphone_data = {
            "name": "Iphone 14 pro Max",
            "price": 8500.00,
            "quantity": 10,
            "status": True,
        }
        body = ProductIn(**iphone_data)
        created_product = await product_usecase.create(body=body)

        # Atualizar preço
        update_data = ProductUpdate(price=7999.99)
        result = await product_usecase.update(id=created_product.id, body=update_data)

        assert result.price == 7999.99
        assert result.name == "Iphone 14 pro Max"  # Nome não mudou

    @pytest.mark.asyncio
    async def test_delete_product_should_return_success(self):
        """Test: Deletar produto deve retornar sucesso"""
        # Primeiro criar um produto
        body = ProductIn(**product_data())
        created_product = await product_usecase.create(body=body)

        # Depois deletar o produto
        result = await product_usecase.delete(id=created_product.id)

        assert result is True

    @pytest.mark.asyncio
    async def test_delete_product_should_return_false_when_not_found(self):
        """Test: Deletar produto inexistente deve retornar False"""
        result = await product_usecase.delete(
            id="507f1f77bcf86cd799439011"
        )  # ObjectId válido mas inexistente

        assert result is False
