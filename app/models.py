from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    coins = Column(Integer, default=1000)

    # Update relationships with back_populates
    transactions_received = relationship(
        "Transaction",
        foreign_keys="Transaction.to_user_id",
        back_populates="to_user"
    )
    transactions_sent = relationship(
        "Transaction",
        foreign_keys="Transaction.from_user_id",
        back_populates="from_user"
    )
    inventory = relationship("Inventory", back_populates="user")


class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, index=True)
    from_user_id = Column(Integer, ForeignKey('users.id'))
    to_user_id = Column(Integer, ForeignKey('users.id'))
    amount = Column(Integer)

    # Update relationships with back_populates
    from_user = relationship(
        "User",
        foreign_keys=[from_user_id],
        back_populates="transactions_sent"
    )
    to_user = relationship(
        "User",
        foreign_keys=[to_user_id],
        back_populates="transactions_received"
    )


class Merchandise(Base):
    __tablename__ = 'merchandise'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    price = Column(Integer)

    # Add relationship to inventory
    inventories = relationship("Inventory", back_populates="merchandise")


class Inventory(Base):
    __tablename__ = 'inventory'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    merchandise_id = Column(Integer, ForeignKey('merchandise.id'))

    user = relationship("User", back_populates="inventory")
    merchandise = relationship("Merchandise", back_populates="inventories")