from pydantic import BaseModel
from typing import List, Optional


class AuthRequest(BaseModel):
    username: str
    password: str


class AuthResponse(BaseModel):
    token: str


class TransactionHistoryReceived(BaseModel):
    fromUser: str
    amount: int


class TransactionHistorySent(BaseModel):
    toUser: str
    amount: int


class CoinHistory(BaseModel):
    received: List[TransactionHistoryReceived]
    sent: List[TransactionHistorySent]


class InventoryItem(BaseModel):
    type: str
    quantity: int


class InfoResponse(BaseModel):
    coins: int
    inventory: List[InventoryItem]
    coinHistory: CoinHistory


class SendCoinRequest(BaseModel):
    toUser: str
    amount: int


class ErrorResponse(BaseModel):
    errors: str


class UserCreate(BaseModel):
    username: str
    password: str


class MerchandiseResponse(BaseModel):
    name: str
    price: int
