"""Teste de integração para produtos usando as factories"""
from store.schemas.product import ProductIn
from tests.factories import iphone_14_pro_max_data, iphone_products_data


def test_iphone_14_pro_max_from_factory():
    """Teste do iPhone 14 Pro Max usando dados da factory"""
    data = iphone_14_pro_max_data()
    product = ProductIn(**data)

    assert product.name == "Iphone 14 pro Max"
    assert product.price == 8500.00
    assert product.quantity == 10
    assert product.status is True


def test_multiple_iphone_products():
    """Teste de múltiplos produtos iPhone incluindo o 14 Pro Max"""
    products_data = iphone_products_data()
    products = [ProductIn(**data) for data in products_data]

    assert len(products) == 4

    # Verificar iPhone 14 Pro Max especificamente
    iphone_14_pro_max = next(p for p in products if p.name == "Iphone 14 pro Max")
    assert iphone_14_pro_max.price == 8500.00
    assert iphone_14_pro_max.quantity == 10
    assert iphone_14_pro_max.status is True


def test_iphone_14_pro_max_price_validation():
    """Teste específico de validação de preço do iPhone 14 Pro Max"""
    data = iphone_14_pro_max_data()

    # Teste com preço válido
    product = ProductIn(**data)
    assert product.price > 0

    # Teste com diferentes preços válidos
    data["price"] = 9000.00
    product_premium = ProductIn(**data)
    assert product_premium.price == 9000.00


def test_iphone_14_pro_max_stock_management():
    """Teste de gerenciamento de estoque do iPhone 14 Pro Max"""
    data = iphone_14_pro_max_data()

    # Produto com estoque
    product_in_stock = ProductIn(**data)
    assert product_in_stock.status is True
    assert product_in_stock.quantity > 0

    # Produto sem estoque
    data["quantity"] = 0
    data["status"] = False
    product_out_of_stock = ProductIn(**data)
    assert product_out_of_stock.status is False
    assert product_out_of_stock.quantity == 0
