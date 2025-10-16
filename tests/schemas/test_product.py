import pytest
from pydantic import ValidationError

from store.schemas.product import ProductIn


def test_schemas_validated():
    product = ProductIn(
        name="Iphone 14 pro Max", price=7999.99, quantity=10, status=True
    )

    assert product.name == "Iphone 14 pro Max"
    assert product.price == 7999.99
    assert product.quantity == 10
    assert product.status is True


def test_schemas_iphone_14_pro_max_complete():
    """Teste específico para iPhone 14 Pro Max com dados completos"""
    product = ProductIn(
        name="Iphone 14 pro Max", price=8500.00, quantity=5, status=True
    )

    assert product.name == "Iphone 14 pro Max"
    assert product.price == 8500.00
    assert product.quantity == 5
    assert product.status is True


def test_schemas_validation_error_negative_price():
    """Teste para validar que preço negativo gera erro"""
    with pytest.raises(ValidationError) as exc_info:
        ProductIn(name="Iphone 14 pro Max", price=-100.00, quantity=10, status=True)

    assert "greater than 0" in str(exc_info.value)


def test_schemas_validation_error_negative_quantity():
    """Teste para validar que quantidade negativa gera erro"""
    with pytest.raises(ValidationError) as exc_info:
        ProductIn(name="Iphone 14 pro Max", price=8500.00, quantity=-5, status=True)

    assert "greater than or equal to 0" in str(exc_info.value)


def test_schemas_validation_error_missing_name():
    """Teste para validar que nome obrigatório gera erro"""
    with pytest.raises(ValidationError) as exc_info:
        ProductIn(price=8500.00, quantity=10, status=True)

    assert "Field required" in str(exc_info.value)
