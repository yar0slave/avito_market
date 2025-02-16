from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from . import crud, models, schemas, database, auth
from .config import SECRET_KEY
from typing import List

MERCHANDISE_ITEMS = [
    {"name": "t-shirt", "price": 80},
    {"name": "cup", "price": 20},
    {"name": "book", "price": 50},
    {"name": "pen", "price": 10},
    {"name": "powerbank", "price": 200},
    {"name": "hoody", "price": 300},
    {"name": "umbrella", "price": 200},
    {"name": "socks", "price": 10},
    {"name": "wallet", "price": 50},
    {"name": "pink-hoody", "price": 500}
]

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth")


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/api/auth", response_model=schemas.AuthResponse)
def authenticate(request: schemas.AuthRequest, db: Session = Depends(get_db)):
    try:
        user = auth.authenticate_user(db, request.username, request.password)
    except HTTPException:
        # Если пользователь не найден, создаем нового
        hashed_password = auth.get_password_hash(request.password)
        user = crud.create_user(db, request)

    access_token = auth.create_access_token(data={"sub": user.username})
    return {"token": access_token}


@app.post("/api/register", response_model=schemas.AuthResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        new_user = crud.create_user(db, user)
        access_token = auth.create_access_token(data={"sub": new_user.username})
        return {"token": access_token}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/info", response_model=schemas.InfoResponse)
def get_info(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user = auth.get_current_user(db, token)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    inventory_items = crud.get_user_inventory(db, user.id)
    inventory_dict = {}
    for item in inventory_items:
        if item.name in inventory_dict:
            inventory_dict[item.name].quantity += 1
        else:
            inventory_dict[item.name] = schemas.InventoryItem(
                type=item.name,
                quantity=1
            )

    coin_history = crud.get_user_coin_history(db, user.id)

    return {
        "coins": user.coins,
        "inventory": list(inventory_dict.values()),
        "coinHistory": coin_history
    }


@app.post("/api/sendCoin")
def send_coins(request: schemas.SendCoinRequest, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    from_user = auth.get_current_user(db, token)
    if from_user is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    to_user = crud.get_user(db, request.toUser)
    if not to_user:
        raise HTTPException(status_code=404, detail="User not found")

    if from_user.coins < request.amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")

    crud.send_coins(db, from_user.id, to_user.id, request.amount)

    from_user.coins -= request.amount
    to_user.coins += request.amount
    db.commit()

    return {"message": "Coins sent successfully"}


@app.get("/api/buy/{item}")
def buy_item(item: str, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user = auth.get_current_user(db, token)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    merchandise = crud.get_merchandise(db, item)
    if not merchandise:
        raise HTTPException(status_code=404, detail="Item not found")

    if user.coins < merchandise.price:
        raise HTTPException(status_code=400, detail="Insufficient funds")

    user.coins -= merchandise.price
    crud.add_item_to_inventory(db, user.id, merchandise)
    db.commit()

    return {"message": f"Item {item} bought successfully"}


@app.on_event("startup")
async def initialize_merchandise():
    db = next(get_db())
    for item in MERCHANDISE_ITEMS:
        existing_item = db.query(models.Merchandise).filter(models.Merchandise.name == item["name"]).first()
        if not existing_item:
            db_item = models.Merchandise(name=item["name"], price=item["price"])
            db.add(db_item)
    db.commit()
    db.close()


@app.get("/api/merchandise", response_model=List[schemas.MerchandiseResponse])
def get_merchandise(db: Session = Depends(get_db)):
    return db.query(models.Merchandise).all()