"""
Base Schema Mixins
Seguindo padrão da professora Nayanna Nara - DIO.me Store API
"""
from datetime import datetime
from decimal import Decimal

from bson import Decimal128
from pydantic import UUID4, BaseModel, Field, model_validator


class BaseSchemaMixin(BaseModel):
    """Base mixin para schemas com configuração padrão"""

    class Config:
        from_attributes = True


class OutSchema(BaseModel):
    """Schema base para saída com campos de controle"""

    id: UUID4 = Field()
    created_at: datetime = Field()
    updated_at: datetime = Field()

    @model_validator(mode="before")
    def set_schema(cls, data):
        """Converte Decimal128 do MongoDB para Decimal Python"""
        for key, value in data.items():
            if isinstance(value, Decimal128):
                data[key] = Decimal(str(value))

        return data
