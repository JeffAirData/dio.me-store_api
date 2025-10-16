"""
Base Model para MongoDB
Seguindo padrão da professora Nayanna Nara - DIO.me Store API
"""
import uuid
from datetime import datetime
from decimal import Decimal
from typing import Any

from bson import Decimal128
from pydantic import UUID4, BaseModel, Field, model_serializer


class CreateBaseModel(BaseModel):
    """
    Base model para criação de documentos MongoDB
    Inclui campos padrão: id, created_at, updated_at
    """

    id: UUID4 = Field(default_factory=uuid.uuid4)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    @model_serializer
    def set_model(self) -> dict[str, Any]:
        """
        Serializa o modelo convertendo Decimal para Decimal128 (MongoDB)
        """
        self_dict = dict(self)

        for key, value in self_dict.items():
            if isinstance(value, Decimal):
                self_dict[key] = Decimal128(str(value))

        return self_dict
