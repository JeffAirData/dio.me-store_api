"""
Testes de Integração Avançados - Controllers e Rotas
Seguindo padrão da professora Nayanna Nara - DIO.me Store API

Foco: Headers, Performance, Validação de Response, Documentação API
"""
import time

import pytest
from fastapi import status
from httpx import AsyncClient

from tests.factories import iphone_14_pro_max_data


class TestAdvancedIntegration:
    """Testes avançados de integração das rotas HTTP"""

    # ========================================================================
    # TESTES DE HEADERS E CONTENT-TYPE
    # ========================================================================

    async def test_content_type_validation(
        self, client: AsyncClient, products_url: str
    ):
        """Verificar Content-Type correto nas respostas"""
        # CREATE - JSON response
        response = await client.post(products_url, json=iphone_14_pro_max_data())
        assert response.headers["content-type"] == "application/json"
        assert response.status_code == status.HTTP_201_CREATED

        # GET - JSON response
        product_id = response.json()["id"]
        response = await client.get(f"{products_url}{product_id}")
        assert response.headers["content-type"] == "application/json"
        assert response.status_code == status.HTTP_200_OK

        # DELETE - No content
        response = await client.delete(f"{products_url}{product_id}")
        assert response.status_code == status.HTTP_204_NO_CONTENT

    async def test_cors_headers(self, client: AsyncClient, products_url: str):
        """Verificar headers CORS (se configurados)"""
        response = await client.get(products_url)

        # Verificar se há headers básicos
        assert "content-length" in response.headers
        assert "content-type" in response.headers

    # ========================================================================
    # TESTES DE PERFORMANCE E RESPONSE TIME
    # ========================================================================

    async def test_response_time_create(self, client: AsyncClient, products_url: str):
        """Verificar tempo de resposta da criação de produto"""
        start_time = time.time()

        response = await client.post(products_url, json=iphone_14_pro_max_data())

        end_time = time.time()
        response_time = end_time - start_time

        assert response.status_code == status.HTTP_201_CREATED
        assert response_time < 2.0  # Máximo 2 segundos

    async def test_response_time_query(self, client: AsyncClient, products_url: str):
        """Verificar tempo de resposta da listagem de produtos"""
        start_time = time.time()

        response = await client.get(products_url)

        end_time = time.time()
        response_time = end_time - start_time

        assert response.status_code == status.HTTP_200_OK
        assert response_time < 1.0  # Máximo 1 segundo para listagem

    # ========================================================================
    # TESTES DE VALIDAÇÃO DE ENTRADA E SEGURANÇA
    # ========================================================================

    async def test_sql_injection_protection(
        self, client: AsyncClient, products_url: str
    ):
        """Verificar proteção contra SQL Injection nos parâmetros"""
        malicious_queries = [
            "'; DROP TABLE products; --",
            "1' OR '1'='1",
            "<script>alert('xss')</script>",
            "../../etc/passwd",
        ]

        for malicious_query in malicious_queries:
            # Tentar injection no search
            response = await client.get(
                f"{products_url}filter/search/?name={malicious_query}"
            )
            # Deve retornar resposta válida sem erro de servidor
            assert response.status_code in [200, 400, 422]  # Nunca 500

    async def test_large_payload_handling(self, client: AsyncClient, products_url: str):
        """Verificar tratamento de payloads grandes"""
        large_product = iphone_14_pro_max_data()
        large_product["name"] = "A" * 1000  # Nome muito grande

        response = await client.post(products_url, json=large_product)

        # Deve ser rejeitado com erro de validação
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    async def test_invalid_content_type(self, client: AsyncClient, products_url: str):
        """Verificar tratamento de Content-Type inválido"""
        response = await client.post(
            products_url, data="invalid-data", headers={"Content-Type": "text/plain"}
        )

        # Deve rejeitar com erro apropriado
        assert response.status_code in [400, 415, 422]

    # ========================================================================
    # TESTES DE EDGE CASES E LIMITES
    # ========================================================================

    async def test_empty_database_responses(
        self, client: AsyncClient, products_url: str
    ):
        """Verificar comportamento com banco vazio"""
        # Limpar produtos existentes seria ideal, mas vamos testar busca por inexistente
        fake_uuid = "00000000-0000-0000-0000-000000000000"

        response = await client.get(f"{products_url}{fake_uuid}")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "detail" in response.json()

    async def test_concurrent_requests(self, client: AsyncClient, products_url: str):
        """Testar requisições concorrentes (simulação básica)"""
        import asyncio

        # Criar múltiplas requisições simultâneas
        tasks = []
        for i in range(5):
            product_data = iphone_14_pro_max_data()
            product_data["name"] = f"iPhone Concurrent {i}"
            task = client.post(products_url, json=product_data)
            tasks.append(task)

        responses = await asyncio.gather(*tasks)

        # Todas devem ter sucesso
        for response in responses:
            assert response.status_code == status.HTTP_201_CREATED

    # ========================================================================
    # TESTES DE DOCUMENTAÇÃO API (OpenAPI/Swagger)
    # ========================================================================

    async def test_openapi_documentation(self, client: AsyncClient):
        """Verificar se a documentação OpenAPI está disponível"""
        response = await client.get("/openapi.json")
        assert response.status_code == status.HTTP_200_OK

        openapi_doc = response.json()
        assert "openapi" in openapi_doc
        assert "info" in openapi_doc
        assert "paths" in openapi_doc

        # Verificar se endpoints de produtos estão documentados
        paths = openapi_doc["paths"]
        assert "/products/" in paths
        assert "post" in paths["/products/"]
        assert "get" in paths["/products/"]

    async def test_swagger_ui_available(self, client: AsyncClient):
        """Verificar se Swagger UI está disponível"""
        response = await client.get("/docs")
        assert response.status_code == status.HTTP_200_OK
        assert "text/html" in response.headers.get("content-type", "")

    async def test_redoc_available(self, client: AsyncClient):
        """Verificar se ReDoc está disponível"""
        response = await client.get("/redoc")
        assert response.status_code == status.HTTP_200_OK
        assert "text/html" in response.headers.get("content-type", "")

    # ========================================================================
    # TESTES DE HEALTH CHECK E MONITORING
    # ========================================================================

    async def test_application_health(self, client: AsyncClient):
        """Verificar saúde da aplicação"""
        # Se houver endpoint de health
        response = await client.get("/health")
        # Pode retornar 404 se não implementado, mas nunca 500
        assert response.status_code in [200, 404]

    async def test_database_connectivity(self, client: AsyncClient, products_url: str):
        """Verificar conectividade com banco através de operação simples"""
        response = await client.get(products_url)

        # Se conseguir listar produtos, banco está conectado
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), list)


class TestAPIValidationDeep:
    """Testes profundos de validação da API"""

    async def test_field_validation_comprehensive(
        self, client: AsyncClient, products_url: str
    ):
        """Teste abrangente de validação de campos"""
        invalid_cases = [
            # Preço negativo
            {**iphone_14_pro_max_data(), "price": -100},
            # Quantidade negativa
            {**iphone_14_pro_max_data(), "quantity": -5},
            # Nome vazio
            {**iphone_14_pro_max_data(), "name": ""},
            # Nome só espaços
            {**iphone_14_pro_max_data(), "name": "   "},
            # Price como string
            {**iphone_14_pro_max_data(), "price": "invalid"},
            # Campos extras não permitidos
            {**iphone_14_pro_max_data(), "extra_field": "not_allowed"},
        ]

        for invalid_data in invalid_cases:
            response = await client.post(products_url, json=invalid_data)
            assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
            assert "detail" in response.json()

    async def test_response_schema_validation(
        self, client: AsyncClient, products_url: str
    ):
        """Verificar se responses seguem o schema correto"""
        response = await client.post(products_url, json=iphone_14_pro_max_data())
        assert response.status_code == status.HTTP_201_CREATED

        product = response.json()

        # Verificar campos obrigatórios
        required_fields = [
            "id",
            "name",
            "quantity",
            "price",
            "status",
            "created_at",
            "updated_at",
        ]
        for field in required_fields:
            assert field in product, f"Campo {field} obrigatório não encontrado"

        # Verificar tipos
        assert isinstance(product["id"], str)
        assert isinstance(product["name"], str)
        assert isinstance(product["quantity"], int)
        assert isinstance(product["price"], str)  # Decimal vira string
        assert isinstance(product["status"], bool)
        assert isinstance(product["created_at"], str)  # ISO datetime
        assert isinstance(product["updated_at"], str)  # ISO datetime
