from pydantic import BaseModel

class ClanCreateRequest(BaseModel):
    clan_name: str
    clan_owner_id: int

class UserClanRequest(BaseModel):
    clan_id: int
    user_id: int

class UserRequest(BaseModel):
    user_id: int
