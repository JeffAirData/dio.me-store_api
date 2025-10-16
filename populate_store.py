#!/usr/bin/env python3
"""
Script para popular o banco de dados com produtos variados da loja
"""
import asyncio

from store.db.mongo import connect_to_mongo, get_collection
from store.schemas.product import ProductIn
from store.usecases.product import product_usecase
from tests.factories import all_products_data


async def populate_store():
    """Popular loja com produtos variados"""
    print("🏪 Populando Store API com produtos variados...\n")

    # Conectar ao MongoDB
    await connect_to_mongo()

    # Limpar produtos existentes
    products_collection = get_collection("products")
    await products_collection.delete_many({})
    print("🧹 Banco limpo!")

    # Obter todos os produtos das factories
    all_products = all_products_data()

    print(f"📦 Criando {len(all_products)} produtos...")

    # Categorias para organizar
    categories = {
        "📱 ELETRÔNICOS": [
            "iPhone",
            "Samsung",
            "MacBook",
            "Dell",
            "Lenovo",
            "AirPods",
            "Apple Watch",
        ],
        "⚽ ESPORTIVOS": [
            "Nike",
            "Adidas",
            "New Balance",
            "Bola",
            "Raquete",
            "Bicicleta",
        ],
        "🏠 CONSUMO": [
            "Cafeteira",
            "Fritadeira",
            "Aspirador",
            "Perfume",
            "Secador",
            "Livro",
            "Curso",
            "Mochila",
            "Garrafa",
        ],
    }

    created_by_category = {cat: [] for cat in categories}

    # Criar produtos
    for product_data in all_products:
        try:
            body = ProductIn(**product_data)
            created_product = await product_usecase.create(body=body)

            # Categorizar produto
            for category, keywords in categories.items():
                if any(
                    keyword.lower() in product_data["name"].lower()
                    for keyword in keywords
                ):
                    created_by_category[category].append(created_product)
                    break

        except Exception as e:
            print(f"❌ Erro ao criar produto {product_data['name']}: {e}")

    # Relatório por categoria
    print("\n" + "=" * 60)
    print("📊 RELATÓRIO DE PRODUTOS CRIADOS")
    print("=" * 60)

    total_created = 0
    for category, products in created_by_category.items():
        if products:
            print(f"\n{category} ({len(products)} produtos):")
            for product in products[:3]:  # Mostrar apenas 3 primeiros
                print(f"  • {product.name} - R$ {product.price:.2f}")
            if len(products) > 3:
                print(f"  ... e mais {len(products) - 3} produtos")
        total_created += len(products)

    print(f"\n🎉 TOTAL: {total_created} produtos criados com sucesso!")

    # Demonstrar filtros
    print("\n" + "=" * 60)
    print("🔍 DEMONSTRAÇÃO DE FILTROS")
    print("=" * 60)

    # Filtro de preço: R$ 5000 - R$ 8000
    price_filtered = await product_usecase.query_by_price_range(5000, 8000)
    print(
        f"\n💰 Produtos entre R$ 5.000 e R$ 8.000 ({len(price_filtered)} encontrados):"
    )
    for product in price_filtered[:5]:
        print(f"  • {product.name} - R$ {product.price:.2f}")

    # Produtos de luxo
    luxury_products = await product_usecase.get_luxury_products()
    print(f"\n💎 Produtos de Luxo (> R$ 5.000) ({len(luxury_products)} encontrados):")
    for product in luxury_products[:5]:
        print(f"  • {product.name} - R$ {product.price:.2f}")

    # Produtos acessíveis
    affordable_products = await product_usecase.get_affordable_products()
    print(
        f"\n🎯 Produtos Acessíveis (< R$ 500) ({len(affordable_products)} encontrados):"
    )
    for product in affordable_products[:5]:
        print(f"  • {product.name} - R$ {product.price:.2f}")

    # Busca por categoria
    iphone_products = await product_usecase.search_products("iPhone")
    print(f"\n📱 Busca por 'iPhone' ({len(iphone_products)} encontrados):")
    for product in iphone_products:
        print(f"  • {product.name} - R$ {product.price:.2f}")

    print("\n" + "=" * 60)
    print("✅ Store API populada com sucesso!")
    print("🚀 Pronto para os testes dos desafios!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(populate_store())
