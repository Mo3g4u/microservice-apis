
from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Extra, conint, validator, conlist

# 列挙スキーマを宣言
class Size(Enum):
    small = 'small'
    medium = 'medium'
    big = 'big'

class StatusEnum(Enum):
    created = 'created'
    paid = 'paid'
    progress = 'progress'
    cancelled = 'cancelled'
    dispatched = 'dispatched'
    delivered = 'delivered'

# pydantic モデルはそれぞれ pydantic の BaseModel クラスを継承
class OrderItemSchema(BaseModel):
    # Pyton の方ヒントを使って属性の型を指定
    product: str
    # 型を列挙型に設定することで、プロパティの値を制限
    size: Size
    # quantity の最小値とデフォルト値を指定
    quantity: Optional[conint(ge=1, strict=True)] = 1

    # Config を使って、スキーマ定義されていないプロパティを禁止
    class Config:
        extra = Extra.forbid

    @validator('quantity')
    def quantity_non_nullable(cls, value):
        assert value is not None, 'quantity may not be None'
        return value

class CreateOrderSchema(BaseModel):
    # pydantic の conlist 型を使って少なくとも１つの要素を持つリストを定義
    order: conlist(OrderItemSchema, min_length=1)

    class Config:
        extra = Extra.forbid

class GetOrderSchema(CreateOrderSchema):
    id: UUID
    created: datetime
    status: StatusEnum

class GetOrdersSchema(BaseModel):
    orders: List[GetOrderSchema]

