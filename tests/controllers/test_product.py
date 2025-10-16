"""
Testes de Integração HTTP - Controllers FastAPI
Seguindo padrão da professora Nayanna Nara - DIO.me Store API

Testando TODOS os desafios:
1. Create - Exceções capturadas na controller
2. Update - Not Found na controller com mensagem amigável
3. Filtros - Preço (5000 < price < 8000)
"""
from typing import List

import pytest
from fastapi import status

from tests.factories import iphone_14_pro_max_data


class TestProductController:
    """Testes de integração dos controllers de produto"""

    # ========================================================================
    # DESAFIO 1: CREATE - Exceções capturadas na controller
    # ========================================================================

    async def test_controller_create_should_return_success(
        self, client, products_url, setup_database
    ):
        """Teste CREATE - Sucesso"""
        response = await client.post(products_url, json=iphone_14_pro_max_data())

        content = response.json()

        # Remover campos dinâmicos para comparação
        del content["created_at"]
        del content["updated_at"]
        del content["id"]  # ProductModel retorna id como UUID

        assert response.status_code == status.HTTP_201_CREATED
        assert content == {
            "name": "iPhone 14 Pro Max",
            "quantity": 10,
            "price": "8500.0",  # Decimal é serializado como string
            "status": True,
        }

    async def test_controller_create_should_return_validation_error(
        self, client, products_url
    ):
        """Teste CREATE - Erro de validação capturado na controller"""
        invalid_product = {
            "name": "",  # Nome vazio (inválido)
            "quantity": -5,  # Quantidade negativa (inválida)
            "price": -100.0,  # Preço negativo (inválido)
        }

        response = await client.post(products_url, json=invalid_product)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert "detail" in response.json()

    # ========================================================================
    # GET - Testes de busca
    # ========================================================================

    async def test_controller_get_should_return_success(
        self, client, products_url, product_inserted
    ):
        """Teste GET - Sucesso"""
        response = await client.get(f"{products_url}{product_inserted.id}")

        content = response.json()

        # Remover campos dinâmicos
        del content["created_at"]
        del content["updated_at"]

        assert response.status_code == status.HTTP_200_OK
        assert content == {
            "id": str(product_inserted.id),
            "name": "iPhone 14 Pro Max",
            "quantity": 10,
            "price": "8500.0",  # Decimal é serializado como string
            "status": True,
        }

    async def test_controller_get_should_return_not_found(self, client, products_url):
        """Teste GET - Not Found"""
        fake_id = "4fd7cd35-a3a0-4c1f-a78d-d24aa81e7dca"
        response = await client.get(f"{products_url}{fake_id}")

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Product with ID" in response.json()["detail"]

    # ========================================================================
    # QUERY - Listar produtos
    # ========================================================================

    @pytest.mark.usefixtures("products_inserted")
    async def test_controller_query_should_return_success(self, client, products_url):
        """Teste QUERY - Listar todos os produtos"""
        response = await client.get(products_url)

        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), List)
        assert len(response.json()) > 1

    # ========================================================================
    # DESAFIO 2: UPDATE - Not Found tratado na controller
    # ========================================================================

    async def test_controller_patch_should_return_success(
        self, client, products_url, product_inserted
    ):
        """Teste UPDATE - Sucesso com updated_at atualizado"""
        response = await client.patch(
            f"{products_url}{product_inserted.id}", json={"price": 7500.0}
        )

        content = response.json()

        # Verificar se updated_at foi atualizado
        assert "updated_at" in content

        # Remover campos dinâmicos para comparação
        del content["created_at"]
        del content["updated_at"]

        assert response.status_code == status.HTTP_200_OK
        assert content == {
            "id": str(product_inserted.id),
            "name": "iPhone 14 Pro Max",
            "quantity": 10,
            "price": "7500.0",  # Decimal é serializado como string
            "status": True,
        }

    async def test_controller_patch_should_return_not_found_friendly_message(
        self, client, products_url
    ):
        """
        **DESAFIO 2**: UPDATE - Not Found com mensagem amigável na controller
        """
        # Usar um UUID válido mas inexistente
        fake_uuid = "507f1f77-bcf8-6cd7-9943-9011abcdef01"
        response = await client.patch(
            f"{products_url}{fake_uuid}", json={"price": 7500.0}
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        detail = response.json()["detail"]

        # Verificar se a mensagem é amigável
        assert "Produto não encontrado para atualização" in detail

    # ========================================================================
    # DELETE - Remoção de produtos
    # ========================================================================

    async def test_controller_delete_should_return_no_content(
        self, client, products_url, product_inserted
    ):
        """Teste DELETE - Sucesso"""
        response = await client.delete(f"{products_url}{product_inserted.id}")

        assert response.status_code == status.HTTP_204_NO_CONTENT

    async def test_controller_delete_should_return_not_found(
        self, client, products_url
    ):
        """Teste DELETE - Not Found"""
        fake_id = "4fd7cd35-a3a0-4c1f-a78d-d24aa81e7dca"
        response = await client.delete(f"{products_url}{fake_id}")

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Product with ID" in response.json()["detail"]


class TestProductFiltersController:
    """
    DESAFIO 3: Testes dos filtros de produtos
    """

    @pytest.mark.usefixtures("products_inserted")
    async def test_controller_price_filter_range_5000_to_8000(
        self, client, products_url
    ):
        """
        **DESAFIO 3**: Filtro de preço (price > 5000 and price < 8000)
        """
        response = await client.get(
            f"{products_url}filter/price-range/?min_price=5000&max_price=8000"
        )

        assert response.status_code == status.HTTP_200_OK

        products = response.json()
        assert isinstance(products, List)

        # Verificar se todos os produtos estão na faixa de preço
        for product in products:
            price = float(product["price"])
            assert (
                5000 < price < 8000
            ), f"Produto {product['name']} com preço R$ {price} fora da faixa!"

    @pytest.mark.usefixtures("products_inserted")
    async def test_controller_luxury_products_filter(self, client, products_url):
        """Teste filtro de produtos de luxo (> R$ 5.000)"""
        response = await client.get(f"{products_url}filter/luxury/")

        assert response.status_code == status.HTTP_200_OK

        products = response.json()
        assert isinstance(products, List)

        # Verificar se todos são produtos de luxo
        for product in products:
            price = float(product["price"])
            assert price > 5000, f"Produto {product['name']} não é de luxo: R$ {price}"

    @pytest.mark.usefixtures("products_inserted")
    async def test_controller_affordable_products_filter(self, client, products_url):
        """Teste filtro de produtos acessíveis (< R$ 500)"""
        response = await client.get(f"{products_url}filter/affordable/")

        assert response.status_code == status.HTTP_200_OK

        products = response.json()
        assert isinstance(products, List)

        # Verificar se todos são produtos acessíveis
        for product in products:
            price = float(product["price"])
            assert price < 500, f"Produto {product['name']} não é acessível: R$ {price}"

    @pytest.mark.usefixtures("products_inserted")
    async def test_controller_search_products_by_name(self, client, products_url):
        """Teste busca de produtos por nome"""
        response = await client.get(f"{products_url}search/?q=iPhone")

        assert response.status_code == status.HTTP_200_OK

        products = response.json()
        assert isinstance(products, List)

        # Verificar se todos contêm "iPhone" no nome
        for product in products:
            assert (
                "iPhone" in product["name"]
            ), f"Produto {product['name']} não contém 'iPhone'"
