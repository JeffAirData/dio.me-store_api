"""Factory functions para gerar dados de teste"""


def product_data():
    """Dados genéricos de produto para testes"""
    return {
        "name": "Produto Teste",
        "price": 99.99,
        "quantity": 5,
        "status": True,
    }


# ========== ELETRÔNICOS ==========


def iphone_14_pro_max_data():
    """Dados do iPhone 14 Pro Max para testes"""
    return {
        "name": "iPhone 14 Pro Max",
        "price": 8500.00,
        "quantity": 10,
        "status": True,
    }


def electronics_products_data():
    """Produtos eletrônicos variados"""
    return [
        # Smartphones
        {"name": "iPhone 15 Pro Max", "price": 10500.00, "quantity": 5, "status": True},
        {"name": "iPhone 14 Pro", "price": 7500.00, "quantity": 8, "status": True},
        {
            "name": "Samsung Galaxy S24 Ultra",
            "price": 9200.00,
            "quantity": 12,
            "status": True,
        },
        {"name": "iPhone 13", "price": 5500.00, "quantity": 15, "status": True},
        # Laptops
        {"name": "MacBook Pro M3 16", "price": 15000.00, "quantity": 3, "status": True},
        {"name": "Dell XPS 13", "price": 6800.00, "quantity": 7, "status": True},
        {"name": "Lenovo ThinkPad X1", "price": 8900.00, "quantity": 4, "status": True},
        # Acessórios
        {"name": "AirPods Pro 2", "price": 1200.00, "quantity": 25, "status": True},
        {
            "name": "Apple Watch Series 9",
            "price": 3500.00,
            "quantity": 8,
            "status": True,
        },
    ]


# ========== ESPORTIVOS ==========


def sports_products_data():
    """Produtos esportivos variados"""
    return [
        # Calçados
        {"name": "Nike Air Jordan 1", "price": 899.90, "quantity": 20, "status": True},
        {
            "name": "Adidas Ultraboost 23",
            "price": 749.90,
            "quantity": 15,
            "status": True,
        },
        {"name": "New Balance 574", "price": 450.00, "quantity": 30, "status": True},
        # Roupas
        {
            "name": "Camisa Nike Dri-FIT",
            "price": 149.90,
            "quantity": 50,
            "status": True,
        },
        {
            "name": "Shorts Adidas Running",
            "price": 89.90,
            "quantity": 40,
            "status": True,
        },
        # Equipamentos
        {"name": "Bola Nike Futebol", "price": 120.00, "quantity": 25, "status": True},
        {
            "name": "Raquete Wilson Tennis",
            "price": 580.00,
            "quantity": 8,
            "status": True,
        },
        {
            "name": "Bicicleta Caloi Elite",
            "price": 2400.00,
            "quantity": 5,
            "status": True,
        },
    ]


# ========== CONSUMO GERAL ==========


def consumer_products_data():
    """Produtos de consumo geral"""
    return [
        # Casa e Cozinha
        {
            "name": "Cafeteira Nespresso",
            "price": 450.00,
            "quantity": 12,
            "status": True,
        },
        {
            "name": "Fritadeira Airfryer Philips",
            "price": 680.00,
            "quantity": 8,
            "status": True,
        },
        {
            "name": "Aspirador Robô Roomba",
            "price": 1800.00,
            "quantity": 6,
            "status": True,
        },
        # Beleza e Cuidados
        {"name": "Perfume Chanel N°5", "price": 520.00, "quantity": 15, "status": True},
        {
            "name": "Secador Philco Ceramic",
            "price": 180.00,
            "quantity": 20,
            "status": True,
        },
        # Livros e Educação
        {"name": "Livro Clean Code", "price": 85.00, "quantity": 30, "status": True},
        {
            "name": "Curso Python Completo",
            "price": 299.90,
            "quantity": 100,
            "status": True,
        },
        # Diversos
        {"name": "Mochila Jansport", "price": 220.00, "quantity": 25, "status": True},
        {
            "name": "Garrafa Stanley Térmica",
            "price": 320.00,
            "quantity": 18,
            "status": True,
        },
    ]


def all_products_data():
    """Todos os produtos combinados"""
    return (
        electronics_products_data() + sports_products_data() + consumer_products_data()
    )


def products_by_price_range(min_price: float = 0, max_price: float = float("inf")):
    """Filtra produtos por faixa de preço"""
    all_products = all_products_data()
    return [
        product
        for product in all_products
        if min_price <= product["price"] <= max_price
    ]


def luxury_products_data():
    """Produtos de luxo (acima de R$ 5000)"""
    return products_by_price_range(min_price=5000)


def affordable_products_data():
    """Produtos acessíveis (até R$ 500)"""
    return products_by_price_range(max_price=500)
