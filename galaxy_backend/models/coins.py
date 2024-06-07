from pydantic import BaseModel


class AddRequest(BaseModel):
    tg_id: int
    amount: int


class GetResponse(BaseModel):
    coins: int

class autoClickRequest(BaseModel):
    tg_id: int
    interval: int
    duration: int
