import pytest

from store.exceptions.base import (InvalidProductId, ProductNotFound,
                                   ProductUpdateError)
from store.schemas.product import ProductIn, ProductUpdate
from store.usecases.product import product_usecase
from tests.factories import product_data


class TestStoreExceptions:
    """Testes para exceções customizadas da loja"""

    @pytest.mark.asyncio
    async def test_get_product_not_found_exception(self):
        """Test: Exceção ProductNotFound ao buscar produto inexistente"""
        invalid_id = "507f1f77bcf86cd799439011"

        with pytest.raises(ProductNotFound) as exc_info:
            await product_usecase.get(id=invalid_id)

        assert f"Product with ID '{invalid_id}' not found" in str(exc_info.value)
        assert exc_info.value.status_code == 404

    @pytest.mark.asyncio
    async def test_invalid_product_id_exception(self):
        """Test: Exceção InvalidProductId para ID inválido"""
        invalid_id = "invalid-id-format"

        with pytest.raises(InvalidProductId) as exc_info:
            await product_usecase.get(id=invalid_id)

        assert f"Invalid product ID format: '{invalid_id}'" in str(exc_info.value)
        assert exc_info.value.status_code == 400

    @pytest.mark.asyncio
    async def test_update_product_not_found_exception(self):
        """Test: Exceção ProductNotFound ao atualizar produto inexistente"""
        invalid_id = "507f1f77bcf86cd799439011"
        update_data = ProductUpdate(name="Produto Atualizado")

        with pytest.raises(ProductNotFound) as exc_info:
            await product_usecase.update(id=invalid_id, body=update_data)

        assert f"Product with ID '{invalid_id}' not found" in str(exc_info.value)
        assert exc_info.value.status_code == 404

    @pytest.mark.asyncio
    async def test_update_no_fields_exception(self):
        """Test: Exceção ProductUpdateError quando não há campos para atualizar"""
        # Criar um produto primeiro
        body = ProductIn(**product_data())
        created_product = await product_usecase.create(body=body)

        # Tentar atualizar sem dados
        empty_update = ProductUpdate()

        with pytest.raises(ProductUpdateError) as exc_info:
            await product_usecase.update(id=created_product.id, body=empty_update)

        assert "No fields to update" in str(exc_info.value)
        assert exc_info.value.status_code == 422

    @pytest.mark.asyncio
    async def test_delete_product_not_found_exception(self):
        """Test: Exceção ProductNotFound ao deletar produto inexistente"""
        invalid_id = "507f1f77bcf86cd799439011"

        with pytest.raises(ProductNotFound) as exc_info:
            await product_usecase.delete(id=invalid_id)

        assert f"Product with ID '{invalid_id}' not found" in str(exc_info.value)
        assert exc_info.value.status_code == 404

    @pytest.mark.asyncio
    async def test_update_with_custom_updated_at(self):
        """Test: Atualizar produto permitindo modificar updated_at manualmente"""
        from datetime import datetime, timedelta

        # Criar produto
        body = ProductIn(**product_data())
        created_product = await product_usecase.create(body=body)

        # Atualizar com data customizada
        custom_date = datetime.now() - timedelta(days=1)
        update_data = ProductUpdate(name="Produto Atualizado", updated_at=custom_date)

        updated_product = await product_usecase.update(
            id=created_product.id, body=update_data
        )

        assert updated_product.name == "Produto Atualizado"
        # Verificar se a data customizada foi aplicada (aproximadamente)
        time_diff = abs((updated_product.updated_at - custom_date).total_seconds())
        assert time_diff < 1  # Diferença menor que 1 segundo
