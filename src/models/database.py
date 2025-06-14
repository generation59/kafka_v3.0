from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class User:
    id: int
    name: str
    email: str
    created_at: datetime

    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        return cls(
            id=data['id'],
            name=data['name'],
            email=data['email'],
            created_at=datetime.fromisoformat(data['created_at'].replace('Z', '+00:00'))
        )


@dataclass
class Order:
    id: int
    user_id: int
    product_name: str
    quantity: int
    order_date: datetime

    @classmethod
    def from_dict(cls, data: dict) -> 'Order':
        return cls(
            id=data['id'],
            user_id=data['user_id'],
            product_name=data['product_name'],
            quantity=data['quantity'],
            order_date=datetime.fromisoformat(data['order_date'].replace('Z', '+00:00'))
        ) 