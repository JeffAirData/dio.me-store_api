"""
Product Schemas
Seguindo padrão da professora Nayanna Nara - DIO.me Store API
"""
from decimal import Decimal
from typing import Annotated, Optional

from bson import Decimal128
from pydantic import AfterValidator, Field

from store.schemas.base import BaseSchemaMixin, OutSchema


class ProductBase(BaseSchemaMixin):
    """Schema base do produto com validações"""

    name: str = Field(..., description="Product name")
    quantity: int = Field(..., description="Product quantity")
    price: Decimal = Field(..., description="Product price")
    status: bool = Field(..., description="Product status")


class ProductIn(ProductBase, BaseSchemaMixin):
    """Schema de entrada para criação de produtos"""

    pass


class ProductOut(ProductIn, OutSchema):
    """Schema de saída com campos de controle (id, created_at, updated_at)"""

    pass


def convert_decimal_128(v):
    """Converter Decimal para Decimal128 do MongoDB"""
    return Decimal128(str(v))


Decimal_ = Annotated[Decimal, AfterValidator(convert_decimal_128)]


class ProductUpdate(BaseSchemaMixin):
    """Schema para atualização parcial de produtos"""

    quantity: Optional[int] = Field(None, description="Product quantity")
    price: Optional[Decimal_] = Field(None, description="Product price")
    status: Optional[bool] = Field(None, description="Product status")


class ProductUpdateOut(ProductOut):
    """Schema de saída para produtos atualizados"""

    pass
