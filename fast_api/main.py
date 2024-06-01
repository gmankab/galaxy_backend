from fastapi import FastAPI, HTTPException
from tortoise import fields, Tortoise
from tortoise.models import Model
from contextlib import asynccontextmanager

app = FastAPI(title="galaxy_backend")

class Coin(Model):
    id = fields.IntField(primary_key=True)
    user_id = fields.IntField(db_index=True)
    amount = fields.IntField()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await Tortoise.init(
        db_url='sqlite://data.db',
        modules={'models': ['main']}
    )
    await Tortoise.generate_schemas()
    yield
    await Tortoise.close_connections()

app.router.lifespan_context = lifespan

@app.get("/save/{user_id}/{coins}")
async def save_coins(user_id: int, coins: int):
    coin, created = await Coin.get_or_create(user_id=user_id, defaults={"amount": coins})
    if not created:
        coin.amount += coins
        await coin.save()
    return {"message": "Coins saved successfully", "user_id": user_id, "coin": coin.amount}

@app.get("/get/{user_id}")
async def get_coins(user_id: int):
    coin = await Coin.get_or_none(user_id=user_id)
    if coin is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user_id": user_id, "coin": coin.amount}
