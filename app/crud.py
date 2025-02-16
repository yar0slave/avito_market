from fastapi import HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, auth


def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, user: schemas.UserCreate):
    # Check if user already exists
    if get_user(db, user.username):
        raise HTTPException(status_code=400, detail="Username already registered")

    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(username=user.username, password_hash=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def send_coins(db: Session, from_user_id: int, to_user_id: int, amount: int):
    db_transaction = models.Transaction(from_user_id=from_user_id, to_user_id=to_user_id, amount=amount)
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


def get_merchandise(db: Session, item_name: str):
    return db.query(models.Merchandise).filter(models.Merchandise.name == item_name).first()


def add_item_to_inventory(db: Session, user_id: int, merchandise: models.Merchandise):
    db_inventory = models.Inventory(user_id=user_id, merchandise_id=merchandise.id)
    db.add(db_inventory)
    db.commit()


def get_user_inventory(db: Session, user_id: int):
    return db.query(models.Merchandise)\
             .join(models.Inventory)\
             .filter(models.Inventory.user_id == user_id)\
             .all()

def get_user_coin_history(db: Session, user_id: int):
    received = db.query(models.Transaction).filter(models.Transaction.to_user_id == user_id).all()
    sent = db.query(models.Transaction).filter(models.Transaction.from_user_id == user_id).all()

    received_history = [
        {"fromUser": trans.from_user.username, "amount": trans.amount}
        for trans in received
    ]
    sent_history = [
        {"toUser": trans.to_user.username, "amount": trans.amount}
        for trans in sent
    ]

    return {
        "received": received_history,
        "sent": sent_history
    }