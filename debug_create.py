"""
Debug test para ver o que está sendo retornado
"""
import asyncio

from httpx import ASGITransport, AsyncClient

from store.db.mongo import connect_to_mongo
from store.main import app
from tests.factories import iphone_14_pro_max_data


async def debug_create_product():
    # Forçar conexão MongoDB antes do teste
    await connect_to_mongo()
    print("🔗 MongoDB conectado manualmente")

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        data = iphone_14_pro_max_data()
        print("📤 Dados enviados:", data)

        response = await client.post("/products/", json=data)
        print("📊 Status Code:", response.status_code)

        try:
            content = response.json()
            print("📋 Resposta completa:", content)
        except Exception as e:
            print("❌ Erro ao parsear JSON:", e)
            print("📄 Conteúdo raw:", response.text)


if __name__ == "__main__":
    asyncio.run(debug_create_product())
