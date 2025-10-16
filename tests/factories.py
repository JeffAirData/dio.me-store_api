"""Factory functions para gerar dados de teste"""


def iphone_14_pro_max_data():
    """Dados do iPhone 14 Pro Max para testes"""
    return {
        "name": "Iphone 14 pro Max",
        "price": 8500.00,
        "quantity": 10,
        "status": True,
    }


def iphone_products_data():
    """Lista de produtos iPhone para testes"""
    return [
        {"name": "Iphone 12 pro Max", "price": 6500.00, "quantity": 15, "status": True},
        {"name": "Iphone 13 pro Max", "price": 7500.00, "quantity": 8, "status": True},
        {"name": "Iphone 14 pro Max", "price": 8500.00, "quantity": 10, "status": True},
        {
            "name": "Iphone 15 pro Max",
            "price": 10500.00,
            "quantity": 3,
            "status": False,  # Fora de estoque
        },
    ]
