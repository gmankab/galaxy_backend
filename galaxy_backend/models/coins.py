from pydantic import BaseModel


class AddRequest(BaseModel):
    tg_id: int
    amount: int


class GetResponse(BaseModel):
    coins: int

