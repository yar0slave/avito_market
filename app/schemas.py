from pydantic import BaseModel
from typing import List, Optional

# Auth
class AuthRequest(BaseModel):
    username: str
    password: str

class AuthResponse(BaseModel):
    token: str

# Transactions and history
class TransactionHistoryReceived(BaseModel):
    fromUser: str
    amount: int

class TransactionHistorySent(BaseModel):
    toUser: str
    amount: int

class CoinHistory(BaseModel):
    received: List[TransactionHistoryReceived]
    sent: List[TransactionHistorySent]

# Inventory
class InventoryItem(BaseModel):
    type: str
    quantity: int

# Main responses
class InfoResponse(BaseModel):
    coins: int
    inventory: List[InventoryItem]
    coinHistory: CoinHistory

# Requests
class SendCoinRequest(BaseModel):
    toUser: str
    amount: int

# Error response
class ErrorResponse(BaseModel):
    errors: str

# Дополнительные схемы (не из документации)
class UserCreate(BaseModel):
    username: str
    password: str

class MerchandiseResponse(BaseModel):
    name: str
    price: int