"""
Product Model para MongoDB
Seguindo padrão da professora Nayanna Nara - DIO.me Store API
"""
from store.models.base import CreateBaseModel
from store.schemas.product import ProductIn


class ProductModel(ProductIn, CreateBaseModel):
    """
    Modelo de produto para persistência no MongoDB

    Herda:
    - ProductIn: Schema de entrada (name, price, quantity, status)
    - CreateBaseModel: Campos base (id, created_at, updated_at) + serialização MongoDB
    """

    pass
