"""
Testes de Stress e Load Testing
Seguindo padrão da professora Nayanna Nara - DIO.me Store API

Foco: Performance sob carga, limites do sistema, resiliência
"""
import asyncio
import time
from typing import List

import pytest
from fastapi import status
from httpx import AsyncClient

from tests.factories import iphone_14_pro_max_data


class TestLoadAndStress:
    """Testes de carga e stress da API"""

    # ========================================================================
    # TESTES DE LOAD (Carga Normal)
    # ========================================================================

    async def test_load_create_products(self, client: AsyncClient, products_url: str):
        """Teste de carga - criar múltiplos produtos"""
        num_products = 10
        start_time = time.time()

        tasks = []
        for i in range(num_products):
            product_data = iphone_14_pro_max_data()
            product_data["name"] = f"Load Test Product {i}"
            task = client.post(products_url, json=product_data)
            tasks.append(task)

        responses = await asyncio.gather(*tasks, return_exceptions=True)
        end_time = time.time()
        total_time = end_time - start_time

        # Verificar que não houve exceptions
        exceptions = [r for r in responses if isinstance(r, Exception)]
        assert (
            len(exceptions) == 0
        ), f"Houve {len(exceptions)} exceptions durante o teste de carga"

        # Verificar que todas as respostas foram bem-sucedidas
        successful_responses = [
            r for r in responses if hasattr(r, "status_code") and r.status_code == 201
        ]
        assert len(successful_responses) == num_products

        # Verificar performance (tempo médio por requisição)
        avg_time_per_request = total_time / num_products
        assert (
            avg_time_per_request < 1.0
        ), f"Tempo médio por requisição muito alto: {avg_time_per_request:.2f}s"

    async def test_load_concurrent_read_operations(
        self, client: AsyncClient, products_url: str
    ):
        """Teste de carga - operações de leitura concorrentes"""
        num_concurrent_reads = 20

        start_time = time.time()

        # Executar múltiplas leituras simultaneamente
        tasks = [client.get(products_url) for _ in range(num_concurrent_reads)]
        responses = await asyncio.gather(*tasks, return_exceptions=True)

        end_time = time.time()
        total_time = end_time - start_time

        # Verificar que não houve exceptions
        exceptions = [r for r in responses if isinstance(r, Exception)]
        assert len(exceptions) == 0

        # Verificar que todas as respostas foram bem-sucedidas
        successful_responses = [
            r for r in responses if hasattr(r, "status_code") and r.status_code == 200
        ]
        assert len(successful_responses) == num_concurrent_reads

        # Performance deve ser boa para leituras
        assert (
            total_time < 5.0
        ), f"Tempo total para {num_concurrent_reads} leituras muito alto: {total_time:.2f}s"

    # ========================================================================
    # TESTES DE STRESS (Limites do Sistema)
    # ========================================================================

    @pytest.mark.slow
    async def test_stress_rapid_fire_requests(
        self, client: AsyncClient, products_url: str
    ):
        """Teste de stress - rajadas rápidas de requisições"""
        num_requests = 50
        batch_size = 10

        all_responses = []

        # Enviar requisições em batches
        for batch in range(0, num_requests, batch_size):
            batch_tasks = []
            for i in range(batch, min(batch + batch_size, num_requests)):
                product_data = iphone_14_pro_max_data()
                product_data["name"] = f"Stress Test Product {i}"
                task = client.post(products_url, json=product_data)
                batch_tasks.append(task)

            batch_responses = await asyncio.gather(*batch_tasks, return_exceptions=True)
            all_responses.extend(batch_responses)

            # Pequena pausa entre batches para não sobrecarregar
            await asyncio.sleep(0.1)

        # Analisar resultados
        exceptions = [r for r in all_responses if isinstance(r, Exception)]
        successful = [
            r
            for r in all_responses
            if hasattr(r, "status_code") and r.status_code == 201
        ]
        server_errors = [
            r
            for r in all_responses
            if hasattr(r, "status_code") and r.status_code >= 500
        ]

        # O sistema deve lidar graciosamente com a carga
        assert (
            len(exceptions) < num_requests * 0.1
        ), f"Muitas exceptions: {len(exceptions)}"
        assert (
            len(server_errors) == 0
        ), f"Não deve haver erros 5xx: {len(server_errors)}"
        assert (
            len(successful) >= num_requests * 0.8
        ), f"Taxa de sucesso muito baixa: {len(successful)}/{num_requests}"

    # ========================================================================
    # TESTES DE RESILIÊNCIA
    # ========================================================================

    async def test_mixed_operation_stress(self, client: AsyncClient, products_url: str):
        """Teste de stress com operações mistas (CRUD)"""
        # Primeiro criar alguns produtos
        created_products = []
        for i in range(5):
            product_data = iphone_14_pro_max_data()
            product_data["name"] = f"Mixed Test Product {i}"
            response = await client.post(products_url, json=product_data)
            if response.status_code == 201:
                created_products.append(response.json()["id"])

        # Operações mistas simultâneas
        mixed_tasks = []

        # Adicionar tarefas de criação
        for i in range(10):
            product_data = iphone_14_pro_max_data()
            product_data["name"] = f"Mixed Create {i}"
            mixed_tasks.append(client.post(products_url, json=product_data))

        # Adicionar tarefas de leitura
        for _ in range(15):
            mixed_tasks.append(client.get(products_url))

        # Adicionar tarefas de busca por ID (se temos produtos criados)
        for product_id in created_products[:3]:
            mixed_tasks.append(client.get(f"{products_url}{product_id}"))

        # Adicionar tarefas de update
        for product_id in created_products[:2]:
            mixed_tasks.append(
                client.patch(f"{products_url}{product_id}", json={"price": 9999.99})
            )

        # Executar todas as tarefas
        start_time = time.time()
        responses = await asyncio.gather(*mixed_tasks, return_exceptions=True)
        end_time = time.time()

        # Analisar resultados
        exceptions = [r for r in responses if isinstance(r, Exception)]
        server_errors = [
            r for r in responses if hasattr(r, "status_code") and r.status_code >= 500
        ]

        assert (
            len(exceptions) == 0
        ), f"Houve {len(exceptions)} exceptions em operações mistas"
        assert len(server_errors) == 0, f"Houve {len(server_errors)} erros de servidor"

        total_time = end_time - start_time
        assert total_time < 10.0, f"Operações mistas demoraram muito: {total_time:.2f}s"

    # ========================================================================
    # TESTES DE MEMORY E RESOURCE LEAK
    # ========================================================================

    async def test_memory_leak_detection(self, client: AsyncClient, products_url: str):
        """Teste básico para detectar vazamentos de memória"""
        # Executar muitas operações e verificar se o sistema continua responsivo
        num_iterations = 100

        for i in range(num_iterations):
            # Criar produto
            product_data = iphone_14_pro_max_data()
            product_data["name"] = f"Memory Test {i}"
            create_response = await client.post(products_url, json=product_data)

            if create_response.status_code == 201:
                product_id = create_response.json()["id"]

                # Ler produto
                await client.get(f"{products_url}{product_id}")

                # Atualizar produto
                await client.patch(
                    f"{products_url}{product_id}", json={"price": 1000 + i}
                )

                # Deletar produto (para não acumular no banco)
                await client.delete(f"{products_url}{product_id}")

            # A cada 20 iterações, verificar que a API ainda responde
            if i % 20 == 0:
                health_response = await client.get(products_url)
                assert (
                    health_response.status_code == 200
                ), f"API não responsiva na iteração {i}"

    # ========================================================================
    # MÉTRICAS E BENCHMARKS
    # ========================================================================

    async def test_response_time_consistency(
        self, client: AsyncClient, products_url: str
    ):
        """Verificar consistência dos tempos de resposta"""
        num_tests = 20
        response_times = []

        for _ in range(num_tests):
            start_time = time.time()
            response = await client.get(products_url)
            end_time = time.time()

            assert response.status_code == 200
            response_times.append(end_time - start_time)

        # Calcular estatísticas
        avg_time = sum(response_times) / len(response_times)
        max_time = max(response_times)
        min_time = min(response_times)

        # Verificar que os tempos são consistentes
        assert avg_time < 1.0, f"Tempo médio muito alto: {avg_time:.3f}s"
        assert max_time < 2.0, f"Tempo máximo muito alto: {max_time:.3f}s"

        # Variação não deve ser muito grande (max não deve ser mais que 5x o min)
        assert (
            max_time / min_time < 5
        ), f"Muita variação nos tempos: min={min_time:.3f}s, max={max_time:.3f}s"

    async def test_throughput_measurement(self, client: AsyncClient, products_url: str):
        """Medir throughput (requisições por segundo)"""
        duration_seconds = 5
        start_time = time.time()
        request_count = 0

        # Enviar requisições por um período determinado
        while time.time() - start_time < duration_seconds:
            response = await client.get(products_url)
            assert response.status_code == 200
            request_count += 1

        actual_duration = time.time() - start_time
        throughput = request_count / actual_duration

        # Verificar throughput mínimo (ajustar conforme necessário)
        min_throughput = 10  # 10 req/seg mínimo
        assert (
            throughput >= min_throughput
        ), f"Throughput muito baixo: {throughput:.2f} req/s (mínimo: {min_throughput})"

        print(f"Throughput medido: {throughput:.2f} requisições por segundo")
