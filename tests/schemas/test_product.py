from store.schemas.product import ProductIn


def test_schemas_validated():
    product = ProductIn(
        name="Iphone 14 pro Max", price=7999.99, quantity=10, status=True
    )

    assert product.name == "Iphone 14 pro Max"
