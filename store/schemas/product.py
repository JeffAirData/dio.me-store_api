from pydantic import Field

from store.schemas.base import BaseSchemaMixin


class ProductIn(BaseSchemaMixin):
    name: str = Field(description="Product name")
    price: float = Field(gt=0, description="Product price")
    quantity: int = Field(ge=0, description="Product quantity")
    status: bool = Field(default=True, description="Product status")
